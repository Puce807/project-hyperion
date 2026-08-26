def clean_val(val):
    # TODO: Remove duplicate code in pipeline
    if val in (None, "NOT_AVAILABLE") or str(val).strip() == "":
        return None
    if isinstance(val, bool) or isinstance(val, str):
        return val
    try:
        return float(val)
    except (ValueError, TypeError):
        return None
