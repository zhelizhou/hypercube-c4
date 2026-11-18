"""Coordinate cube geometry, rebuilt for the independent upper-bound project."""
from itertools import combinations


class Cube:
    def __init__(self, n):
        self.n = n
        self.vertices = range(1 << n)
        self.edges = [(v, v ^ (1 << i)) for v in self.vertices for i in range(n) if not v >> i & 1]
        self.index = {e: k for k, e in enumerate(self.edges)}
        self.incident = [[] for _ in self.vertices]
        for k, (u, v) in enumerate(self.edges):
            self.incident[u].append(k)
            self.incident[v].append(k)
        self.squares = []
        for i, j in combinations(range(n), 2):
            for v in self.vertices:
                if v & ((1 << i) | (1 << j)):
                    continue
                w, z, t = v ^ (1 << i), v ^ (1 << j), v ^ (1 << i) ^ (1 << j)
                self.squares.append([self.index[tuple(sorted(e))] for e in [(v,w),(v,z),(w,t),(z,t)]])

