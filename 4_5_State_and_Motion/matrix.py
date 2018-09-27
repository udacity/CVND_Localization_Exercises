

def zeroes(height, width):
    """ Creates a matrix of zeroes. """
    g = [[0.0 for _ in range(width)] for __ in range(height)]
    return Matrix(g)


class Matrix(object):
    
    # Initializes a matrix from a 2D grid of values
    # Assumes and initializes a grid-specified number of rows and columns
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
    
    # Overloading the multiplication operator
    def __mul__(self, other):
        ''' self and other are Matrix objects.
        This function check the dimensions of the two matrices, 
        multiplies them according to the rules of linear algebra, 
        and returns a new matrix.'''

        if(self.cols == other.rows):
            # Then the dimensions match for multiplication!

            # Create a new matrix of zeroes of the appropriate size (self.rows x other.cols)
            self_times_other = zeroes(self.rows, other.cols)

            # iterate through the rows of self
            for i in range(self.rows):

                # iterate through the columns of other
                for j in range(other.cols):

                    # iterate through rows of other and sum
                    for k in range(other.rows):
                        # multiply and sum step
                        self_times_other[i][j] += (self[i][k] * other[k][j])

                        # for debugging
                        #print(' i = ' + str(i) +', j = ' + str(j) + ', k = ' + str(k))
            return self_times_other

        else:
            print('Invalid matrix dimensions!')
            print('A_cols = ' + str(self.cols) + ', and B_rows = ' + str(other.rows))
            # return []
        
        
    # Overloading indexing
    def __getitem__(self, index):
        return self.grid[index]
        
    # Overloading print output
    def __repr__(self):
        s = '['
        for row in self.grid:
            s += '['
            for item in row:
                s += str(item) +' '
            s += ']\n'
            
        s += ']'
        
        return s


        
    
