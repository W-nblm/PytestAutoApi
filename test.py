from typing import List


class Solution:
    def sortMatrix(self, grid: List[List[int]]) -> List[List[int]]:
        if len(grid) == 1:
            return grid
        n = len(grid)
        cp_grid = grid
        print(cp_grid)
        j = 0
        k = 1
        while n > 1:

            temp_j = []
            temp_k = []
            for i in range(n-1):
                temp_k.append(cp_grid[i][i + k])
                i += 1

            temp_k.sort(reverse=False)
            for i in range(n-1):
                cp_grid[i][i + k] = temp_k[i]
                i += 1



            for i in range(n):
                temp_j.append(cp_grid[i + j][i])
                i += 1

            temp_j.sort(reverse=True)
            for i in range(n):
                cp_grid[i + j][i ] = temp_j[i]
                i += 1
            j += 1
            k += 1
            n -= 1
        return cp_grid


# grid = [[1, 7, 3], [9, 8, 2], [4, 5, 6]]
# grid = [[0,1],[1,2]]
grid = [[-1,2,1],[0,3,-5],[0,2,1]]
if __name__ == "__main__":
    s = Solution()
    print(s.sortMatrix(grid))
# -1 2  1
# 0  3 -5
# 0  2  1

# 3  -5  1
# 2  1  2
# 0  0  -1