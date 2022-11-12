class Model:
	def __init__(self, conv_activation_functions, dense_activation_functions, num_stacked_frames, kernel_sizes, strides, dense_layer_output_sizes):
		self.model = []
		
		self.num_stacked_frames = num_stacked_frames
		self.kernel_sizes = kernel_sizes
		self.strides = strides
		self.dense_layer_output_sizes = dense_layer_output_sizes

		self.conv_activation, self.conv_activation_prime = conv_activation_functions
		self.dense_activation, self.dense_activation_prime = dense_activation_functions

	def build_model():
		self.model = []
		for kernel_shape, stride in self.kernel_sizes, self.strides:
			self.model.append(ConvolutionalLayer((self.num_stacked_frames, DS_WIDTH, DS_HEIGHT), stride, kernel_shape)
			self.model.append(ActivationLayer3D(self.conv_activation, self.conv_activation_prime))
		
		self.model.append(DenseLayer(model[-1].output_shape), self.dense_layer_output_sizes[0]))
		self.model.append(ActivationLayer3D(self.dense_activation, self.dense_activation_prime))
		self.model.append(DenseLayer(self.dense_layer_output_sizes[0], self.dense_layer_output_sizes[1]))

	def forward_propagation(self, a):
		self.model[0].forward_propagation(a)
		output = self.model[0].output
		for layer in self.model[1:]:
			layer.forward_propagation(output)
			output = layer.output

		return output