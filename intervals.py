import numpy as np
import math

class Interval:
    def __init__(self,a: float=None, b: float=None):
        if a is not None and b is None:
            b = a 
        
        if b < a:
            raise ValueError("Upper bound must be greater than or equal to lower bound")
        self.lower = a
        self.upper = b

    def __repr__(self):
        return f"[{self.lower}, {self.upper}]"
    
    def __add__(self, other):
        return Interval(self.lower + other.lower, self.upper + other.upper)

    def __sub__(self, other):
        return Interval(self.lower - other.upper, self.upper - other.lower)

    def __mul__(self, other):
        return Interval(min(self.lower * other.lower, self.lower * other.upper, self.upper * other.lower,
                            self.upper * other.upper),
                        max(self.lower * other.lower, self.lower * other.upper, self.upper * other.lower,
                            self.upper * other.upper))

    def __truediv__(self, other):
        return self * other.reciprocal()

    def __pow__(self, val):
        res = self
        for i in range(val):
            res *= res
        return res

    def __str__(self):
        return "[" + str(self.lower) + "," + str(self.upper) + "]"
    
    def inf(self):
        return self.lower

    def sup(self):
        return self.upper

    def contains(self, val):
        return self.lower <= val <= self.upper

    def middle_of_interval(self):
        return (self.upper + self.lower) / 2

    def reciprocal(self):
        if self.lower == 0 or self.upper == 0:
            raise ValueError("Interval can't include 0")
        return Interval(1 / self.upper, 1 / self.lower)

    def sqrt(self):
        if self.inf() < 0 or self.sup() < 0:
            raise Exception("Cant make square of negative number!")
        return Interval(math.sqrt(self.inf()), math.sqrt(self.sup()))
    
class IntervalVector:
    def __init__(self, intervals):
        self.intervals = np.array(intervals)

    def __repr__(self):
        return f"IntervalVector({self.intervals})"

class IntervalMatrix:
    def __init__(self, matrix):
        self.matrix = np.array(matrix)

    def __mul__(self, vector):
        if not isinstance(vector, IntervalVector):
            raise ValueError("The operand must be an IntervalVector")
        
        result_intervals = []
        for row in self.matrix:
            sum_interval = Interval(0, 0)
            for interval, vector_interval in zip(row, vector.intervals):
                sum_interval += interval * vector_interval
            result_intervals.append(sum_interval)
        
        return IntervalVector(result_intervals)

    def __repr__(self):
        return f"IntervalMatrix({self.matrix})"
