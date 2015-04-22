class Matrix:
        # Initializer
        def __init__(self, lst2D = [[0]]):
                length = len(lst2D[0])
                for lst in lst2D:
                        if len(lst) != length:
                                raise AttributeError("Cannot have ragged matrix")
                self.contents = lst2D
        
        # __str__
        def __str__(self):
                r = "[ "
                for s in self.contents:
                        for t in s:
                                r += str(t) + " "
                        r += "]\n[ "
                return r[:-3]
        
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
                        total = 0
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
                        total = 0
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
                                sub_row = 0
                                while sub_row < row:
                                        # Subtracts multiple of the pivot column from sub_row
                                        if self.contents[sub_row][col] != 0:
                                                self.row_add(sub_row, row, -self.contents[sub_row][col])
                                        sub_row += 1
                                if col >= len(self.contents[0]) - 1 and row >= len(self.contents) - 1:
                                        done = True
                                if row < len(self.contents) - 1:
                                        row += 1
                                if col < len(self.contents[0]) - 1:
                                        col += 1
                self.int_convert()
        
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
                                        if self.contents[row][col] != 0 and self.contents[row][col] != 0:
                                                self.row_mul(row, 1 / self.contents[row][col])
                                        # Check to see if everything in the current column is zero
                                        sub_row = row + 1
                                        while sub_row < len(self.contents):
                                                if self.contents[sub_row][col] != 0:
                                                        self.row_add(sub_row, row, -self.contents[sub_row][col])
                                                sub_row += 1
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
                                                sub_row = 0
                                                while sub_row < len(self.contents):
                                                        # Swap row and sub_row if row has a nonzero element
                                                        if self.contents[row][col]:
                                                                self.row_swap(row, sub_row)
                                                        sub_row += 1
                                                row += 1
                                        col +=1
                        self.int_convert()
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
                                elif num == 1 and (len(pivots) == 0 or col > pivots[-1]):
                                        pivots.append(col)
                                        col_flag = True
                                elif num == 1 and (len(pivots) == 0 or col < pivots[-1]):
                                        ref = False
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
        
        # dim
        # Gets the dimensions of the matrix
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
                                        tmp_row.append(1)
                                else:
                                        tmp_row.append(0)
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
        
        # int_convert
        # Converts things in the matrix back to integers, if possible
        def int_convert(self):
                for row in range(len(self.contents)):
                        for col in range(len(self.contents[0])):
                                if type(self.contents[row][col]) == type(float()) and self.contents[row][col] == int(self.contents[row][col]):
                                        self.contents[row][col] = int(self.contents[row][col])
        
        ## Elementary Row Operations ##
        # row_swap
        # Swaps 2 rows in a matrix
        def row_swap(self, row1, row2):
                tmp_row = list(self.contents[row1])
                self.contents[row1] = list(self.contents[row2])
                self.contents[row2] = tmp_row
        
        # row_mul
        # Multiplies a row in a matrix by a constant
        def row_mul(self, row, const):
                if const == 0:
                        raise ValueError("Constant cannot be zero")
                for i in range(len(self.contents[0])):
                        self.contents[row][i] *= const
        
        # row_add
        # adds two rows together (row1 = row1 + const * row2)
        def row_add(self, row1, row2, const):
                if const == None:
                        const = 1
                elif const == 0:
                        raise ValueError("Constant cannot be zero")
                tmp_row = list(self.contents[row2])
                for i in range(len(self.contents[0])):
                        tmp_row[i] *= const
                for i in range(len(self.contents[0])):
                        self.contents[row1][i] += tmp_row[i]
