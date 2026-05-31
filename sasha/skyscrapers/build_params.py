from mcpq import Vec3


from dataclasses import dataclass


@dataclass
class BuildParams:
    floors: int
    floor_height: int
    width: int
    depth: int
    start: Vec3
