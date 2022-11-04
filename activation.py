import numpy as np
from layer import Layer

class Activation(Layer):
	def __init__(self, activation, activation_prime):
		self.activation = activation
		self.activation_prime = activation_prime
	
	def forward_propogation(self, a):
		self.input = a
		return self.activation(self.input)

	def backward_propogation(self, output_gradient, learning_rate):
		return np.multiply(output_gradient, self.activation_prime(self.input))
		