""" CRP: Classical Rodrigues Parameters: q_i = b_i / b_0.
    MRP: Modified Rodrigues Parameters: s_i = b_i / (1 + b_0).
"""
from functools import partial

import jax.numpy as jnp
from jax import jit

from jaxitude.base import Primitive


class CRP(Primitive):
    """ Classical Rodrigues parameter rotation class.
    """
    def __init__(self, q: jnp.ndarray) -> None:
        super().__init__()
        self.q = q
        self.dcm = self._build_crp(q)

    @partial(jit, static_argnums=0)
    def _build_crp(self, q: jnp.ndarray) -> jnp.ndarray:
        """ Builds dcm from CRP q parameters.

        Args:
            q (jnp.ndarray): 1x3 matrix of CRP parameters

        Returns:
            jnp.ndarray: 3x3 rotation matrix
        """
        c = 1. + jnp.dot(q, q)
        return jnp.array(
            [[1. + q[0]**2. - q[1]**2. - q[2]**2., 2. * (q[0] * q[1] + q[2]), 2. * (q[0] * q[2] - q[1])],
             [2. * (q[0] * q[1] - q[2]), 1. - q[0]**2. + q[1]**2. - q[2]**2., 2. * (q[1] * q[2] + q[0])],
             [2. * (q[0] * q[2] + q[1]), 2. * (q[1] * q[2] - q[0]), 1. - q[0]**2. - q[1]**2. + q[2]**2.]]
        ) / c

    def get_quat_from_q(self) -> jnp.ndarray:
        """ Builds Euler parameters from CRP q.

        Returns:
            jnp.ndarray: 1x4 matrix of Euler parameters b.
        """
        q_dot_q = jnp.dot(self.q, self.q)
        b0 = 1. / jnp.sqrt(1. + q_dot_q)
        return jnp.array(
            [b0,
             self.q[0] * b0,
             self.q[1] * b0,
             self.q[2] * b0]
        )

    def get_s_from_q(self) -> jnp.ndarray:
        """ Build MRP s from CRP q.

        Returns:
            jnp.ndarray: 1x3 matrix of MRP s parameters
        """
        denom = 1. + jnp.sqrt(1. + jnp.dot(self.q, self.q))
        return self.q / denom

    def inv_copy(self):
        """ Returns new instance of CRP with q -> -q.

        Returns:
            CRP: new instance inverse CRP.
        """
        return self.__class__(-self.q)


class MRP(Primitive):
    """ Classical Rodrigues parameter rotation class.
    """
    def __init__(self, s: jnp.ndarray) -> None:
        super().__init__()
        self.s = s
        self.dcm = self._build_mrp(s)

    def get_quat_from_s(self) -> jnp.ndarray:
        """ Builds Euler parameters from MRP s.

        Returns:
            jnp.ndarray: 1x4 matrix of Euler parameters b.
        """
        s_dot_s = jnp.dot(self.s, self.s)
        c = 1. / (1. + s_dot_s)
        return jnp.array(
            [(1. - s_dot_s) * c,
             2. * self.s[0] * c,
             2. * self.s[1] * c,
             2. * self.s[2] * c]
        )

    def get_q_from_s(self) -> jnp.ndarray:
        """ Build CRP q from MRP s.

        Returns:
            jnp.ndarray: 1x3 matrix of CRP q parameters:
        """
        denom = 1. - jnp.dot(self.s, self.s)
        return 2. * self.s / denom

    @partial(jit, static_argnums=0)
    def _build_mrp(self, s: jnp.ndarray) -> jnp.ndarray:
        """ Builds dcm from MRP s parameters.

        Args:
            s (jnp.ndarray): 1x3 matrix of MRP s parameters

        Returns:
            jnp.ndarray: 3x3 rotation matrix
        """
        c = 1. - jnp.dot(s, s)
        return jnp.array(
            [[4. * (s[0]**2. - s[1]**2. - s[2]**2.) + c**2., 8. * s[0] * s[1] + 4. * c * s[2], 8. * s[0] * s[2] - 4. * c * s[1]],
             [8. * s[0] * s[1] - 4. * c * s[2], 4. * (- s[0]**2. + s[1]**2. - s[2]**2.) + c**2., 8. * s[1] * s[2] + 4. * c * s[0]],
             [8. * s[0] * s[2] + 4. * c * s[1], 8. * s[1] * s[2] - 4. * c * s[0], 4. * (- s[0]**2. - s[1]**2. + s[2]**2.) + c**2.]]
        ) / (1. + jnp.dot(s, s))**2.

    def inv_copy(self):
        """ Returns new instance of MRP with q -> -q.

        Returns:
            MRP: new instance inverse MRP.
        """
        return self.__class__(-self.s)

    def get_shadow(self):
        """ Returns shadow set instance of MRP class.

        Returns:
            CRP: new instance shadow MRP.
        """
        s_shadow = MRP.shadow(self.s)
        return self.__class__(s_shadow)

    @staticmethod
    @jit
    def shadow(s: jnp.array) -> jnp.array:
        """ Calculates shadow set from 1x3 matrix of MRP s values.

        Args:
            s (jnp.array): MRP s 1x3 matrix.

        Returns:
            jnp.array: Shadow set of MRP s 1x3 matrix.
        """
        return -s / jnp.dot(s, s)
