goods = {}  # explored coordinates


def gridTraveler(row, col):
    key = (row, col)  # current coordinate
    if (key in goods):
        return goods[key]  # avoids exploring again
    if (row == 1 and col == 1):
        return 1
    if (not row or not col):
        return 0
    goods[key] = gridTraveler(row-1, col) + gridTraveler(row, col-1)
    return goods[key]


print(gridTraveler(18, 18))
