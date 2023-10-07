def dict_no_empty(original_dict: dict):
    return {k: v for (k, v) in original_dict.items() if v is not None}
