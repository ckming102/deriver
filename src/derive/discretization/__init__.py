"""
Discretization module - Convert symbolic derivatives to finite difference stencils.

Provides tools for discretizing variational derivatives and generating
numerical simulation code in multiple programming languages.
"""

from derive.discretization.stencils import (
    Discretize,
    Discretizer,
    ToStencil,
    StencilCodeGen,
)

__all__ = [
    'Discretize',
    'Discretizer',
    'ToStencil',
    'StencilCodeGen',
]
