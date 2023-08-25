from flask import Flask, render_template, request
import json
import asyncio

app = Flask(__name__)


async def process_object(obj, indent_level=1, indent=2):
    indent_spaces = ' ' * (indent_level * indent)
    type_properties = []

    for key, value in obj.items():
        if isinstance(value, dict):
            nested_type = await process_object(value, indent_level + 1)
            type_properties.append(f"{indent_spaces}{key}: {nested_type}")
        elif isinstance(value, list):
            if value and isinstance(value[0], str):
                type_properties.append(
                    f"{indent_spaces}{key}: {'Array'}<{'string'}>,")
            else:
                value_type = type(value[0]).__name__
                type_properties.append(
                    f"{indent_spaces}{key}: {'Array'}<{value_type}>,")
        elif isinstance(value, str):
            type_properties.append(f"{indent_spaces}{key}: {'string'},")
        elif isinstance(value, int) or isinstance(value, float):
            type_properties.append(f"{indent_spaces}{key}: {'number'},")

    return f"{{\n{chr(10).join(type_properties)}\n{indent_spaces}}}"


@app.route('/', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        try:
            object_data = json.loads(request.form.get('inputText'))
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
            type_definitions = loop.run_until_complete(
                process_object(object_data))
            # return f"Generated Types:\n\n{type_definitions}"
            return render_template('app.html', data_to_display=type_definitions)
        except Exception as e:
            return f"Error: {e}"
    return render_template('app.html')


if __name__ == '__main__':
    app.run(debug=True)
