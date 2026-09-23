# import unittest
# from test import support

from .curry import curry3

def f(x: int, y: int, z: int) -> int:
    return x + y + z

def g(x: int, y: int, z: int, a: int) -> int:
    return x + y + z + a

def test_all_curried_all_invoked():
    fc = curry3(f)
    assert fc(1)(1)(3) == 5

def test_all_curried_partial_invoked():
    fc = curry3(f)
    assert fc(1)(1)(2) == 4
    assert fc(1, 1, 2) == 4
    assert fc(1, 1)(2) == 4
    assert fc(1)(1, 2) == 4
    #assert fc(y=1)(1, 2) == 4

def test_all_curried_partial_invoked2():
    gc = curry3(g)
    assert gc(1)(1)(2)(3) == 7
    assert gc(1, 1, 2, 3) == 7
    assert gc(1, 1, 2)(3) == 7
    assert gc(1, 1)(2, 3) == 7
    assert gc(1, 1)(2)(3) == 7
    assert gc(1)(1, 2, 3) == 7
    assert gc(1)(1, 2)(3) == 7


# class MyTestCase1(unittest.TestCase):

#     # Only use setUp() and tearDown() if necessary

#     def setUp(self):
#         self.fc = curry(f)

#     def tearDown(self):
#         pass

#     def test_feature_one(self):
#         # self.assertEqual(self.fc(1, 1, 1), 3)
#         # self.assertEqual(self.fc(1, 1), 5)
#         self.assertEqual(self.fc(1)(1)(3), 5)
#         # self.assertEqual(self.fc(1)(1, 1), 3)
#         # self.assertEqual(self.fc(x=1, y=1, z=1), 3)
#         # self.assertEqual(self.fc(x=1, y=1), 5)
#         # self.assertEqual(self.fc(1)(y=1, z=1), 3)
#         # self.assertEqual(self.fc(1)(y=1), 5)
#         # self.assertEqual(self.fc(z=10)(1, 1), 12)
#         # self.assertEqual(self.fc(y=10)(1), 14)

# if __name__ == '__main__':
#     unittest.main()
