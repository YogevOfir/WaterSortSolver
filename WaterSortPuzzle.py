# WaterSortPuzzle.py
import bisect
from collections import Counter

class WaterSortPuzzle:
    def __init__(self, tubes, size, full, empty, colors):
        self.tubes = [tube[:] for tube in tubes]
        self.size = size
        self.full = full
        self.empty = empty
        self.colors = colors

    def is_solved(self):
        # check if there are self.colors tubes with 1 color and self.empty tubes are empty
        # return len([tube for tube in self.tubes if not tube]) == self.empty and len([tube for tube in self.tubes if len(set(tube)) == 1]) == self.colors
        return len([tube for tube in self.tubes if not tube]) == self.empty and len([tube for tube in self.tubes if len(set(tube)) == 1]) == self.colors



    def get_possible_moves(self):
        print(self.heuristic())
        # print(self.heur istic())
        moves = []
        seen_moves = set()

        for i, src in enumerate(self.tubes):
            if not src:
                continue
            top_color = src[-1]
            check_empty = False
            for j, dst in enumerate(self.tubes):
                if i != j:
                    if not dst and not check_empty:
                        count = 1
                        while (len(src) - 1 - count >= 0) and top_color == src[len(src) - 1 - count] and len(dst) + count < self.size:
                            count += 1
                        check_empty = True
                        
                        move = (i, j, count)
                    elif dst and dst[-1] == top_color and len(dst) < self.size:
                        count = 1
                        while (len(src) - 1 - count >= 0) and top_color == src[len(src) - 1 - count] and len(dst) + count < self.size:
                            count += 1

                        move = (i, j, count)
                    else:
                        continue

                    # Compute priority
                    priority = (-len(set(dst)), len(dst))
                    if move not in seen_moves:
                        moves.append(move)
                        seen_moves.add(move)

        return moves






    def execute_move(self, src_idx, dst_idx, count):
        new_tubes = [tube[:] for tube in self.tubes]
        for _ in range(count):
            new_tubes[dst_idx].append(new_tubes[src_idx].pop())
        return WaterSortPuzzle(new_tubes, self.size, self.full, self.empty, self.colors)



    def misplaced_colors(self):
        res = [0] * self.colors
        for i, tube in enumerate(self.tubes):
            if tube:
                # iterate from the bottom of the tube to the top
                for j in range(len(tube)-1):
                    color = tube[j]
                    while j + 1 < len(tube) and tube[j+1] == color:
                        j += 1
                        if j == len(tube) - 1:
                            break
                    res[color] += (self.size - j - 1) - (self.size - 1 - len(tube))
                    
        heuristic_value = sum(res)
                
        return heuristic_value





    def heuristic(self):
        mixed_tubes = 0
        complete_tubes = 0
        misplaced_colors = 0
        empty_tubes = 0

        for tube in self.tubes:
            if not tube:
                empty_tubes += 1
            elif len(set(tube)) == 1:
                if len(tube) == self.size:
                    complete_tubes += 1
            else:
                mixed_tubes += 1
                misplaced_colors += len(tube) - max(Counter(tube).values())

        heuristic_value = 4 * mixed_tubes + 2 * misplaced_colors - complete_tubes - 0.5 * empty_tubes 
        return heuristic_value