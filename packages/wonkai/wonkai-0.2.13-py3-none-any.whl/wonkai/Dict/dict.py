def flatten_dict(d, parent_key='', sep='___'):
    flattened = {}
    for key, value in d.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            flattened.update(flatten_dict(value, new_key, sep=sep))
        else:
            flattened[new_key] = value
    return flattened

def deflatten_dict(d, sep='___'):
    def set_nested_item(dictionary, keys, value):
        for key in keys[:-1]:
            dictionary = dictionary.setdefault(key, {})
        dictionary[keys[-1]] = value

    deflattened = {}
    for key, value in d.items():
        keys = key.split(sep)
        set_nested_item(deflattened, keys, value)

    return deflattened
