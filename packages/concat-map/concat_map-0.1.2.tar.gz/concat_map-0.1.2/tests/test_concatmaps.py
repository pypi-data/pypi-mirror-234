"""
This module contains unit tests for the ConcatMap and Concat classes.
"""

import unittest
import random
from concat_map import Concat

class TestConcatMap(unittest.TestCase):
  """
  Unit Test class for testing the ConcatMap and Concat classes.
  """

  def setUp(self):
    """
    Set up the test fixture.
    """

  def test_empty(self):
    """
    Test that the empty map is empty.
    """
    c = Concat.from_arrays([])
    self.assertEqual(len(c), 0)

  def test_one(self):
    """
    Test that a single element map works.
    """
    c = Concat.from_arrays([1])
    self.assertEqual(len(c), 1)

  def test_two(self):
    """
    Test that a two element map works.
    """
    c = Concat.from_arrays([1, 2], [3, 4])
    self.assertEqual([x for x in c], list(range(1, 5)))

  def test_strings(self):
    """
    Test that strings work.
    """
    c = Concat.from_arrays("hello", " ", "world", "!")
    self.assertEqual("".join(c), "hello world!")

  def test_random(self):
    """
    Test that random elements work.
    """
    lsts = []
    for _ in range(100):
      n = random.randint(1, 100)
      l = list(range(n))
      random.shuffle(l)
      lsts.append(l)
    c = Concat.from_arrays(*lsts)
    flat = [x for l in lsts for x in l]
    self.assertEqual(flat, list(c))

  def test_slice(self):
    """
    Test that slices work.
    """
    lsts = []
    for _ in range(100):
      n = random.randint(1, 100)
      l = list(range(n))
      random.shuffle(l)
      lsts.append(l)
    c = Concat.from_arrays(*lsts)
    flat = [x for l in lsts for x in l]
    self.assertEqual(flat[20:80], list(c[20:80]))
