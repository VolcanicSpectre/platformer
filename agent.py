from collections import deque

from activation import ActivationLayer
from convolutional import ConvolutionalLayer
from dense import DenseLayer
from constants import *

class Agent:
	def __init__(self, state_size, action_size):
		self.state_size = state_size
		self.action_size = action_size

		self.memory_buffer = deque(maxlen=MEMORY_BUFFER_MAX_SIZE)

		self.gamma = INITIAL_GAMMA_VALUE
		self.epsilon = INITIAL_EPSILION_VALUE
		
	@staticmethod
	def build_network():
		model = []
		for kernel_shape in KERNEL_SIZES:
			model.append(ConvolutionalLayer((NUM_STACKED_FRAMES, DS_WIDTH, DS_HEIGHT), )
