def strip(field: str):
    return field.strip()


def get_own_fields(class_):
    all_fields = class_.__fields__
    inherited_fields = set(class_.__base__.__fields__.keys())
    own_fields = {name: field for name, field in all_fields.items() if name not in inherited_fields}

    return own_fields
