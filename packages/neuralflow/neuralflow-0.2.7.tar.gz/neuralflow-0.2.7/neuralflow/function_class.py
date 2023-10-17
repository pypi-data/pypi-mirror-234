from collections import Counter
from .gpu import *
from .function import *
from .model import *

class BaseFunction():
    def __init__(self):
        pass

    def __call__(self, arg):
        result = self._forward(arg)
        return result

    def _forward(self, x):
        pass

    def __repr__(self) -> str:
        return "Function"


class Step(BaseFunction):
    def __init__(self):
        super().__init__()

    def _forward(self, x):
        return step_function(x)


class Identity(BaseFunction):
    def __init__(self):
        super().__init__()

    def _forward(self, x):
        return identity(x)


class Sigmoid(BaseFunction):
    def __init__(self):
        self.differentiable = False
        self.out = None
        super().__init__()

    def _forward(self, x):
        out = sigmoid(x)
        self.out = out

        return out

    def _backward(self, input):
        result = input * self.out * (1.0 - self.out)

        return result


class Softmax(BaseFunction):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        return softmax(x)


class ReLU(BaseFunction):
    def __init__(self):
        self.differentiable = False
        self.mask = None
        super().__init__()

    def _forward(self, x):
        self.mask = (x <= 0)
        result = x.copy()
        result[self.mask] = 0

        return result

    def _backward(self, input):
        input[self.mask] = 0
        result = input

        return result


class CrossEntropyLoss():
    def __init__(self):
        self.loss = None
        self.pred = None
        self.true = None
        self.cache = None
        self.ignore_label = -1

    def __repr__(self):
        return "Function"

    def __call__(self, *arg):
        result = self._forward(*arg)
        return result

    def _forward(self, pred, true):
        if pred.ndim == 3:
            batch_size, n_timestep, vocab_size = pred.shape

            if true.ndim == 3:
                true = true.argmax(axis=2)

            mask = (true != self.ignore_label)

            self.pred = pred.reshape(batch_size * n_timestep, vocab_size)
            self.true = true.reshape(batch_size * n_timestep)
            mask = mask.reshape(batch_size * n_timestep)

            pred_sentence = softmax(self.pred)
            ls = np.log(pred_sentence[np.arange(batch_size * n_timestep), self.true])
            ls *= mask
            self.loss = -np.sum(ls)
            self.loss /= mask.sum()

            self.cache = (self.true, pred_sentence, mask, (batch_size, n_timestep, vocab_size))

            return self.loss
        else:
            self.pred = softmax(pred)
            self.true = true
            self.loss = cross_entropy_error(self.pred, self.true)

            return self.loss

    def _backward(self):
        if self.cache is not None:
            true, pred_sentence, mask, (batch_size, n_timestep, vocab_size) = self.cache

            dx = pred_sentence
            dx[np.arange(batch_size * n_timestep), true] -= 1
            dx *= 1
            dx /= mask.sum()
            dx *= mask[:, np.newaxis]  # ignore_label에 해당하는 데이터는 기울기를 0으로 설정

            dx = dx.reshape((batch_size, n_timestep, vocab_size))

            return dx

        batch_size = self.true.shape[0]
        if self.true.size == self.pred.size:
            dx = (self.pred - self.true) / batch_size
        else:
            dx = self.pred.copy()
            dx[np.arange(batch_size), self.true] -= 1
            dx = dx / batch_size

        return dx


class BinaryCrossEntropyLoss():
    def __init__(self):
        self.loss = None
        self.pred = None
        self.true = None

    def __repr__(self) -> str:
        return "Function"

    def __call__(self, *arg):
        result = self._forward(*arg)
        return result

    def _forward(self, pred, true):
        self.pred = sigmoid(pred)
        self.true = true
        self.loss = cross_entropy_error(self.pred, self.true)

        return self.loss

    def _backward(self):
        batch_size = self.true.shape[0]
        if self.true.size == self.pred.size:
            dx = (self.pred - self.true) / batch_size
        else:
            dx = self.pred.copy()
            dx[np.arange(batch_size), self.true] -= 1
            dx = dx / batch_size

        return dx
