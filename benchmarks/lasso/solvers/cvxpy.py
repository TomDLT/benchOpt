from benchopt.base import BaseSolver
from benchopt.util import safe_import


with safe_import() as solver_import:
    import cvxpy as cp
    # Hack cvxpy to be able to retrieve a sub optimal solution when
    # reaching max_iter
    cp.reductions.solvers.conic_solvers.ECOS.STATUS_MAP[-1] = \
        'optimal_inaccurate'


class Solver(BaseSolver):
    name = 'cvxpy'

    install_cmd = 'pip'
    requirements = ['cvxpy']

    def set_objective(self, X, y, lmbd):
        self.X, self.y, self.lmbd = X, y, lmbd

        n_features = self.X.shape[1]
        self.beta = cp.Variable(n_features)

        loss = 0.5 * cp.norm2(self.y - cp.matmul(self.X, self.beta))**2
        self.problem = cp.Problem(cp.Minimize(
            loss + self.lmbd * cp.norm(self.beta, 1)))

        cp.settings.ERROR = ['solver_error']
        # log_likelihood = cp.sum(
        #     cp.multiply(y, X @ self.beta) - cp.logistic(X @ self.beta)
        # )
        # self.problem = cp.Problem(cp.Maximize(
        #     log_likelihood / n_features - self.lmbd * cp.norm(self.beta, 1)))
        # self.problem.solve(verbose=True)

    def run(self, n_iter):
        self.problem.solve(max_iters=n_iter, verbose=False)

    def get_result(self):
        return self.beta.value.flatten()
