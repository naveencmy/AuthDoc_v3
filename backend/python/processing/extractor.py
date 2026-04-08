from processing.correction import score_word


# -------------------------------
# NAME LINE DETECTION
# -------------------------------
def is_name_line(tokens, NAMES):
    if not tokens:
        return False

    scores = [score_word(t, NAMES) for t in tokens]

    max_score = max(scores)
    avg_score = sum(scores) / len(scores)

    # strong signal
    if max_score > 85:
        return True

    # moderate multi-token signal
    if avg_score > 60 and len(tokens) <= 4:
        return True

    return False


# -------------------------------
# CLUSTER BUILDING
# -------------------------------
def build_name_clusters(lines_tokens, NAMES):
    clusters = []
    current = []

    for tokens in lines_tokens:
        if is_name_line(tokens, NAMES):
            current.append(tokens)
        else:
            if current:
                clusters.append(current)
                current = []

    if current:
        clusters.append(current)

    return clusters


# -------------------------------
# UTILITIES
# -------------------------------
def flatten_cluster(cluster):
    words = []
    for line in cluster:
        words.extend(line)
    return words


def pick_best_surname(words, NAMES):
    best_word = None
    best_score = 0

    for w in words:
        score = score_word(w, NAMES)

        if score > best_score:
            best_score = score
            best_word = w

    return best_word if best_word else (words[0] if words else None)


def parse_name(words, NAMES):
    if not words:
        return None, None

    surname = pick_best_surname(words, NAMES)

    # remove duplicates + surname
    given = []
    for w in words:
        if w != surname and w not in given:
            given.append(w)

    return surname, " ".join(given) if given else None


def cluster_score(cluster, NAMES):
    words = flatten_cluster(cluster)
    if not words:
        return 0

    scores = [score_word(w, NAMES) for w in words]
    return sum(scores) / len(scores)


# -------------------------------
# FALLBACK EXTRACTION
# -------------------------------
def fallback_extraction(lines_tokens, NAMES):
    flat_words = [w for line in lines_tokens for w in line]

    # score words
    scored = [(w, score_word(w, NAMES)) for w in flat_words]

    # filter strong candidates only
    scored = [s for s in scored if s[1] > 70]

    if not scored:
        return empty_fields()

    # sort descending
    scored.sort(key=lambda x: x[1], reverse=True)

    # remove duplicates
    unique_words = []
    for w, _ in scored:
        if w not in unique_words:
            unique_words.append(w)

    if len(unique_words) < 2:
        return empty_fields()

    # split into two halves
    mid = len(unique_words) // 2

    groom_words = unique_words[:mid]
    bride_words = unique_words[mid:]

    groom_s, groom_g = parse_name(groom_words, NAMES)
    bride_s, bride_g = parse_name(bride_words, NAMES)

    return {
        "Groom_Surname": groom_s,
        "Groom_Given": groom_g,
        "Bride_Surname": bride_s,
        "Bride_Given": bride_g
    }


# -------------------------------
# MAIN EXTRACTION
# -------------------------------
def extract_fields(lines_tokens, NAMES):

    clusters = build_name_clusters(lines_tokens, NAMES)
    print("CLUSTERS:", clusters)

    if not clusters:
        return empty_fields()

    # rank clusters by name-likeness
    ranked = sorted(
        clusters,
        key=lambda c: cluster_score(c, NAMES),
        reverse=True
    )

    ranked = ranked[:2]

    # fallback if insufficient clusters
    if len(ranked) < 2:
        return fallback_extraction(lines_tokens, NAMES)

    # extract groom + bride
    groom_words = flatten_cluster(ranked[0])
    bride_words = flatten_cluster(ranked[1])

    groom_s, groom_g = parse_name(groom_words, NAMES)
    bride_s, bride_g = parse_name(bride_words, NAMES)

    fields = {
        "Groom_Surname": groom_s,
        "Groom_Given": groom_g,
        "Bride_Surname": bride_s,
        "Bride_Given": bride_g
    }

    print("FIELDS:", fields)
    return fields


# -------------------------------
# EMPTY STRUCTURE
# -------------------------------
def empty_fields():
    return {
        "Groom_Surname": None,
        "Groom_Given": None,
        "Bride_Surname": None,
        "Bride_Given": None
    }