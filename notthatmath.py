from poly import Poly
from matrix import Matrix

if __name__ == "__main__":
        p = Poly({2:1, 0:2})
        q = Poly({2:1, 1:2})
        print(p * q)
