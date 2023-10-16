import re

def snake_to_camel(key):
    components = key.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def keys_to_camel_case(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            new_key = snake_to_camel(key)
            new_value = keys_to_camel_case(value)
            new_data[new_key] = new_value
        return new_data
    elif isinstance(data, list):
        return [keys_to_camel_case(item) for item in data]
    else:
        return data




def camel_to_snake(key):
    pattern = re.compile(r'(.)([A-Z][a-z]+)')
    return pattern.sub(r'\1_\2', key).lower()

def keys_to_snake_case(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            new_key = camel_to_snake(key)
            new_value = keys_to_snake_case(value)
            new_data[new_key] = new_value
        return new_data
    elif isinstance(data, list):
        return [keys_to_snake_case(item) for item in data]
    else:
        return data

