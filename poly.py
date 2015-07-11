class Poly:
        # Initializer
        def __init__(self, terms = {}, var = "x"):
                # Dictionary with degrees paired with their coefficients
                self.terms = {}
                # If it's already a dictionary
                if isinstance(terms, dict):
                        self.terms = terms
                # If it's a Poly already
                elif isinstance(terms, Poly):
                        self = terms
                # If it's a number
                elif isinstance(terms, int):
                        self.terms[0] = terms
                else:
                        self.terms[0] = 0
                # Variable name
                self.var = var
        
        # __str__
        # String representation of the polynomial
        def __str__(self):
                r = ""
                n = max(self.terms)
                end = min(self.terms) - 1
                while n > end:
                        if n in self.terms:
                                # Append the coefficient Cx^n
                                c = self.terms[n]
                                # Decide whether or not to truncate a decimal
                                if isinstance(c, float) and c == int(c):
                                        trunc = True
                                else:
                                        trunc = False
                                # + n is max (need to display sign out front)
                                if n == max(self.terms):
                                        if c < 0:
                                                r += "-"
                                # + C is 0: do not display the term at all, unless n == 0
                                # + C is 1: display only the term, not the 1, unless n == 0
                                if n == 0:
                                        if c == 0 or c > 0:
                                                if trunc:
                                                        r += str(int(c))
                                                else:
                                                        r += str(c)
                                        elif c < 0:
                                                if trunc:
                                                        r += str(abs(int(c)))
                                                else:
                                                        r += str(abs(c))
                                else:
                                        if abs(c) != 1 and c != 0:
                                                # + C < 0 (and n !max): need to take abs(C)
                                                if c < 0 and n < max(self.terms):
                                                        if trunc:
                                                                r += str(absint((c)))
                                                        else:
                                                                r += str(abs(c))
                                                else:
                                                        if trunc:
                                                                r += str(int(c))
                                                        else:
                                                                r += str(c)
                                # Append the variable and the power
                                if self.terms[n] != 0:
                                        if n != 0 and n != 1:
                                                r += self.var + "^" + str(n)
                                        elif n == 1:
                                                r += self.var
                                # Append the next sign
                                if n - 1 in self.terms and c != 0:
                                        if self.terms[n - 1] < 0:
                                                r += " - "
                                        elif self.terms[n - 1] > 0:
                                                r += " + "
                        n -= 1
                return r
        
        # __repr__
        def __repr__(self):
                return self.__str__()
        
        # __add__
        # Adds 2 polynomials together
        def __add__(self, other):
                tmp = {}
                for n in self.terms:
                        tmp[n] = self.terms[n]
                if type(other) == type(Poly()):
                        for n in other.terms:
                                if n in tmp:
                                        tmp[n] += other.terms[n]
                                else:
                                        tmp[n] = other.terms[n]
                else:
                        if 0 in tmp:
                                tmp[0] += other
                        else:
                                tmp[0] = other
                return Poly(tmp, self.var)
        
        # __sub__
        # Subtracts `other` from `self`
        def __sub__(self, other):
                tmp = {}
                for n in self.terms:
                        tmp[n] = self.terms[n]
                if type(other) == type(Poly()):
                        for n in other.terms:
                                if n in tmp:
                                        tmp[n] -= other.terms[n]
                                else:
                                        tmp[n] = -other.terms[n]
                else:
                        if 0 in tmp:
                                tmp[0] -= other
                        else:
                                tmp[0] = -other
                return Poly(tmp, self.var)
        
        # __mul__
        # Multiplies two polynomials together
        def __mul__(self, other):
                # We have 2 different tmps to prevent the dictionary from overwriting values
                tmp1 = {}
                tmp2 = {}
                for n in self.terms:
                        # TODO isinstance()
                        if type(other) == type(Poly()):
                                for m in other.terms:
                                        if n + m not in tmp1:
                                                tmp1[n + m] = self.terms[n] * other.terms[m]
                                                if tmp1[n + m] == 0:
                                                        if 0 not in tmp1:
                                                                tmp1[0] = 0
                                                        del(tmp1[n + m])
                                        else:
                                                tmp2[n + m] = self.terms[n] * other.terms[m]
                                                if tmp2[n + m] == 0:
                                                        if 0 not in tmp2:
                                                                tmp2[0] = 0
                                                        del(tmp2[n + m])
                        else:
                                tmp1[n] = self.terms[n] * other 
                return Poly(tmp1, self.var) + Poly(tmp2)
        
        # __truediv__
        # Temporary fix for ref
        # TODO actually implement this
        def __truediv__(self, other):
                if isinstance(other, Poly):
                        if max(self.terms) == 0 and max(other.terms) == 0:
                                return Poly({0:self.terms[0] / other.terms[0]})
                elif isinstance(other, int) or isinstance(other, float):
                        return Poly({0:self.terms[0] / other})
        
        # __mod__
        # Finds the remainder (by synthetic division) of a polynomial with a root
        def __mod__(self, root):
                coeffs = []
                n = max(self.terms)
                end = min(self.terms) - 1
                while n > end:
                        if n in self.terms:
                                coeffs.append(self.terms[n])
                        else:
                                coeffs.append(0)
                        n -= 1
                remainders = [coeffs[0]]
                middle = [0]
                i = 1
                while i < len(coeffs):
                        middle.append(root * remainders[i - 1])
                        remainders.append(middle[i] + coeffs[i])
                        i += 1
                return(remainders[-1])
        
        # __neg__
        # Unary negation
        def __neg__(self):
                tmp_terms = dict(self.terms)
                for n in tmp_terms:
                        tmp_terms[n] = -tmp_terms[n]
                return Poly(tmp_terms)
        
        # __eq__
        # Equal to
        def __eq__(self, other):
                flag = True
                i = 0
                if isinstance(other, Poly):
                        while i < max(self.terms) and not flag:
                                if i in self.terms:
                                        if i not in other.terms:
                                                flag = False
                                        else:
                                                if self.terms[i] != other.terms[i]:
                                                        flag = False
                                i += 1
                elif isinstance(other, int) or isinstance(other, float):
                        if max(self.terms) != 0 or self.terms[0] != other:
                                flag = False
                return flag
        
        # __ne__
        # Not equal to
        def __ne__(self, other):
                return not self == other
        
        # evauluate
        # Evaluates a polynomial at a given value
        def evaluate(self, value):
                total = 0
                for n in self.terms:
                        total += self.terms[n] * (value ** n)
                return total
        
        # roots
        # Finds the roots (zeroes) of a polynomial
        def roots(self):
                if max(self.terms) <= 2:
                        return self.quad()
                possible = self.root_guess()
                actual = []
                for root in possible:
                        if self % root == 0:
                                actual.append(root)
                return tuple(actual)
        
        # quad
        # Performs the quadratic formula on the polynomial
        def quad(self):
                a = self.terms[2]
                b = self.terms[1]
                c = self.terms[0]
                x1 = (-b + (b ** 2 - 4 * (a * c)) ** .5) / (2 * a)
                x2 = (-b - (b ** 2 - 4 * (a * c)) ** .5) / (2 * a)
                if x1 == int(x1):
                        x1 = int(x1)
                if x2 == int(x2):
                        x2 = int(x2)
                return (x1, x2)
        
        # root_guess
        # Guesses probable roots for the polynomial
        def root_guess(self):
                lc = self.terms[max(self.terms)]
                tc = self.terms[min(self.terms)]
                lead_factors = Poly.factors(lc)
                tail_factors = Poly.factors(tc)
                all_factors = []
                for lead in lead_factors:
                        for tail in tail_factors:
                                if tail / lead not in all_factors:
                                        all_factors.append(tail / lead)
                # Convert back to ints if possible
                for i in range(len(all_factors)):
                        if all_factors[i] == int(all_factors[i]):
                                all_factors[i] = int(all_factors[i])
                return all_factors
        
        # factors
        # Static method to factor an integer (including negatives
        def factors(num = 1):
                num = abs(num)
                i = 1
                factors = []
                while i <= num:
                        if num % i == 0:
                                factors.append(i)
                                factors.append(-i)
                        i += 1
                return factors
