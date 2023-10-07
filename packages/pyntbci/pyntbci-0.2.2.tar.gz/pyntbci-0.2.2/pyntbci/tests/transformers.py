import numpy as np
import unittest

import pyntbci


class TestCCA(unittest.TestCase):

    def test_X2D_Y2D(self):
        X = np.random.rand(111, 17)
        Y = np.random.rand(111, 23)
        cca = pyntbci.transformers.CCA(n_components=1)
        cca.fit(X, Y)
        self.assertEqual(cca.w_x_.shape, (X.shape[1], 1))
        self.assertEqual(cca.w_y_.shape, (Y.shape[1], 1))

        x = cca.transform(X)
        self.assertEqual(x.shape, (X.shape[0], 1))

        y = cca.transform(None, Y)
        self.assertEqual(y.shape, (Y.shape[0], 1))

        x, y = cca.transform(X, Y)
        self.assertEqual(x.shape, (X.shape[0], 1))
        self.assertEqual(y.shape, (Y.shape[0], 1))

    def test_X3D_Y3D(self):
        X = np.random.rand(111, 17, 57)
        Y = np.random.rand(111, 23, 57)
        cca = pyntbci.transformers.CCA(n_components=1)
        cca.fit(X, Y)
        self.assertEqual(cca.w_x_.shape, (X.shape[1], 1))
        self.assertEqual(cca.w_y_.shape, (Y.shape[1], 1))

        x = cca.transform(X)
        self.assertEqual(x.shape, (X.shape[0], 1, X.shape[2]))

        y = cca.transform(None, Y)
        self.assertEqual(y.shape, (Y.shape[0], 1, Y.shape[2]))

        x, y = cca.transform(X, Y)
        self.assertEqual(x.shape, (X.shape[0], 1, X.shape[2]))
        self.assertEqual(y.shape, (Y.shape[0], 1, Y.shape[2]))

    def test_X3D_Y1D(self):
        X = np.random.rand(111, 17, 57)
        Y = np.random.choice(5, 111)
        cca = pyntbci.transformers.CCA(n_components=1)
        cca.fit(X, Y)
        self.assertEqual(cca.w_x_.shape, (X.shape[1], 1))
        self.assertEqual(cca.w_y_.shape, (X.shape[1], 1))

        x = cca.transform(X)
        self.assertEqual(x.shape, (X.shape[0], 1, X.shape[2]))

        x = cca.transform(None, X)
        self.assertEqual(x.shape, (X.shape[0], 1, X.shape[2]))

        x1, x2 = cca.transform(X, X)
        self.assertEqual(x1.shape, (X.shape[0], 1, X.shape[2]))
        self.assertEqual(x2.shape, (X.shape[0], 1, X.shape[2]))

    def test_multiple_components(self):
        X = np.random.rand(111, 17)
        Y = np.random.rand(111, 23)
        cca = pyntbci.transformers.CCA(n_components=7)
        cca.fit(X, Y)
        self.assertEqual(cca.w_x_.shape, (X.shape[1], 7))
        self.assertEqual(cca.w_y_.shape, (Y.shape[1], 7))

        x = cca.transform(X)
        self.assertEqual(x.shape, (X.shape[0], 7))

        y = cca.transform(None, Y)
        self.assertEqual(y.shape, (Y.shape[0], 7))

        x, y = cca.transform(X, Y)
        self.assertEqual(x.shape, (X.shape[0], 7))
        self.assertEqual(y.shape, (Y.shape[0], 7))


class TestTRCA(unittest.TestCase):

    def test_X(self):
        X = np.random.rand(111, 7, 1001)

        trca = pyntbci.transformers.TRCA(n_components=1)
        trca.fit(X)
        self.assertEqual(trca.w_.shape, (X.shape[1], 1))
        Z = trca.transform(X)
        self.assertEqual(Z.shape, (X.shape[0], 1, X.shape[2]))

        trca = pyntbci.transformers.TRCA(n_components=3)
        trca.fit(X)
        self.assertEqual(trca.w_.shape, (X.shape[1], 3))
        Z = trca.transform(X)
        self.assertEqual(Z.shape, (X.shape[0], 3, X.shape[2]))

    def test_X_y(self):
        X = np.random.rand(111, 7, 1001)
        y = np.random.choice(5, 111)

        trca = pyntbci.transformers.TRCA(n_components=1)
        trca.fit(X, y)
        self.assertEqual(trca.w_.shape, (X.shape[1], 1, np.unique(y).size))
        Z = trca.transform(X)
        self.assertEqual(Z.shape, (X.shape[0], 1, X.shape[2], np.unique(y).size))
        Z = trca.transform(X, y)
        self.assertEqual(Z.shape, (X.shape[0], 1, X.shape[2]))

        trca = pyntbci.transformers.TRCA(n_components=3)
        trca.fit(X, y)
        self.assertEqual(trca.w_.shape, (X.shape[1], 3, np.unique(y).size))
        Z = trca.transform(X)
        self.assertEqual(Z.shape, (X.shape[0], 3, X.shape[2], np.unique(y).size))
        Z = trca.transform(X, y)
        self.assertEqual(Z.shape, (X.shape[0], 3, X.shape[2]))


if __name__ == "__main__":
    unittest.main()
