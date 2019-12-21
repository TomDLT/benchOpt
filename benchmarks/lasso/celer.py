from celer import Lasso

from benchopt.base import BaseSolver


class Solver(BaseSolver):
    name = 'Celer'

    def set_loss(self, loss_parameters):
        self.X, self.y, self.lmbd = loss_parameters

        n_samples = self.X.shape[0]
        self.lasso = Lasso(
            alpha=self.lmbd/n_samples, max_iter=1, gap_freq=10,
            max_epochs=100000, p0=10, verbose=False, tol=1e-12, prune=True,
            fit_intercept=False, normalize=False, warm_start=False,
            positive=False
        )

    def run(self, n_iter):
        self.lasso.max_iter = n_iter
        self.lasso.fit(self.X, self.y)

    def get_result(self):
        return self.lasso.coef_.flatten()
