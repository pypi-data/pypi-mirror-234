from __future__ import annotations

import logging
import os
from types import ModuleType
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import UUID

import jsonschema
import yaml
from drb.addons.addon import Addon
from drb.core.node import DrbNode
from drb.drivers.image import DrbImageBaseNode
from drb.exceptions.core import DrbException
from drb.extractor import Extractor
from drb.extractor.extractor import parse_extractor
from drb.topics import resolver
from drb.topics.dao import ManagerDao
from drb.topics.topic import DrbTopic
from drb.utils.plugins import get_entry_points

_logger = logging.getLogger("DrbImage")
_schema = os.path.join(os.path.dirname(__file__), "schema.yml")


# FIXME Refactor this method in drb.utils.plugin
def _retrieve_cortex_file(module: ModuleType) -> str:
    """
    Retrieves the metadata cortex file from the given module.

    Parameters:
        module (ModuleType): target module where the cortex metadata file will
                             be search
    Returns:
        str - path to the cortex metadata file
    Raises:
        FileNotFound: If the metadata cortex file is not found
    """
    directory = os.path.dirname(module.__file__)
    path = os.path.join(directory, "cortex.yml")
    if not os.path.exists(path):
        path = os.path.join(directory, "cortex.yaml")

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    return path


def validate_md_cortex_file(path: str) -> None:
    """
    Checks the given metadata cortex file is valid.

    Parameters:
        path (str): metadata cortex file path

    Raises:
        DrbException: If the given cortex file is not valid
    """
    with open(_schema) as f:
        schema = yaml.safe_load(f)
    f.close()

    with open(path) as file:
        for data in yaml.safe_load_all(file):
            try:
                jsonschema.validate(data, schema)
            except jsonschema.ValidationError as ex:
                file.close()
                raise DrbException(
                    f"Invalid metadata cortex file: {path}"
                ) from ex
        file.close()


def _load_image(yaml_data: dict, node) -> Tuple[UUID, list[Image], str]:
    images = yaml_data["image"]
    res = []
    for image in images:
        aux_data = image.get("aux_data", {})
        name_extractor = parse_extractor(image["name"])
        source_extractor = parse_extractor(image["source"])
        try:
            names = name_extractor.extract(node)
        except Exception:
            continue
        if isinstance(names, List):
            for name in names:
                res.append(
                    Image(name=name, extractor=source_extractor, data=aux_data)
                )
        else:
            res.append(
                Image(name=names, extractor=source_extractor, data=aux_data)
            )
    return res


def _get_working_uuids() -> List[UUID]:
    entry_point_group = "drb.addon.image"
    uuids = []

    for ep in get_entry_points(entry_point_group):
        try:
            package = ep.load()
        except ModuleNotFoundError:
            continue
        try:
            cortex = _retrieve_cortex_file(package)
            validate_md_cortex_file(cortex)
        except FileNotFoundError:
            continue
        except (FileNotFoundError, DrbException) as ex:
            _logger.warning(ex)
            continue

        with open(cortex) as file:
            for data in yaml.safe_load_all(file):
                uuids.append(UUID(data["topic"]))

    return uuids


def _get_parents_UUIDs(topic: DrbTopic) -> List[UUID]:
    uuids = [topic.id]
    if topic.subClassOf is None:
        return uuids
    for parent in topic.subClassOf:
        uuids += _get_parents_UUIDs(ManagerDao().get_drb_topic(parent))
    return uuids


class Image:
    def __init__(self, name: str, extractor: Extractor, data: dict = {}):
        self._name = name
        self.extractor = extractor
        self._data = data
        self._node = None

    def __getattr__(self, item):
        if item in self._data.keys():
            return self._data[item]
        raise AttributeError

    @property
    def name(self) -> str:
        """
        Provide the name of the image.
        """
        return self._name

    @property
    def addon_data(self) -> Optional[dict]:
        """
        Provide the raw data of the image addon,
        in the dict format.
        in the dict format.
        """
        return self._data

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, value: DrbNode) -> None:
        self._node = value

    def image_node(self) -> DrbNode:  # DrbImageNode
        """
        Provides the current image as a DrbNode
        """
        return self.extractor.extract(self.node, image_name=self.name)

    def get_impl(self, impl):
        return self.image_node().get_impl(impl)


class ImageAddon(Addon):
    __instance = None
    __working_uuids = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(ImageAddon, cls).__new__(
                cls, *args, **kwargs
            )
        cls.__working_uuids = _get_working_uuids()
        return cls.__instance

    @classmethod
    def identifier(cls) -> str:
        return "image"

    @classmethod
    def return_type(cls) -> type:
        return Image

    def apply(self, node: DrbNode, **kwargs) -> Any:
        topic, node = resolver.resolve(node)
        uuids = _get_parents_UUIDs(topic)
        images_obj = self._get_images(uuids, node)
        image_name = kwargs.pop("image_name", None)

        if not images_obj:
            raise DrbException(f"No descriptor found for node {node.name}")

        if image_name is None and not kwargs:
            # return the first Image object
            # from the most refined topic available otherwise
            result = images_obj[0]
            result.node = node
            return result

        if image_name is not None and not kwargs:
            for image in images_obj:
                if image.name == image_name:
                    result = image
                    result.node = node
                    return result

        if kwargs:
            for image in images_obj:
                if image_name is not None and image_name != image.name:
                    continue
                # check if all options are in image's addon data
                # and if their values are equals
                if kwargs.items() <= image.addon_data.items():
                    result = image
                    result.node = node
                    return result

        raise DrbException(
            f"No image descriptor found for " f"{image_name}, {kwargs}"
        )

    def can_apply(self, source: DrbTopic) -> bool:
        source_uuids = _get_parents_UUIDs(source)
        return any(uuid in source_uuids for uuid in self.__working_uuids)

    def _get_images(self, uuids, node=None) -> List(Image):
        images = []
        entry_point_group = "drb.addon.image"

        for ep in get_entry_points(entry_point_group):
            try:
                package = ep.load()
            except ModuleNotFoundError:
                continue
            try:
                cortex = _retrieve_cortex_file(package)
                validate_md_cortex_file(cortex)
            except FileNotFoundError:
                continue
            except (FileNotFoundError, DrbException) as ex:
                _logger.warning(ex)
                continue

            with open(cortex) as file:
                for data in yaml.safe_load_all(file):
                    if UUID(data["topic"]) in uuids:
                        images += _load_image(data, node)
        return images

    def available_images(self, source) -> List[Tuple(str, Dict)]:
        """
        Returns available images list that can be generated
        Parameters:
          source (DrbNode, str, Topic):
        """
        res = []
        if isinstance(source, DrbNode) or isinstance(source, str):
            topic, node = resolver.resolve(source)
        elif isinstance(source, DrbTopic):
            topic = source
            node = None
        else:
            raise DrbException(
                f"Cannont find any image addon corresponding to {source}"
            )
        uuids = _get_parents_UUIDs(topic)
        images_obj = self._get_images(uuids, node)
        for image in images_obj:
            res.append((image.name, image.addon_data))

        return res
