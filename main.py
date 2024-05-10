from intervals import Interval, IntervalVector, IntervalMatrix
from calc import branch_and_prune, plot_boxes

def solveIPLS(matrix, vector, output_file="boxes.png"):

    # Define an initial box covering a wide range in each dimension
    initial_box = IntervalVector([Interval(-10, 10), Interval(-10, 10)])
    
    # Run the branch-and-prune algorithm on the defined problem for different depths
    boxes_max_depth = branch_and_prune(initial_box, matrix, vector, MAX_DEPTH=15)
    boxes_mid_depth = branch_and_prune(initial_box, matrix, vector, MAX_DEPTH=10)
    boxes_low_depth = branch_and_prune(initial_box, matrix, vector, MAX_DEPTH=5)

    # Plot the resulting feasible boxes
    plot_boxes([boxes_max_depth, boxes_mid_depth, boxes_low_depth], save=True, filename=output_file)
        
if __name__ == "__main__":
    solveIPLS(IntervalMatrix([[Interval(1, 2), Interval(4, 7)], [Interval(-1, 1), Interval(1, 4)]]), IntervalVector([Interval(4, 7), Interval(1, 3)]), "result1.png")
    solveIPLS(IntervalMatrix([[Interval(4, 5), Interval(1, 3)], [Interval(-5, -3), Interval(2, 3)]]), IntervalVector([Interval(4, 5), Interval(1, 6)]), "result2.png")
    solveIPLS(IntervalMatrix([[Interval(1, 3), Interval(4, 5)], [Interval(-1, 3), Interval(7, 8)]]), IntervalVector([Interval(1, 2), Interval(4, 6)]), "result3.png")

