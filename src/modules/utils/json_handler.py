import json
from config_reader import load_config


def find_input_attribute(input_attributes, input_element):
    # From the pre-loaded input attributes list, find the field name for the given element
    target_field = None

    for item in input_attributes:
        if input_element in item:
            target_field = item[input_element]['field']
            break

    if target_field:
        return target_field
    else:
        print(f"  {input_element} not found.")

def get_list_of_input_attributes():
    # From the input file layout, find the corresponding field that matches the src field

    input_json = load_config('input.json')

    # Ensure the 'input' key is in the data and it's a list
    if 'input' in input_json:
    # Extract the attributes
        attributes = [list(item.keys())[0] for item in input_json['input']]

        # Print the attributes
        return attributes 