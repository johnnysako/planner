from Planner import convert_numeric_strings_to_numbers


def test_string_integer_conversion():
    assert convert_numeric_strings_to_numbers("123") == 123


def test_string_float_conversion():
    assert convert_numeric_strings_to_numbers("123.45") == 123.45


def test_string_with_commas_integer_conversion():
    assert convert_numeric_strings_to_numbers("1,234") == 1234


def test_string_with_commas_float_conversion():
    assert convert_numeric_strings_to_numbers("1,234.56") == 1234.56


def test_string_with_commas_dollar_sign_float_conversion():
    assert convert_numeric_strings_to_numbers("$1,234.56") == 1234.56


def test_string_with_leading_trailing_spaces():
    assert convert_numeric_strings_to_numbers("  123  ") == 123
    assert convert_numeric_strings_to_numbers("  123.45  ") == 123.45
    assert convert_numeric_strings_to_numbers("  $1,234.56  ") == 1234.56


def test_non_numeric_string():
    assert convert_numeric_strings_to_numbers("abc") == "abc"


def test_list_of_strings():
    assert convert_numeric_strings_to_numbers(
        ["1", "2.5", "three", "4,000"]) == [1, 2.5, "three", 4000]


def test_dict_of_strings():
    assert convert_numeric_strings_to_numbers({
        "a": "1", "b": "2.5", "c": "three", "d": "4,000"
        }) == {
            "a": 1, "b": 2.5, "c": "three", "d": 4000}


def test_nested_structures():
    assert convert_numeric_strings_to_numbers({
        "a": ["1", "2.5", {"b": "3", "c": "4,000"}],
        "d": "5.678"
    }) == {
        "a": [1, 2.5, {"b": 3, "c": 4000}],
        "d": 5.678
    }
