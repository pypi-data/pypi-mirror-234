from IPython.display import display, IFrame
from urllib.parse import ParseResult
from pathlib import PurePath, Path
from zarr_file_server import host_file
from threading import Thread
from socket import socket
from typing import Union
import pkg_resources

def get_free_port()->int:
    """
    Grabs any free port available on the system

    Return: A free port on the system
    """

    sock = socket()  # Creates a socket
    sock.bind(('', 0))      
    port = sock.getsockname()[1]
    sock.close()
    return port

def run_local_render(port:int)->None:
    """
    Runs a local version of render with a specified port number

    Pre: current in src folder
    """
    Thread(target=host_file, args=(Path(pkg_resources.resource_filename(__name__, "apps/render-ui")),port,)).start()


def render(image_location:Union[ParseResult,PurePath] = "", microjson_overlay_location:Union[ParseResult, PurePath] = "", width:int=960, height:int=500, image_port:int=0, \
           microjson_overlay_port:int=0, use_local_render:bool=True, render_url:str = "https://render.ci.ncats.io/")->str:
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
    Returns: Render URL
        
    """

    # Extract url from local file path if provided. ?imageUrl is required scheme for render
    if isinstance(image_location, PurePath):
        # We could've call 0 in host_file to use a random server but we need to know the port number to display render
        if image_port == 0:
            image_port = get_free_port()
        # NOTE - uses local http server to serve local file to render, ran multithreaded b/c server does not end
        Thread(target=host_file, args=(image_location,image_port,)).start()
        image_location = "?imageUrl=http://localhost:" + str(image_port) + "/"

    # Otherwise, extract url from user provided url if provided
    elif isinstance(image_location, ParseResult):
        image_location = "?imageUrl=" + image_location.geturl() # Can be manually rebuilt to check if a valid format url is sent
    
    # Do the same but for JSON
    if isinstance(microjson_overlay_location, PurePath):
        if microjson_overlay_port == 0:
            microjson_overlay_port = get_free_port()
        Thread(target=host_file, args=(microjson_overlay_location,microjson_overlay_port,)).start()
        microjson_overlay_location = "&overlayUrl=http://localhost:" + str(microjson_overlay_port) + f"/{(microjson_overlay_location.name)}" 

    elif isinstance(microjson_overlay_location, ParseResult):
        microjson_overlay_location = "&overlayUrl=" + microjson_overlay_location.geturl()    

    # Serve local build of polus render if specified
    if use_local_render:
        render_port = get_free_port()
        run_local_render(render_port)
        render_url = f"http://localhost:{render_port}"

    #print(f"rendering {render_url}{image_location}{microjson_overlay_location}")
    # Display render
    display(IFrame(src=(f"{render_url}{image_location}{microjson_overlay_location}")
                                                        , width=width, height=height))
    
    return f"{render_url}{image_location}{microjson_overlay_location}"

