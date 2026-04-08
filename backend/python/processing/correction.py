from rapidfuzz import fuzz
import json


def load_names():
    try:
        with open("dictionaries/names.json") as f:
            return json.load(f)
    except:
        return []


def score_word(word, NAMES):
    best = 0
    for n in NAMES:
        score = fuzz.ratio(word, n)

        # length constraint
        if abs(len(word) - len(n)) <= 2:
            score += 5

        # substring bonus
        if word in n or n in word:
            score += 10

        best = max(best, score)

    return best


# ✅ FIXED VERSION
def correct_word(word, NAMES):
    best = word
    best_score = 0

    for n in NAMES:
        score = fuzz.ratio(word, n)

        if abs(len(word) - len(n)) <= 2:
            score += 5

        if word in n or n in word:
            score += 10

        if score > best_score:
            best_score = score
            best = n

    # 🔴 STRICT THRESHOLD (critical)
    if best_score > 80:
        return best

    return word

def split_merged_token(word, NAMES):
    matches = []

    for n in NAMES:
        if n in word:
            matches.append(n)
    if matches:
        return matches

    return [word]
def correct_line(line, NAMES):
    tokens = line.split()
    final = []

    for t in tokens:
        corrected = correct_word(t, NAMES)

        split_tokens = split_merged_token(corrected, NAMES)

        if not split_tokens:
            split_tokens = [corrected]

        final.extend(split_tokens)

    return final