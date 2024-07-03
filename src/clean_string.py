def convert_numeric_strings_to_numbers(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_numeric_strings_to_numbers(value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = convert_numeric_strings_to_numbers(item)
    elif isinstance(data, str):
        cleaned_data = data.strip().replace("$", "").replace(",", "")
        if cleaned_data.isdigit():
            return int(cleaned_data)
        elif cleaned_data.replace(".", "").isdigit():
            return float(cleaned_data)
    return data