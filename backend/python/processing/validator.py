def validate(fields):
    result = {}

    for k, v in fields.items():
        if not v:
            status = "MISSING"
        elif len(v) < 3:
            status = "FLAGGED"
        else:
            status = "VERIFIED"

        result[k] = {
            "value": v,
            "status": status
        }

    return result


def confidence(fields):
    total = len(fields)
    filled = sum(1 for f in fields.values() if f["value"])
    return round(filled / total, 2)