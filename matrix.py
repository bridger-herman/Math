from poly import Poly
class Matrix:
        # Initializer
        def __init__(self, lst2D = [[Poly(0)]]):
                length = len(lst2D[0])
                for lst in lst2D:
                        if len(lst) != length:
                                raise AttributeError("Cannot have ragged matrix")
                # Convert everything to a polynomial
                for r in range(len(lst2D)):
                        for c in range(len(lst2D[0])):
                                if type(lst2D[r][c]) != type(Poly()):
                                        lst2D[r][c] = Poly(lst2D[r][c])
                self.contents = lst2D
        
        # __str__
        def __str__(self):
                r = "[ "
                def space(num):
                        r = ""
                        for n in range(num):
                                r += " "
                        return r
                max_width = len(str(self.contents[0][0]))
                for row in range(len(self.contents)):
                        for col in range(len(self.contents[0])):
                                if len(str(self.contents[row][col])) > max_width:
                                        max_width = len(str(self.contents[row][col]))
                for row in range(len(self.contents)):
                        for col in range(len(self.contents[0])):
                                cur_width = len(str(self.contents[row][col]))
                                r += space((max_width - cur_width) // 2) + str(self.contents[row][col]) + space((max_width - cur_width) // 2 + 1)
                        r += "]\n[ "
                return r[:-3]
        
        # __repr__
        def __repr__(self):
                return self.__str__()
        
        # det
        # Takes the determinant of a matrix
        def det(self):
                # Check if the matrix is square
                if self.dim()[0] != self.dim()[1]:
                        raise AttributeError("Cannot take the determinant of a non-square matrix")
                # Take the determinant, recursively
                if self.dim() == (1, 1):
                        return self.contents[0][0]
                elif self.dim() == (2, 2):
                        total = Poly()
                        total += self.contents[0][0] * self.contents[1][1] - self.contents[1][0] * self.contents[0][1]
                        return total
                else:
                        minors = []
                        for r in range(len(self.contents)):
                                tmp_contents = []
                                for r2 in range(len(self.contents)):
                                        if r2 != r:
                                                tmp_contents.append(self.contents[r2][1:])
                                minors.append(Matrix(tmp_contents))
                        total = Poly()
                        for r in range(len(self.contents)):
                                total += minors[r].det() * self.contents[r][0] * (-1) ** r
                return total
        
        # inverse
        # Takes the inverse of a matrix
        def inverse(self):
                if self.dim()[0] != self.dim()[1]:
                        raise AttributeError("Cannot take the inverse of a non-square matrix")
                # Augment the identity matrix to the beginning
                self.augment(Matrix.identity(len(self.contents)))
                self.rref()
                # Take the identity matrix off of the beginning
                for row in range(len(self.contents)):
                        self.contents[row] = self.contents[row][len(self.contents):]
                # Take RREF of this... LOL
                # Saving this comment because I thought I couldn't do it... ^^^
                return self
        
        # eigenvalues
        # Finds the eigenvalues of a matrix
        def eigenvalues(self):
                # Make the polynomial matrix
                #       [x - a   b  ]
                #       [  c   x - d]
                # from this matrix:
                #       [ a  b ]
                #       [ c  d ]
                x = Matrix.identity(self.dim()[0]) * Poly({1:1})
                mat = self - x
                d = mat.det()
                return d.roots()
        
        # eigenvectors
        # Finds the eigenvectors of a matrix
        def eigenvectors(self, equal_matrix = None):
                # Make the polynomial matrix
                #       [x - a   b  ]
                #       [  c   x - d]
                # from this matrix:
                #       [ a  b ]
                #       [ c  d ]
                x = Matrix.identity(self.dim()[0]) * Poly({1:1})
                mat = self - x
                # Find the eigenvalues of the matrix
                values = mat.det().roots()
                evaluated = []
                for value in values:
                        tmp_contents = []
                        for row in range(len(self.contents)):
                                tmp_row = []
                                for col in range(len(self.contents[0])):
                                        tmp_row.append(mat.contents[row][col].evaluate(value))
                                tmp_contents.append(tmp_row)
                        evaluated.append(Matrix(tmp_contents))
                vector_mats = []
                for m in evaluated:
                        if not equal_matrix:
                                o = Poly(0)
                                m.augment(Matrix([[o],[o]]))
                        else:
                                m.augment(equal_matrix)
                        m.rref()
                        vector_mats.append(m)
                # TODO improve upon this after equations
                return vector_mats
        
        # rref
        # Takes the Reduced Row Echelon form of a matrix
        def rref(self):
                if not self.is_ref():
                        self.ref()
                while not self.is_rref():
                        row = 0
                        col = 0
                        done = False
                        while not done and not self.is_rref():
                                tmp_row = 0
                                while tmp_row < row:
                                        # Subtracts multiple of the pivot column from tmp_row
                                        if self.contents[tmp_row][col] != 0:
                                                self.row_sub(tmp_row, row, self.contents[tmp_row][col])
                                        tmp_row += 1
                                if col >= len(self.contents[0]) - 1 and row >= len(self.contents) - 1:
                                        done = True
                                if row < len(self.contents) - 1:
                                        row += 1
                                if col < len(self.contents[0]) - 1:
                                        col += 1
                return self
        
        # is_rref
        # Determines if a matrix is in Reduced Row Echelon Form
        def is_rref(self):
                if not self.is_ref():
                        return False
                else:
                        rref = True
                        row = 0
                        pivots = []
                        while row < len(self.contents) and rref:
                                col = 0
                                col_flag = False
                                while col < len(self.contents[0]) and not col_flag and rref:
                                        if self.contents[row][col] == 1 and (len(pivots) == 0 or col > pivots[-1]):
                                                col_flag = True
                                                pivots.append(col)
                                        elif self.contents[row][col] == 1 and (len(pivots) == 0 or col > pivots[-1]):
                                                rref = False
                                        col += 1
                                row += 1
                        for pivot in pivots:
                                row = 0
                                while row < len(self.contents):
                                        if row != pivot and self.contents[row][pivot] != 0:
                                                rref = False
                                        row += 1
                        return rref
                        
        # ref
        # Takes the Row Echelon form of a matrix
        def ref(self):
                while not self.is_ref():
                        if self.contents[0][0] != 0:
                                row = 0
                                col = 0
                                done = False
                                while not done and not self.is_ref():
                                        # Divide everything in current row by item at (0, 0)
                                        if self.contents[row][col] != 0:
                                                self.row_div(row, self.contents[row][col])
                                        # Check to see if everything in the current column is zero
                                        tmp_row = row + 1
                                        while tmp_row < len(self.contents):
                                                if self.contents[tmp_row][col] != 0:
                                                        self.row_sub(tmp_row, row, self.contents[tmp_row][col])
                                                tmp_row += 1
                                        if col >= len(self.contents[0]) - 1 and row >= len(self.contents) - 1:
                                                done = True
                                        if row < len(self.contents) - 1:
                                                row += 1
                                        if col < len(self.contents[0]) - 1:
                                                col += 1
                        else:
                                col = 0
                                while col < len(self.contents[0]):
                                        row = 0
                                        while row < len(self.contents):
                                                tmp_row = 0
                                                while tmp_row < len(self.contents):
                                                        # Swap row and tmp_row if row has a nonzero element
                                                        if self.contents[row][col] != 0:
                                                                self.row_swap(row, tmp_row)
                                                        tmp_row += 1
                                                row += 1
                                        col +=1
                return self
                
        # is_ref
        # Checks if a matrix is in Row Echelon Form
        def is_ref(self):
                ref = True
                row = 0
                pivots = []
                while row < len(self.contents) and ref:
                        col = 0
                        col_flag = False
                        while col < len(self.contents[0]) and not col_flag and ref:
                                num = self.contents[row][col]
                                if num != 0 and num != 1:
                                        ref = False
                                elif num == 1:
                                        if len(pivots) != 0:
                                                if col > pivots[-1]:
                                                        pivots.append(col)
                                                        col_flag = True
                                                else:
                                                        ref = False
                                        else:
                                                pivots.append(col)
                                                col_flag = True
                                col += 1
                        row += 1
                return ref
        
        # augment
        # Augments current matrix with another matrix, if the number of rows is equivalent
        def augment(self, other):
                if self.dim()[0] != other.dim()[0]:
                        raise AttributeError("Cannot augment matrices with a different number of rows")
                for i in range(len(self.contents)):
                        self.contents[i] += other.contents[i]
                return self
        
        # dim
        # Gets the dimensions of the matrix (rows, cols)
        def dim(self):
                return (len(self.contents), len(self.contents[0]))
        
        # identity
        # Returns the identity matrix, of dimension n
        def identity(n = 3):
                contents = []
                tmp_row = []
                for r in range(n):
                        tmp_row = []
                        for c in range(n):
                                if r == c:
                                        tmp_row.append(Poly(1))
                                else:
                                        tmp_row.append(Poly(0))
                        contents.append(tmp_row)
                return Matrix(contents)
        
        # __mul__
        # Muitlplies a constant by the contents of a matrix
        def __mul__(self, const):
                new_contents = []
                for row in self.contents:
                        tmp_col = []
                        for col in row:
                                tmp_col.append(col * const)
                        new_contents.append(tmp_col)
                return Matrix(new_contents)
        
        # __sub__
        # Subtracts a matrix `other` from `self`
        def __sub__(self, other):
                if self.dim() != other.dim():
                        raise AttributeError("Cannot subtract matrices of different sizes")
                new_contents = []
                for row in range(len(self.contents)):
                        tmp_col = []
                        for col in range(len(self.contents[0])):
                                tmp_col.append(self.contents[row][col] - other.contents[row][col])
                        new_contents.append(tmp_col)
                return Matrix(new_contents)
        
        # int_convert
        # Converts things in the matrix back to integers, if possible
        def int_convert(self):
                for row in range(len(self.contents)):
                        for col in range(len(self.contents[0])):
                                if type(self.contents[row][col]) == type(float()) and self.contents[row][col] == int(self.contents[row][col]):
                                        self.contents[row][col] = int(self.contents[row][col])
                return self
        
        # poly_convert
        # Converts everything in the matrix to a polynomial
        def poly_convert(self):
                tmp_contents = []
                for row in range(len(self.contents)):
                        tmp_row = []
                        for col in range(len(self.contents[0])):
                                if type(self.contents[row][col]) != type(Poly()):
                                        tmp_row.append(Poly(self.contents[row][col]))
                                else:
                                        tmp_row.append(self.contents[row][col])
                        tmp_contents.append(tmp_row)
                return Matrix(tmp_contents)
        
        # has_poly
        # Checks if there is a polynomial in the matrix
        def has_poly(self):
                for row in range(len(self.contents)):
                        for col in range(len(self.contents[0])):
                                if type(self.contents[row][col]) == type(Poly()):
                                        return True
                return False
        
        ## Elementary Row Operations ##
        # row_swap
        # Swaps 2 rows in a matrix
        def row_swap(self, row1, row2):
                tmp_row = list(self.contents[row1])
                self.contents[row1] = list(self.contents[row2])
                self.contents[row2] = tmp_row
                return self
        
        # row_mul
        # Multiplies a row in a matrix by a constant
        def row_mul(self, row, const):
                if const == 0:
                        raise ValueError("Constant cannot be zero")
                for i in range(len(self.contents[0])):
                        self.contents[row][i] *= const
                return self
        
        # row_div
        # Divides a row in a matrix by a constant
        def row_div(self, row, const):
                if const == 0:
                        raise ZeroDivisionError
                for i in range(len(self.contents[0])):
                        self.contents[row][i] /= const
                return self
        
        # row_add
        # Adds two rows in a matrix together (row1 = row1 + const * row2)
        def row_add(self, row1, row2, const):
                if not const:
                        const = 1
                elif const == 0:
                        raise ValueError("Constant cannot be zero")
                tmp_row = list(self.contents[row2])
                for i in range(len(self.contents[0])):
                        tmp_row[i] *= const
                for i in range(len(self.contents[0])):
                        self.contents[row1][i] += tmp_row[i]
                return self
                
        # row_sub
        # Subtracts two rows in a matrix (row1 = row1 - const * row2
        def row_sub(self, row1, row2, const):
                if not const:
                        const = 1
                elif const == 0:
                        raise ValueError("Constant cannot be zero")
                tmp_row = list(self.contents[row2])
                for i in range(len(self.contents[0])):
                        tmp_row[i] *= const
                for i in range(len(self.contents[0])):
                        self.contents[row1][i] -= tmp_row[i]
                return self
