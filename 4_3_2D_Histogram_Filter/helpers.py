def normalize(grid):
    """
    Given a grid of unnormalized probabilities, computes the
    correspond normalized version of that grid. 
    """
    total = 0.0
    for row in grid:
        for cell in row:
            total += cell
    for i,row in enumerate(grid):
        for j,cell in enumerate(row):
            grid[i][j] = float(cell) / total
    return grid


def blur(grid, blurring):
    """
    Spreads probability out on a grid using a 3x3 blurring window.
    The blurring parameter controls how much of a belief spills out
    into adjacent cells. If blurring is 0 this function will have 
    no effect. 
    """
    height = len(grid)
    width  = len(grid[0])

    center_prob = 1.0-blurring
    corner_prob = blurring / 12.0
    adjacent_prob = blurring / 6.0

    window = [
            [corner_prob,  adjacent_prob,  corner_prob],
            [adjacent_prob, center_prob,  adjacent_prob],
            [corner_prob,  adjacent_prob,  corner_prob]
        ]
    new = [[0.0 for i in range(width)] for j in range(height)]
    for i in range(height):
        for j in range(width):
            grid_val = grid[i][j]
            for dx in range(-1,2):
                for dy in range(-1,2):
                    mult = window[dx+1][dy+1]
                    new_i = (i + dy) % height
                    new_j = (j + dx) % width
                    new[new_i][new_j] += mult * grid_val
    return normalize(new)

def is_robot_localized(beliefs, true_pos):
    """
    Returns None if the robot has no "strong opininon" about
    its belief. The robot has a strong opinion when the 
    size of it's best belief is greater than twice the size of 
    its second best belief.

    If it DOES have a strong opinion then this function returns 
    True if that opinion is correct and False if it is not.
    """
    best_belief = 0.0
    best_pos = None
    second_best = 0.0
    for y, row in enumerate(beliefs):
        for x, belief in enumerate(row):
            if belief > best_belief:
                second_best = best_belief
                best_belief = belief
                best_pos = (y,x)
            elif belief > second_best:
                second_best = belief
    if second_best <= 0.00001 or best_belief / second_best > 2.0:
        # robot thinks it knows where it is
        localized =  best_pos == true_pos
        return localized, best_pos
    else:
        # No strong single best belief
        return None, best_pos

def close_enough(g1, g2):
    if len(g1) != len(g2):
        return False
    if len(g1) == 0 or len(g1[0]) != len(g2[0]):
        return False
    for r1, r2 in zip(g1,g2):
        for v1, v2 in zip(r1, r2):
            if abs(v1 - v2) > 0.001:
                print(v1, v2)
                return False
    return True