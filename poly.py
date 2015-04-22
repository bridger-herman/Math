class Poly:
        # Initializer
        def __init__(self, terms = {}, var = "x"):
                # Dictionary with degrees paired with their coefficients
                self.terms = terms
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
                                if self.terms[n] != 0:
                                        if self.terms[n] != 1 and n < max(self.terms):
                                                r += str(abs(self.terms[n]))
                                        elif self.terms[n] != 1 and n == max(self.terms):
                                                r += str(self.terms[n])
                                        if n != 0 and n != 1:
                                                r += self.var + "^" + str(n)
                                        elif n == 1:
                                                r += self.var
                                if n - 1 in self.terms:
                                        if self.terms[n - 1] < 0:
                                                r += " - "
                                        else:
                                                r += " + "
                        n -= 1
                return r
        
        # __add__
        # Adds 2 polynomials together
        def __add__(self, other):
                tmp = {}
                for n in self.terms:
                        tmp[n] = self.terms[n]
                for n in other.terms:
                        if n in tmp:
                                tmp[n] += other.terms[n]
                        else:
                                tmp[n] = other.terms[n]
                return Poly(tmp, self.var)
        
        # __sub__
        # Subtracts `other` from `self`
        def __sub__(self, other):
                tmp = {}
                for n in self.terms:
                        tmp[n] = self.terms[n]
                for n in other.terms:
                        if n in tmp:
                                tmp[n] -= other.terms[n]
                        else:
                                tmp[n] = -other.terms[n]
                return Poly(tmp, self.var)
        
        # __mul__
        # Multiplies two polynomials together
        def __mul__(self, other):
                # We have 2 different tmps to prevent the dictionary from overwriting values
                tmp1 = {}
                tmp2 = {}
                for n in self.terms:
                        for m in other.terms:
                                if n + m not in tmp1:
                                        tmp1[n + m] = self.terms[n] * other.terms[m]
                                else:
                                        tmp2[n + m] = self.terms[n] * other.terms[m]
                return Poly(tmp1, self.var) + Poly(tmp2)
        
        # quad
        # Performs the quadratic formula on the polynomial
        def quad(self):
                a = self.terms[2]
                b = self.terms[1]
                c = self.terms[0]
                x1 = (-b + (b ** 2 - 4 * (a * c)) ** .5) / (2 * a)
                x2 = (-b - (b ** 2 - 4 * (a * c)) ** .5) / (2 * a)
                return (x1, x2)
