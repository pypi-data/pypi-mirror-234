import typing as t


def get_message_recursive(e: Exception) -> t.List[str]:
    result = []

    head_e = e
    for _ in range(32):  # against infinite loops
        result.append(f"{head_e.__class__.__name__}: {head_e}")
        if head_e.__cause__ is not None:
            head_e = head_e.__cause__
        else:
            break

    return result
