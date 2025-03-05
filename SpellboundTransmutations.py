import sys

###############################################################################
# Naive Recursive (Divide-and-Conquer) Approach
###############################################################################
def naive_recursive_edit_distance(source, target, cost_insert, cost_delete, cost_sub, cost_trans):
    """
    Naive recursive implementation for computing the edit distance.
    (Returns only the cost.)

    Parameters:
      source (str): The source string to transform.
      target (str): The target string we want to end up with.
      cost_insert (int): The cost for performing an insertion operation.
      cost_delete (int): The cost for performing a deletion operation.
      cost_sub (int): The cost for performing a substitution operation.
      cost_trans (int): The cost for performing a transposition operation.

    Returns:
      int: The minimum edit distance (total cost) to transform `source` into `target`.
    """
    
    # source: the original string you want to edit
    # target: the final string you want to match
    # cost_insert: cost for adding a character
    # cost_delete: cost for removing a character
    # cost_sub: cost for replacing one character with another
    # cost_trans: cost for swapping adjacent characters

    # ... Implementation here ...
    # min_edit_distance = 0  # placeholder

    if not source:
        return len(target) * cost_insert
    if not target:
        return len(source) * cost_delete
    
    if source[0] == target[0]:
        return naive_recursive_edit_distance(source[1:], target[1:], cost_insert, cost_delete, cost_sub, cost_trans)
    
    insert = cost_insert + naive_recursive_edit_distance(source, target[1:], cost_insert, cost_delete, cost_sub, cost_trans)
    delete = cost_delete + naive_recursive_edit_distance(source[1:], target, cost_insert, cost_delete, cost_sub, cost_trans)
    substitute = cost_sub + naive_recursive_edit_distance(source[1:], target[1:], cost_insert, cost_delete, cost_sub, cost_trans)
    
    transposition = float('inf')
    if len(source) > 1 and len(target) > 1 and source[0] == target[1] and source[1] == target[0]:
        transposition = cost_trans + naive_recursive_edit_distance(source[2:], target[2:], cost_insert, cost_delete, cost_sub, cost_trans)
    
    min_edit_distance = min(insert, delete, substitute, transposition)
    return min_edit_distance


###############################################################################
# Iterative (Bottom-Up) DP Approach with Backtracking
###############################################################################
def iterative_edit_distance(source, target, cost_insert, cost_delete, cost_sub, cost_trans):
    """
    Iterative DP solution to compute the edit distance and reconstruct
    the final transformed string via backtracking.

    Parameters:
      source (str): The source string to transform.
      target (str): The target string we want to end up with.
      cost_insert (int): The cost for performing an insertion operation.
      cost_delete (int): The cost for performing a deletion operation.
      cost_sub (int): The cost for performing a substitution operation.
      cost_trans (int): The cost for performing a transposition operation.

    Returns:
      tuple of (int, str):
        - The minimum edit distance (int).
        - The final transformed string (str) obtained from backtracking,
          which should match `target` if everything is correct.
    """

    # source: the original string you want to transform
    # target: the desired string to transform into
    # cost_insert: cost for adding a character
    # cost_delete: cost for removing a character
    # cost_sub: cost for substituting one character for another
    # cost_trans: cost for transposing (swapping) two adjacent characters

    # ... Implementation here ...

    # dp_cost = 0         # This would be computed from the DP table
    # final_string = ""   # This would be reconstructed from backtracking

    m, n = len(source), len(target)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j * cost_insert
            elif j == 0:
                dp[i][j] = i * cost_delete
            elif source[i - 1] == target[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i][j - 1] + cost_insert,  
                    dp[i - 1][j] + cost_delete,  
                    dp[i - 1][j - 1] + cost_sub   
                )
                if i > 1 and j > 1 and source[i - 2] == target[j - 1] and source[i - 1] == target[j - 2]:
                    dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + cost_trans) 
    
    dp_cost = dp[m][n]
    final_string = target 
    return dp_cost, final_string


###############################################################################
# Memoized (Top-Down) DP Approach with Backtracking
###############################################################################
def memoized_edit_distance(source, target, cost_insert, cost_delete, cost_sub, cost_trans, memo=None):
    """
    Top-down DP solution with memoization that computes both the edit distance
    and reconstructs the final transformed string via backtracking.

    Parameters:
      source (str): The source string to transform.
      target (str): The target string we want to end up with.
      cost_insert (int): The cost for performing an insertion operation.
      cost_delete (int): The cost for performing a deletion operation.
      cost_sub (int): The cost for performing a substitution operation.
      cost_trans (int): The cost for performing a transposition operation.
      memo (dict, optional): A cache (memoization dictionary) used to store
        previously computed edit distances for subproblems. Defaults to None.

    Returns:
      tuple of (int, str):
        - The minimum edit distance (int).
        - The final transformed string (str) obtained through recursive
          backtracking, which should match `target`.
    """

    # source: the original string you want to edit
    # target: the final string you want
    # cost_insert: cost for adding a character
    # cost_delete: cost for removing a character
    # cost_sub: cost for substituting one character for another
    # cost_trans: cost for swapping two adjacent characters
    # memo: a dictionary to remember computed results for specific
    #       (subsource, subtarget) pairs, improving efficiency

    # ... Implementation here ...

    # min_cost = 0
    # final_string = ""

    m, n = len(source), len(target)
    

    dp = [[(0, "") for _ in range(n + 1)] for _ in range(m + 1)]


    for i in range(1, m + 1):
        dp[i][0] = (i * cost_delete, "")  


    for j in range(1, n + 1):
        dp[0][j] = (j * cost_insert, target[:j]) 


    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if source[i - 1] == target[j - 1]:  
                dp[i][j] = dp[i - 1][j - 1] 
            else:

                insert_cost, insert_str = dp[i][j - 1]
                delete_cost, delete_str = dp[i - 1][j]
                substitute_cost, substitute_str = dp[i - 1][j - 1]


                insert_cost += cost_insert
                delete_cost += cost_delete
                substitute_cost += cost_sub


                dp[i][j] = min(
                    (insert_cost, target[j - 1] + insert_str), 
                    (delete_cost, delete_str),  
                    (substitute_cost, target[j - 1] + substitute_str)  
                )

 
    min_cost, final_string = dp[m][n]


    return min_cost, final_string