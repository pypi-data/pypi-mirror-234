import unittest

import rasterio
from drb.drivers.file import DrbFileNode
from drb.drivers.image import DrbImageBaseNode
from drb.drivers.netcdf import DrbNetcdfNode
from drb.exceptions.core import DrbException
from drb.image.core import Image, ImageAddon
from drb.topics import resolver


def my_method(node):
    return DrbImageBaseNode(node)


def my_method_2(node):
    return node


class TestImageAddon(unittest.TestCase):
    addon = None
    S1 = (
        "tests/resources/S1A_IW_SLC__1SDV_20230131T104608_"
        "20230131T104643_047026_05A40B_2AFB.SAFE"
    )
    S2 = (
        "tests/resources/S2A_MSIL2A_20230131T075141_N0509_R135_"
        "T36MYD_20230131T131152.SAFE"
    )
    S2_L1C = (
        "tests/resources/S2A_MSIL1C_20230624T104621_N0509_R051_"
        "T31UDP_20230624T142921.SAFE"
    )
    S5 = (
        "tests/resources/S5P_NRTI_L2__AER_AI_20230203T111306_"
        "20230203T111806_27510_03_020400_20230203T130053.nc"
    )
    S1_LO = (
        "tests/resources/S1A_IW_RAW__0SDH_20220201T1017"
        "15_20220201T101734_041718_04F6C6_A26E.SAFE"
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.addon = ImageAddon()

    def test_addon(self):
        topic, node = resolver.resolve(self.S1)
        self.assertTrue(self.addon.can_apply(topic))

        image = self.addon.apply(node)

        self.assertIsNotNone(image)
        self.assertIsInstance(image, Image)
        self.assertEqual("preview", image.name)
        image_node = image.image_node()
        self.assertIsInstance(image_node, DrbImageBaseNode)
        self.assertEqual("preview.png", image_node.name)

        image = self.addon.apply(node, image_name="quicklook")

        self.assertIsNotNone(image)
        self.assertIsInstance(image, Image)
        self.assertEqual("quicklook", image.name)
        image_node = image.image_node()
        self.assertIsInstance(image_node, DrbImageBaseNode)
        self.assertEqual("quick-look.png", image_node.name)

    def test_python(self):
        topic, node = resolver.resolve(self.S2)

        self.assertTrue(self.addon.can_apply(topic))

        image = self.addon.apply(node)
        self.assertIsNotNone(image)
        self.assertIsInstance(image, Image)
        self.assertEqual("TrueColorImage", image.name)
        image_node = image.image_node()
        self.assertIsInstance(image_node, DrbImageBaseNode)
        self.assertEqual("T36MYD_20230131T075141_TCI_10m.jp2", image_node.name)

        node = resolver.create(self.S2_L1C)
        image = self.addon.apply(
            node, image_name="T31UDP_20230624T104621_B01.jp2"
        )
        self.assertIsNotNone(image)
        self.assertIsInstance(image, Image)
        self.assertEqual("T31UDP_20230624T104621_B01.jp2", image.name)
        image_node = image.image_node()
        self.assertIsInstance(image_node, DrbImageBaseNode)
        self.assertEqual("T31UDP_20230624T104621_B01.jp2", image_node.name)

    def test_script(self):
        topic, node = resolver.resolve(self.S5)

        self.assertTrue(self.addon.can_apply(topic))

        image = self.addon.apply(node)
        self.assertIsNotNone(image)
        self.assertIsInstance(image, Image)

    def test_resolutions(self):
        topic, node = resolver.resolve(self.S1_LO)

        self.assertTrue(self.addon.can_apply(topic))

        image = self.addon.apply(node, resolution="10m")
        self.assertIsNotNone(image)
        self.assertIsInstance(image, Image)
        image_node = image.image_node()
        self.assertIsInstance(image_node, DrbFileNode)

        image = self.addon.apply(node, resolution="20m")
        self.assertIsNotNone(image)
        self.assertIsInstance(image, Image)
        image_node = image.image_node()
        self.assertIsInstance(image_node, DrbImageBaseNode)

    def test_freq(self):
        topic, node = resolver.resolve(self.S5)

        self.assertTrue(self.addon.can_apply(topic))

        image = self.addon.apply(node, frequency=[270, 300])
        self.assertIsNotNone(image)
        self.assertIsInstance(image, Image)
        image_node = image.image_node()
        self.assertIsInstance(image_node, DrbNetcdfNode)

        image = self.addon.apply(node, frequency=310)
        self.assertIsNotNone(image)
        self.assertIsInstance(image, Image)

        with self.assertRaises(DrbException):
            self.addon.apply(node, frequency=320)

    def test_available_images(self):
        images = self.addon.available_images(self.S1)
        images_names = [image[0] for image in images]
        self.assertIsNotNone(images)
        self.assertIsInstance(images, list)
        self.assertEqual(len(images), 2)
        self.assertEqual(images_names[0], "preview")
        self.assertEqual(images_names[1], "quicklook")

        topic, node = resolver.resolve(self.S1)

        images = self.addon.available_images(node)
        images_names = [image[0] for image in images]
        self.assertIsNotNone(images)
        self.assertIsInstance(images, list)
        self.assertEqual(len(images), 2)
        self.assertEqual(images_names[0], "preview")
        self.assertEqual(images_names[1], "quicklook")

        images = self.addon.available_images(topic)
        images_names = [image[0] for image in images]
        self.assertIsNotNone(images)
        self.assertIsInstance(images, list)
        self.assertEqual(len(images), 2)
        self.assertEqual(images_names[0], "preview")
        self.assertEqual(images_names[1], "quicklook")

        node = resolver.create(self.S2_L1C)
        images = self.addon.available_images(node)
        images_names = [image[0] for image in images]
        self.assertIsNotNone(images_names)
        self.assertEqual(len(images_names), 2)
        self.assertTrue("T31UDP_20230624T104621_B01.jp2" in images_names)
        self.assertTrue("T31UDP_20230624T104621_B10.jp2" in images_names)

        with self.assertRaises(DrbException):
            self.addon.available_images(1)

        with self.assertRaises(TypeError):
            self.addon.available_images()

    def test_simpl_usage(self):
        image = self.addon.apply(resolver.create(self.S1))
        self.assertIsNotNone(image)
        self.assertIsInstance(image, Image)
        impl = image.get_impl(rasterio.DatasetReader)
        self.assertIsInstance(impl, rasterio.io.DatasetReader)
        self.assertIsNotNone(impl)

    def test_filter(self):
        topic, node = resolver.resolve(self.S1_LO)

        self.assertTrue(self.addon.can_apply(topic))

        image = self.addon.apply(node, resolution="20m")
        self.assertIsNotNone(image)
        self.assertEqual(image.resolution, "20m")
        image = self.addon.apply(node, resolution="20m", frequency=[205, 305])
        self.assertIsNotNone(image)
        self.assertEqual(image.resolution, "20m")
        self.assertEqual(image.frequency, [205, 305])
        image = self.addon.apply(node, resolution="20m", frequency=[105, 205])
        self.assertIsNotNone(image)
        self.assertEqual(image.resolution, "20m")
        self.assertEqual(image.frequency, [105, 205])
