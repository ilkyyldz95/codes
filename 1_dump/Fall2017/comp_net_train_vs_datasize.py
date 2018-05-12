from __future__ import absolute_import
from __future__ import print_function
from keras.layers import Input, Lambda
from keras import optimizers
from keras import backend as K
from googlenet import *
from importData import *

'''Imports F and trains with comparison labels'''

def BTPred(scalars):
    """
    This is the output when we predict comparison labels. s1, s2 = scalars (beta.*x)
    """
    s1 = scalars[0]
    s2 = scalars[1]
    return s1 - s2

def BTLoss(y_true, y_pred):
    """
    Negative log likelihood of Bradley-Terry Penalty, to be minimized. y = beta.*x
    """
    exponent = K.exp(-y_true * (y_pred))
    return K.log(1 + exponent)

# INITIALIZE PARAMETERS
data_size = int(sys.argv[1])
epochs = 30 #CAN CHANGE

no_of_features = 1024
batch_size = 32 #1 for validation, 100 for prediction
loss = BTLoss
lr = 1e-06
sgd = optimizers.SGD(lr=lr)

# LOAD DATA FOR COMPARISON LABELS
kthFold = int(0)
importer = importData(kthFold)
# control data size inside importData if there are no rotations
k_img_train_1, k_img_train_2, k_label_train = importer.importCompTrainData(data_size)

# LOAD JAMES' NETWORK FOR F
F_prev = create_googlenet(no_classes=1000, no_features=no_of_features)
F_prev.load_weights("googlenet_weights.h5", by_name=True)
F1 = create_googlenet(no_classes=1, no_features=no_of_features)
F2 = create_googlenet(no_classes=1, no_features=no_of_features)
for i in range(len(F1.layers) - 2): #last 2 layers depends on the number of classes
    F1.layers[i].set_weights(F_prev.layers[i].get_weights())
    F2.layers[i].set_weights(F_prev.layers[i].get_weights())

# CREATE TWIN NETWORKS: Siamese
# because we re-use the same instance `base_network`, the weights of the network will be shared across the two branches
input_a = F1.input
input_b = F2.input

processed_a = F1(input_a)
processed_b = F2(input_b)

distance = Lambda(BTPred, output_shape=(1,))([processed_a, processed_b])

comp_net = Model([input_a, input_b], distance)

# train
comp_net.compile(loss=loss, optimizer=sgd)
comp_net.fit([k_img_train_1, k_img_train_2], k_label_train, batch_size=batch_size, epochs=epochs)

# Save model
comp_net.save("comp_label_data_size_" + str(data_size) + ".h5")


