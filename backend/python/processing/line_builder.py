def build_lines(blocks, y_threshold=25):
    if not blocks:
        return []

    blocks = sorted(blocks, key=lambda b: (b["y"], b["x"]))

    lines = []
    current = [blocks[0]]

    for b in blocks[1:]:
        if abs(b["y"] - current[-1]["y"]) <= y_threshold:
            current.append(b)
        else:
            lines.append(current)
            current = [b]

    lines.append(current)

    final_lines = []
    for line in lines:
        sorted_line = sorted(line, key=lambda x: x["x"])
        text = " ".join([w["text"] for w in sorted_line])
        final_lines.append(text)

    print("LINES:", final_lines)
    return final_lines