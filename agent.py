from collections import deque
from calc import relu, relu_prime, leaky_relu, leaky_relu_prime
from activation import ActivationLayer3D
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
		for kernel_shape, stride in KERNEL_SIZES, STRIDES:
			model.append(ConvolutionalLayer((NUM_STACKED_FRAMES, DS_WIDTH, DS_HEIGHT), stride, kernel_shape)
			model.append(ActivationLayer3D(leaky_relu, leaky_relu_prime))
		

		model.append(DenseLayer(model[-1].output_shape), DENSE_OUTPUT_SIZES[0])
		model.append(ActivationLayer3D(relu, relu_prime))
		model.append(DenseLayer(DENSE_OUTPUT_SIZES), DENSE_OUTPUT_SIZES[1])
