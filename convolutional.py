import numpy as np
from scipy.signal import correlate2d, convolve2d
from layer import Layer

class ConvolutionalLayer(Layer):
	def __init__(self, input_shape, kernel_size, depth):
		self.input_depth, self.input_height, self.input_width = input_shape
		self.depth = depth
		self.input_shape = input_shape

		self.output_shape = (depth, self.input_height - kernel_size + 1, self.input_width - kernel_size + 1)
		self.kernel_shape = (depth, kernel_size, kernel_size)
		self.kernels = np.random.randn(*kernels_shape)
		self.biases = np.random.randn(*self.output_shape)

	def forward_propogation(self, a):
		self.input = a
		self.output = np.copy(self.biases)

		for i in range(self.depth):
			for j in range(self.input_depth):
					self.output[i] += signal.correlate2d(self.input[j], self.kernels[i, j], "valid")

	def backward_propogation(self, output_gradient, learning_rate):
		kernels_gradient = np.zeros(self.kernel_shape)
		input_gradient = np.zeros(self.input_shape)

		for i in range(self.depth):
			for j in range(self.input_depth):
				 kernels_gradient[i, j] = signal.correlate2d(self.input[j], output_gradient[i], "valid")
				 input_gradient[j] += signal.convolve2d(output_gradient[i], self.kernels[i, j], "full")

		self.kernels -= learning_rate * kernels_gradient
		self.biases -= learning_rate * output_gradient

		return input_gradient
