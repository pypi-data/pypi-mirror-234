"""
This module defines the Concat and ConcatMap classes, which provide a
unified means of indexing lazy concatenations of objects of different
sizes.  For example, suppose we have a set of files and we wish to access
them as if they were a single blob.  A ConcatMap can be built from list of
file (name, size) tuples.  The resulting ConcatMap would have a "length"
equal to the sum of the file sizes, and will accept any index in the range
[0, length-1].  The ConcatMap will then map the index to the appropriate
file and offset within that file, via a balanced binary search tree over
offsets.  A Concat object includes a ConcatMap, but also provides getitem
and iter methods, so that it can be used like an array or list.
"""

# concat.py
#
# Copyright (c) 2022 Gary William Flake
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

###############################################################################

class ConcatMap:
  """
  Given N objects of different sizes, a ConcatMap provides a unified
  interface for accessing the objects as if they were a single array-like
  object.  The ConcatMap is built from a list of (key, size) tuples, where
  the key uniquely identified an object and size is the size of the
  object.  The ConcatMap will then map the index to the appropriate key
  and offset within that object, via a balanced binary search tree over
  offsets.
  """

  #############################################################################

  def __init__(self, key, size):
    """
    Create a ConcatMap leaf node, storing the key and size, but leaving
    the start and total fields to be determined later.  The start field is
    eventually set to the cumulative size of the left subtree, and the
    total field is eventually set to the cumulative size of this node and
    its descendants.
    Args:
      key: The key of the object.
      size: The size of the object.
    """
    self.key = key
    self.size = size
    self.start = 0
    self.total = 0
    self.left = None
    self.right = None

  #############################################################################

  @staticmethod
  def _optimize(pairs):
    """
    Helper function to reorder a sorted list of (key, size) pairs so as to
    minimize the expected runtime of the binary search tree.  Given the
    tree building algorithm used by ConcatMap, this function reorders the
    list so that that the largest objects are closest to the root.
    Args:
      pairs: The list of objects.
    Returns:
      The reordered list of objects.
    """
    n = len(pairs)
    if n <= 1: return pairs
    # The left subtree contains the odd-indexed pairs.
    left = [pairs[i] for i in range(1, n) if i % 2 == 1]
    # The right subtree contains the even-indexed pairs.
    right = [pairs[i] for i in range(1, n) if i % 2 == 0]
    # The root is the first pair.  If we recursively reorder the nodes in
    # this way, the largest objects will be placed closest to the root.
    return ConcatMap._optimize(left) + [pairs[0]] + ConcatMap._optimize(right)

  #############################################################################

  @staticmethod
  def from_list(items, reorder=False):
    """
    Create a ConcatMap object from a list of (key, size) tuples.
    Args:
      items: The list of items.
      reorder: A boolean indicating whether items can be reordered to
                optimize the expected lookup time.  (Default: False)
    Returns:
      The root of the ConcatMap object.
    """
    if reorder:
      # Sort the items by size, largest first.
      items = sorted(items, key=lambda x: x[1], reverse=True)
      # Optimize the order of the items.
      items = ConcatMap._optimize(items)
    # Create the ConcatMap object.
    root = ConcatMap._from_list(items)
    # Update the indices.
    ConcatMap._update_indices(root)
    return root

  #############################################################################

  @staticmethod
  def _from_list(items):
    """
    Helper function to create a ConcatMap object from a list of items.
    Args:
      items: The list of items.
    Returns:
      The root of the ConcatMap object.
    """
    n = len(items) if items else 0
    if n == 0: return None
    mid = n // 2
    # Create the root node.
    root = ConcatMap(*items[mid])
    # Create the left subtree.
    root.left = ConcatMap._from_list(items[:mid])
    # Create the right subtree.
    root.right = ConcatMap._from_list(items[mid + 1:])
    return root

  #############################################################################

  @staticmethod
  def _update_indices(root, cumulative_size=0):
    """
    Helper function to update the indices of the ConcatMap object.
    Args:
      root: The root of the ConcatMap object.
      cumulative_size: The cumulative size of the objects.
    Returns:
      The updated cumulative size.
    """
    if root is None: return cumulative_size
    # Update start indices and total size for left subtree
    cumulative_size = ConcatMap._update_indices(root.left, cumulative_size)
    # Update start index for the current node
    root.start = cumulative_size
    # Update cumulative size for this node
    cumulative_size += root.size
    # Update start indices and total size for right subtree
    cumulative_size = ConcatMap._update_indices(root.right, cumulative_size)
    # Update total size for the current subtree
    root.total = cumulative_size
    return cumulative_size

  #############################################################################

  def __getitem__(self, index):
    """
    Get the item at the specified index (with range checking).
    Args:
      index: The index of the item.
    Returns:
      The item at the specified index.
    """
    if index < 0: index += self.total
    if index < 0 or index >= self.total:
      raise IndexError("Index out of range")
    return self._get(index)

  #############################################################################

  def _get(self, index):
    """
    Helper function to get the item at the specified index.
    Args:
      index: The index of the item.
    Returns:
      The item at the specified index.
    """
    # pylint: disable=protected-access
    if index < self.start:
      return self.left._get(index)
    if index >= self.start + self.size:
      return self.right._get(index)
    # pylint: enable=protected-access
    return self.key, index - self.start

  #############################################################################

  def __len__(self):
    """
    Get the total size of the ConcatMap object.
    Returns:
      The total size of the ConcatMap object.
    """
    return self.total if self is not None else 0

###############################################################################

class Concat:
  """
  Given N objects of different sizes, a Concat provides a unified interface
  for accessing the objects as if they were a single array-like object.
  The Concat is built from a list of (key, size) tuples, where key uniquely
  identified an object, and size is the size of the object.  The Concat
  will then map the index to the appropriate key and offset within that
  object, via a balanced binary search tree over offsets.
  """

  #############################################################################

  def __init__(self, pairs, reorder=False, getitem=None):
    """
    Create a Concat object from a list of (key, size) tuples.
    Args:
      pairs: The list of (key, size) tuples.
      reorder: A boolean indicating whether items can be reordered to
               optimize the expected lookup time.  (Default: False)
    """
    self.map = ConcatMap.from_list(pairs, reorder=reorder)
    self.getitem = getitem

  #############################################################################

  @staticmethod
  def from_arrays(*args, **kwargs):
    """
    Create a Concat object from a list of array-like objects.
    Args:
      args: The list of items.
      reorder: A boolean indicating whether items can be reordered to
               optimize the expected lookup time.  (Default: False)
    Returns:
      The root of the ConcatMap object.
    """
    pairs = [(x, len(x)) for x in args if len(x) > 0]
    reorder = kwargs.get("reorder", False)
    getitem = kwargs.get("getitem", None)
    return Concat(pairs, reorder=reorder, getitem=getitem)

  #############################################################################

  def __getitem__(self, index):
    """
    Get the item at the specified index.
    Args:
      index: The index of the item.
    Returns:
      The item at the specified index.
    """
    sz = len(self)
    if isinstance(index, int):
      if index < 0: index = sz + index
      if index >= sz or index < 0:
        raise IndexError("Index out of range")
      x, i = self.map[index]
      return x[i] if self.getitem is None else self.getitem(x, i)
    elif isinstance(index, slice):
      return self.__getslice__(index)
    raise TypeError("Invalid index.")

  #############################################################################

  def __getslice__(self, index):
    """
    Generates a slice from a Concat.

    Parameters:
      start (int): The starting index of the Concat element to get.
      stop (int): The stopping index of the Concat element to get.
      step (int): The step size of the Concat element to get.

    Returns:
      generator of the slice of the Concat specified.
    """
    sz = len(self)
    start = index.start or 0
    if start < 0: start = sz + start
    stop = index.stop or sz
    if stop < 0: stop = sz + stop
    step = index.step or 1
    if step < 0: step = sz + step
    for idx in range(start, stop, step):
      yield self.__getitem__(idx)

  #############################################################################

  def __iter__(self):
    """
    Iterate over the items in the Concat object.
    Returns:
      An iterator over the items in the Concat object.
    """
    for i in range(len(self)):
      yield self.__getitem__(i)

  #############################################################################

  def __len__(self):
    """
    Get the total size of the Concat object.
    Returns:
      The total size of the Concat object.
    """
    return len(self.map) if self.map is not None else 0

###############################################################################
