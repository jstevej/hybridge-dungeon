- Homework from last time:
    - Make tileset image
    - Make map with Tiled
- Review tilesets and maps
- Export map from Tiled
    - TODO: details
- Code to import map
    - Install pytmx
    - `tile.py`
        - Modify to accept image as argument to `__init__`
            - `def __init__(self, pos, image, *args):`
            - `self.image = image`
    - `level.py`
        - Extract map loading in `__init__` to its own function
            - Takes `map_file_name` argument
        - In `__init__`, call `self.load_map('assets/Level1.tmx')`
        - `from pytmx.util_pygame import load_pygame`
        - 