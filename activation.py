import numpy as np
from layer import Layer

class ActivationLayer3D(Layer):
	def __init__(self, activation, activation_prime):
		self.activation = activation
		self.activation_prime = activation_prime
	
	def apply_activation_function(self, prime):
		activation_func = self.activation_prime if prime else self.activation
		
		self.output = np.zeros(self.input.shape)
		for c, channel in enumerate(self.input):
			for y, row in enumerate(channel):
				for x, element in enumerate(row):
					self.output[c][y][x] = self.activation(element)

	def forward_propogation(self, a):
		self.input = a
		self.apply_activation_function(False)
		return self.output

	def backward_propogation(self, output_gradient):
		return np.multiply(output_gradient, self.apply_activation_function(True))


class ActivationLayer2D(Layer):
	def __init__(self, activation, activation_prime):
		self.activation = activation
		self.activation_prime = activation_prime
	
	def apply_activation_function(self, prime):
		activation_func = self.activation_prime if prime else self.activation
		
		self.output = np.zeros(self.input.shape)
		
		for y, row in enumerate(self.input):
			for x, element in enumerate(row):
				self.output[y][x] = self.activation(element)

	def forward_propogation(self, a):
		self.input = a
		self.apply_activation_function(False)
		return self.output

	def backward_propogation(self, output_gradient):
		return np.multiply(output_gradient, self.apply_activation_function(True))