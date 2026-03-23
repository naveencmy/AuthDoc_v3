def detect_columns(text_blocks):
    xs = [b["x"] for b in text_blocks]
    if not xs:
        return {"left": [], "right": []}
    midpoint = (min(xs) + max(xs)) / 2
    left = []
    right = []
    for block in text_blocks:
        if block["x"] < midpoint:
            left.append(block)
        else:
            right.append(block)
    return {
        "left": sorted(left, key=lambda b: b["y"]),
        "right": sorted(right, key=lambda b: b["y"])
    }

def group_paragraphs(blocks, gap=25):
    paragraphs = []
    current = []
    last_y = None
    for block in sorted(blocks, key=lambda b: b["y"]):
        if last_y is None:
            current.append(block)
        elif abs(block["y"] - last_y) < gap:
            current.append(block)
        else:
            paragraphs.append(current)
            current = [block]
        last_y = block["y"]
    if current:
        paragraphs.append(current)
    return paragraphs

def detect_signatures(blocks):
    if not blocks:
        return []
    max_y = max(b["y"] for b in blocks)
    threshold = max_y * 0.8
    return [b for b in blocks if b["y"] > threshold]
    
def analyze_layout(text_blocks):

    columns = detect_columns(text_blocks)
    left_paragraphs = group_paragraphs(columns["left"])
    right_paragraphs = group_paragraphs(columns["right"])
    signatures = detect_signatures(text_blocks)

    return {
        "left_column": columns["left"],
        "right_column": columns["right"],
        "left_paragraphs": left_paragraphs,
        "right_paragraphs": right_paragraphs,
        "signatures": signatures
    }