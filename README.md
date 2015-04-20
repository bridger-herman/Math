# Math
Mathematics library
## Matrix
### Methods:
+ `__init__(self, lst2D)` - Initializer, takes a 2 Dimensional list
 + No ragged matrices (all rows must have the same length)
+ `__str__(self)` - String representation
+ `det(self)` - Determinant
 + No non-square matrices
+ `inverse(self)` - Inverse
 + No non-square matrices
+ `rref(self)` - Reduced Row Echelon Form
+ `is_rref(self)` - Is the matrix in Reduced Row Echelon Form?
+ `ref(self)` - Row Echelon Form
+ `is_ref()` - Is the matrix in Row Echelon Form?
+ `augment(self, other)` - Augments `self` with other matrix
 + `self` and `other` must have the same number of rows
+ `dim(self)` - Dimensions of the matrix
+ `identity(n = 3)` - Static method, returns the identity matrix I<sub>n</sub>
+ `__mul__(self, const)` - Multiplies the entire matrix by a constant
#### Elementary Row Operations
+ `row_swap(self, row1, row2)` - Swaps rows `row1` and `row2`
+ `row_mul(self, row, const)` - Multiplies `row` by a constant, `const`
+ `row_add(self, row1, row2, const)` - Adds two rows together in the fashion `row1 = row1 + const * row2`
