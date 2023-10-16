def generic_repr(obj: object):
    if hasattr(obj, "__slots__"):
        attrs = {s: getattr(obj, s) for s in obj.__slots__ if hasattr(obj, s)}
    else:
        attrs = obj.__dict__
    fields = ", ".join(f"{k}={v!r}" for k, v in attrs.items())
    return f"{type(obj).__name__}({fields})"
