import netket as nk
import numpy as np
from typing import Tuple, Union, List, Optional


class DMOp(nk.operator.GraphOperator):
    r"""
    The Heisenberg hamiltonian on a lattice.
    """

    def __init__(
        self,
        hilbert: nk.hilbert.AbstractHilbert,
        graph: nk.graph.AbstractGraph,
        J: float = 1,
        H: float = 0,
        DM: float = 0,
        *,
        acting_on_subspace: Union[List[int], int] = None,
    ):
        """
        Constructs an Heisenberg operator given a hilbert space and a graph providing the
        connectivity of the lattice.

        Args:
            hilbert: Hilbert space the operator acts on.
            graph: The graph upon which this hamiltonian is defined.
            J: The strength of the coupling. Default is 1.
               Can pass a sequence of coupling strengths with coloured graphs:
               edges of colour n will have coupling strength J[n]
            sign_rule: If True, Marshal's sign rule will be used. On a bipartite
                lattice, this corresponds to a basis change flipping the Sz direction
                at every odd site of the lattice. For non-bipartite lattices, the
                sign rule cannot be applied. Defaults to True if the lattice is
                bipartite, False otherwise.
                If a sequence of coupling strengths is passed, defaults to False
                and a matching sequence of sign_rule must be specified to override it
            acting_on_subspace: Specifies the mapping between nodes of the graph and
                Hilbert space sites, so that graph node :code:`i ∈ [0, ..., graph.n_nodes - 1]`,
                corresponds to :code:`acting_on_subspace[i] ∈ [0, ..., hilbert.n_sites]`.
                Must be a list of length `graph.n_nodes`. Passing a single integer :code:`start`
                is equivalent to :code:`[start, ..., start + graph.n_nodes - 1]`.

        Examples:
         Constructs a ``Heisenberg`` operator for a 1D system.

            >>> import netket as nk
            >>> g = nk.graph.Hypercube(length=20, n_dim=1, pbc=True)
            >>> hi = nk.hilbert.Spin(s=0.5, total_sz=0, N=g.n_nodes)
            >>> op = nk.operator.Heisenberg(hilbert=hi, graph=g)
            >>> print(op)
            Heisenberg(J=1.0, sign_rule=True; dim=20)
        """
        self._J = J
        self._DM = DM
        
        # sigma_x*sigma_x + sigma_y*sigma_y + sigma_z*sigma_z
        J_op = np.array(
            [
                [1, 0, 0, 0],
                [0, -1, 2, 0],
                [0, 2, -1, 0],
                [0, 0, 0, 1],
            ]
        )

        DM_op = np.array(
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ]
        )

        H_op = np.array(
            [
                [1, 0],
                [0, -1],
            ]
        )

        site_ops = [H_op]

        bond_ops = [J * J_op + DM * DM_op]
        bond_ops_colors = []

        super().__init__(
            hilbert,
            graph,
            site_ops=site_ops,
            bond_ops=bond_ops,
            bond_ops_colors=bond_ops_colors,
            acting_on_subspace=acting_on_subspace,
        )

    @property
    def J(self) -> float:
        """The coupling strength."""
        return self._J

    @property
    def DM(self) -> float:
        """The coupling strength."""
        return self._DM

    def __repr__(self):
        return f"Heisenberg(J={self._J}, DM={self._DM}; dim={self.hilbert.size})"
