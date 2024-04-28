from z3 import *

# (SUM, VOLT_AMOUNT)

KNOWN_GRID = [
    ([0, 0, 0, 0, 0], 4, 1),
    ([0, 0, 0, 1, 0], 4, 1),
    ([0, 0, 0, 1, 0], 4, 1),
    ([0, 1, 1, 1, 0], 4, 1),
    ([0, 0, 0, 0, 0], 4, 1),
    (4, 1), (4, 1), (4, 1), (4, 1), (4, 1)
]

s = Solver()

grid = [[Int(f"tile_{i}_{j}") for j in range(5)] for i in range(5)]

for i in range(5):
    for j in range(5):
        s.add(And(grid[i][j] >= 0, grid[i][j] <= 3))

for i in range(0, 5):
    (row, sum_row, amount_volts) = KNOWN_GRID[i]

    for j in range(0, 5):
        if row[j] > 0:
            s.add(grid[i][j] == row[j])
    
    s.add(Sum(grid[i]) == sum_row)
    s.add(
        And(
            AtLeast(
                grid[i][0] == 0, 
                grid[i][1] == 0, 
                grid[i][2] == 0, 
                grid[i][3] == 0, 
                grid[i][4] == 0, 
                amount_volts
            ),
            AtMost(
                grid[i][0] == 0, 
                grid[i][1] == 0, 
                grid[i][2] == 0, 
                grid[i][3] == 0, 
                grid[i][4] == 0, 
                amount_volts
            )
        )
    )

for i in range(5, 10):
    (sum_row, amount_volts) = KNOWN_GRID[i]
    s.add(
        Sum(
            grid[0][i - 5],
            grid[1][i - 5],
            grid[2][i - 5],
            grid[3][i - 5],
            grid[4][i - 5]
        ) == sum_row
    )

    s.add(
        And(
            AtLeast(
                grid[0][i - 5] == 0,
                grid[1][i - 5] == 0,
                grid[2][i - 5] == 0,
                grid[3][i - 5] == 0,
                grid[4][i - 5] == 0,
                amount_volts
            ),
            AtMost(
                grid[0][i - 5] == 0,
                grid[1][i - 5] == 0,
                grid[2][i - 5] == 0,
                grid[3][i - 5] == 0,
                grid[4][i - 5] == 0,
                amount_volts
            )
        )
    )

while s.check() == sat:
    model = s.model()
    solution = [[model[grid[i][j]].as_long() for j in range(5)] for i in range(5)]

    print("===> Solution:")
    for row in solution:
        print(row)

    s.add(Or([grid[i][j] != model[grid[i][j]].as_long() for i in range(5) for j in range(5)]))
