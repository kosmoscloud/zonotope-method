import numpy as np
import math

class Interval:
    def __init__(self,a: float=None, b: float=None):
        # If only one bound is provided, assume it's both lower and upper bound
        if a is not None and b is None:
            b = a 

        # Ensure the upper bound is greater than or equal to the lower bound
        if b < a:
            raise ValueError("Upper bound must be greater than or equal to lower bound")
        self.lower = a
        self.upper = b

    # Representation of the interval
    def __repr__(self):
        return f"[{self.lower}, {self.upper}]"
    
    # Addition of two intervals
    def __add__(self, other):
        return Interval(self.lower + other.lower, self.upper + other.upper)

    # Subtraction of two intervals
    def __sub__(self, other):
        return Interval(self.lower - other.upper, self.upper - other.lower)

    # Multiplication of two intervals
    def __mul__(self, other):
        return Interval(min(self.lower * other.lower, self.lower * other.upper, self.upper * other.lower,
                            self.upper * other.upper),
                        max(self.lower * other.lower, self.lower * other.upper, self.upper * other.lower,
                            self.upper * other.upper))

    # Division of two intervals
    def __truediv__(self, other):
        return self * other.reciprocal()

    # Exponentiation of an interval to a scalar power
    def __pow__(self, val):
        res = self
        for i in range(val):
            res *= res
        return res

    # String representation of the interval
    def __str__(self):
        return "[" + str(self.lower) + "," + str(self.upper) + "]"
    
    # Return the lower bound of the interval
    def inf(self):
        return self.lower

    # Return the upper bound of the interval
    def sup(self):
        return self.upper

    # Check if a value is contained within the interval
    def contains(self, val):
        return self.lower <= val <= self.upper

    # Compute the middle point of the interval
    def middle_of_interval(self):
        return (self.upper + self.lower) / 2

    # Compute the reciprocal interval
    def reciprocal(self):
        if self.lower == 0 or self.upper == 0:
            raise ValueError("Interval can't include 0")
        return Interval(1 / self.upper, 1 / self.lower)

    # Compute the square root interval
    def sqrt(self):
        if self.inf() < 0 or self.sup() < 0:
            raise Exception("Cant make square of negative number!")
        return Interval(math.sqrt(self.inf()), math.sqrt(self.sup()))
    
class IntervalVector:
    # Initialize an IntervalVector with a list of intervals
    def __init__(self, intervals):
        self.intervals = np.array(intervals)

    # Representation of the IntervalVector
    def __repr__(self):
        return f"IntervalVector({self.intervals})"

class IntervalMatrix:
    # Initialize an IntervalMatrix with a 2D array of intervals
    def __init__(self, matrix):
        self.matrix = np.array(matrix)

    # Matrix multiplication with an IntervalVector
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

    # Representation of the IntervalMatrix
    def __repr__(self):
        return f"IntervalMatrix({self.matrix})"
