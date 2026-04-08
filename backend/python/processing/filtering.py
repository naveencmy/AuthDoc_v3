def is_valid_name_token(word):
    word = word.lower().replace(",", "").replace(".", "")

    if len(word) < 3:
        return False

    # reject noise
    noise = {
        "mariage", "volume", "case", "feuillet",
        "n", "no", "fo"
    }

    if word in noise:
        return False

    # reject numbers
    if any(char.isdigit() for char in word):
        return False

    return True


def filter_blocks(blocks):
    return [
        b for b in blocks
        if is_valid_name_token(b["text"])
    ]