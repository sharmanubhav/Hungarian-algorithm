# Hungarian-algorithm

## Joseph Tadrous and Anubhav Sharma


### Introduction

The Hungarian Algorithm is an optimization algorithm that solves n x n minimization assignment problems. It was developed and published in 1955 by Harold Kuhn. It is given the name “Hungarian algorithm” because it is significantly based on the works of the two Hungarian mathematicians, Dénes Kőnig and Jenő Egerváry. 

The Hungarian Algorithm involves four main steps: Reduce, Cover, Adjust and Solve.

In the reduce step, for each row, the smallest element in that row is subtracted from each element in the row. Then, for each column, the smallest element in that column is subtracted from each element in the column.

In the cover step, the aim is to draw as few lines as possible to cover all the zeros in the matrix. If less than n lines are needed, the adjust step is performed. If exactly n lines are needed, the solve step is performed.

In the adjust step, the smallest number not covered by lines is subtracted from all uncovered numbers and added to every number that is covered twice. Then, all the lines are erased and the cover step is performed again.

In the solve step, there will be at least one permutation set of zeros. Each permutation set of zeros corresponds to a solution of the original problem.


### Motivation

Performing the Hungarian Algorithm by hand might be time inefficient and risky because it involves many steps that can be repeated and might push people to make mistakes. Therefore, we found that coding the Hungarian Algorithm will benefit students and anyone using this algorithm because it is more convenient, accurate, and time efficient.


### Methods

The main function is titled hungarian_algorithm which takes parameters matrix and type with type being optional. The matrix is a  2-D n x n numpy array. The optional parameter type is the type of the problem to be solved. By default, type is `min` i.e. the algorithm aims to minimize the sum of the entries in the matrix. If the type is set to `max`, the algorithm runs to maximize.  If something else is given for type, it defaults to minimization.

Before running the algorithm, the code checks if the matrix provided is compatible to run the Hungarian algorithm. This is achieved by a function called `type_check`. This function takes a numpy array and checks if the array is n x n, and if all entries are non-negative integers. If any of these conditions are not passed, it returns false. If all of them are satisfied, it returns true and proceeds to the next steps.
 
#### Reduce
i. `reduce`
This function takes an array and performs the first step of the Hungarian Algorithm on it, the reduce step. Through a loop, in each row, the minimum element is found and
subtracted from all the entries in its row. Through another loop, in each column, the minimum element is found and subtracted from all the entries in its column. The function returns a new reduced version of the original array.

#### Cover
i. `num_zeros`
This function takes an array and returns a 2 x n array with a number of zeros in each row and column. The first vector of the return array gives numbers of zeros in the rows. The second vector of the return array gives numbers of zeros in the columns. This function is a helper for `min_zero` function.

ii. `min_zero`
This function takes a 2 x n array returned from the num_zeros function and returns a 1 x 2 array. The first element of the returned array states whether the minimum number of zeros occur at a row or column-- 0 means it occurs at row and 1 means it occurs at column. The second element is the row or the column number where the minimum zero can be found.

iii. `boxed_zero`
This function takes an array, uses `min_zero` to find the zero that is to be boxed, and returns a 1 x 3 array. The first element states whether the minimum number of zeros occur at a row or column-- 0 means it occurs at row and 1 means it occurs at column.
The second element is the row where the boxed zero can be found. The third element is the column where the boxed zero can be found.

iv. `cover_helper`
This is the primary function of the cover step and takes the following parameters: <br/>
`matrix`: The original matrix we are trying to cover. <br/>
`matrix_copy`: The matrix after we have covered some lines. Once a row or column is covered, all elements of this copy are replaced with -1. <br/>
`covered_zeros`: The number of zeros we have covered so far. This helps us know when to terminate the cover step i.e. when we have covered all zeros. <br/>
`cover_array`: A 2 x n array of 0's and 1's that includes which rows/ columns are covered right now. 1 means covered and 0 means uncovered. <br/>
	The function uses recursion to do the covering and returns the cover array.

v. `cover`
	This function takes an array and returns the cover array. It utilizes the `cover_helper`. 

#### Adjust
i. `uncovered_min`
This function takes an array and the 2D cover array. It returns the minimum uncovered number in the array by traversing the whole array and utilizing the cover array to check for uncovered numbers.

ii. `adjust`
This is the primary function of the adjust step. It takes an array and the cover array. It performs the adjust step by traversing through each element in the matrix, adding the minimum uncovered number from `uncovered_min` to entries covered twice, and subtracting it from uncovered entries.




The following flowchart illustrates the big picture on how the code runs:

![flowchart](https://github.com/sharmanubhav/Hungarian-algorithm/blob/main/flowchart.png)


### Examples

Some examples presented in the code at the bottom are taken from the class lecture slides and homework problems:
Assign workers A-D to tasks 1-4 minimizing the total cost.

|  | Task 1 | Task 2 | Task 3 | Task 4 |
| --- | --- | --- | ---  | --- |
| Worker A | 5 | 7 | 3 | 6 |
| Worker B | 6 | 6 | 5 | 4 |
| Worker C | 6 | 5 | 10 | 15 |
| Worker D | 9 | 7 | 6 | 7 |



This data is entered as matrix M and after running the algorithm, we get 
```
[[ 0  3  0  2]
 [ 1  2  2  0]
 [ 0  0  6 10]
 [ 1  0  0  0]]
 ```
The solution is A-3, B-4, C-1, and D-2.

Assign six employees to six tasks maximizing the total ratings.

|  | Task 1 | Task 2 | Task 3 | Task 4 | Task 5 | Task 6 |
| --- | --- | --- | ---  | --- | ---  | --- |
| Employee 1 | 6 | 8 | 5 | 9 | 6 | 7 |
| Employee 2 | 3 | 5 | 7 | 4 | 8 | 7 |
| Employee 3 | 4 | 8 | 6 | 8 | 9 | 7 |
| Employee 4 | 7 | 5 | 5 | 6 | 4 | 3 |
| Employee 5 | 9 | 7 | 3 | 3 | 7 | 5 |
| Employee 6 | 8 | 5 | 7 | 5 | 7 | 8 |



This data is entered as matrix N and since it is a maximization problem, we need to supply “max” as a parameter to our function. After running the algorithm, we get 
```
[[4 0 3 0 3 2]
 [6 2 0 4 0 1]
 [6 0 2 1 0 2]
 [0 0 0 0 2 3]
 [0 0 4 5 1 3]
 [1 2 0 3 1 0]]
 ```

There are multiple solutions in this case. 
One of them is E1-T4, E2-T5, E3-T2, E4-T3, E5-T1, E6-T6.
The advantage of our code over the linprog or simplex algorithm is that it gives the possibility of multiple solutions. For instance, E1-T2, E2-T3, E3-T5, E4-T4, E5-T1, E6-T6 is another solution.


### Limitations

Given the matrix and the type of the problem, the code can successfully run the Hungarian Algorithm and give a resulting equivalent matrix with zeros on entries where solutions are likely to occur.  However, since multiple solutions might exist and algorithms for finding the permutation sets of zeros is beyond the scope of this paper, we leave that up to the user.  Furthermore, matrices with non-integer or negative entries are ruled out by the code during type checking. Future work could involve matrix transformations that can allow floating point entries by offesting it to whole numbers. It can include finding one (or more) permutation sets of zeros thereby giving the optimized assignments rather than the matrix.






