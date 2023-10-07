# PEP 0616
def removeprefix(src: str, prefix: str) -> str:
    """
    Remove the prefix of a string.
    Using PEP-0616 implementation reference code.
    """
    if src.startswith(prefix):
        return src[len(prefix):]
    else:
        return src[:]

def removesuffix(src: str, suffix: str) -> str:
    """
    Remove the prefix of a string.
    Using PEP-0616 implementation reference code.
    """
    # suffix='' should not call self[:-0].
    if suffix and src.endswith(suffix):
        return src[:-len(suffix)]
    else:
        return src[:]