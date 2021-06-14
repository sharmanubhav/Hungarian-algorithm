import numpy as np
import copy


# Takes an array
# Returns a new matrix with each row subtracted from it the smallest element in that row.
#     and with each column subtracted from it, the smallest element in that column.

def reduce(matrix):
    rows = np.shape(matrix)[0]  # Get number of rows
    cols = np.shape(matrix)[1]  # Get number of columns
    for i in range(rows):  # Loop through each element in the rows
        matrix[i] = matrix[i] - np.amin(matrix[i], axis=0)  # Subtract min from each row
    print("\n" + "Running Reduce... result is")
    matrix = np.transpose(matrix)
    for j in range(cols):  # Loop through each element in the columns
        matrix[j] = matrix[j] - np.amin(matrix[j], axis=0)  # Subtract min from each column
    matrix = np.transpose(matrix)
    print(matrix)
    return matrix


# Takes an array. This function is a helper for min_zero eventually used in Cover Step.
# Returns 2 x n array with number of zeros in each row and column. The first vector of the return array gives number of zeros in the rows.
#     The second vector of the return array gives number of zeros in the columns.

def num_zeros(matrix):
    n = np.shape(matrix)[0]
    num_zeros = np.zeros((2, n))
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 0:  # If an element is zero, update the respective column and row entry accordingly.
                num_zeros[0][i] += 1
                num_zeros[1][j] += 1
    return num_zeros


# Takes a 2 x n array returned from the num_zeros function.
# Returns a 1 x 2 array. The first element states whether the minimum number of zeros occur at a row or column [0 means it occurs at row and 1 means it occurs at column].
#       The second element is the row or the column number where the minimum zero can be found.

def min_zero(num_zeros_array):
    min_zero_index = np.zeros(2)
    n = np.shape(num_zeros_array)[1]
    min = n  # Initializing min to be the maximum number of zeros it can have i.e. n
    for i in range(2):
        for j in range(n):
            if num_zeros_array[i][j] != 0 and num_zeros_array[i][j] <= min:  # If we find a min that is less than the current min, we update it.
                min = num_zeros_array[i][j]
                min_zero_index[0] = i
                min_zero_index[1] = j
    return min_zero_index


# Takes an array, uses min_zero to find the zero that is to be boxed.
# Returns a 1 x 3 array. The first element states whether the minimum number of zeros occur at a row or column [0 means it occurs at row and 1 means it occurs at column].
#       The second element is the row where the boxed zero can be found. The third element is the column where the boxed zero can be found.

def boxed_zero(matrix):
    index_min_zero = min_zero(num_zeros(matrix))
    n = np.shape(matrix)[1]
    if index_min_zero[0] == 0:  # If we select boxed zero based on the row.
        for i in range(n):  # Iterate through the column and find the one where zero occurs.
            j = int(index_min_zero[1])
            if matrix[j][i] == 0:
                return np.array([0, j, i])
    else:  # If we select boxed zero based on the column.
        for i in range(n):  # Iterate through the row and find the one where zero occurs.
            j = int(index_min_zero[1])
            if matrix[i][j] == 0:
                return np.array([1, i, j])


# Parameters:
#     matrix: The original matrix we are trying to cover.
#     matrix_copy: The matrix after we have covered some lines. Once a row or column is covered, all elements of this copy is replaced with -1.
#     covered_zeros: The number of zeros we have covered so far. This helps us know when to terminate the cover step-- when we have covered all zeros.
#     cover_array: A 2 x n array of 0's and 1's that included which rows/ columns are covered right now. 1 means covered and 0 means uncovered.
# Uses recursion to do the covering and returns the cover array.

def cover_helper(matrix, matrix_copy, covered_zeros, cover_array):
    nzeros = num_zeros(matrix_copy)
    total_zeros = np.sum(num_zeros(matrix)[0])  # The total zeros we have in the matrix.
    if covered_zeros == total_zeros:  # If we covered all the zeros, cover step is done.
        return cover_array
    index = boxed_zero(matrix_copy)
    if index[0] == 0:  # If boxed zero occurs in row:
        j = int(index[2])
        cover_array[1][j] = 1  # Update the cover array
        matrix_copy[:, j] = -1  # Update the column in the copy with -1s.
        covered_zeros += nzeros[1][j]  # Keep track of how many zeros we have actually covered.
        return cover_helper(matrix, matrix_copy, covered_zeros, cover_array)
    else:  # If boxed zero occurs in column:
        i = int(index[1])
        cover_array[0][i] = 1  # Update the cover array
        matrix_copy[i, :] = -1  # Update the row in the copy with -1s.
        covered_zeros += nzeros[0][i]  # Keep track of how many zeros we have actually covered.
        return cover_helper(matrix, matrix_copy, covered_zeros, cover_array)


# Takes an array. This utilizes the cover_helper.
# Returns the cover array. Cover Array is a 2 x n array of 0's and 1's that includes which rows/ columns are covered right now. 1 means covered and 0 means uncovered.

def cover(matrix):
    n = np.shape(matrix)[0]
    cover_array = np.zeros((2, n))
    return cover_helper(matrix, copy.deepcopy(matrix), 0, cover_array)


# Takes a matrix and the 2D Cover Array
# Returns the minimum uncovered number in the matrix

def uncovered_min(matrix, cover_array):
    rows = np.shape(matrix)[0]
    cols = np.shape(matrix)[1]
    min = 10 * 10
    for i in range(rows):  # Loop through each element in the matrix
        for j in range(cols):
            if cover_array[0][i] == 0 and cover_array[1][j] == 0 and matrix[i][j] < min:  # If the element is uncovered and less than min, assign it to min
                min = matrix[i][j]
    return min


# Takes the matrix and the 2D Cover Array. This utilizes uncovered_min
# Performs the adjust step and returns the new adjusted matrix

def adjust(matrix, cover_array):
    rows = np.shape(matrix)[0]
    cols = np.shape(matrix)[1]
    min = uncovered_min(matrix, cover_array)  # Get minimum uncovered number
    for i in range(rows):  # Loop through each element in the matrix
        for j in range(cols):
            if cover_array[0][i] == 0 and cover_array[1][j] == 0:  # If the element is uncovered, subtract minimum uncovered number from it
                matrix[i][j] -= min
            elif cover_array[0][i] == 1 and cover_array[1][j] == 1:  # If the element is covered twice, add minimum uncovered number to it
                matrix[i][j] += min
    return matrix


# Takes a numpy array and checks if it is suited to run hungarian algorithm. Checks if the array is nxn, and if all entries are non-negative integers.
# Returns boolean true or false based on if the matrix passed the type checking.

def type_check(matrix):
    rows = np.shape(matrix)[0]
    cols = np.shape(matrix)[1]
    if rows != cols:  # Check if array is n x n.
        return False
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] < 0 or matrix[i][j] != np.floor(matrix[i][j]):  # Check if each entry is non-negative integer.
                return False
    return True


# Takes a 2D nxn numpy array and optional parameter type. By default, type is "min" but can be given "max" to maximize the sum of entries.
#       If something else is given for type, it deafults to "min".
# Runs hungarian algorithm and returns an equivalent 2D array with some zeros. Each set of permutation zero is the solution to the problem.

def hungarian_algorithm(matrix, type="min"):
    print("\n" + "\n" + "Initial matrix:")
    print(matrix)
    if type_check(matrix):  # If type_check passes, algorithm runs.
        if type == "max":  # For maximizing, negate the entries and make it non-negative by adding an offset.
            matrix = np.amin(matrix) + matrix * (-1)
        matrix = reduce(matrix)  # Reduce Step
        n = np.shape(matrix)[0]
        covered_lines = 0
        while covered_lines < n:  # Cover runs until we have n cover lines
            cover_array = cover(matrix)
            covered_lines = np.sum(cover_array)
            if covered_lines < n:
                matrix = adjust(matrix, cover_array)  # Adjust Step
        print("\n" + "Algorithm success! Result is")
        print(matrix)
    else:  # Type Check Error
        print("ERROR: Computation failed due to type error in matrix." + "\n"
              + "Try fixing some of these:" + "\n"
              + "1. Matrix must be square (n x n) i.e. same number of rows and columns." + "\n"
              + "2. There must be no negative entries." + "\n"
              + "3. All entries must be integers." + "\n")


# ---------------------------------------
# SOME EXAMPLES

M = np.array([[5, 7, 3, 6],
              [6, 6, 5, 4],
              [6, 5, 10, 15],
              [9, 7, 6, 7]])

N = np.array([[6, 8, 5, 9, 6, 7],
              [3, 5, 7, 4, 8, 7],
              [4, 8, 6, 8, 9, 7],
              [7, 5, 5, 6, 4, 3],
              [9, 7, 3, 3, 7, 5],
              [8, 5, 7, 5, 7, 8]])

hungarian_algorithm(M)
hungarian_algorithm(N, "max")

# ----------------------------------------