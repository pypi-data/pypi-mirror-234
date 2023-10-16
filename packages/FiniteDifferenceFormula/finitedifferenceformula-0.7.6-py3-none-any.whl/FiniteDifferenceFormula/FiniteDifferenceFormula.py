"""
Ported from a Julia package, https://github.com/Winux2k/FiniteDifferenceFormula.jl,
this Python package provides a general finite difference formula generator and a
tool for teaching/learning the finite difference method. It generates finite
difference formulas for derivatives of various orders by using Taylor series
expansions of a function at evenly spaced points. It also gives the truncation
error of a formula in the big-O notation. We can use it to generate new formulas
in addition to verification of known ones. By changing decimal places, we can
also see how rounding errors may affect a result.

Beware, though formulas are mathematically correct, they may not be numerically
useful. This is true especially when we derive formulas for a derivative of higher
order. For example, run compute(9,range(-5, 6)), provided by this package, to
generate a 10-point central formula for the 9-th derivative. The formula is
mathematically correct, but it can hardly be put into use for numerical computing
without, if possible, rewriting it in a special way. Similarly, the more points
are used, the more precise a formula is mathematically. However, due to rounding
errors, this may not be true numerically.

The package exports a class, FDFormula, fd (an object of the class), and member
functions, activatepythonfunction, compute, decimalplaces, find, findbackward,
findforward, formula, formulas, taylor, taylorcoefs, tcoefs, truncationerror,
verifyformula.

See also https://github.com/fdformula/FiniteDifferenceFormula.py/blob/main/README.md.
"""
#-------------------------------------------------------------------------------
# Name:        FiniteDifferenceFormula
#
# Purpose:     A general finite difference formula generator and a teaching
#              tool of the finite difference method
#
# Author:      david wang, dwang at liberty dot edu
#
# Created:     01/27/2023
# Copyright:   (c) dwang 2023
# Licence:     MIT License
#
# This code is ported from my Julia package FiniteDifferenceFormula found
# at https://github.com/Winux2k/FiniteDifferenceFormula.jl
#-------------------------------------------------------------------------------
from fractions import Fraction
import math

class _FDData:
    n      : int
    points : list
    k      : list
    m      : Fraction
    coefs  : list

    def __init__(self, n, points, k, m, coefs):
        self.n = n
        self.points = points
        self.k = k
        self.m = m
        self.coefs = coefs
# end of class _FDData

class FDFormula:
    _data : _FDData           = None  # share results between functions
    _computedq                = False # make sure compute() is called first
    _formula_status           = 0     # a formula may not be available
                                      # values? see _test_formula_validity()

    _NUM_OF_EXTRA_TAYLOR_TERMS= 8     # for examining truncation error
    _decimal_places : int     = 16    # for generating Python function(s)
                                      # call decimalplaces(n) to reset it

    # a vector of the coefficients of Taylor series of the linear combination:
    # k[1]*f(x[i+points[1]]) + k[2]*f(x[i+points[2]]) + ...
    _lcombination_coefs       = None

    _range_inputq             = False
    _range_input              = range(0,0) # compute receives a range? save it

    _python_exact_func_expr   = ""    # 1st exact Python function for f**(n)(x[i])
    _python_exact_func_expr1  = ""    # 2nd exact Python function for f**(n)(x[i])
    _python_decimal_func_expr = ""    # decimal Python function for f**(n)(x[i])
    _python_func_basename     = ""

    _bigO : str               = ""    # truncation error of a formula
    _bigO_exp : int           = -1    # the value of n as in O(h**n)

    # lambda functions of generated formula
    fde                       = None
    fde1                      = None
    fdd                       = None

    # environment for experiments
    _x                        = []
    _h                        = 0.01

    # This function returns the first 'max_num_of_terms' terms of Taylor series of
    # f(x[i+1]) centered at x=x[i] in a column vector with f(x[i]), f'(x[i]), ...,
    # removed. The purpose is to obtain Taylor series expansions for f(x[i±k]) =
    # f(x[i]±kh]) which are used to derive the m-point finite difference formulas
    # for the first, second, ..., order derivatives at x[i].
    #
    #       f(x[i+1]) = f(x[i]) + 1/1! f'(x[i]) h + 1/2! f''(x[i]) h**2 + ...
    #
    # where h = x[i+1] - x[i].
    #
    # Usage:
    #   for f(x[i+k]), call _taylor_coefs(k, ...), k = ±0, ±1, ±2, ...
    def _taylor_coefs(self, h, max_num_of_terms = 30):
        result = [None] * max_num_of_terms
        factorial = 1
        for n in range(max_num_of_terms): # order of derivatives in Taylor series
            if n > 0:
                factorial *= n
            result[n] = (Fraction(1, factorial)) * (h ** n)
        return result  # a column vector
    # end of _taylor_coefs

    # for future coders/maintainers of this package:
    # to compute a new formula, this function must be called first.
    def _initialization(self):
        self._data                     = None
        self._computedq                = False
        self._formula_status           = 0
        self._lcombination_coefs       = None

        self._range_inputq             = False
        self._range_input              = None

        self._python_exact_func_expr   = ""
        self._python_exact_func_expr1  = ""
        self._python_decimal_func_expr = ""
        self._python_func_basename     = ""

        self._bigO                     = ""
        self._bigO_exp                 = -1

        self.fde                       = None
        self.fde1                      = None
        self.fdd                       = None
    # end of _initialization

    # convert a coefficient to a readable string
    def _c2s(self, c, first_termq = False, decimalq = False):
        s = ""
        if c < 0:
            if first_termq:
                s = "-"
            else:
                s = " - "
        elif not first_termq:
            s = " + "

        c = abs(c)
        d = round(c)
        if d == c:
            if c != 1:
                s += str(d) + " "
        elif decimalq:
            fmt = "%." + str(self._decimal_places) + "f "
            s += fmt % float(c)
        else:
            s += str(c.numerator) + "/" + str(c.denominator) + " "

        return s
    # end of _c2s

    # convert f(x[i+k]) to a readable string
    def _f2s(self, k):
        s = "f(x[i"
        if k != 0:
            if k > 0:
                s += "+"
            s += str(k)
        return s + "])"
    # end of _f2s

    # print readable Taylor series
    #
    # Input: An array that contains the coefficients of the first terms of Taylor
    #        series expansion of a function
    def _print_taylor(self, coefs, num_of_nonzero_terms = 10):
        first_termq = True
        for n in range(len(coefs)):
            if coefs[n] == 0:
                continue

            print(self._c2s(coefs[n], first_termq), sep = '', end = '')
            if abs(coefs[n]) != 1:
                print("* ", sep = '', end = '')
            if n <= 3:
                print("f", "'" * n, "(x[i])", sep = '', end = '')
            else:
                print("f**(", n, ")(x[i])", sep = '', end = '')
            if n >= 1:
                print(" * h", sep = '', end = '')
                if n > 1:
                    print("**", n, sep = '', end = '')
            first_termq = False

            num_of_nonzero_terms -= 1
            if num_of_nonzero_terms == 0:
                break
        print(" + ...")
    # end of _print_taylor

    def _dashline(self, n = 105):
        return "-" * n

    def _validate_input(self, n, points, printformulaq = False):
        if (not isinstance(n, int)) or n < 1:
            print("Invalid order of derivatives, ", n, ". A positive integer",
                  " is expected.", sep = '')
            return []

        length = len(points)
        all_intq = True
        for i in points:
            if not isinstance(i, int):
                all_intq = False
                break
        if length == 0 or isinstance(points, tuple) or not all_intq:
            print("Invalid input, ", points, ". A list of integers like",
                  " range(-1, 3) or [-1, 0, 1, 2] is expected.", sep = '')
            return []
        if not isinstance(printformulaq, bool):
            print("Invalid input, ", printformulaq, ". A value, False or ",
                  "True, is expected.", sep = '')

        oldpoints = list(points) # v0.7.4
        points = sorted(set(points))
        length = len(points)
        if length < 2:
            print("Invalid input, ", points, ". A list of two or more ",
                  "different points is expected.", sep = '')
            return []

        self._initialization()
        if oldpoints != points:
            input_points = self._format_of_points(points)
            print(self._dashline(), "\nYour input is converted to (", n, ", ",
                  input_points, sep = '', end = '')
            if printformulaq:
                print(", True", sep = '', end = '')
            print(").\n", self._dashline(), sep = '')
        else:
            self._format_of_points(points)   # no change; set _range_input[q]

        return points
    # end of _validate_input

    def compute(self, n, points, printformulaq = False):
        """
        Compute a formula for the nth order derivative using the given points.

                    n: the n-th order derivative to be found
               points: in the format of a range(start, stop) or a list
        printformulaq: print the computed formula or not

        |  points     |   The points/nodes to be used             |
        | ----------- | ----------------------------------------- |
        | range(0:3)  |   x[i], x[i+1], x[i+2]                    |
        | range(-2:1) |   x[i-2], x[i-1], x[i]                    |
        | range(-2:3) |   x[i-2], x[i-1], x[i], x[i+1], x[i+2]    |
        | [1, 1, -1]  |   x[i-1], x[i+1]                          |

        A list will be rearranged so that elements are ordered from lowest to
        highest with duplicate ones removed.

        Examples
        ========
        fd.compute(2, [0, 1, 2, 3])
        fd.compute(2, range(0, 4))
        fd.compute(3, [-5, -2, 1, 2, 4], True)
        """
        points = self._validate_input(n, points, printformulaq)
        if points == []:
            return None
        return self._compute(n, points, printformulaq)
    # end of compute

    def find(self, n, points, printformulaq = False):
        """
        Compute a formula for the nth order derivative using the given points.

        For the input, n and points (See [compute]), there may not
        be formulas which use the two end points like -2 and 3 in -2 : 3 or [-2, -1,
        0, 1, 2, 3]. In this case, find tries to find a formula by shrinking
        the range to, first -1 : 3, then, -2 : 2, then -1 : 2, and so on, until a
        formula is found or no formulas can be found at all.

        See also [compute], [findbackward], and [findforward].

        Examples
        ========
        fd.find(2, range(-10, 10))
        """
        points = self._validate_input(n, points, printformulaq)
        if points == []:
            return None
        result = self._compute(n, points, printformulaq)
        while result == None and len(points) > n + 1:   # failed
            if self._range_inputq:
                self._range_input = range(points[1], points[-1] + 1)
            result = self._compute(n, points[1 : ], printformulaq)

            if result == None:
                if self._range_inputq:
                    self._range_input = range(points[0], points[-1])
                result = self._compute(n, points[ : - 1], printformulaq)

                if result == None:
                    points.pop()
                    points.pop(0)  # points = points[2 : end - 1]
                    if self._range_inputq:
                        self._range_input = range(points[0], points[-1] + 1)
        return result
    # end of find

    def _findforward(self, n, points, printformulaq = False, forwardq:bool = True):
        points = self._validate_input(n, points, printformulaq)
        if points == []:
            return None
        result = self._compute(n, points, printformulaq)
        while result == None and len(points) > n + 1:   # failed
            #points = forwardq ? points[2 : end] : points[1 : end - 1]
            if forwardq:
                points.pop(0)
            else:
                points.pop()
            if self._range_inputq:
                self._range_input = range(points[1], points[-1] + 1)
            result = self._compute(n, points, printformulaq)
        return result
    # end of _findforward

    def findforward(self, n, points, printformulaq = False):
        """
        Compute a formula for the nth order derivative using the given points.

        For the input, n and points (See [compute]), there may not
        be formulas which use the two end points like -2 and 3 in -2 : 3 or [-2, -1,
        0, 1, 2, 3]. In this case, findforward tries to find a formula by
        shrinking the range from the left endpoint to, first -1 : 3, then, 0 : 3,
        then 1 : 3, and so on, until a formula is found or no formulas can be found
        at all.

        See also [compute], [find], and [findbackward].

        Examples
        ========
        fd.findforward(2, range(-10, 10))
        """
        return self._findforward(n, points, printformulaq, True)

    def findbackward(self, n, points, printformulaq = False):
        """
        Compute a formula for the nth order derivative using the given points.

        For the input, n and points (See [compute]), there may not
        be formulas which use the two end points like -2 and 3 in -2 : 3 or [-2, -1,
        0, 1, 2, 3]. In this case, findbackward tries to find a formula by
        shrinking the range from the right endpoint to, first -2 : 2, then, -2 : 1,
        then -2 : 0, and so on, until a formula is found or no formulas can be found
        at all.

        See also [compute], [find], and [findforward].

        Examples
        ========
        fd.compute(3,range(-100, 51))
        fd.findbackward(3,range(-99, 51))
        """
        return self._findforward(n, points, printformulaq, False)

    #
    # Algorithm
    # ---------
    # General generator of finite difference formulas for the n-th order
    # derivatives of f(x) at x[i] using points in a sorted list, e.g., [-2, -1,
    # 0, 1, 3, 5, 6, 7].
    #
    # It uses the linear combination of f(x[i+j]), j in points, to eliminate
    # f(x[i]), f'(x[i]), ..., so that the first term of the Taylor series
    # expansion of the linear combination is f**(n)(x[i]):
    #
    #  k[1]*f(x[i+points[1]]) + k[2]*f(x[i+points[2]]) + ...
    #     = m*f**(n)(x[i]) + ..., m > 0, len = length(points)
    #
    # It is this equation that gives the formula for computing f**(n)(x[i]).
    #
    # Values of the cofficients k[:] and m will be determined, and the first few
    # terms of the remainder will be listed for calculating the truncation error
    # of a formula.
    #
    # Python's Fraction type and related arithmetic operations, defined in module
    # fractions, are a perfect fit for obtaining an "exact" formula.
    #
    # Input  See 'compute'
    # -----
    # Output
    # ------
    # The function returns a tuple, (n, points, [k[1], k[2], ..., k[len]], m).
    #
    def _compute(self, n, points, printformulaq = False):
        self._computedq = False
        self._formula_status = 0
        self._bigO = ""
        points = sorted(set(points))
        #
        # for teaching's purpose, we don't do so:
        # if len(points) <= n
        #     pts = _range_inputq ? "$(_range_input)" : "$(points')"
        #     th = n == 1 ? "st" : (n == 2 ? "nd" : (n == 3 ? "rd" : "th"))
        #     println("$pts is invalid because at least $(n + 1) points are ",
        #             "needed for the $n$th derivative.")
        #     return None
        # end
        #
        # setup a linear system Ak = B first
        length = len(points)
        max_num_of_terms = max(length, n) + self._NUM_OF_EXTRA_TAYLOR_TERMS
        #
        # setup the coefficients of Taylor series expansions of f(x) at each of
        # the involved points
        #
        self._lcombination_coefs = [Fraction(0,1)] * max_num_of_terms
        coefs = [Fraction(0,1)] * max_num_of_terms
        for i in range(length):
            coefs[i] = self._taylor_coefs(points[i], max_num_of_terms)
        #
        # We find a linear combination of
        # f(x[i+points[1]]), f(x[i+points[2]]), ..., f(x[i+points[len]]),
        #
        # k[1]*f(x[i+points[1]]) + k[2]*f(x[i+points[2]]) + ...
        #  = 0*f(x[i]) + 0*f'(x[i]) + ... + 0*f**(n-1)(x[i]) + m*f**(n)(x[i]) + ...
        #    m != 0
        #
        # so that it must eliminate f(x[i]), f'(x[i]), ..., f**(n-1)(x[i]); given
        # more points, it also eliminates f**(n+1)(x[i]), f**(n+2)(x[i]), ....
        #
        # For example, to eliminate f(x[i]), we have
        #
        #    k[1]*coefs[1][1] + k[2]*coefs[2][1] + ... + k[len]*coefs[len][1] = 0
        #
        # and to eliminate f'(x[i]), we have
        #
        #    k[1]*coefs[1][2] + k[2]*coefs[2][2] + ... + k[len]*coefs[len][2] = 0
        #
        # Therefore, a linear system is detemined by the following equations
        #
        #  k[1]*coefs[1][j] + k[2]*coefs[2][j] + ... + k[len]*coefs[len][j] = 0 ... (1)
        #
        # where j = 1, 2, ..., len but not n.
        #
        A = [[Fraction(0) for col in range(length)] for row in range(length)]
        A[0][0]      = Fraction(1)  # 1st row is [1, 0,...,0] so that k[1] = 1
        k = [Fraction(0) for col in range(length)]
        k[0] = 1
        #
        row = 1
        for order in range(length):  # correspond to f(x[i]), f'(x[i]), f''(x[i]), ...
            if order == n:
                continue             # skip f**(n)(x[i])
            #
            # eliminating f**(order)(x[i])
            # A[:,j] stores coefs of
            #  k[1]*coefs[1][j] + k[2]*coefs[2][j] + ... + k[len]*coefs[len][j] = 0
            for j in range(length):
                A[row][j] = coefs[j][order]
            row += 1
            if row == length:
                break

        # The homogeneous linear system (1) has no nontrivial solution or has
        # inifinitely many nontrivial solutions. It is understandable that it may
        # not have a nontrivial solution. But why inifinitely many nontrivial
        # solutions? It is because, if k[:] is a nontrivial solution, α k[:] is
        # also a nontrivial solution, where α is any nonzero real constant, i.e.,
        # all nontrivial solutions (a subspace spanned by this k[:]) are parallel
        # to each other. Therefore, in the case that there are infinitely many
        # nontrivial solutions, if we know one entry k[which] is nonzero and let
        # it be a nonzero constant (say, 1), then, a nontrivial solution k[:] is
        # uniquely determined.
        #
        # Beware, there may be multiple nontrivial solutions,
        #  k[:] = [k1, k2, ...], k[:] = [K1, K2, ...], ..., or k[:] = [κ1, κ2, ...]
        # of which no two are parallel to each other. However, each of these
        # solutions must satisfy the condition that both k[1] and k[end] can't be
        # zero. Why? If, say, k[1] = 0, in other words, a formula only uses/depends
        # on (at most) x[i+points[2]], x[i+points[3]], ..., x[i+points[len]], why
        # should we say it is a formula that uses/depends on x[i+points[1]] (and
        # x[i+points[2]], ..., x[i+points[len]])? Therefore, we can assume that
        # k[1] != 0.
        #
        # solve Ak = B for k
        # A = self._rref(A) # _rref(A) is removed and its code is as follows. 10/5/2023

        # -------------------------- begin of _rref(A) --------------------------
        # input: A, n x (n + 1) "matrix" of Fraction numbers
        # output: a "matrix" in reduced row echelon form
        #
        # input: A = [1 0 0 ... 0 | 1; ...] # the 1st row is set so

        # optimized again on 10/5/2023 for the purpose of this project. at the
        # end, # A is "virtually" an identity matrix (but not actually). the time
        # performance has a 35% increase with Julia.
        #
        # assume: A is invertible
        #
        # Apply Gauss-Jordan elimination to [A | k] and k is finally the solution
        row = length - 1
        i = 0
        while i < row: # Gauss elimination
            j = i + 1
            # make A[i][i] the pivotal entry
            if i != 0:                      # A[0][0] is already the pivotal entry
                m, mi = abs(A[i][i]), i     # pivoting by finding the largest entry
                for r in range(j, length):  # on A[i : length][i]
                    absv = abs(A[r][i])
                    if absv > m:
                        m, mi = absv, r
                if mi != i:                 # interchange two rows
                    A[i][i : length], A[mi][i : length] = A[mi][i : length], A[i][i : length]
                    k[i], k[mi] = k[mi], k[i]

                # Can A[i][i] == 0 ?!
                for c in range(j, length):      # have A[i][i] = 1
                    A[i][c] /= A[i][i]
                k[i] /= A[i][i]
                ## A[i][i] = Fraction(1)    # unnecessary

            for r in range(j, length):      # eliminate entries below A[i][i]
                if A[r][i] != 0:
                    for c in range(j, length):
                        A[r][c] -= A[r][i] * A[i][c]
                    k[r] -= A[r][i] * k[i]
                    ## A[r][i] = Fraction(0)
            i = j
        k[row] /= A[row][row]               # the last row
        ## A[row][row] = Fraction(1)

        for i in range(row, 0, -1):         # eliminate entries above A[i][i]
            for r in range(0, i):
                if A[r][i] != 0:
                    k[r] -= k[i] * A[r][i]
                    ## A[r][i] = Fraction(0)
        # -------------------------- end of _rref(A) --------------------------

        A = []
        ### k = k / gcd(*k)
        #
        # make each element of k[:] an integer
        for i in range(length):
            d = k[i].denominator
            if d != 1:    # not an integer
                for j in range(length):
                    k[j] *= d
        # Taylor series of the linear combination
        # k[1]*f(x[i+points[1]]) + k[2]*f(x[i+points[2]]) + ...
        for i in range(length):
            if k[i] == 0:
                continue
            ##_lcombination_coefs += k[i] * coefs[i]
            for j in range(max_num_of_terms):
                self._lcombination_coefs[j] += k[i] * coefs[i][j]
        #
        m = self._lcombination_coefs[n]
        for i in range(n):
            if self._lcombination_coefs[i] != 0:
                m = self._lcombination_coefs[i]
                break
        #
        # "normalize" k[:] and m so that m is a positive integer
        if m < 0:
            for i in range(length):
                k[i] *= -1
            for i in range(max_num_of_terms):
                self._lcombination_coefs[i] *= -1
        #
        m = self._lcombination_coefs[n]
        x = round(m)
        if x == m:
            m = x    # so that m = 5 rather than Fraction(5, 1)
        #
        # save the results for other functions
        self._data = _FDData(n, points, k, m, coefs)
        self._computedq = True

        self._test_formula_validity()

        if printformulaq:
            self.formula()

        if self._formula_status >= 0:
            return (n, self._format_of_points(points),
                    list(map(lambda x: int(x), k)), m)
        else:
            return None
    # end of _compute

    def loadcomputingresults(self, results):
        """
        Input: 'results' is a tuple, (n, points, k[:], m). See compute(...).

        Load computing results from the output of compute(...). After this
        command, formula(), activatepythonfunction(), truncationerror(0, etc.,
        are available. It allows users to work on saved computing results (say,
        in a textfile). For example, when it takes hours to compute/find a
        formula, users may run commands like the following one from OS terminal

        python -c "from FiniteDifferenceFormula import fd;print(fd.compute(1,range(-200,201)))" > data.txt

        and then mannually load data from data.txt to this function later.
        """
        if type(results) != tuple or len(results) != 4:
            print("Invalid input. A tuple of the form (n, points, k, m) is expected.")
            return

        self._initialization()
        n, points, k, m, = results
        points = list(points)
        self._format_of_points(points)
        k = list(map(lambda x: Fraction(x, 1), k))

        length = len(points)
        max_num_of_terms = max(length, n) + self._NUM_OF_EXTRA_TAYLOR_TERMS

        # setup the coefficients of Taylor series expansions of f(x) at each of
        # the involved points
        self._lcombination_coefs = [Fraction(0,1)] * max_num_of_terms
        coefs = [Fraction(0,1)] * max_num_of_terms
        for i in range(length):
            coefs[i] = self._taylor_coefs(points[i], max_num_of_terms)

        # Taylor series of the linear combination
        # k[1]*f(x[i+points[1]]) + k[2]*f(x[i+points[2]]) + ...
        for i in range(length):
            if k[i] == 0:
                continue
            ##_lcombination_coefs += k[i] * coefs[i]
            for j in range(max_num_of_terms):
                self._lcombination_coefs[j] += k[i] * coefs[i][j]

        self._data = _FDData(n, points, k, m, coefs)
        self._computedq = True
        self._test_formula_validity(True)
    # end of loadcomputingresults

    # return a string of the linear combination
    # k[1]*f(x[i+points[1]]) + k[2]*f(x[i+points[2]]) + ...
    def _lcombination_expr(self, data:_FDData, decimalq = False,
                           python_REPL_funcq = False):
        firstq = True
        s = ""
        for i in range(len(data.points)):
            if data.k[i] == 0:
                continue
            times = ""
            if abs(data.k[i]) != 1:
                times = "* "
            if python_REPL_funcq and firstq:
                c2s = self._c2s(data.k[i], True, decimalq)
                if c2s == "":
                    c2s = "1"
                    times = "*"  #v0.6.0, Julia: -2x == -2*x; an error in Python
                elif c2s == "-":
                    c2s = "-1"
                    times = "*"  #same as above
                s += "float(" + c2s + ") "
            else:
                s += self._c2s(data.k[i], firstq, decimalq)
            s += times + self._f2s(data.points[i])
            firstq = False
        return s
    # end of _lcombination_expr

    # return string of 1st, 2nd, 3rd, 4th ...
    def _nth(self, n : int):
        if   n == 1:
            th = "st"
        elif n == 2:
            th = "nd"
        elif n == 3:
            th = "rd"
        else:
            th = "th"
        return "%d%s" % (n, th)
    # end of _nth

    # check if the newly computed formula is valid. results are saved in
    # _formula_status:
    #  100 - perfect, even satifiying some commonly seen "rules", such as the
    #        sum of coefficients = 0, symmetry of coefficients about x[i] in a
    #        central formula
    # -100 - no formula can't be found
    # -200 - same as -100, but do not try to find a formula if
    #        activatepythonfunction(n, point, k, m) fails
    #  250 - same as -100, but used for communication btw 'verifyformula' and
    #        'activatepythonfunction'
    # > 0  - mathematically, the formula is still valid but may not satisfy some
    #        commonly seen "rules" such as the sum of coefficients = 0 and
    #        symmetry of coefficients about x[i]
    #
    # return m as in equation (1) for 'activatepythonfunction'
    def _test_formula_validity(self, verifyingq = False):
        # to find f**(n)(x[i]) by obtaining
        #
        # k[1]*f(x[i+points[1]]) + k[2]*f(x[i+points[2]]) + ...
        #   = m*f**(n)(x[i]) + ..., m > 0
        #
        # the most important step is to know if f(x[i]), f'(x[i]), ..., f**(n-1)(x[i])
        # are all eliminated, i.e.,
        #    k[1]*coefs[1][j] + k[2]*coefs[2][j] + ... + k[len]*coefs[len][j] = 0
        # where j = 1:n
        n, k   = self._data.n, self._data.k
        points = self._data.points
        length = len(points)

        if length > 4 and self._range_inputq:  # v0.7.4, length > 4
            input_points = self._range_input
        else:
            input_points = points

        # Is there any equation in system (2) that is not satisfied?
        has_solutionq = True
        self._formula_status = 0
        for i in range(n):
            if self._lcombination_coefs[i] != 0:
                x = round(self._lcombination_coefs[i])
                if x != self._lcombination_coefs[i]:
                    x = float(self._lcombination_coefs[i])
                if i <= 3:
                    ds = "'" * i
                else:
                    ds = "**(%d)" % i
                fnxi = "f" + ds + "(x[i])"

                print("***** Error: ", n, ", ", input_points, sep = '', end = '')
                if verifyingq:
                    print(", ", k, sep = '', end = '')
                print(": k[1]*coefs[1][", i, "] + k[2]*coefs[2][", i,
                      "] + ... = ", x, " != 0, i.e., ", fnxi,
                      " can't be eliminated as indicated ",
                      "in the following computing result:", sep = '')
                print(self._dashline())
                print(self._lcombination_expr(self._data), "=\n    ", end = '')
                self._print_taylor(self._lcombination_coefs, 5)
                print(self._dashline())
                has_solutionq = False
                break

        m = self._lcombination_coefs[n]
        if m == 0:
            has_solutionq = False

        # there could be a solution that doesn't use all given points
        formula_for_inputq = True
        if has_solutionq:
            start, stop = 0, length - 1   # actual left and right endpoints
            while start < length and k[start] == 0:
                start += 1
            while stop >= 0 and k[stop] == 0:
                stop -= 1
            #if start >= stop  # can't be true b/c m != 0
            #    has_solutionq = False
            #    # what's the error?
            #else
            if start > 0 or stop < length - 1:
                if self._range_inputq:
                    s = self._range_input = range(points[start], points[stop] + 1)
                else:
                    s = points[start : stop + 1]
                print("***** Warning: ", n, ", ", s, " might be your input for ",
                      "which a formula is found.\n", sep = '')
                formula_for_inputq = False

        if not has_solutionq:
            if length <= n:
                print("***** Error: ", n, ", ", input_points, " : Invalid input. ",
                      "At least ", n + 1, " points are needed for the ",
                      self._nth(n), " derivative.", sep = '')
                self._formula_status = -200
                return m
            print("\n***** Error: ", n, ", ", input_points, sep = '', end = '')
            if verifyingq:
                print(", ", k, sep = '', end = '')
            print(": can't find a formula.\n")
            self._formula_status = -100
            return m

        if sum(k) != 0:   # sum of coefficients must be 0
            print("***** Warning: ", n, ", ", input_points, " : sum(k[:]) != 0",
                  sep = '')
            self._formula_status += 1

        # are coefficients of central formulas symmetrical about x[i]?
        if formula_for_inputq and self._range_inputq and \
           abs(self._range_input.start) == self._range_input.stop - 1:
            j = len(k) - 1
            for i in range(round(len(k)/2)):
                if abs(k[i]) != abs(k[j]):
                    print("***** Warning: ", n, ", ", input_points,
                          " : k[", i, "] != k[", j, "]", sep = '')
                    self._formula_status += 1
                    break
                j -= 1

        if self._formula_status == 0:
            self._formula_status = 100    # perfect

        # now, determine the big-O notation - what is x in O(h**x)?
        x = len(self._lcombination_coefs)
        for i in range(n + 1, x):            # skip f**(n)(x[i])
            if self._lcombination_coefs[i] != 0:
                x = i
                break
        x -= n
        self._bigO = "O(h"
        if x > 1:
            self._bigO += "**%d" % x
        self._bigO += ")"
        self._bigO_exp = x

        return m
    # end of _test_formula_validity

    def _denominator_expr(self, data : _FDData, python_REPL_funcq : bool = False):
        ms = ""
        if isinstance(data.m, Fraction):
            ms = "%d/%d" % ((data.m).numerator, (data.m).denominator)
        else:
            ms = str(data.m)
        s  = ""
        if data.m != 1:
            s = "(%s * " % ms
        if python_REPL_funcq:
            s += "float(h)"
        else:
            s += "h"
        if data.n != 1:
            s += "**%d" % data.n  # Python
        if data.m != 1:
            s += ")"
        return s
    # end of _denominator_expr

    # print and return Python lambda expression for the newly computed formula
    def _lambda_expr(self, data:_FDData, decimalq = False):
        fexpr  = "lambda f, x, i, h: "
        #fexpr += "float( "
        fexpr += "("    # convert the final result
        fexpr += self._lcombination_expr(data, decimalq, True)
        fexpr += " ) / " + self._denominator_expr(data, True)
        #fexpr += " )"
        return fexpr
    #end of _lambda_expr

    # print and return the function for the newly computed formula
    def _python_func_expr(self, data:_FDData, decimalq = False,
                          python_REPL_funcq = False):
        s = ""
        if self._range_inputq:
            if -self._range_input.start == self._range_input.stop - 1:
                s = "central"
            elif self._range_input.start == 0:
                s = "forward"
            elif self._range_input.stop == 1:
                s = "backward"

        n = self._num_of_used_points()    # how many points are actually involved?

        self._python_func_basename = "fd%sderiv%dpt%s" % (self._nth(data.n), n, s)
        fexpr  = "(f, x, i, h) = "
        if python_REPL_funcq:
            fexpr += "float( "    # convert the final result
        fexpr += "( "
        fexpr += self._lcombination_expr(data, decimalq, python_REPL_funcq)
        fexpr += " ) / " + self._denominator_expr(data, python_REPL_funcq)
        if python_REPL_funcq:
            fexpr += " )"

        return fexpr
    #end of _python_func_expr

    # print the formula with big-O notation for the newly computed formula
    def _print_bigo_formula(self, data :_FDData, bigO):
        if data.n <=3:
            ds = "'" * data.n
        else:
            ds = "**(%d)" % data.n
        print("f", ds, "(x[i]) = ( ", self._lcombination_expr(data, False),
              sep = '', end = '')
        print(" ) / ", self._denominator_expr(data), " + ", bigO, "\n",
              sep = '')
    # end of _print_bigo_formula

    def formula(self):
        """
        Generate and display readable formula and other computing results,
        including

        1. k[1]*f(x[i+points[1]]) + k[2]*f(x[i+points[2]]) + ...
               = m*f**(n)(x[i]) + ..., m > 0

        1. The formula for f**(n)(x[i]), including estimation of accuracy in the
           big-O notation.

        1. "Python" function(s) for f**(n)(x[i]).

        Calling compute(n, points, True) is the same as calling
        compute(n, points) and then formula().

        Even if no formula can be found, it still lists the computing results
        from which we can see why. For example, after compute(2,1:2), try
        formula().
        """
        if not self._computedq:
            print("Please call 'compute', 'find', 'findbackward', or"
                  "'findforward' first!")
            return

        if self._formula_status > 0:
            print("The following formula ", end = '')
            if self._formula_status == 100:
                print("passed all tests: sum of coefs being zero", end = '')
                if self._range_inputq and \
                   abs(self._range_input.start) == self._range_input.stop - 1:
                    print(", symmetry of coefs about x[i]", end = '')
                print(", etc.\n")
            else:
                print("may still be valid, though it didn't pass tests like sum ",
                      "of the coefficients being zero.\n")

        # print Taylor series expansion of the linear combination:
        # k[1]*f(x[i+points[1]]) + k[2]*f(x[i+points[2]]) + ...
        print("Computing result:\n")
        print(self._lcombination_expr(self._data), "=\n    ", end = '')
        self._print_taylor(self._lcombination_coefs, 5)

        if self._formula_status > 0:
            print("\nThe exact formula:\n")
            self._print_bigo_formula(self._data, self._bigO)
            if self._data.m != 1:                 # print in another format
                data1 = _FDData(self._data.n, self._data.points,
                                list(map(lambda x: Fraction(x, self._data.m),
                                         self._data.k)),
                                1, self._data.coefs)
                print("Or\n")
                self._print_bigo_formula(data1, self._bigO)

            print("\"Python\" function:\n")
            self._python_exact_func_expr = self._python_func_expr(self._data)
            suffix = ""
            if self._data.m != 1:
                suffix = "e"
            print(self._python_func_basename, suffix, self._python_exact_func_expr,
                  "\n", sep = '')
            if self._data.m != 1:                 # other formats
                self._python_exact_func_expr1  = self._python_func_expr(data1)
                print("Or\n\n", self._python_func_basename, "e1",
                      self._python_exact_func_expr1, "\n\nOr\n", sep = '')
                self._python_decimal_func_expr = self._python_func_expr(data1, True)
                print(self._python_func_basename, "d",
                      self._python_decimal_func_expr, "\n", sep = '')
        else:
            print("\nNo formula can be found.")
    # end of formula

    def truncationerror(self):
        """
        Show the truncation error of the last computed formula in the big_O
        notation.

        Output:
           (-1, "")      - There is no valid formula
           (n, "O(h**n)") - There is a valid formula

        Examples
        ========
        fd.compute(2,range(-3, 4))
        fd.truncationerror()
        fd.find(3,[-2, 1, 2, 5, 7, 15])
        fd.truncationerror()
        """
        if self._computedq:
            if self._formula_status <= -100:
                print("No valid formula is available.")
                return (-1, "")
            else:
                return (self._bigO_exp, self._bigO)
        print("Please call 'compute', 'find', 'findbackward', or",
              "'findforward' first!")
        return (-1, "")
    # end of truncationerror

    ###################### for teaching/learning/exploring #####################

    def decimalplaces(self, n = 16):
        """
        Set to n the decimal places for generating Python function(s) of computed
        formulas. Note: pass a negative integer to show the present decimal places.

        Examples
        ========
        fd.compute(2,range(-3, 4))
        fd.formula()  # by default, use 16 decimal places to generate a Python function
        fd.decimalplaces(4)
        fd.formula()  # now, use 4 decimal places to generate a Python function
        """
        if isinstance(n, int) and n > 0:
            self._decimal_places = n
            if self._computedq:
                print("Please call 'formula' to generate (or ",
                      "'activatepythonfunction' to generate and activate) a ",
                      "Python function for the newly computed formula, using ",
                      "the new decimal places.", sep = '')
            else:
                print("You may start your work by calling 'compute', 'find',",
                      "'findbackward', or 'findforward'.")
        else:
            print("decimalplaces(n): a positive integer is expected.")

        return self._decimal_places
    # end of decimalplaces

    def _format_of_points(self, points):
        length = len(points)
        if length == len(range(points[0], points[-1] + 1)):
            self._range_inputq = True
            self._range_input  = range(points[0], points[-1] + 1)
            if length < 5:
                return points   # v0.7.3
            else:
                return self._range_input
        return points
    # end of _format_of_points

    def verifyformula(self, n, points, k, m = 1):
        """
        Verify if a formula is valid. If it is valid, generate and activate its Python
        function(s). If not, try to find a formula for the derivative using the points.

             n: the n-th order derivative
        points: in the format of a range, start : stop, or a vector
             k: a list of the coefficients in a formula
             m: the coefficient in the denominator of a formula

        Examples
        ========
        fd.verifyformula(1,[-1,2],[-3,4],5)  # f'(x[i]) = (-3f(x[i-1])+4f(x[i+2]))/(5h)?
        fd.verifyformula(2, range(-3, 4), [2,-27,270,-490,270,-27,2], 18)
        fd.verifyformula(2, range(-3, 4), [1/90,-3/20,3/2,-49/18,3/2,-3/20,1/90])
        """
        if (not isinstance(n, int)) or n <= 0:
            print("Error: invalid first argument, ", n, ". A positive ",
                  "integer is expected.", sep = '')
            return None
        if len(points) == 1:
            print("Error: invalid input, points = ", points, ". A list of ",
                  "two or more points is expected.", sep = '')
            return None
        all_intq = True
        for i in points:
            if not isinstance(i, int):
                all_intq = False
                break
        if not all_intq:
            print("Error: invalid input, ", points, ". Integers are expected.",
                  sep = '')
            return None

        if isinstance(points, tuple):
            print("Invalid input, ", points,
                  ". A list like [1, 2, ...] is expected.", sep = '')
            return None
        if isinstance(k, tuple):
            print("Invalid input, ", k, ". A list like [1, 2, ...] is expected",
                  sep = '')
            return None

        length = len(points)
        if length != len(set(points)): # v0.7.3, removed sorted(..)
            print("Error: Invalid input -", points, "contains duplicate points.")
            return None
        points = list(points)

        # don't do so for teaching
        #if n <= len
        #    println("Error: at least $(n+1) points are needed for the $(_nth(n))",
        #            " derivative.")
        #    return None
        #end
        if length != len(k):
            print("Error: The number of points != the number of coefficients.");
            return None

        self._initialization()      # needed b/c it's like computing a new formula
        input_points = self._format_of_points(points)

        rewrittenq = False
        # "normalize" input so that m > 0, and m is integer
        if m < 0:
            for i in range(length):
                k[i] *= -1
            m *= -1
            rewrittenq = True
        if m == round(m):
            m = round(m)
        else:
            if not isinstance(m, Fraction):
                m = Fraction(m).limit_denominator()   # rationalize
            for i in range(length):
                k[i] *= m.denominator
            m = m.numerator
            rewrittenq = True
        if m == 0:
            if rewrittenq:
                print("You input: ", n, ", ", input_points, ", ", k, ", ", m, ".",
                      sep = '')
            print("Error: invalid input, the last argument m = 0. ",
                  "It can't be zero.")
            return None

        # "normalize" k[:] so that each element is integer
        all_intq = True
        for i in range(length):
            if not isinstance(k[i], int):
                all_intq = False
                if not isinstance(k[i], Fraction):
                    k[i] = Fraction(k[i]).limit_denominator()
        for i in range(length):
            if isinstance(k[i], Fraction):
                if k[i].denominator == 1:
                    continue
                m *= k[i].denominator
                rewrittenq = True
                d = k[i].denominator
                for j in range(length):
                    k[j] *= d
        if rewrittenq:
            for i in range(length):
                k[i] = round(k[i])

            # print k[:] nicely
            ks = "[%d" % k[0]
            for i in range(1, length):
                ks += ", %d" % k[i]
            ks += "]"
            print(self._dashline(), "\nYour input is converted to (",
                  n, ", ", input_points, ", ", ks, ", ", m, ").\n",
                  self._dashline(), sep = '')

        # setup the coefficients of Taylor series expansions of f(x) at each of
        # the involved points
        max_num_of_terms = max(length, n) + self._NUM_OF_EXTRA_TAYLOR_TERMS
        coefs = [None] * max_num_of_terms
        for i in range(length):
            coefs[i] = self._taylor_coefs(points[i], max_num_of_terms)

        # Taylor series of the linear combination
        # k[1]*f(x[i+points[1]]) + k[2]*f(x[i+points[2]]) + ...
        self._lcombination_coefs = [Fraction(0,1)] * max_num_of_terms
        for i in range(length):
            if k[i] == 0:
                continue
            for j in range(max_num_of_terms):
                self._lcombination_coefs[j] += k[i] * coefs[i][j]

        self._data = _FDData(n, points, k, m, coefs)
        M = self._test_formula_validity(True)
        find_oneq : bool = self._formula_status == -100

        # perhaps, the coefficients k[:] is correct, but m is not
        if self._formula_status == 100 and M != m:
            x = round(M)
            ms = str(M)
            if M == x:
                ms = str(x)            # don't print Fraction(5, 1)
            elif isinstance(M, Fraction):
                ms = "%d/%d" % (M.numerator, M.denominator)
            print("***** Error: The last argument m = ", m, " is incorrect. ",
                    "It should be ", ms, ".\n", sep = '')
            find_oneq = True

        if find_oneq:
            # v0.7.3
            print(">>>>> Your input doesn't define a valid formula, but it is",
                  "still activated for your examination.\n")

            self._formula_status = 250 # force to activate Python function
            # 250, reserved for communication w/ another 'activatepythonfunction'
        else: # v0.7.3
            print(">>>>> Your input defines a valid formula.\n")

        self._computedq = True         # assume a formula has been computed

        # force to activate even for invalid input formula
        b200 : bool = self._formula_status == -200
        if b200:
            self._formula_status = 100 # assume it is valid
        self.activatepythonfunction(True)
        if b200:
            self._formula_status = -200 # change it back

        if find_oneq:                   # use the input to generate a formula
            self._formula_status = -100
            print(self._dashline(), "\nFinding a formula using the points...\n")
            result = self._compute(n, points)
            if self._formula_status >= 0:
                print("Call fd.formula() to view the results and",
                      "fd.activatepythonfunction() to activate the new",
                      "Python function(s).")
                return result
        return None
    # end of verifyformula

    def _printexampleresult(self, suffix, i, exact):
        apprx = eval("self.fd" + suffix + "(math.sin, self._x, " + str(i) + ", self._h)")
        relerr = abs((apprx - exact) / exact) * 100
        spaces = ""
        if suffix != "e1":
            spaces  = " "
        print("  fd.fd", suffix, "(f, x, i, h)  ",
              spaces, "# result: ", "%.16f, " % apprx,
              "relative error = ", "%.8f%%" % relerr, sep = '')
    # end of _printexampleresult

    def activatepythonfunction(self, external_dataq = False):
        """
        Activate function(s) for the newly computed finite difference formula,
        and allow immediate evaluation of the function(s) in current Python REPL.
        """
        if not (external_dataq or self._computedq):
            print("Please call 'compute', 'find', 'findbackward', or ",
                  "'findforward' first!")
            return
        # Python's lambda function can't be too complicated. therefore, we have
        # to write Python functions to a Python script file, fd3rdderiv20ptcentral.py"

        # generate Python function in/for current REPL session
        count = 1
        if self._formula_status > 0:
            self.fde = eval(self._lambda_expr(self._data, False))
            if self._data.m != 1:  # functions in other formats
                data1 = _FDData(self._data.n, self._data.points,
                                list(map(lambda x: Fraction(x, self._data.m),
                                        self._data.k)),
                                1, self._data.coefs)
                self.fde1 = eval(self._lambda_expr(data1, False))
                self.fdd  = eval(self._lambda_expr(data1, True))
                count = 3
            # m = 1? no decimal formula
        else:
            print("No valid formula is for activation.")
            return

        self._python_func_expr(self._data)  # set _python_func_basename
        print("The following function(s) is available ",
              "temporarily in the FiniteDifferenceFormula module.\n\n",
              "Usage:\n=====", sep = '')

        # v0.7.6, data points are determined according to input points rather than
        # f, x, i, h = sin, 0:0.01:10, 500, 0.01
        center = max(list(map(lambda x: abs(x), self._data.points))) + 1
        if center < 251:
            center = 251
        stop = center * 2 + 1
        self._x = [ self._h * i for i in range(0, stop) ]

        print("from math import sin, cos, tan, pi, exp, log")
        print("f, i, h = sin, ", center, ", ", self._h, " # xi = %.2f" % self._x[center], sep = '')
        print("x = [ ", self._h, " * i for i in range(0, ", stop, ") ]", sep = '')
        print("fd.fde(f, x, i, h)   # ", self._python_func_basename, "e", sep = '')
        if count == 3:
            print("fd.fde1(f, x, i, h)  # ", self._python_func_basename, "e1", sep = '')
            print("fd.fdd(f, x, i, h)   # ", self._python_func_basename, "d", sep = '')

        # sine is taken as the example b/c sin**(n)(x) = sin(n π/2 + x), simply
        exact = math.sin(self._data.n * math.pi / 2 + self._x[center])

        print("\nFor the", self._python_func_basename,
              "formula the computing results are as follows.")
        self._printexampleresult("e", center, exact)
        if count == 3:
            self._printexampleresult("e1", center, exact)
            self._printexampleresult("d", center, exact)
        length = len("fd.fde")
        #if count == 3:
        #    length += 1
        print(" " * (length + 17), "# cp:     ", "%.16f\n" % exact,
              sep = '', end = '')

        # 250, a sepcial value for communication w/ 'verifyformula'
        if not (external_dataq and self._formula_status == 250):
            print("\nCall fd.formula() to view the very definition.")
    # end of activatepythonfunction

    def tcoefs(self, j, n = 10):
        """
        Same as taylorcoefs(j, n).
        """
        return self.taylorcoefs(j, n) # v0.6.9 add 'return'

    def taylorcoefs(self, j, n = 10):
        """
        Same as tcoefs(j, n). Compute and return coefficients of the first n
        terms of the Taylor series of f(x[i + j]) = f(x[i] + jh) about x[i],
        where h is the increment in x.

        Examples
        ========
        fd.tcoefs(-2)
        fd.tcoefs(5, 4)
        """
        if n < 1:
            print("n = %d? It is expected to be an positive integer." % n)
            return None

        if isinstance(j, int):
            return self._taylor_coefs(j, n)
        else:
            print("Invalid input, ", j, ". An integer is expected.")
            return None
    # end of taylorcoefs

    # print readable Taylor series expansion of f(x[i + j]) about x[i]
    # for teaching/learning!
    def _printtaylor1(self, j, n = 10):
        coefs = self.taylorcoefs(j, n)
        js = ""
        if j > 0:
            js = "+%d" % j
        elif j < 0:
            js = "%d" % j
        print("f(x[i", js, "]) = ", sep = '', end = '')
        self._print_taylor(coefs, n)
    # end of _printtaylor1

    # print readable Taylor series of a function/expression about x[i]. e.g.,
    # fd.taylor(2*fd.tcoefs(0) - 5*fd.tcoefs(1) + 4*fd.tcoefs(2))
    # sad. base Python doesn't provide this convenience. use numpy.
    def _printtaylor2(self, coefs, n = 10):
        self._print_taylor(coefs, n)

    # awkard implementation: Julia's multiple dispatchment is super...
    #
    # input: points_k can be an integer, a list of coefficients of a Taylor
    # series, or a tuple (points, k[:]), where points and k are as in the
    # linear combination:
    #     k[1]*f(x[i+points[1]]) + k[2]*f(x[i+points[2]]) + ...
    def taylor(self, points_k = (), n = 10):
        """
        taylor()       # added in v0.6.4
          - Print the first few nonzero terms of the Taylor series of the linear
            combination k[0]f(x[i+points[0]]) + k[1]f(x[i+points[1]]) + ... for
            the newly computed formula (even if failed).

        taylor(j, n = 10)
          - Print the 1st n terms of Taylor series of f(x[i+j]) about x[i].

        taylor(coefs, n = 10)
          - Print the 1st n terms of Taylor series with coefficients in 'coefs'

        taylor((points, k), n = 10)
          - Prints the 1st n nonzero terms of the Taylor series of the linear
            combination:  k[0]f(x[i+points[0]]) + k[1]f(x[i+points[1]]) + ...

        The last two provide also another way to verify if a formula is
        mathematically valid or not.

        See also [verifyformula], [activatepythonfunction], and [taylorcoefs].

        Examples
        ========
        fd.compute(1, [0, 1, 5, 8])
        fd.taylor()

        fd.taylor(2)

        coefs = [2,-27,270,-490,270,-27,2]
        fd.taylor(coefs, 6)

        fd.taylor((range(0,4), [-1, 3, -3, 1]), 6)

        import numpy as np
        n = 50
        # -2f(x[i+1) + 3f(x[i+2]) -4f(x[i+5])
        coefs  = -2 * np.array(fd.tcoefs(1, n)) + 3 * np.array(fd.tcoefs(2, n))
        coefs += -4 * np.array(fd.tcoefs(5, n))
        fd.taylor(list(coefs), n)

        Note
        ====
        Julia's multiple dispatchment is super. We wish Python to 1) adopt it;
        2) provide basic vectorization functionality with lists and tuples in its
        very base, rather than through packages like numpy.
        """
        if n < 1:
            print("n = %d? It is expected to be an positive integer." % n)
            return

        if isinstance(points_k, tuple):
            if len(points_k) == 0:
                # print the Taylor series of the linear combination of
                # k[0]f(x[i+j0]) + k[1]f(x[i+j1]) + ... for the newly computed formula
                if self._computedq:
                    print(self._lcombination_expr(self._data), "=\n    ", end = '')
                    self._print_taylor(self._lcombination_coefs, 5)
                else:
                    print("Please call 'compute', 'find', 'findbackward', or",
                          "'findforward' first!")
                return
            elif len(points_k) == 2:
                points, k = points_k
            else:
                print("Invalid input, ", points_k, ". Two lists are expected ",
                      " in the tuple.", sep = '')
                return
        elif isinstance(points_k, list):
            self._printtaylor2(points_k, n)
            return
        else:
            self._printtaylor1(points_k, n)
            return

        oldpoints = list(points)
        points = sorted(set(points))
        length = len(points)
        if oldpoints != points:
            print(self._dashline())
            print("Your input: points = ", points, ".", sep = '')
            print(self._dashline())
        if length != len(k):
            print("Error: invalid input. The sizes of points and k are",
                  "not the same.")
            return

        max_num_of_terms = max(n, length, 30) + self._NUM_OF_EXTRA_TAYLOR_TERMS
        coefs = [0] * max_num_of_terms
        for i in range(length):
            for j in range(max_num_of_terms):
                coefs[j] += k[i] * self._taylor_coefs(points[i], max_num_of_terms)[j]
        self._print_taylor(coefs, n)
    # end of taylor

    # return the number of points actually used in a formula
    def _num_of_used_points(self):
        n = 0    # how many points are actually involved?
        for i in range(len(self._data.points)):
            if self._data.k[i] == 0:
                continue
            n += 1
        return n
    # end of _num_of_used_points

    def formulas(self, orders = range(1, 4), min_num_of_points : int = 2,
                 max_num_of_points : int = 5):
        """
        By default, the function prints all forward, backward, and central finite
        difference formulas for the 1st, 2nd, and 3rd derivatives, using 2 to 5 points.

        Examples
        ========
        # The following examples show all forward, backward, and central finite
        # difference formulas for the specified derivatives, using at least 4 and
        # at most 11 points.
        from FiniteDifferenceFormula import fd
        fd.formulas(range(2, 6), 4, 11)    # the 2nd, 3rd, .., 5th derivatives
        fd.formulas([2, 4], 4, 11)         # the 2nd and 4th derivatives
        fd.formulas(3, 4, 11)              # the 3rd derivative
        """
        if min_num_of_points < 2:
            print("Error: Invalid input, min_num_of_points = ",
                  min_num_of_points, ". It must be at least 2.", sep = '')
            return
        elif max_num_of_points < min_num_of_points:
            print("Error: Invalid input, max_num_of_points = ",
                  max_num_of_points, ". It must be at least ",
                  min_num_of_points, ".", sep = '')
            return

        if isinstance(orders, int) and orders >= 1:
            orders = [ orders ]
        elif isinstance(orders, range) and orders.start >= 1:
            orders = list(orders)
        elif isinstance(orders, list):
            for i in orders:
                if not (isinstance(i, int) and i >= 1):
                    print("Error: Invalid input, orders = ", orders, ". ",
                          "A list of positive integers are expected.", sep = '')
                    return
        else:
            print("Error: Invalid input, orders = ", orders, ". ",
                  "An positive integer or a list of positive integers ",
                  "are expected.", sep = '')
            return

        oldorders = list(orders)
        orders = sorted(set(orders))
        if oldorders != orders:
            print(self._dashline())
            print("Your input: formulas(", orders, ", ", min_num_of_points,
                  ", ", max_num_of_points, ")", sep = '')
            print(self._dashline())
        oldorders = []

        for n in orders:
            # forward schemes
            start = max(n + 1, min_num_of_points)
            for num_of_points in range(start, max_num_of_points + 1):
                self.compute(n, range(0, num_of_points))
                if self._formula_status > 0:
                    print(self._num_of_used_points(),
                          "-point forward finite difference formula:", sep = '')
                    self._print_bigo_formula(self._data, self._bigO)

            # backward schemes
            for num_of_points in range(start, max_num_of_points + 1):
                self.compute(n, range(1 - num_of_points, 1))
                if self._formula_status > 0:
                    print(self._num_of_used_points(),
                          "-point backward finite difference formula:", sep = '')
                    self._print_bigo_formula(self._data, self._bigO)

            # central schemes
            start = math.floor(max(n, min_num_of_points) / 2)
            stop  = math.ceil(max_num_of_points / 2) + 1
            for num_of_points in range(start, stop):
                length = 2 * num_of_points + 1
                if n >= length:
                    continue
                self.compute(n, range(-num_of_points, num_of_points + 1))
                if self._formula_status > 0:
                    x = self._num_of_used_points()
                    if x <= max_num_of_points:
                        print(x, "-point central finite difference formula:", sep = '')
                        self._print_bigo_formula(self._data, self._bigO)
                    #else:
                    #   self._initialization() # v0.6.9
    # end of formulas

# end of class FDFormula:

#if __name__ == '__main__':
fd = FDFormula()
