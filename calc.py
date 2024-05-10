from intervals import *
import matplotlib.pyplot as plt

def infeasibility_test(box : IntervalVector, A : IntervalMatrix, b: IntervalVector):
    """Test if the given box is infeasible based on the interval system Ax = b.
    Args:
        box (IntervalVector): The current box representing ranges of x.
        A (IntervalMatrix): Interval matrix.
        b (IntervalVector): Interval vector.
    Returns:
        bool: True if the box is infeasible, False otherwise.
    """
    result = A * box
    for result_interval, target_interval in zip(result.intervals, b.intervals):
        if result_interval.upper < target_interval.lower or result_interval.lower > target_interval.upper:
            return True  # No overlap, infeasible
    return False

def feasibility_test(box : IntervalVector, A : IntervalMatrix, b: IntervalVector):
    """Test if the given box is feasible based on the interval system Ax = b.
    Args:
        box (IntervalVector): The current box representing ranges of x.
        A (IntervalMatrix): Interval matrix.
        b (IntervalVector): Interval vector.
    Returns:
        bool: True if the box is entirely feasible, False otherwise.
    """
    result = A * box
    for result_interval, target_interval in zip(result.intervals, b.intervals):
        if not (result_interval.lower >= target_interval.lower and result_interval.upper <= target_interval.upper):
            return False  # Not entirely contained
    return True

def split_box(box):
    """Split the given box along its widest dimension into two halves."""
    max_width = 0
    max_index = -1
    for i, interval in enumerate(box.intervals):
        width = interval.upper - interval.lower
        if width > max_width:
            max_width = width
            max_index = i
    
    # Split along the widest dimension
    middle_value = (box.intervals[max_index].lower + box.intervals[max_index].upper) / 2
    left_intervals = box.intervals.copy()
    right_intervals = box.intervals.copy()

    left_intervals[max_index] = Interval(box.intervals[max_index].lower, middle_value)
    right_intervals[max_index] = Interval(middle_value, box.intervals[max_index].upper)

    return [IntervalVector(left_intervals), IntervalVector(right_intervals)]

def branch_and_prune(box: IntervalVector, A: IntervalMatrix, b: IntervalVector, depth=0, MAX_DEPTH=10):
    """Zonotope-based pruning"""
    if infeasibility_test(box, A, b):
        return []
    elif feasibility_test(box, A, b):
        return [box]
    elif depth >= MAX_DEPTH:
        return [box]  # Return as borderline if too deep

    # Split the box into smaller sub-boxes
    split_boxes = split_box(box)
    feasible_boxes = []
    for sub_box in split_boxes:
        result = branch_and_prune(sub_box, A, b, depth + 1, MAX_DEPTH)
        feasible_boxes.extend(result)

    return feasible_boxes

def plot_boxes(boxes):
    colors = ['blue', 'red', 'green', 'yellow', 'purple', 'orange']
    plt.figure(figsize=(6, 6))
    for i, depth in enumerate(boxes):
        for box in depth:
            lower_left = (box.intervals[0].lower, box.intervals[1].lower)
            width = box.intervals[0].upper - box.intervals[0].lower
            height = box.intervals[1].upper - box.intervals[1].lower
            plt.gca().add_patch(plt.Rectangle(lower_left, width, height, fill=None, edgecolor=colors[i%len(colors)], linewidth=1))
    plt.xlim(-11, 11)
    plt.ylim(-11, 11)
    plt.show()