import uuid


def to_class(new_object, response, all_attr=True):
    for key, value in response.items():
        if hasattr(new_object, key) or all_attr:
            setattr(new_object, key, value)
    return new_object


def is_valid_uuid(s):
    try:
        uuid.UUID(s)
        return True
    except ValueError:
        return False
