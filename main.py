from intervals import Interval, IntervalVector, IntervalMatrix
from calc import branch_and_prune, plot_boxes

def main():
    
    # Define an example interval matrix A and vector b
    A_example = IntervalMatrix([
        [Interval(1, 2), Interval(4, 6)],
        [Interval(0, 1), Interval(1, 3)]
    ])

    b_example = IntervalVector([
        Interval(4, 7),
        Interval(1, 3)
    ])

    # Define an initial box covering a wide range in each dimension
    initial_box = IntervalVector([Interval(-10, 10), Interval(-10, 10)])
    
    # Run the branch-and-prune algorithm on the defined problem for different depths
    boxes_max_depth = branch_and_prune(initial_box, A_example, b_example, MAX_DEPTH=15)
    boxes_mid_depth = branch_and_prune(initial_box, A_example, b_example, MAX_DEPTH=10)
    boxes_low_depth = branch_and_prune(initial_box, A_example, b_example, MAX_DEPTH=5)

    # Plot the resulting feasible boxes
    plot_boxes([boxes_max_depth, boxes_mid_depth, boxes_low_depth])
        
if __name__ == "__main__":
    main()
    