from keras import backend as K
from keras.engine.topology import Layer
import numpy as np

'''G for pre-plus disease'''
class GausLayer(Layer):
    def __init__(self, input_dim, output_dim=1, **kwargs):
        self.output_dim = output_dim
        self.input_dim = input_dim
        super(GausLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        # initiate the tensor variables
        self.mu = self.add_weight(name='mean', shape=(self.output_dim, input_shape[1]), initializer='uniform',
                                 trainable=True)
        self.var = self.add_weight(name='variance', shape=(self.output_dim, 1), initializer='uniform',
                                 trainable=True)
        # Create a trainable weight variable for this layer.
        self.trainable_weights = [self.mu, self.var]
        super(GausLayer, self).build(input_shape)  # built=true

    def call(self, x):
        # Gaussian with mu and var
        # *: elementwise
        return K.exp(-(K.dot(x-self.mu,K.transpose(x-self.mu)) * K.pow(2 * self.var,-1))) * K.pow((2*np.pi*self.var),-0.5)

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.output_dim)