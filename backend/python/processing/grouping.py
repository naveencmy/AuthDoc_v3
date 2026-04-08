def split_groups(blocks, gap_threshold=120):
    if not blocks:
        return []

    blocks = sorted(blocks, key=lambda b: b["y"])

    groups = []
    current = [blocks[0]]

    for i in range(1, len(blocks)):
        prev = blocks[i - 1]
        curr = blocks[i]

        if curr["y"] - prev["y"] > gap_threshold:
            groups.append(current)
            current = []

        current.append(curr)

    groups.append(current)

    return groups