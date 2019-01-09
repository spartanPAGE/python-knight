from .core import scaffolding
from .core.scene import Scene

def main_scene():
    return Scene()

def initialize_scenes(scenes=[main_scene()]):    
    return {'scenes': scenes}

def run():
    game_vars = scaffolding.initialize_pygame()
    game_vars.update(initialize_scenes())
    
    scaffolding.loop(game_vars)
    scaffolding.finalize()
