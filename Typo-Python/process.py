async def process_object(obj, indent_level=1, indent=2):
    indent_spaces = ' ' * (indent_level * indent)
    type_properties = []

    for key, value in obj.items():
        if isinstance(value, dict):
            nested_type = process_object(value, indent_level + 1)
            type_properties.append(f"{indent_spaces}{key}: {nested_type};")
        elif isinstance(value, list):
            if value and isinstance(value[0], str):
                type_properties.append(
                    f"{indent_spaces}{key}: {'Array'}<{'string'}>;")
            else:
                value_type = type(value[0]).__name__
                type_properties.append(
                    f"{indent_spaces}{key}: {'Array'}<{value_type}>;")
        elif isinstance(value, str):
            type_properties.append(f"{indent_spaces}{key}: {'string'};")
        elif isinstance(value, int) or isinstance(value, float):
            type_properties.append(f"{indent_spaces}{key}: {'number'};")

    return f"{{\n{chr(10).join(type_properties)}\n{indent_spaces}}}"
