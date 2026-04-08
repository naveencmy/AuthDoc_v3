import re


def normalize_lines(lines):
    cleaned = []

    for line in lines:
        line = line.lower()
        line = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ\s]", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        cleaned.append(line)

    print("NORMALIZED:", cleaned)
    return cleaned