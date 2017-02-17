assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

# Define units and peers to ease cell references in algorithm
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Addition to handle diagonal units
diag_units = [[row+col for (row, col) in zip(rows, cols)], [row+col for (row, col) in zip(rows, reversed(cols))]]

unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    for unit in unitlist:
        # Find all box with only 2 remaining potential values

        two_box = [values[box] for box in unit if len(values[box])==2]

        # Loop through the boxes with only 2 remaining potential values to find twins
        for i in range(len(two_box)):
            for j in range(i+1, len(two_box)):
                # If naked twin is found
                if two_box[i] == two_box[j]:

                    # Eliminate the naked twins as possibilities for their peers
                    for k in range(2):
                        update_box = [square for square in unit if two_box[i][k] in values[square] and two_box[i] != values[square]]
                        for box in update_box:
                            assign_value(values,box,values[box].replace(two_box[i][k],''))
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = {}
    for i in range(len(grid)):
        if grid[i] == '.':
            values[boxes[i]] = '123456789'
        else:
            values[boxes[i]] = grid[i]

    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_box = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_box:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values,peer,values[peer].replace(digit,''))

    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """

    for unit in unitlist:
        for num in '123456789':
            has_num = [square for square in unit if num in values[square]]
            if len(has_num) == 1:
                values = assign_value(values, has_num[0], num)



    return values

def reduce_puzzle(values):
    """
    Reduce the puzzle first by repeatedly using the eliminate strategy, the only choice strategy,
    and the naked twin strategy

    Input: Sudoku in dictionary form
    Output: Return false when sudoku has no solution. Otherwise, return the resulting sudoku
    when the current strategies are no longer improving the solution.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked Twin Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[box])==1 for box in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    value, box = min((len(values[box]),box) for box in boxes if len(values[box]) > 1)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[box]:
        new_values = values.copy()
        new_values = assign_value(new_values, box, value)
        attempt = search(new_values)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'



    # Solve the Sudoki
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
