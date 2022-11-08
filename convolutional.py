import numpy as np
from calc import convolve2d
from layer import Layer

class ConvolutionalLayer(Layer):
	def __init__(self, input_shape, stride, kernel_size, number_of_filters):
		self.input_depth, self.input_height, self.input_width = input_shape
		self.number_of_filters = number_of_filters
		self.input_shape = input_shape
		self.stride = stride

		self.output_shape = (number_of_filters, (self.input_height - kernel_size) // self.stride + 1, (self.input_width - kernel_size) // self.stride + 1)
		self.kernel_shape = (number_of_filters, kernel_size, kernel_size)
		self.kernels = np.random.randn(*self.kernel_shape)
		self.biases = np.random.randn(*self.output_shape)

	def forward_propogation(self, a):
		self.input = a
		self.output = np.copy(self.biases)

		for i, channel in enumerate(self.input):
			for j, kernel in enumerate(self.kernels):
				self.output[i] = np.add(self.output[i], convolve2d(channel, kernel, self.stride, self.output_shape[1:]))

	
	def backward_propogation(self, output_gradient, learning_rate):
		kernels_gradient = np.zeros(self.kernel_shape)
		input_gradient = np.zeros(self.input_shape)

		for i in range(self.number_of_filters):
			for j in range(self.input_depth):
				 kernels_gradient[i, j] = correlate2d(self.input[j], output_gradient[i], "valid")
				 input_gradient[j] += convolve2d(output_gradient[i], self.kernels[i, j],)

		self.kernels -= learning_rate * kernels_gradient
		self.biases -= learning_rate * output_gradient

		return input_gradient

	def backward_propogation(self, output_gradient, learning_rate):
		kernels_gradient = np.zeros(self.kernel_shape)
		input_gradient = np.zeros(self.input_shape)

		for i, channel in enumerate(self.input):
			for j, kernel in enumerate(self.kernels):
				kernel = convolve2d(self.input[j], output_gradient[i])
				input_gradient[j] = 
if __name__ == "__main__":
	layer = ConvolutionalLayer((4, 84, 84), 4, 8, 32)
	print(layer.output_shape)
	a = np.random.rand(4, 84, 84)
	print(a.shape)
	layer.forward_propogation(a)
