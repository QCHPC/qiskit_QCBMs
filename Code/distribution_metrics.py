"""
distribution_metrics.py

Unified module for distribution comparison, kernel metrics,
information-theoretic losses, and entropy-regularized optimal transport.

Callable as:
    from distribution_metrics import DistributionMetrics as DM
"""

import numpy as np
import qiskit  # kept for downstream quantum workflows and namespace consistency


class DistributionMetrics:
    """
    Stateless utility namespace for:
    - Kernel-based metrics (RBF, MMD)
    - Information-theoretic divergences (KL)
    - Bitstring / probability utilities
    - Sinkhorn (entropy-regularized OT) distance
    """

    # ------------------------------------------------------------------
    # Kernel utilities
    # ------------------------------------------------------------------

    @staticmethod
    def rbf_kernel(x, y, gamma):
        return np.exp(-gamma * (x - y) ** 2)

    @staticmethod
    def compute_kernel_matrix(space: np.ndarray, gammas: np.ndarray) -> np.ndarray:
        sq_dists = np.abs(space[:, None] - space[None, :]) ** 2
        K = sum(np.exp(-gamma * sq_dists) for gamma in gammas) / len(gammas)
        return K

    @staticmethod
    def kernel_expectation(px: np.ndarray, py: np.ndarray, kernel_matrix: np.ndarray) -> float:
        return px.T @ kernel_matrix @ py

    @staticmethod
    def mmd_loss(px: np.ndarray, py: np.ndarray, kernel_matrix: np.ndarray) -> float:
        diff = px - py
        return DistributionMetrics.kernel_expectation(diff, diff, kernel_matrix)

    # ------------------------------------------------------------------
    # Information-theoretic utilities
    # ------------------------------------------------------------------

    @staticmethod
    def kl_divergence(p: np.ndarray, q: np.ndarray, eps: float = 1e-12) -> float:
        p = np.clip(p, eps, 1.0)
        q = np.clip(q, eps, 1.0)
        return np.sum(p * np.log(p / q))

    @staticmethod
    def safe_log(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
        return np.log(np.clip(x, eps, None))

    @staticmethod
    def normalize_probs(probs: np.ndarray) -> np.ndarray:
        total = np.sum(probs)
        return probs / total if total > 0 else probs

    # ------------------------------------------------------------------
    # Bitstring utilities
    # ------------------------------------------------------------------

    @staticmethod
    def int_to_bitstring(n: int, length: int) -> str:
        return format(n, f"0{length}b")

    @staticmethod
    def bitstring_to_int(bitstring: str) -> int:
        return int(bitstring, 2)

    @staticmethod
    def probs_to_bitstrings(prob_vector: np.ndarray, threshold: float = 1e-6) -> list:
        n = int(np.log2(len(prob_vector)))
        return [
            DistributionMetrics.int_to_bitstring(i, n)
            for i, p in enumerate(prob_vector)
            if p > threshold
        ]

    @staticmethod
    def compute_chi(samples: list, valid_bitstrings: list) -> float:
        return np.mean([s in valid_bitstrings for s in samples])

    # ------------------------------------------------------------------
    # Sinkhorn / Optimal Transport
    # ------------------------------------------------------------------

    @staticmethod
    def sinkhorn_kernel(cost_matrix: np.ndarray, epsilon: float) -> np.ndarray:
        return np.exp(-cost_matrix / epsilon)

    @staticmethod
    def build_cost_matrix(space: np.ndarray) -> np.ndarray:
        diff = space[:, None] - space[None, :]
        return diff * diff

    @staticmethod
    def sinkhorn_loss(
        p: np.ndarray,
        q: np.ndarray,
        space: np.ndarray = None,
        epsilon: float = 0.05,
        max_iter: int = 200,
        tol: float = 1e-9,
    ) -> float:
        p = p.astype(float)
        q = q.astype(float)
        p /= np.sum(p)
        q /= np.sum(q)

        if space is None:
            space = np.arange(len(p), dtype=float)

        C = DistributionMetrics.build_cost_matrix(space)
        K = DistributionMetrics.sinkhorn_kernel(C, epsilon)
        K += 1e-300

        u = np.ones_like(p)
        v = np.ones_like(q)

        for _ in range(max_iter):
            u_prev = u.copy()
            u = p / (K @ v)
            v = q / (K.T @ u)

            if np.linalg.norm(u - u_prev, ord=1) < tol:
                break

        T = np.outer(u, v) * K
        return float(np.sum(T * C))

    @staticmethod
    def sinkhorn_report(p: np.ndarray, q: np.ndarray, epsilon: float = 0.05) -> float:
        space = np.arange(len(p), dtype=float)
        val = DistributionMetrics.sinkhorn_loss(p, q, space=space, epsilon=epsilon)
        print(f"Sinkhorn OT (eps={epsilon}): {val}")
        return val
