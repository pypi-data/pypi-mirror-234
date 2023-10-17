import numpy
from pympler import muppy, summary
import gc
from sys import getrefcount
from pinenut import Tensor, matmul, mean_squared_error, build_graph, Operator
import numpy as np


def test_func():
    a = Tensor(np.array([2.0, 3.0]), 'a')
    b = Tensor(np.array([4.0, 5.0]), 'b')
    c = a * b
    d = matmul(a, b)
    c.name = 'c'
    print(c)
    e = b * 3

    c.backward()
    c.unchain_backward()
    print(a.grad)
    print('d=', d)
    d.backward()
    d.unchain_backward()

    '''
    # --------------------------
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
        return matmul(x, W) + b

    lr = 0.1

    loss_data = []
    for i in range(1):
        y_pred = predict(x)  # forward
        y_pred.name = 'y_pred'
        loss = mean_squared_error(y_pred, y)
        # build_graph(loss, 'test_memory.png', view=False)
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

    # --------------------------

    # objs = muppy.get_objects()
    # dicts = [ao for ao in objs if isinstance(ao, numpy.ndarray)]
    # for d in dicts:
    #     print(d, id(d))

    # -------

    return c
    '''


if __name__ == "__main__":
    test_func()
    gc.collect()

    print('---- after gc.collect() ----')
    objs = muppy.get_objects()
    dicts = [ao for ao in objs if isinstance(ao, (numpy.ndarray, Operator))]
    print('len=', len(dicts))
    for d in dicts:
        # if str(d.data.dtype)=='int64':
            print(d, id(d))
            # print(gc.get_referrers(d))
            print(gc.get_referents(d))



    # for obj_ref in gc.get_referrers(c):
    #     print('\n------\n')
    #     print(obj_ref)
    #     print('\n######\n')
    # print(gc.get_referents(c))
