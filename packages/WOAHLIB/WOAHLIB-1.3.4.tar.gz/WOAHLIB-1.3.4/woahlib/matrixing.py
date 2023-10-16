def scale_2d_list(lst, scale_factor):
    scaled_list = []

    # Scale the number of rows
    scaled_rows = len(lst) * scale_factor

    # Scale the number of columns
    scaled_columns = len(lst[0]) * scale_factor

    # Generate the scaled list
    for i in range(scaled_rows):
        scaled_list.append([0] * scaled_columns)

    # Copy the elements from the original list to the scaled list
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            for k in range(scale_factor):
                for l in range(scale_factor):
                    scaled_list[i*scale_factor+k][j*scale_factor+l] = lst[i][j]

    return scaled_list

def empty2d(height=10,width=10):
    """
    Make an empty 2d list
    
    Parameters:
        height (int): Amount of rows
        width (int): Length of the rows
    
    Returns:
        list: The 2d list generated
    """
    out = []
    for x in range(height):
        out.append([])
        for y in range(width):
            out[x].append(0)
    return out
def circle2d(matrix, center_x, center_y, radius, fill=False, fill_value=1):
    """
    Draw a circle in a 2D matrix using the Midpoint Circle Algorithm.

    Parameters:
        matrix (numpy.ndarray): The 2D matrix to draw the circle on.
        center_x (int): X-coordinate of the center of the circle.
        center_y (int): Y-coordinate of the center of the circle.
        radius (int): The radius of the circle.
        fill (bool): Whether to fill the circle or just draw its boundary.
        fill_value: Unsupported

    Returns:
        numpy.ndarray: The updated matrix with the circle drawn on it.
    """
    height = len(matrix)
    width = len(matrix[0])
    x = radius
    y = 0
    err = 0

    while x >= y:
        if center_x + x < width and center_y + y < height:
            matrix[center_y + y][ center_x + x] = fill_value
        if center_x + y < width and center_y + x < height:
            matrix[center_y + x][ center_x + y] = fill_value
        if center_x - y >= 0 and center_y + x < height:
            matrix[center_y + x][ center_x - y] = fill_value
        if center_x - x >= 0 and center_y + y < height:
            matrix[center_y + y][ center_x - x] = fill_value
        if center_x - x >= 0 and center_y - y >= 0:
            matrix[center_y - y][ center_x - x] = fill_value
        if center_x - y >= 0 and center_y - x >= 0:
            matrix[center_y - x][ center_x - y] = fill_value
        if center_x + y < width and center_y - x >= 0:
            matrix[center_y - x][ center_x + y] = fill_value
        if center_x + x < width and center_y - y >= 0:
            matrix[center_y - y][ center_x + x] = fill_value

        if err <= 0:
            y += 1
            err += 2 * y + 1
        if err > 0:
            x -= 1
            err -= 2 * x + 1

    return matrix