# DRB Image Extractor
It's an applicative part using DRB allowing to extract image from
data according its topic.

### Packaging
The package python containing an addon image of a DRB topic must have the following
instruction:
 - a `drb.addon.image` entry point whose its value is the targeted Python
   package containing the `cortex.yaml` file

### How to define an addon image ?
Addon Image are defined in a `cortex.yaml` file following the template:
```yaml
topic: <topic_uuid>                         # target topic
image:                                      # image is an array of object with a name, a source and auxiliaries data
  - name: 
      <extractor>: <extractor_content>      # An extrator for the images name
    source:
      <extractor>: <extractor_content>      # An extractor the images itself
    aux_data:                               # Auxiliaries data are optional
      <aux_data1>: value1
      <aux_data2>: value2


### How to extract an image ?

For the following addon description.

```yaml
topic: b0dad6fa-9ae4-4694-b00b-449cd456d32a # Sentinel-1A Interferometric Wide Swath Level 1 S Product
image:
  - name:
      constant: quicklook
    source:
      xquery: |
        /preview/quick-look.png
  - name:
      constant: thumbnail
    source:
      xquery: /thumbnail.png
```

The different image node can be extract with this:

```python
from drb.image.core import ImageAddon
import drb.topics.resolver as resolver


if __name__ == '__main__':
    node = resolver.create('S1A_IW_RAW__0SDH_20220201T101715_20220201T101734_041718_04F6C6_A26E.SAFE')
    
    # Retrieve the first addon image object corresponding to the product
    # here, the quicklook image
    image = ImageAddon().apply(node)
    
    # Retrieve the addon image object corresponding to the image name
    image = ImageAddon().apply(node=node, image_name='thumbnail') 

    # Retrieve the addon image object corresponding to the image_name and resolution given in argument
    image = ImageAddon().apply(node=node, image_name='quickLook', resolution='10m')
    
    # This will raise an DrbException because it can't find any image addon
    image = ImageAddon().apply(node=node, image_name='Non_existing_image')
    
    # To retrieve the DrbNode corresponding to the image, use:
    image_node = image.image_node()

```

If a topic defines more than one image, and image_name is not specified, ImageAddon().apply() return the first image declared in the topic. If the topic of the node is not found in the cortex file, it will also check all the topic's parents recursively.

### Extractor

All the information about extractor can be found [here](https://gitlab.com/drb-python/metadata/extractor)
