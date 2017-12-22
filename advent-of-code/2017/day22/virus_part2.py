# --- Day 22: Sporifica Virus ---

import numpy as np
from operator import add, sub
from time import time, sleep
from typing import Any, Dict, Callable, Tuple


Grid = np.ndarray
Nav = Dict[int, Callable[[Any, Any], Any]]
T = Tuple[int, int, int]


def print_grid(burst: int, grid: Grid, y: int, x: int) -> None:
    binary_to_pixels = {0: ' . ', 1: ' W ', 2: ' # ', 3: ' F ',
                        4: '[.]', 5: '[W]', 6: '[#]', 7: '[F]'}
    grid[y][x] += 4

    print('\nBurst {}'.format(burst))
    for row in grid:
        print(''.join([binary_to_pixels[n] for n in row]))


def move(y: int, x: int, d: int) -> Tuple[int, int]:
    if d == 0:
        return y - 1, x
    elif d == 1:
        return y, x + 1
    elif d == 2:
        return y + 1, x
    return y, x - 1


def main():
    bursts = 10000000
    grid_size = bursts // 500
    nav = {0: sub, 1: lambda d, n: d, 2: add, 3: lambda d, n: d + 2}
    pixels_to_binary = {'#': 2, '.': 0}

    with open('input.txt', 'r') as fr:
        grid = np.array([[pixels_to_binary[ch] for ch in line.strip()]
                        for line in fr.readlines()])

    # Extend grid
    grid = np.lib.pad(grid, (grid_size, grid_size),
                      'constant', constant_values=(0, 0))
    y, x = [x // 2 for x in grid.shape]
    infections, d = 0, 0
    start = time()

    for burst in range(1, bursts + 1):
        d = nav[grid[y][x]](d, 1) % 4
        state = (grid[y][x] + 1) % 4
        grid[y][x] = state
        infections += int(state == 2)
        y, x = move(y, x, d)

    # print_grid(burst, np.copy(grid), y, x)
    print('Number of bursts that caused an infection is {}'.format(infections))
    print('Finished in {:.4f}'.format(time() - start))


if __name__ == '__main__':
    main()