import numpy as np
from scipy.linalg import eigh, inv, sqrtm, svd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted


class CCA(BaseEstimator, TransformerMixin):
    """
    Canonical correlation analysis [1]_. Maximizes the correlation between two variables in their projected spaces.
    Here, CCA is implemented as the SVD of (cross)covariance matrices.

    References:
    .. [1] Hotelling, H. (1992). Relations between two sets of variates. In Breakthroughs in statistics: methodology and
           distribution (pp. 162-190). New York, NY: Springer New York. doi: 10.1007/978-1-4612-4380-9_14
    """

    def __init__(self, n_components, lx=None, ly=None, template_metric="mean"):
        """
        Constructor of CCA.

        Args:
            n_components: int
                The number of CCA components to use.
            lx: float | list (default: None)
                Regularization on the covariance matrix for CCA for all or each individual parameter along n_features_x.
                If None, no regularization is applied.
            ly: float | list (default: None)
                Regularization on the covariance matrix for CCA for all or each individual parameter along n_features_y.
                If None, no regularization is applied.
            template_metric: str (default: "mean")
                Metric to use to compute templates: mean, median.
        """
        self.n_components = n_components
        self.lx = lx
        self.ly = ly
        self.template_metric = template_metric

    def _fit_X2D_Y2D(self, X, Y):
        """
        Fit the CCA for a 2D X data matrix and 2D Y data matrix.

        Args:
            X: np.ndarray
                Data matrix of shape (n_samples, n_features_x).
            Y: np.ndarray
                Data matrix of shape (n_samples, n_features_y).

        Returns:
            np.ndarray
                Weight vector for X of shape (n_features_x, n_components).
            np.ndarray
                Weight vector for Y of shape (n_features_y, n_components).
            np.ndarray
                Mean vector of X of shape (n_features_x,).
            np.ndarray
                Mean vector of Y of shape (n_features_y,).
            np.ndarray
                Standard deviation vector of X of shape (n_features_x,).
            np.ndarray
                Standard deviation vector of Y of shape (n_features_y,).
        """
        X = check_array(X, ensure_2d=True, allow_nd=False)
        X = X.astype("float32")
        Y = check_array(Y, ensure_2d=True, allow_nd=False)
        Y = Y.astype("float32")

        # Zero mean
        mu_x = np.mean(X, axis=0, keepdims=True)
        mu_y = np.mean(Y, axis=0, keepdims=True)
        X -= mu_x
        Y -= mu_y

        # Unit variance
        sigma_x = np.std(X, axis=0, keepdims=True)
        sigma_y = np.std(Y, axis=0, keepdims=True)
        X /= sigma_x
        Y /= sigma_y

        # Regularization penalty
        if self.lx is None:
            lx = np.zeros((1, X.shape[1]))
        elif isinstance(self.lx, int) or isinstance(self.lx, float):
            lx = self.lx * np.ones((1, X.shape[1]))
        elif np.array(self.lx).ndim == 1:
            lx = np.array(self.lx)[np.newaxis, :]
        else:
            lx = self.lx
        if self.ly is None:
            ly = np.zeros((1, Y.shape[1]))
        elif isinstance(self.ly, int) or isinstance(self.ly, float):
            ly = self.ly * np.ones((1, Y.shape[1]))
        elif np.array(self.ly).ndim == 1:
            ly = np.array(self.ly)[np.newaxis, :]
        else:
            ly = self.ly

        # Covariance matrices
        C = np.cov(np.concatenate((X, Y), axis=1).T)
        Cxx = C[:X.shape[1], :X.shape[1]] + lx @ np.eye(X.shape[1])
        Cxy = C[:X.shape[1], X.shape[1]:]
        Cyy = C[X.shape[1]:, X.shape[1]:] + ly @ np.eye(Y.shape[1])

        # Inverse square root
        iCxx = np.real(inv(sqrtm(Cxx)))
        iCyy = np.real(inv(sqrtm(Cyy)))

        # SVD
        U, s, V = svd(iCxx @ Cxy @ iCyy)

        # Compute projection vectors
        Wx = iCxx @ U
        Wy = iCyy @ V.T

        w_x = Wx[:, :self.n_components]
        w_y = Wy[:, :self.n_components]

        return w_x, w_y, mu_x, mu_y, sigma_x, sigma_y

    def _fit_X3D_Y3D(self, X, Y):
        """
        Fit the CCA for a 3D X data matrix and 3D Y data matrix.

        Args:
            X: np.ndarray
                Data matrix of shape (n_trials, n_features_x, n_samples).
            Y: np.ndarray
                Data matrix of shape (n_trials, n_features_y, n_samples).

        Returns:
            np.ndarray
                Weight vector for X of shape (n_features_x, n_components).
            np.ndarray
                Weight vector for Y of shape (n_features_y, n_components).
            np.ndarray
                Mean vector of X of shape (n_features_x,).
            np.ndarray
                Mean vector of Y of shape (n_features_y,).
            np.ndarray
                Standard deviation vector of X of shape (n_features_x,).
            np.ndarray
                Standard deviation vector of Y of shape (n_features_y,).
        """
        X = check_array(X, ensure_2d=False, allow_nd=True)
        X = X.astype("float32")
        Y = check_array(Y, ensure_2d=False, allow_nd=True)
        Y = Y.astype("float32")

        n_trials, n_features_x, n_samples = X.shape
        n_features_y = Y.shape[1]

        # Create aligned matrices
        X = X.transpose((0, 2, 1)).reshape((n_samples * n_trials, n_features_x))
        Y = Y.transpose((0, 2, 1)).reshape((n_samples * n_trials, n_features_y))

        # CCA
        w_x, w_y, mu_x, mu_y, sigma_x, sigma_y = self._fit_X2D_Y2D(X, Y)

        return w_x, w_y, mu_x, mu_y, sigma_x, sigma_y

    def _fit_X3D_Y1D(self, X, Y):
        """
        Fit the CCA for a 3D X data matrix and 1D Y label vector.

        Args:
            X: np.ndarray
                Data matrix of shape (n_trials, n_features_x, n_samples).
            Y: np.ndarray
                Label vector of shape (n_trials,).

        Returns:
            np.ndarray
                Weight vector for X of shape (n_features_x, n_components).
            np.ndarray
                Weight vector for Y of shape (n_features_y, n_components).
            np.ndarray
                Mean vector of X of shape (n_features_x,).
            np.ndarray
                Mean vector of Y of shape (n_features_y,).
            np.ndarray
                Standard deviation vector of X of shape (n_features_x,).
            np.ndarray
                Standard deviation vector of Y of shape (n_features_y,).
        """
        X, Y = check_X_y(X, Y, ensure_2d=False, allow_nd=True, y_numeric=True)
        X = X.astype("float32")
        Y = Y.astype(np.uint)

        n_trials, n_channels, n_samples = X.shape
        labels = np.unique(Y)
        n_classes = labels.size

        # Compute templates
        T = np.zeros((n_classes, n_channels, n_samples))
        for i, label in enumerate(labels):
            T[i, :, :] = np.mean(X[Y == labels[i], :, :], axis=0)

        # CCA
        w_x, w_y, mu_x, mu_y, sigma_x, sigma_y = self._fit_X3D_Y3D(X, T[Y, :, :])

        return w_x, w_y, mu_x, mu_y, sigma_x, sigma_y

    def fit(self, X, Y):
        """
        Fit the CCA in one of 3 ways: (1) X (data) is 3D and y (labels) is 1D, (2) X (data) is 3D and Y (data) is 3D,
        or (3) X (data) is 2D and Y (data) is 2D.

        Args:
            X: np.ndarray
                Data matrix of shape (n_trials, n_features_x, n_samples) or (n_samples, n_features_x).
            Y: np.ndarray
                Data matrix of shape (n_trials, n_features_y, n_samples) or (n_samples, n_features_y), or
                label vector of shape (n_trials,).

        Returns:
            CCA
                Itself.
        """
        if X.ndim == 3 and Y.ndim == 1:
            self.w_x_, self.w_y_, self.mu_x_, self.mu_y_, self.sigma_x_, self.sigma_y_ = self._fit_X3D_Y1D(X, Y)
        elif X.ndim == 3 and Y.ndim == 3:
            self.w_x_, self.w_y_, self.mu_x_, self.mu_y_, self.sigma_x_, self.sigma_y_ = self._fit_X3D_Y3D(X, Y)
        elif X.ndim == 2 and Y.ndim == 2:
            self.w_x_, self.w_y_, self.mu_x_, self.mu_y_, self.sigma_x_, self.sigma_y_ = self._fit_X2D_Y2D(X, Y)
        else:
            raise Exception(f"Dimensions of X and/or Y are not valid: X={X.shape}, Y={Y.shape}.")

        return self

    def _transform_X2D(self, X, mu, sigma, w):
        """
        Transform the 2D data matrix from feature space to component space.

        Args:
            X: np.ndarray
                Data matrix of shape (n_samples, n_features).
            mu: np.ndarray
                Means of shape (1, n_features).
            sigma: np.ndarray
                Standard deviations of shape (1, n_features).
            w: np.ndarray
                Weight vector of shape (n_features, n_components).

        Returns:
            np.ndarray
                Projected data matrix of shape (n_samples, n_components).
        """
        X = check_array(X, ensure_2d=True, allow_nd=False)
        X = X.astype("float32")
        X -= mu
        X /= sigma
        return np.dot(X, w)

    def _transform_X3D(self, X, mu, sigma, w):
        """
        Transform the 3D data matrix from feature space to component space.

        Args:
            X: np.ndarray
                Data matrix of shape (n_trials, n_features, n_samples).
            mu: np.ndarray
                Means of shape (1, n_features).
            sigma: np.ndarray
                Standard deviations of shape (1, n_features).
            w: np.ndarray
                Weight vector of shape (n_features, n_components).

        Returns:
            np.ndarray
                Projected data matrix of shape (n_trials, n_components, n_samples).
        """
        X = check_array(X, ensure_2d=False, allow_nd=True)
        X = X.astype("float32")
        n_trials, n_channels, n_samples = X.shape
        X = X.transpose((0, 2, 1)).reshape((n_trials * n_samples, n_channels))
        return self._transform_X2D(X, mu, sigma, w).reshape((n_trials, self.n_components, n_samples))

    def transform(self, X=None, Y=None):
        """
        Transform the data matrix from feature space to component space. Note, works with both 2D and 3D data, and can
        operate on both X and Y if both are not None, or on each separately if the other is None.

        Args:
            X: np.ndarray (default: None)
                Data matrix of shape (n_samples, n_features_x) or (n_trials, n_features_x, n_samples).
                If None, only performs projection of Y.
            Y: np.ndarray (default: None)
                Data matrix of shape (n_samples, n_features_y) or (n_trials, n_features_y, n_samples).
                If None, only performs projection of X.

        Returns:
            X: np.ndarray
                Projected data matrix of shape (n_samples, n_components) or (n_trials, n_components, n_samples).
            Y: np.ndarray
                Projected data matrix of shape (n_samples, n_components) or (n_trials, n_components, n_samples).
        """
        check_is_fitted(self, ["w_x_", "w_y_", "mu_x_", "mu_y_", "sigma_x_", "sigma_y_"])

        # Projection of  X
        if X is not None:
            if X.ndim == 2:
                X = self._transform_X2D(X, self.mu_x_, self.sigma_x_, self.w_x_)
            elif X.ndim == 3:
                X = self._transform_X3D(X, self.mu_x_, self.sigma_x_, self.w_x_)
            if Y is None:
                return X

        # Projection of Y
        if Y is not None:
            if Y.ndim == 2:
                Y = self._transform_X2D(Y, self.mu_y_, self.sigma_y_, self.w_y_)
            elif Y.ndim == 3:
                Y = self._transform_X3D(Y, self.mu_y_, self.sigma_y_, self.w_y_)
            if X is None:
                return Y

        return X, Y


class TRCA(BaseEstimator, TransformerMixin):
    """
    Task related component analysis [1]_. Maximizes the intra-class covariances, i.e., the intra-class consistenty.
    TRCA was applied to (SSVEP) BCI [2]_. Alternative implementations, also used as example for this code, see Matlab
    code in [1]_ for the original, Matlab code in [3]_ for the SSVEP BCI introduction, and two Python implementation in
    MOABB [4]_, and MEEGKit [5]_.

    References:
    .. [1] Tanaka, H., Katura, T., & Sato, H. (2013). Task-related component analysis for functional neuroimaging and
           application to near-infrared spectroscopy data. NeuroImage, 64, 308-327.
           doi: 10.1016/j.neuroimage.2012.08.044
    .. [2] Nakanishi, M., Wang, Y., Chen, X., Wang, Y. T., Gao, X., & Jung, T. P. (2017). Enhancing detection of SSVEPs
           for a high-speed brain speller using task-related component analysis. IEEE Transactions on Biomedical
           Engineering, 65(1), 104-112. doi: 10.1109/TBME.2017.2694818
    .. [3] https://github.com/mnakanishi/TRCA-SSVEP/blob/master/src/train_trca.m
    .. [4] https://github.com/NeuroTechX/moabb/blob/develop/moabb/pipelines/classification.py
    .. [5] https://github.com/nbara/python-meegkit/blob/master/meegkit/trca.py
    """

    def __init__(self, n_components):
        """
        Constructor of TRCA.

        Args:
            n_components: int
                The number of TRCA components to use.
        """
        self.n_components = n_components

    def _fit_X(self, X):
        """
        Fit TRCA without labels by computing one filter across all trials.

        Args:
            X: np.ndarray
                Data matrix of shape (n_trials, n_features, n_samples).

        Returns:
            np.ndarray:
                The learned weights of shape (n_features, n_components).
        """
        X = check_array(X, ensure_2d=False, allow_nd=True)
        X = X.astype("float32")
        n_trials, n_channels, n_samples = X.shape

        # Covariance of all data
        Xa = X.transpose((1, 0, 2)).reshape((n_channels, n_trials * n_samples))
        Xa -= Xa.mean(axis=1, keepdims=True)
        Q = Xa.dot(Xa.T)

        # Covariance of pairs of trials
        S = np.zeros((n_channels, n_channels))
        for i_trial in range(n_trials - 1):
            Xi = X[i_trial, :, :]
            Xi -= Xi.mean(axis=1, keepdims=True)
            for j_trial in range(1 + i_trial, n_trials):
                Xj = X[j_trial, :, :]
                Xj -= Xj.mean(axis=1, keepdims=True)
                S += (Xi.dot(Xj.T) + Xj.dot(Xi.T))

        # Eigenvalue decomposition
        D, V = eigh(S, Q)
        return V[:, np.argsort(D)[::-1][:self.n_components]]

    def _fit_X_y(self, X, y):
        """
        Fit TRCA with labels by computing a filter across all trials of the same label, for each class.

        Args:
            X: np.ndarray
                Data matrix of shape (n_trials, n_features, n_samples).
            y: np.ndarray
                Label vector of shape (n_trials,).

        Returns:
            np.ndarray:
                The learned weights of shape (n_features, n_components, n_classes).
        """
        X, y = check_X_y(X, y, ensure_2d=False, allow_nd=True, y_numeric=True)
        X = X.astype("float32")
        y = y.astype(np.uint)

        n_trials, n_channels, n_samples = X.shape
        classes = np.unique(y)
        n_classes = classes.size
        W = np.zeros((n_channels, self.n_components, n_classes))
        for i_class in range(n_classes):
            W[:, :, i_class] = self._fit_X(X[y == classes[i_class], :, :])
        return W

    def fit(self, X, y=None):
        """
        Fit TRCA in one of 2 ways: (1) without labels (y=None) or with labels (y=vector). If no labels are provided,
        TRCA will compute one filter across all labels. If labels are provided, one filter will be computed for each of
        the classes.

        Args:
            X: np.ndarray
                Data matrix of shape (n_trials, n_features, n_samples) or (n_samples, n_features).
            y: np.ndarray
                Label vector of shape (n_trials,).

        Returns:
            TRCA
                Itself.
        """
        if y is None:
            self.w_ = self._fit_X(X)
        else:
            self.w_ = self._fit_X_y(X, y)

        return self

    def transform(self, X, y=None):
        """
        Transform the data matrix from feature space to component space. Note, can operate on both X and y or just X. If
        X and y are provided, data are filtered with class-specific filters. If only X is provided and a multi-class
        filter was learned, all trials are filtered with all filters. If only one filter was learned, then only this
        filter is applied.

        Args:
            X: np.ndarray
                Data matrix of shape (n_trials, n_features, n_samples).
            y: np.ndarray (default: None)
                Label vector of shape (n_trials,). Can be None.

        Returns:
            X: np.ndarray
                Projected data matrix of shape (n_trials, n_components, n_samples) if X and y were provided, of shape
                (n_trials, n_components, n_samples, n_classes) if y=None and multi-class filters were learned, and
                (n_trials, n_components, n_samples) if y=None and one pooled filter was learned.
        """
        check_is_fitted(self, ["w_"])
        n_trials, n_channels, n_samples = X.shape
        if y is None:
            X = check_array(X, ensure_2d=False, allow_nd=True)
            X = X.astype("float32")
            if self.w_.ndim == 2:
                Y = np.dot(
                    X.transpose((0, 2, 1)).reshape((n_trials * n_samples, n_channels)), self.w_
                ).reshape((n_trials, n_samples, self.n_components)).transpose((0, 2, 1))
            else:
                n_classes = self.w_.shape[2]
                Y = np.zeros((n_trials, self.n_components, n_samples, n_classes))
                for i_class in range(n_classes):
                    Y[:, :, :, i_class] = np.dot(
                        X.transpose((0, 2, 1)).reshape((n_trials * n_samples, n_channels)), self.w_[:, :, i_class]
                    ).reshape((n_trials, n_samples, self.n_components)).transpose((0, 2, 1))
        else:
            X, y = check_X_y(X, y, ensure_2d=False, allow_nd=True, y_numeric=True)
            X = X.astype("float32")
            y = y.astype(np.uint)
            Y = np.zeros((n_trials, self.n_components, n_samples))
            for i_trial in range(n_trials):
                Y[i_trial, :, :] = np.dot(self.w_[:, :, y[i_trial]].T, X[i_trial, :, :])
        return Y
