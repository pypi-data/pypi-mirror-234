from pinenut.core import Tensor, mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
import pinenut as pn
from pympler import muppy, summary
import gc

# generate a linear dataset
np.random.seed(0)
x = np.random.randn(100, 1)
y = 6 + 3 * x + np.random.randn(100, 1)  # noise added
x, y = Tensor(x, 'x'), Tensor(y, 'y')  # convert to Tensor

# initialize parameters
W = Tensor(np.random.randn(1, 1), 'W')
b = Tensor(np.random.randn(1), 'b')


# define a linear function
def predict(x):
    return pn.matmul(x, W) + b


lr = 0.1

loss_data = []
for i in range(10):
    y_pred = predict(x)  # forward
    y_pred.name = 'y_pred'
    loss = mean_squared_error(y_pred, y)
    loss.name = 'loss'
    loss.backward()
    loss.unchain_backward()

    # update parameters
    W.data -= lr * W.grad.data
    b.data -= lr * b.grad.data

    # clear gradients
    W.clear_grad()
    b.clear_grad()

    loss_data.append(loss.data)


print('end.')