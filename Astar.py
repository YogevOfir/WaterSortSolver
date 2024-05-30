# Astar.py
import heapq


def solve(puzzle, max_queue_size = 10000):
    priority_queue = []
    start_state_id = 0
    start_gn = 0
    start_fn = start_gn + puzzle.heuristic()
    heapq.heappush(priority_queue, (start_fn, start_state_id, puzzle, [], start_gn))
    seen = set([tuple(tuple(tube) for tube in puzzle.tubes)])
    state_id = 1
    iterations = 0

    while priority_queue:
        iterations += 1
        fn, _, current_puzzle, path, gn = heapq.heappop(priority_queue)
        if current_puzzle.is_solved():
            print("Num of iterations :", iterations)
            return path, len(path), current_puzzle

        for move in current_puzzle.get_possible_moves():
            next_state = current_puzzle.execute_move(*move)
            next_state_tuple = tuple(tuple(tube) for tube in next_state.tubes)
            if next_state_tuple not in seen:
                seen.add(next_state_tuple)
                next_gn = gn + 1
                next_fn = next_gn + next_state.heuristic()

                # Push the new state into the queue
                heapq.heappush(priority_queue, (next_fn, state_id, next_state, path + [move], next_gn))
                state_id += 1
                
                # If the size of the priority queue exceeds the maximum allowed size, pop the element with the highest heuristic
                while len(priority_queue) > max_queue_size:
                    priority_queue = heapq.nsmallest(2500, priority_queue)
                    heapq.heapify(priority_queue)
                # print(len(priority_queue))

    return None, -1, None

