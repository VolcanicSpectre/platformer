import pygame


class StaticRenderer:
	def __init__(self, static_frame: pygame.Surface):
		"""Creates a StaticRenderer component for a static object
		
		Args:
		    static_frame (pygame.Surface): The static frame to be rendered
		"""
		self.static_frame = static_frame

	def render_entity(self, surface: pygame.Surface, x: int, y: int):
		"""Renders the static frame onto the surface at the given position
		
		Args:
		    surface (pygame.Surface): The surface that the frame is rendered onto
		    x (int): The x position that the static frame is rendered onto
		    y (int): The y position that the static frame is rendered onto
		"""
		surface.blit(self.static_frame, (x, y))

class AnimatedRenderer(StaticRenderer):
	def __init__(self, frames: dict[str, pygame.Surface], current_frame_index: int=0):
		"""Creates an AnimatedRenderer component for an animated object
		
		Args:
		    frames (list[pygame.Surface]): The list of each possible frame for the animated object
		    current_frame_index (int, optional): If specified the starting frame will be the frame specified at the given index, otherwise the first one is selected
		"""
		self.frames = frames
		self.__current_frame_index = current_frame_index

	def render_entity(self, state_name:str, surface: pygame.Surface, x: int, y: int):
		"""Renders the current frame onto the surface at the given position
		Args:
			state_name (str): Description
		    surface (pygame.Surface): Description
		    x (int): The x position that the static frame is rendered onto
		    y (int): The y position that the static frame is rendered onto
		"""
		surface.blit(self.frames[self.__current_frame_index], (x, y))

	def set_current_frame(self, new_frame_index: int):
		"""Sets the index of the current frame to the index specified
		
		Args:
		    new_frame_index (int): The new index of the current frame
		
		Raises:
		    IndexError: Raises an IndexError if the given index is outside of the range 
		"""
		if new_frame_index < 0 or  new_frame_index >= len(self.frames):
			raise IndexError(f"The given index: {new_frame_index} is outside of the range 0 <= new_frame_index <= {len(self.frames)})")
		
		self.__current_frame_index = new_frame_index



