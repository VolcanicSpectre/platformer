from enum import Enum, auto
from nea_game.calc.vector2d import Vector2D


class ForceMode(Enum):

    """Provides a container for the valid ways for a force to be applied to a rigid body

    Attributes:
        FORCE (TYPE): Add a continuous force to the rigidbody, using its mass
        IMPULSE (TYPE): Add an instant force impulse to the rigidbody, using its mass.
    """

    FORCE = auto()
    IMPULSE = auto()
    ACCELERATION = auto()


class RigidBody2D:
    mass: float
    gravity_scale: float
    internal_fps: int
    velocity: Vector2D

    """Creates a 2D rigid body that forces can be applied to"""

    def __init__(self, mass: float, gravity_scale: float, internal_fps: int):
        """Creates a 2D rigid body

        Args:
            mass (float): The mass of the body in kg
            gravity_scale (float): The degree to which the body is affected by gravity
            internal_fps (int): the interanl fps of the simulation
        """
        self.mass = mass
        self.gravity_scale = gravity_scale
        self.internal_fps = internal_fps
        self.velocity = Vector2D(0, 0)

    def add_force(
        self,
        force: Vector2D,
        delta_time: float = 0,
        force_mode: ForceMode = ForceMode.FORCE,
    ):
        """Adds a force to the rigid body

        Args:
            force (Vector2D): The unscaled force that will act on the body
            delta_time (float): The time difference between when the previous frame that was drawn and the current frame was drawn
            force_mode (ForceModes, optional): Dictates the way that the force is applied

        Raises:
            ValueError: A ValueError is raised when the given force_mode is not a valid force_type
        """
        delta_time *= self.internal_fps
        match force_mode:
            case ForceMode.FORCE:
                self.velocity += force.scale(delta_time / self.mass)
            case ForceMode.IMPULSE:
                self.velocity += force.scale(1 / self.mass)
            case ForceMode.ACCELERATION:
                self.velocity += force.scale(delta_time)
            case _:
                raise ValueError(
                    f"The given force_type: {force_mode} is not in {[member.value for member in ForceMode]}"
                )

        self.velocity = self.velocity.near_zero()
