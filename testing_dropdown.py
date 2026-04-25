import cv2
import numpy as np


'''def find_connected_components(adj_matrix):
    visited = set()
    components = []

    def dfs(node, component):
        visited.add(node)
        component.append(node)

        for neighbor, is_connected in enumerate(adj_matrix[node]):
            if is_connected and neighbor not in visited:
                dfs(neighbor, component)

    for node in range(len(adj_matrix)):
        if node not in visited:
            component = []
            dfs(node, component)
            components.append(component)

    return components'''


def dfs(grid, visited, row, col):
    if (
            row < 0 or col < 0 or
            row >= len(grid) or col >= len(grid[0]) or
            visited[row][col] or grid[row][col] == 0
    ):
        return 0

    visited[row][col] = True
    size = 1

    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        size += dfs(grid, visited, row + dr, col + dc)

    return size


def find_largest_island(grid):
    visited = [[False for _ in row] for row in grid]
    largest_island_size = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if not visited[i][j] and grid[i][j] == 1:
                island_size = dfs(grid, visited, i, j)
                largest_island_size = max(largest_island_size, island_size)

    return largest_island_size


# Example usage
def test_drop(image):
    #image = cv2.imread("test/images/img.png",0)
    #image = image[380:430,340:380]
    #image = image / 255.0
    cv2.imshow("image",image)
    cv2.waitKey(0)
    _,thresh= cv2.threshold(image,127,255,cv2.THRESH_BINARY)

    cv2.imshow("thresh",thresh)
    cv2.waitKey(0)
    thresh = thresh / 255.0
    image_array = np.array(thresh)
    reverse_image_array = 1- image_array
    for i in range(0,len(reverse_image_array)):
        for j in range(0,len(reverse_image_array[i])):
            print(reverse_image_array[i][j],end=" ")
        print()

    '''reverse_image_array = np.zeros((50, 40))
    for i in range(0,len(reverse_image_array)):
        for j in range(0,len(reverse_image_array[i])):
            print(reverse_image_array[i][j],end=" ")
        print()'''
    print(reverse_image_array.shape)
    print(reverse_image_array)

    '''graph = {
        1: [2, 3],
        2: [1, 3],
        3: [1, 2],
        4: [5],
        5: [4]
    }'''

    '''components = find_connected_components(reverse_image_array)
    for idx, component in enumerate(components, start=1):
        print(f'Island {idx} has {len(component)} nodes: {component}')'''
    largest_island_size = find_largest_island(reverse_image_array)
    print(f"The largest island has a size of {largest_island_size}")
    return largest_island_size