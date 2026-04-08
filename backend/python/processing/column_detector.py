def get_left_column(blocks):
    # get all x values
    xs = [b["x"] for b in blocks]

    # compute median instead of max
    median_x = sorted(xs)[len(xs)//2]

    # left column = strictly left cluster
    left = [b for b in blocks if b["x"] < median_x * 0.6]

    return sorted(left, key=lambda b: b["y"])