import itertools


def _powerset(iterable):
    # Shamelessly copied from https://docs.python.org/2/library/itertools.html#recipes
    
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


def solve(allowed_step_sizes, target_distance, verbose=False):
    """
        Given a list of allowed step sizes and a target distance, return the number of different ways in which steps can be taken to exactly cover the
        desired distance (without walking backwards). Returns -1 if an error occurred due to invalid input.
    """
    
    INPUT_ERROR = -1
    
    # Avoid miscounting down the line
    allowed_step_sizes = set(allowed_step_sizes)
    
    # Basic sanity checks
    allowed_step_sizes = [x for x in allowed_step_sizes if x != 0]
    
    if not allowed_step_sizes:
        print("Please provide a list of allowed step sizes.")
        return INPUT_ERROR
    
    for step_size in allowed_step_sizes:
        if type(step_size) != int or step_size < 0:
            print("Please only use positive integers for step sizes.")
            return INPUT_ERROR
    
    if target_distance < 1:
        print("Please enter a positive target distance.")
        return INPUT_ERROR
    
    # I cannot take any more actions than this no matter what
    max_number_of_actions = target_distance // min(allowed_step_sizes)
    
    candidate_solutions = set()

    # Take each possible combination of the highest number of actions, e.g. (m1, m1, ... m1) (n times), (m1, m1, ... m2) (n times), ... (mk, mk, ... mk) (n times)
    for combination in itertools.combinations_with_replacement(allowed_step_sizes, max_number_of_actions):

        # For each of these combinations, take the powerset e.g. (), (m1), (m1, m1), ... (m1, m1, ... m1) (n times) for the first combination
        # This is awfully inefficient, but brute force is the best force where the brain doesn't reach
        for pow_set in _powerset(combination):
            candidate_solutions.add(pow_set)

    num_solutions = 0
    for candidate_solution in candidate_solutions:
        if sum(candidate_solution) == target_distance:

            # Try each powerset; if the sum is right, then each unique permutation of it is also another solution
            num_solutions += len(set(itertools.permutations(candidate_solution)))
            
            if verbose:
                for solution in set(itertools.permutations(candidate_solution)):
                    print(solution)

    return num_solutions


def _run_tests():
    tests = [
        # allowed step sizes - target distance - expected result
        
        # Simple cases
        ([1], 1, 1), 
        ([1], 3, 1),
        ([2, 4], 6, 3),
        
        # Invalid inputs
        ([], 1, -1),  
        ([1], 0, -1), 
        ([1, 2, 0.5], 10, -1),
        ([0], 1, -1),
        
        # No solutions
        ([2], 1, 0), 
        ([2, 4, 6], 13, 0),

        # Example provided on Workplace
        ([1, 2], 2, 2), 
        
        # Same example with repeated input
        ([1, 1, 2, 2, 1, 2, 1, 2], 2, 2) 
    ]
    
    for test in tests:
        assert(solve(test[0], test[1]) == test[2])
        
    print("All tests completed successfully.")
    

if __name__ == "__main__":
    # Run tests if interested
    # _run_tests()
    
    allowed_step_sizes = [1, 2]
    target_distance = 5
    
    print(f"Number of different solutions for {allowed_step_sizes} with a target of {target_distance}: {solve(allowed_step_sizes, target_distance, verbose=True)}")