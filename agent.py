from collections import deque
from calc import relu, relu_prime, leaky_relu, leaky_relu_prime
from activation import ActivationLayer3D
from convolutional import ConvolutionalLayer
from dense import DenseLayer
from constants import *

class Agent:
	def __init__(self):
		self.memory_buffer = deque(maxlen=MEMORY_BUFFER_MAX_SIZE)

		self.gamma = INITIAL_GAMMA_VALUE
		self.epsilon = INITIAL_EPSILION_VALUE
		
	def build_network(self):
		self.model = Model((leaky_relu, leaky_relu_prime), (relu, relu_prime), NUM_STACKED_FRAMES, KERNEL_SIZES, STRIDES, DENSE_LAYER_OUTPUT_SIZES)
		self.model.build_network()



