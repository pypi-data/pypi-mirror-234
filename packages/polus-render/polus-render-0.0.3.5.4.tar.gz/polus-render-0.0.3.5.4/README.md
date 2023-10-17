# Polus Render

Enables the embedding of content from polus-render within Jupyer notebooks.
Contains a local build of Polus Render which enables the use of local dataset and MICRO-JSON overlay drag and drop
into Jupyter Notebook Render IFrames.

![image](https://github.com/jcaxle/polus-render/assets/145499292/2fcd525e-d97a-40fa-87f8-37981bd24be1)

## Requirements
* Python 3.9+

## Installation
```
pip install polus-render
```

## Render: Local build vs online
polus-render is bundled with a build of Polus Render which supports additional functionality compared to the web version. Table
is accurate as of 10/4/2023.
| Version           | Zarr from URL/Path | TIF from URL/Path   | Micro-JSON Support | Zarr/TIF Drag & Drop | Micro-JSON Drag & Drop | 
|----------------|---------------|---------------|----------------|-----------|-----|
| Local | :heavy_check_mark:  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:
| Online | :heavy_check_mark:  |  |  |  | 

## Drag & Drop Demo
![ezgif-4-7162ca42b5](https://github.com/jcaxle/polus-render/assets/145499292/7a59db1e-3128-4ee0-b9cc-ad1be7d3faee)


## Sample usage
``` Python
from polus import render
from urllib.parse import urlparse
from pathlib import Path

# Embeds an IFrame of a local build of Polus Render into Jupyter Notebooks
render()

# Embeds an IFrame of Polus Render into Jupyter Notebooks
render(use_local_render=False)

# Embeds an IFrame of a local build of Polus Render with an image file hosted at "https://viv-demo.storage.googleapis.com/LuCa-7color_Scan1/"
render(image_location=urlparse("https://viv-demo.storage.googleapis.com/LuCa-7color_Scan1/"))

# Embeds an IFrame of a local build of Polus Render with an image hosted locally at "C:\Users\JeffChen\OneDrive - Axle Informatics\Documents\zarr files\pyramid.zarr"
render(image_location=Path(r"C:\Users\JeffChen\OneDrive - Axle Informatics\Documents\zarr files\pyramid.zarr"))

# Embeds an IFrame of a local build of Polus Render with an image and overlay file that is hosted locally
render(image_location=Path(r"C:\Users\JeffChen\OneDrive - Axle Informatics\Documents\zarr files\pyramid.zarr"), \
microjson_overlay_location=Path(r"C:\Users\JeffChen\OneDrive - Axle Informatics\Documents\overlay files\x00_y01_c1_segmentations.json"))

# Embeds an IFrame of a local build of Polus Render with an image and overlay file that is hosted online
render(image_location=urlparse("https://files.scb-ncats.io/pyramids/segmentations/x00_y01_c1.ome.tif"), \
microjson_overlay_location=urlparse("https://files.scb-ncats.io/pyramids/segmentations/x00_y03_c1_segmentations.json"))

# Embeds an IFrame with a height of 1080 of a local build of Polus Render.
render(height=1080)
```

## Functions
``` Python
def render(image_location:ParseResult|PurePath = "", microjson_overlay_location:ParseResult|PurePath = "", width:int=960, height:int=500, image_port:int=0, \
           microjson_overlay_port:int=0, use_local_render:bool=True, render_url:str = "https://render.ci.ncats.io/")->None:
    """
    Displays Polus Render with args to specify display dimensions, port to serve,
    image files to use, and overlay to use.
    
    Param:
        image_location(ParseResult|Purepath): Acquired from urllib.parse.ParseResult or Path, renders url in render.
                            If not specified, renders default render url.
        microjson_overlay_location(ParseResult|Purepath): Acquired from urllib.parse.ParseResult or Path, renders url in render.
                            If not specified, renders default render url
        width (int): width of render to be displayed, default is 960
        height (int): height of render to be displayed, default is 500
        image_port (int): Port to run local zarr server on if used (default is 0 which is the 1st available port).
        microjson_overlay_port (int): Port to run local json server on if used (default is 0 which is the 1st available port).
        run_local_render (bool): True to run local build of render with 1st available port, False to use render_url (default is True)
        render_url (str): URL which refers to Polus Render. Used when run_local_render is False. (default is https://render.ci.ncats.io/)
    Pre: zarr_port and json_port selected (if used) is not in use IF path given is Purepath
        
    """
```
