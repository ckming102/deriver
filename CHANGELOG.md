# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New `utils/validation.py` module with reusable validation utilities
  - `validate_tuple`, `validate_range_tuple`, `validate_positive`, `validate_nonnegative`
  - `ValidationError` exception class for consistent error handling
- New `utils/functional.py` module with higher-order functions and functional patterns
  - `matrix_method` factory for creating matrix operations from method names
  - `symbolic_to_callable` wrapper for SymPy lambdify with sensible defaults
  - Functional utilities: `curry`, `flip`, `foldl`, `foldr`, `scanl`, `scanr`

### Changed
- Moved all mid-function imports to module top-level (PEP 8 compliance)
  - display.py: Optional dependencies (rich, IPython) now imported at module level with availability flags
  - notebook.py: IPython and Marimo imports moved to top with IPYTHON_AVAILABLE/MARIMO_AVAILABLE flags
  - numbers.py: Moved re and sympy.parsing imports to top level
  - optimize/core.py: cvxpy imports moved to top with CVXPY_AVAILABLE flag
  - functions/number.py: mpmath imports moved to top with MPMATH_AVAILABLE flag
  - compose.py: sympy simplify/expand/factor/collect moved to top level
  - transforms.py: sympy.Integral import moved to top level
  - indices.py: collections.Counter and sympy.tensorcontraction moved to top
  - symmetry.py: Removed redundant itertools.product imports from functions (already at module level)
  - cache.py: sympy.simplify moved to top level
  - lazy.py: sympy.simplify moved to top level
  - functions/utils.py: sympy.printing imports moved to top level

### Improved
- Refactored `algebra/linear.py` to use `matrix_method` factory pattern for DRY compliance
  - `Det`, `Tr`, `MatrixRank`, `NullSpace`, `MatrixExp` now use factory pattern
  - Added `_ensure_matrix` helper to reduce code duplication
- Added `@lru_cache` memoization to pure functions in `diffgeo/symmetry.py`
  - `symmetric_index_pairs` and `symmetric_christoffel_indices` now cached
- Optimized Ricci tensor and Einstein tensor computation to exploit symmetry
  - `ricci_tensor()` now computes only n(n+1)/2 unique components (R_uv = R_vu)
  - `einstein_tensor()` now computes only n(n+1)/2 unique components (G_uv = G_vu)
- Optimized nested loops using itertools.product for cleaner code
  - transforms.py: Jacobian and metric transformation now use iterproduct
  - metrics.py: Ricci tensor and Einstein tensor use iterproduct; covariant derivative uses sum comprehensions
- Documentation example in variational.py now uses derive's D() instead of SymPy's diff()
- Pre-computed metric substitutions in coordinate transforms for better performance

### Fixed
- Replaced bare `except` clauses with specific exception types for better error handling
  - `patterns/matching.py`: Rule.apply and ReplaceAll now catch (TypeError, ValueError, AttributeError)
  - `patterns/functions.py`: PatternFunction matching now catches specific exceptions
  - `utils/compose.py`: FixedPoint and FixedPointList now catch (TypeError, ValueError, AttributeError)
  - `core/numbers.py`: rationalize and nsimplify now catch (TypeError, ValueError)

## [0.1.0] - 2026-01-18

### Added
- Initial release of derive symbolic mathematics library
- Core symbolic computation functionality built on SymPy
- Numerical computation support via NumPy and SciPy
- Data manipulation with Polars integration
- Visualization capabilities through Matplotlib
- Interactive notebook support with marimo
- GitHub-rendered notebook exports

### Fixed
- LaTeX printing issue
- Variable aliasing issue (#1)
