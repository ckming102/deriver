"""Variational Derivatives to Numerical Stencils: Inflation Simulations

Based on arXiv:1608.04408 - "Robustness of Inflation to Inhomogeneous Initial Conditions"
by Clough, Lim, DiNunno, Fischler, Flauger, and Paban.

This notebook demonstrates how to:
1. Derive equations of motion from Lagrangians using variational calculus
2. Convert symbolic PDEs to finite difference stencils
3. Generate code for numerical simulations in multiple languages
"""

import marimo

__generated_with = "0.19.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    from derive import (
        Symbol, symbols, Function, Rational, R,
        D, Simplify, Expand,
        Exp, Sin, Cos, Sqrt, Pi,
        TeXForm, Pipe,
    )
    from derive.calculus import VariationalDerivative, EulerLagrangeEquation
    from derive.discretization import Discretize, ToStencil, StencilCodeGen
    return (
        D,
        Discretize,
        EulerLagrangeEquation,
        Expand,
        Function,
        Pipe,
        R,
        Rational,
        Simplify,
        StencilCodeGen,
        Sqrt,
        Symbol,
        TeXForm,
        ToStencil,
        VariationalDerivative,
        mo,
        symbols,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # From Lagrangians to Numerical Stencils

    This notebook demonstrates the complete pipeline from theoretical physics to
    numerical simulation code, based on the scalar field dynamics in
    [arXiv:1608.04408](https://arxiv.org/abs/1608.04408).

    ## The Physics

    Single-field inflation uses a scalar field with canonical kinetic term:

    $$\mathcal{L}_\phi = -\frac{1}{2}g^{\mu\nu}\partial_\mu \phi \partial_\nu\phi - V(\phi)$$

    The Klein-Gordon equation governing the field dynamics is:

    $$\partial_t^2 \phi - \gamma^{ij}\partial_i\partial_j\phi + \frac{dV}{d\phi} = 0$$

    We will derive this equation using variational calculus, then convert it to
    finite difference form suitable for numerical simulation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Deriving the Klein-Gordon Equation

    Starting from the scalar field Lagrangian density in flat spacetime:

    $$\mathcal{L} = \frac{1}{2}(\partial_t\phi)^2 - \frac{1}{2}(\partial_x\phi)^2 - V(\phi)$$

    The Euler-Lagrange equation gives us the equation of motion.
    """)
    return


@app.cell
def _(D, Function, R, Simplify, Symbol, VariationalDerivative, mo, symbols):
    # Define coordinates and field
    x, t = symbols('x t')
    phi = Function('phi')(x, t)
    m = Symbol('m', positive=True)  # mass parameter

    # Klein-Gordon Lagrangian: L = (1/2)(d_t phi)^2 - (1/2)(d_x phi)^2 - (1/2)m^2 phi^2
    L_KG = R(1, 2) * D(phi, t)**2 - R(1, 2) * D(phi, x)**2 - R(1, 2) * m**2 * phi**2

    # Derive the equation of motion
    eom_KG = VariationalDerivative(L_KG, phi, [x, t])

    mo.md(f"""
    **Klein-Gordon Lagrangian:**

    $\\mathcal{{L}} = {L_KG}$

    **Equation of Motion** ($\\delta\\mathcal{{L}}/\\delta\\phi = 0$):

    ${Simplify(eom_KG)} = 0$

    This is the Klein-Gordon equation: $\\partial_t^2\\phi - \\partial_x^2\\phi + m^2\\phi = 0$
    """)
    return L_KG, eom_KG, m, phi, t, x


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. The Wave Equation (Massless Limit)

    Setting $m = 0$ gives the wave equation, which appears in the gradient energy
    dominated regime of inflation simulations.
    """)
    return


@app.cell
def _(D, Function, R, Simplify, VariationalDerivative, mo, symbols):
    # Wave equation (massless Klein-Gordon)
    x_w, t_w = symbols('x t')
    phi_w = Function('phi')(x_w, t_w)

    L_wave = R(1, 2) * D(phi_w, t_w)**2 - R(1, 2) * D(phi_w, x_w)**2

    eom_wave = VariationalDerivative(L_wave, phi_w, [x_w, t_w])

    mo.md(f"""
    **Wave Equation Lagrangian:**

    $\\mathcal{{L}} = {L_wave}$

    **Equation of Motion:**

    ${Simplify(eom_wave)} = 0$

    This gives: $\\partial_t^2\\phi = \\partial_x^2\\phi$ (the wave equation)
    """)
    return L_wave, eom_wave, phi_w, t_w, x_w


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Converting to Finite Differences

    For numerical simulation, we need to discretize the spatial derivatives.
    The `Discretize` function converts symbolic derivatives to finite difference
    approximations using Taylor series matching.

    ### Central Difference Stencils

    For a 3-point central difference:
    - First derivative: $\frac{\partial f}{\partial x} \approx \frac{f(x+h) - f(x-h)}{2h}$
    - Second derivative: $\frac{\partial^2 f}{\partial x^2} \approx \frac{f(x+h) - 2f(x) + f(x-h)}{h^2}$
    """)
    return


@app.cell
def _(D, Discretize, Function, Simplify, Symbol, mo):
    # Discretization example
    x_d = Symbol('x')
    h = Symbol('h')  # grid spacing
    f = Function('f')(x_d)

    # Second derivative
    d2f_dx2 = D(f, (x_d, 2))

    # Central difference discretization
    stencil_3pt = Discretize(d2f_dx2, {x_d: ([x_d - h, x_d, x_d + h], h)})

    mo.md(f"""
    **Second Derivative Discretization (3-point central):**

    Symbolic: $\\frac{{\\partial^2 f}}{{\\partial x^2}}$

    Discretized: ${Simplify(stencil_3pt)}$

    This is the standard 3-point stencil: $\\frac{{f_{{i+1}} - 2f_i + f_{{i-1}}}}{{h^2}}$
    """)
    return d2f_dx2, f, h, stencil_3pt, x_d


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Discretizing the Wave Equation

    Now let's discretize the full wave equation for numerical simulation.
    """)
    return


@app.cell
def _(D, Discretize, Function, Simplify, mo, symbols):
    # Full wave equation discretization
    x_full, t_full = symbols('x t')
    hx, ht = symbols('h_x h_t')  # spatial and temporal grid spacing
    u = Function('u')(x_full, t_full)

    # Wave equation: d^2u/dt^2 - d^2u/dx^2 = 0
    wave_eq = D(u, (t_full, 2)) - D(u, (x_full, 2))

    # Discretize both derivatives
    step_map = {
        x_full: ([x_full - hx, x_full, x_full + hx], hx),
        t_full: ([t_full - ht, t_full, t_full + ht], ht),
    }
    wave_discrete = Discretize(wave_eq, step_map)

    mo.md(f"""
    **Wave Equation:**

    $\\frac{{\\partial^2 u}}{{\\partial t^2}} - \\frac{{\\partial^2 u}}{{\\partial x^2}} = 0$

    **Discretized Form:**

    ${Simplify(wave_discrete)} = 0$

    Rearranging for time-stepping: $u(x, t+h_t) = 2u(x,t) - u(x, t-h_t) + \\frac{{h_t^2}}{{h_x^2}}[u(x+h_x,t) - 2u(x,t) + u(x-h_x,t)]$
    """)
    return ht, hx, step_map, t_full, u, wave_discrete, wave_eq, x_full


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Higher-Order Stencils

    For better accuracy, we can use wider stencils. The `ToStencil` function
    automatically generates symmetric stencil points.
    """)
    return


@app.cell
def _(D, Function, Simplify, Symbol, ToStencil, mo):
    # Higher-order stencils
    x_ho = Symbol('x')
    h_ho = Symbol('h')
    f_ho = Function('f')(x_ho)

    # Compare 3-point and 5-point stencils for first derivative
    df_dx = D(f_ho, x_ho)

    stencil_3 = ToStencil(df_dx, {x_ho: h_ho}, width=3)
    stencil_5 = ToStencil(df_dx, {x_ho: h_ho}, width=5)

    mo.md(f"""
    **First Derivative Stencils:**

    3-point: ${Simplify(stencil_3)}$

    5-point: ${Simplify(stencil_5)}$

    The 5-point stencil provides 4th-order accuracy vs 2nd-order for 3-point.
    """)
    return df_dx, f_ho, h_ho, stencil_3, stencil_5, x_ho


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Code Generation

    The `StencilCodeGen` function converts discretized expressions to code
    in multiple programming languages - useful for generating numerical
    relativity simulation code.
    """)
    return


@app.cell
def _(D, Discretize, Function, StencilCodeGen, Symbol, mo):
    # Code generation example
    x_cg = Symbol('x')
    h_cg = Symbol('h')
    phi_cg = Function('phi')(x_cg)

    # Second derivative stencil
    d2phi = D(phi_cg, (x_cg, 2))
    stencil_cg = Discretize(d2phi, {x_cg: ([x_cg - h_cg, x_cg, x_cg + h_cg], h_cg)})

    # Generate code in different languages
    python_code = StencilCodeGen(stencil_cg, language='python',
                                  array_name='phi', index_var='i', spacing_name='dx')
    c_code = StencilCodeGen(stencil_cg, language='c',
                            array_name='phi', index_var='i', spacing_name='dx')
    fortran_code = StencilCodeGen(stencil_cg, language='fortran',
                                   array_name='phi', index_var='i', spacing_name='dx')
    latex_code = StencilCodeGen(stencil_cg, language='latex')

    mo.md(f"""
    **Code Generation for** $\\partial^2\\phi/\\partial x^2$:

    **Python:**
    ```python
    d2phi_dx2 = {python_code}
    ```

    **C:**
    ```c
    double d2phi_dx2 = {c_code};
    ```

    **Fortran:**
    ```fortran
    d2phi_dx2 = {fortran_code}
    ```

    **LaTeX:**
    ${latex_code}$
    """)
    return (
        c_code,
        d2phi,
        fortran_code,
        h_cg,
        latex_code,
        phi_cg,
        python_code,
        stencil_cg,
        x_cg,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Complete Pipeline: Lagrangian to Simulation Code

    Using derive's `Pipe` API, we can chain the entire workflow.
    """)
    return


@app.cell
def _(
    D,
    Discretize,
    Function,
    Pipe,
    R,
    StencilCodeGen,
    Symbol,
    VariationalDerivative,
    mo,
    symbols,
):
    # Complete pipeline example
    x_pipe, t_pipe = symbols('x t')
    h_pipe = Symbol('h')
    psi = Function('psi')(x_pipe, t_pipe)

    # Lagrangian for massless scalar field (1D)
    L_pipe = R(1, 2) * D(psi, t_pipe)**2 - R(1, 2) * D(psi, x_pipe)**2

    # Pipeline: Lagrangian -> EoM -> Discretize spatial part
    eom_spatial = (
        Pipe(L_pipe)
        .then(VariationalDerivative, psi, [x_pipe, t_pipe])
        .then(Discretize, {x_pipe: ([x_pipe - h_pipe, x_pipe, x_pipe + h_pipe], h_pipe)})
        .value
    )

    # Generate simulation code
    sim_code = StencilCodeGen(eom_spatial, language='python',
                               array_name='psi', index_var='i', spacing_name='dx')

    mo.md(f"""
    **Complete Pipeline:**

    1. Start with Lagrangian: $\\mathcal{{L}} = {L_pipe}$

    2. Derive equation of motion via variational derivative

    3. Discretize spatial derivatives

    4. Generate Python code:

    ```python
    # Equation of motion (set to zero and solve for time evolution)
    eom = {sim_code}
    ```

    This can be directly used in a time-stepping numerical scheme!
    """)
    return L_pipe, eom_spatial, h_pipe, psi, sim_code, t_pipe, x_pipe


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Application: Initial Conditions from arXiv:1608.04408

    The paper uses inhomogeneous initial conditions for the scalar field:

    $$\phi(t=0, \mathbf{x}) = \phi_0 + \frac{\Delta\phi}{N}\sum_{n=1}^{N}\left(\cos\frac{2\pi nx}{L} + \cos\frac{2\pi ny}{L} + \cos\frac{2\pi nz}{L}\right)$$

    With initial velocity:
    $$\frac{\partial\phi(t=0, \mathbf{x})}{\partial t} = 0$$

    The gradient energy density is:
    $$\rho_{\mathrm{grad}} = \frac{1}{2}\gamma^{ij}\partial_i\phi\partial_j\phi$$

    Let's compute the discretized gradient energy.
    """)
    return


@app.cell
def _(D, Discretize, Function, R, Simplify, Symbol, mo):
    # Gradient energy density discretization
    x_grad = Symbol('x')
    h_grad = Symbol('h')
    phi_grad = Function('phi')(x_grad)

    # Gradient energy: (1/2)(d phi/dx)^2
    rho_grad = R(1, 2) * D(phi_grad, x_grad)**2

    # Discretize
    rho_grad_discrete = Discretize(rho_grad, {x_grad: ([x_grad - h_grad, x_grad, x_grad + h_grad], h_grad)})

    mo.md(f"""
    **Gradient Energy Density (1D):**

    Continuous: $\\rho_{{\\mathrm{{grad}}}} = \\frac{{1}}{{2}}\\left(\\frac{{\\partial\\phi}}{{\\partial x}}\\right)^2$

    Discretized: $\\rho_{{\\mathrm{{grad}}}} = {Simplify(rho_grad_discrete)}$

    This uses the central difference approximation for the first derivative.
    """)
    return h_grad, phi_grad, rho_grad, rho_grad_discrete, x_grad


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    This notebook demonstrated the complete pipeline from physics to simulation:

    1. **Variational Calculus**: Derive equations of motion from Lagrangians
    2. **Discretization**: Convert PDEs to finite difference form
    3. **Code Generation**: Output simulation code in Python, C, or Fortran

    This workflow is directly applicable to numerical relativity codes like
    GRChombo (used in arXiv:1608.04408) for simulating inflation with
    inhomogeneous initial conditions.

    ### Key Functions Used:
    - `VariationalDerivative(L, field, coords)` - Euler-Lagrange equations
    - `Discretize(expr, step_map)` - Finite difference conversion
    - `ToStencil(expr, spacing, width)` - Convenience function with auto stencil generation
    - `StencilCodeGen(expr, language)` - Code generation
    - `Pipe(expr).then(...)` - Composable API for chaining operations
    """)
    return


if __name__ == "__main__":
    app.run()
