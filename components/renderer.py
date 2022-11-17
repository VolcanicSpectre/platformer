class StaticRenderer:
	def __init__(self, static_frame):
		self.static_frame = static_frame

	def render_entity(surface, x, y):
		surface.blit(self.static_frame, (x, y))

class AnimatedRenderer(StaticRenderer):
	def __init__(self, frames, current_frame_index=0):
		self.frames = frames
		self.__current_frame = frames[current_frame_index]

	def render_entity(surface, x, y):
		surface.blit(self.current_frame, (x, y))

	def set_current_frame(new_frame):
		self.current_frame = new_frame



