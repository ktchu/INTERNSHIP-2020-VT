2020-07-07: Notes on Portfolio Optimization
-------------------------------------------

*Author*: Kevin Chu `<kevin@velexi.com>`

*Last Updated*: 2020-07-08

-------------------------------------------------------------------------------

Preface
-------

* This document is written using GitHub Markdown.  It is best viewed using a
  Markdown viewer that supports GitHub Markdown:

  * [Chrome Markdown Viewer][chrome-markdown-viewer]

    * _Note_: be sure to enable the following extension settings

      * Automatically allow access on the following sites
        * `file:///*`

      * Allow access to file URLS

  * [Atom Editor](https://atom.io/)

-------------------------------------------------------------------------------

## 1. Model Problems in Portfolio Optimization

Two model problems in portfolio optimization are presented below. In studying
the model problems, it is important to distinguish between (1) the optimization
technique and (2) the asset pricing model. For the model problems, the results
are relatively straightforward to calculate and interpret. However, their
applicability to real-world finance is limited due to weaknesses of the asset
pricing model. The optimization techniques (or variations of them) are valid
for all asset pricing models (assuming certain mathematical conditions
are satisfied).

### 1.1. Definitions

* __Return (Relative)__. The return on an asset over a time period is the
  relative change in the price of an asset from the beginning to the end of
  the time period:

  \[
    r = \frac{P_{final} - P_{initial}}{P_{initial}}
      = \frac{P_{final}}{P_{initial}} - 1
  \]

  When the difference between the final and initial prices is small, the
  return may be approximated by

  \[
    r = \log \left( \frac{P_{final}}{P_{initial}} \right)
  \]

  * _Absolute Return_. The relative return is the return per unit investment
    in the asset. The _absolute return_ is the actual amount of money earned
    from investment in an asset:

    \[
      R = r P_{initial}.
    \]

  * _Note_: the term "return" can be used to refer to both relative and
    absolute returns. The meaning can usually be determined from the context.

* __Risk__. In quantiative finance, the variance and standard deviation of
  an asset's return are convenient (but not necessarily valid or accurate)
  measure of an assets riskiness. In financial parlance, the standard
  deviation of an asset's return is known as _volatility_.

  * ___Intuition___. Given a choice between two assets, a "rational" investor
    would rather own the asset that is less volatile.

  * ___Criticisms___. There are many criticisms of the use of volatility as a
    measure of risk. For instance, volatility is a symmetric measure of risk
    (i.e., positive and negative price movements are equally weighted), but
    behavioral economics research has shown that people typically give more
    weight to losses than to gains.

### 1.2. Portfolio Return and Risk

The relative return and risk of a portfolio can be computed in terms of

* $r_i$: the return of the $i$-th asset

* $\sigma_i^2$: the variances of the return for the $i$-th asset

  * For convenience, we will let $\sigma_{ii}$ be an alternate notation for
    $\sigma_i^2$.

* $\sigma_{ij}$: the covariances between returns of assets $i$ and $j$

* $w_i$: the weight (fraction) of $i$-th asset

If there are $n$ assets that could be included in the portfolio, the portfolio
return and variance are:

\[
  r_p = \sum_{i = 1}^n r_i w_i \\
  \sigma_p^2 = \sum_{i=1}^n \sum_{j=1}^n \sigma_{ij} w_i w_j
\]

In vector notation

\[
  r_p = \mathbf{r}^T \mathbf{w} \\
  \sigma_p^2 = \mathbf{w}^T \mathbf{\sigma} \mathbf{w}
\]

where

\[
  \mathbf{w} = [w_1, w_2, \ldots w_n]^T \\
  \mathbf{r} = [r_1, r_2, \ldots r_n]^T \\
  \mathbf{\sigma}
  = \left[
      \begin{array}{cccc}
        \sigma_{11} & \sigma_{12} & \ldots & \sigma_{1n} \\
        \sigma_{21} & \sigma_{22} & \ldots & \sigma_{2n} \\
        \vdots      & \vdots      & \ddots & \vdots      \\
        \sigma_{n1} & \sigma_{n2} & \ldots & \sigma_{nn}
      \end{array}
    \right]
\]

#### Absolute Return and Absolute Risk of a Portfolio

The absolute return and absolute risk of a portfolio can be expressed in terms
of

* $R_i$: the absolute return of the $i$-th asset

* $\tilde{\sigma}_i^2$: the variances of the absolute return for the $i$-th
  asset

* $\tilde{\sigma}_{ij}$: the covariances between the absolute returns of assets
  $i$ and $j$

* $N_i$: the number of units/shares of the $i$-th asset

If there are $n$ assets that could be included in the portfolio, the absolute
return and risk of the portfolio are:

\[
  R_p = \sum_{i = 1}^n R_i N_i \\
  \tilde{\sigma}_p^2 = \sum_{i=1}^n \sum_{j=1}^n \tilde{\sigma}_{ij} N_i N_j
\]

### 1.3. Modern Portfolio Theory (Mean-Variance Analysis)

In this section, we show how to find the optimal portfolio when the objective
function is defined in terms of relative returns. The same approaches can be
used when the objective function is defined in terms of absolute returns.

#### 1.3.1. Optimal Portfolio with a Risk Tolerance

To find an optimal portfolio, we first need to define what "optimal" means. An
intuitive definitions is the following: the portfolio that maximizes the
return while minimizing the risk. To make this mathematically precise, we
define an objective function that encapsulates this intuitive goal:

\[
  F_\tau (w_1, w_2, \ldots, w_n)
  =   r_p(w_1, w_2, \ldots, w_n)
    - \frac{\tau}{2} \sigma_p^2(w_1, w_2, \ldots, w_n) \\
  =   \sum_{i = 1}^n r_i w_i
    - \frac{\tau}{2} \sum_{i=1}^n \sum_{j=1}^n \sigma_{ij} w_i w_j
\]

where $\tau$ is a risk-tolerance parameter. The factor of 1/2 multiplying the
risk term is present for mathematical convenience.

Before we can optimize the objective function, we also need to identify any
constraints that the solution must satisfy. For the objective function
$F_\tau$, we require that

\[
  \sum_{i = 1}^n w_i = 1
\]

To maximize this objective function subject to the constraints on the $w_i$, we
use the method of _Lagrange multipliers_. The key idea underlying this method
is that by augmenting the objective function by adding one term and one
variable (a Lagrange multiplier) for each constraint equation, we can
transform the problem from an optimization with constraints to an optimization
problem _without_ constraints. The augmented objective function is called the
_Lagrangian function_.

1. For each constraint, we add a term of the form
   $\lambda f(w_1, w_2, \ldots, w_n)$ to the original objective function
   $F(w_1, w_2, \ldots, w_n)$ where $f(w_1, w_2, \ldots, w_n) = 0$ is
   equivalent to the constraint equation.

   For the constraint $\sum_{i = 1}^n w_i = 1$, we add a term of the form

    \[
      \lambda \left( 1 - \sum_{i = 1}^n w_i \right)
    \]

   to arrive at the augmented objective function

    \[
      \hat{F}_\tau (w_1, w_2, \ldots, w_n, \lambda)
      =   F_\tau (w_1, w_2, \ldots, w_n)
        - \lambda \left( 1 - \sum_{i = 1}^n w_i \right).
    \]

2. Next, we maximize $\hat{F}_\tau (w_1, w_2, \ldots, w_n, \lambda)$ _without_
   any constraints. The magic of the method of Lagrange multipliers is that the
   constraints are _automatically_ satisfied by the intuitive approach of
   "setting the derivative of the augmented objective function to zero."

   For scalar function $F$ of multiple $n$ variables, the derivative is an
   $n$-dimensional vector of _partial derivatives_ known as the _gradient_ of
   $F$ and is denoted by $\nabla F$:

    \[
      \textrm{(gradient of $F$)} = \nabla F = \left[
        \frac{\partial F}{\partial x_1},
        \frac{\partial F}{\partial x_2},
        \ldots,
        \frac{\partial F}{\partial x_n}
      \right]
    \]

   where the $i$-th partial derivative is computed by differentiating $F$
   with respect to $x_i$ while keeping all of the other variables constant.

   Taking the partial derivatives of $\hat{F}$, we find that

    \[
      \frac{\partial \hat{F}_\tau}{\partial x_1}
      = \frac{\partial F_\tau}{\partial x_1} - \lambda
      = r_1 - \tau \sum_{i = 1}^n \sigma_{1i} w_i - \lambda \\

      \frac{\partial \hat{F}_\tau}{\partial x_2}
      = \frac{\partial F_\tau}{\partial x_2} - \lambda
      = r_2 - \tau \sum_{i = 1}^n \sigma_{2i} w_i - \lambda \\

      \vdots \\

      \frac{\partial \hat{F}_\tau}{\partial x_n}
      = \frac{\partial F_\tau}{\partial x_n} - \lambda
      = r_n - \tau \sum_{i = 1}^n \sigma_{ni} w_i - \lambda \\

      \frac{\partial \hat{F}_\tau}{\partial \lambda}
      =   \frac{\partial \hat{F}_\tau}{\partial x_n}
        - \left( 1 - \sum_{i = 1}^n w_i \right)
      = - \left( 1 - \sum_{i = 1}^n w_i \right)
    \]

   To set the derivative equal to zero, we set _all_ of the partial derivatives
   equal to 0.

    \[
      \left[
        \frac{\partial F}{\partial x_1},
        \frac{\partial F}{\partial x_2},
        \ldots,
        \frac{\partial F}{\partial x_n}
      \right]
      = [0, 0, \ldots, 0]
    \]

   which yields the system of equations

    \[
      \tau \sum_{i = 1}^n \sigma_{1i} w_i - \lambda = r_1 \\
      \tau \sum_{i = 1}^n \sigma_{2i} w_i - \lambda = r_2 \\
      \vdots \\
      \tau \sum_{i = 1}^n \sigma_{ni} w_i - \lambda = r_n \\
      \sum_{i = 1}^n w_i = 1
    \]

   Notice how the constraint equation is automatically satisfied when the
   partial derivative associated with its Lagrange multiplier is set to zero.

   Since this system of equations is _linear_, it can be expressed in matrix
   form as

    \[
      \left[\begin{array}{ccccc}
        \tau \sigma_{11} & \tau \sigma_{12} & \ldots & \tau \sigma_{1n} & -1 \\
        \tau \sigma_{21} & \tau \sigma_{22} & \ldots & \tau \sigma_{2n} & -1 \\
        \vdots & \vdots & \ddots & \vdots & \vdots \\
        \tau \sigma_{n1} & \tau \sigma_{n2} & \ldots & \tau \sigma_{nn} & -1 \\
        1 & 1 & \ldots & 1 & 0
      \end{array}\right]
      \left[\begin{array}{c}
        w_1 \\
        w_2 \\
        \vdots \\
        w_n \\
        \lambda
      \end{array}\right]
      =
      \left[\begin{array}{c}
        r_1 \\
        r_2 \\
        \vdots \\
        r_n \\
        1
      \end{array}\right]
    \]

3. To find the optimal portfolio, we solve the system of linear equations.
   If we have numerical estimates for the asset returns, variances, and
   covariances, then the system of equations is straightforward to solve
   using many readily available software packages (e.g., numpy, scipy, MATLAB,
   R, Octave).

#### 1.3.2. The Efficient Frontier

The relationship between risk and return of optimal portfolios forms the
foundation of several key results in quantitative finance. The curve
risk-return plane that represents optimal portfolios (for varying values of
$\tau$) is known as the _efficient frontier_.

One approach for compute the risk-return relationship is to compute risk and
return for various values of $\tau$ using the method from Section 1.3.1 to
solve the portfolio optimization problem for each $\tau$. However, it is
informative and enlightening to derive the efficient frontier from a slightly
different perspective. Rather than specifying a risk tolerance, we consider the
following variant of the portfolio optimization problem:

* for a specified value of the portfolio return, find the portfolio with the
  minimum risk.

Formulated mathematically, we want to minimize the variance

\[
  V(w_1, w_2, \ldots, w_n)
  = \sigma_p^2(w_1, w_2, \ldots, w_n)
  = \sum_{i=1}^n \sum_{j=1}^n \sigma_{ij} w_i w_j
\]

subject to the two constraints

\[
  \sum_{i = 1}^n w_i = 1 \\
  \sum_{i = 1}^n r_i w_i = \mu
\]

where $\mu$ is a specified value for the portfolio return.

Since there are two constraints, we add to Lagrange multiplier terms to form
the Lagrangian function:

\[
\hat{V} (w_1, w_2, \ldots, w_n, \alpha, \beta)
=   \sum_{i=1}^n \sum_{j=1}^n \sigma_{ij} w_i w_j
  + \alpha \left( 1 - \sum_{i = 1}^n w_i \right)
  + \beta \left( \mu - \sum_{i = 1}^n r_i w_i \right)
\]

Setting the gradient of $\hat{V}$ to zero, we obtain the following linear
system of equations:

\[
  \sum_{j = 1}^n \sigma_{1j} w_j - \alpha - \beta r_1 = 0 \\
  \sum_{j = 1}^n \sigma_{1j} w_j - \alpha - \beta r_2 = 0 \\
  \vdots \\
  \sum_{j = 1}^n \sigma_{1j} w_j - \alpha - \beta r_n = 0 \\
  \sum_{j = 1}^n w_j = 1 \\
  \sum_{j = 1}^n r_j w_j = \mu
\]

Interestingly, we can find the relationship between the variance and the
return $\mu$ without explicitly solving the system of equations. Taking the
sum of the first $n$ equations multiplied by the asset weighting $w_i$, we
find that

\[
0
= \sum_{i = 1}^n w_i
    \left( \sum_{j = 1}^n \sigma_{1j} w_j - \alpha - \beta r_i \right) \\
=   \sum_{i = 1}^n \sum_{j = 1}^n \sigma_{1j} w_i w_j
  - \alpha \sum_{i = 1}^n w_i
  - \beta \sum_{i = 1}^n w_i r_i \\
=   \sigma_p^2 - \alpha - \beta \mu.
\]

Rearranging this equation, we find that the portfolio return $\mu$ is a
quadratic function of the volatility (standard deviation) of the optimal
portfolio:

\[
  r_p = \mu = \frac{1}{\beta} \left( \sigma_p^2 - \alpha \right).
\]

In other words, _the efficient frontier is a parabola in the risk-return plane_.

##### Matrix Formulation of Analysis

In matrix form, the system of equations representing $\nabla \hat{V} = 0$ is

\[
\left[\begin{array}{ccccc}
  \sigma_{11} & \sigma_{12} & \ldots & \sigma_{1n} & -1 & -r_1 \\
  \sigma_{21} & \sigma_{22} & \ldots & \sigma_{2n} & -1 & -r_2 \\
  \vdots & \vdots & \ddots & \vdots & \vdots & \vdots \\
  \sigma_{n1} & \sigma_{n2} & \ldots & \sigma_{nn} & -1 & -r_n \\
  1   & 1   & \ldots & 1   & 0 & 0 \\
  r_1 & r_2 & \ldots & r_n & 0 & 0
\end{array}\right]
\left[\begin{array}{c}
  w_1 \\
  w_2 \\
  \vdots \\
  w_n \\
  \alpha \\
  \beta
\end{array}\right]
=
\left[\begin{array}{c}
  0 \\
  0 \\
  \vdots \\
  0 \\
  1 \\
  \mu
\end{array}\right]
\]

Breaking this into three matrix-vector multiplications, we find that

\[
\left[\begin{array}{ccc}
  \sigma_{11} & \sigma_{12} & \ldots & \sigma_{1n} \\
  \sigma_{21} & \sigma_{22} & \ldots & \sigma_{2n} \\
  \vdots & \vdots & \ddots & \vdots \\
  \sigma_{n1} & \sigma_{n2} & \ldots & \sigma_{nn}
\end{array}\right]
\left[\begin{array}{c}
  w_1 \\
  w_2 \\
  \vdots \\
  w_n
\end{array}\right]
=
\alpha \left[\begin{array}{c}
  1 \\
  1 \\
  \vdots \\
  1
\end{array}\right] +
\beta \left[\begin{array}{c}
  r_1 \\
  r_2 \\
  \vdots \\
  r_n
\end{array}\right]
\]
\[
[1 1 \ldots 1]
\left[\begin{array}{c}
  w_1 \\
  w_2 \\
  \vdots \\
  w_n
\end{array}\right]
= [w_1 w_2 \ldots w_n]
\left[\begin{array}{c}
  1 \\
  1 \\
  \vdots \\
  1
\end{array}\right]
= 1
\]
\[
[r_1 r_2 \ldots r_n]
\left[\begin{array}{c}
  w_1 \\
  w_2 \\
  \vdots \\
  w_n
\end{array}\right]
= [w_1 w_2 \ldots w_n]
\left[\begin{array}{c}
  r_1 \\
  r_2 \\
  \vdots \\
  r_n
\end{array}\right]
= \mu
\]

Multiplying the first matrix equation on the left by $[w_1 w_2 \ldots w_n]$,
we obtain

\[
[w_1 w_2 \ldots w_n]
\left[\begin{array}{ccc}
  \sigma_{11} & \sigma_{12} & \ldots & \sigma_{1n} \\
  \sigma_{21} & \sigma_{22} & \ldots & \sigma_{2n} \\
  \vdots & \vdots & \ddots & \vdots \\
  \sigma_{n1} & \sigma_{n2} & \ldots & \sigma_{nn}
\end{array}\right]
\left[\begin{array}{c}
  w_1 \\
  w_2 \\
  \vdots \\
  w_n
\end{array}\right]
=   \alpha [w_1 w_2 \ldots w_n]
      \left[\begin{array}{c}
        1 \\
        1 \\
        \vdots \\
        1
      \end{array}\right]
  + \beta [w_1 w_2 \ldots w_n]
      \left[\begin{array}{c}
        r_1 \\
        r_2 \\
        \vdots \\
        r_n
      \end{array}\right]
\]

Recognizing that the left-hand side is $\sigma_p^2$ and that the right-hand
side can be simplified using the second and third equations from
$\nabla \hat{V} = 0$, we arrive at

\[
  \sigma_p^2 = \alpha + \beta \mu
\]

-------------------------------------------------------------------------------

## 2. Exercises

1. Explore the relationships between optimal portfolio formulations.

   a. Derive the efficient frontier using the formulation of the optimal
      portfolio problem that uses an objective function involving both risk
      and return.

   b. Find the relationship between the risk tolerance parameter $\tau$
      and $\lambda$ and the Lagrange multipliers in the optimal portfolio
      formulation problem that uses an objective function involving only risk.

-------------------------------------------------------------------------------

## 3. References

* [Wikipedia: Modern portfolio theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory)

* [Wikipedia: Markowitz model](https://en.wikipedia.org/wiki/Markowitz_model)

[-----------------------------EXTERNAL LINKS-----------------------------]: #

[chrome-markdown-viewer]: https://chrome.google.com/webstore/detail/markdown-viewer/ckkdlimhmcjmikdlpkmbgfkaikojcbjk
