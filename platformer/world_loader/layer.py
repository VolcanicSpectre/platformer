from typing import Any, Dict

class Layer:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.grid_height = data["__cHei"]
        self.grid_width = data["__cWid"]

        self.grid_size = data["__gridSize"]
        self.identifer = data["__identifer"]

        self.type = data["__type"]
        
