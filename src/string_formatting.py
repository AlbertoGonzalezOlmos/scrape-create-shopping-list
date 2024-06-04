from _file_read_write import read_file, read_file_line_to_list
from _file_paths import get_latest_file
import ast
import io


def parse_ingredients_between_recipes(input_text: str, recipes_list: list) -> str:

    idx_recipes_in_text = []
    ingredients_text = ""
    for recipe_title in recipes_list:
        idx_recipes_in_text.append(input_text.find(recipe_title))

    num_recipes = len(idx_recipes_in_text)
    start_scan = 0
    end_scan = 0
    for count_idx, idx_recipe in enumerate(idx_recipes_in_text):
        len_recipe_name = len(recipes_list[count_idx])
        start_scan = end_scan + len_recipe_name
        if count_idx < num_recipes - 1:
            end_scan = idx_recipes_in_text[count_idx + 1]
        else:
            end_scan = len(input_text)
        ingredients_text += input_text[start_scan:end_scan]

    ingredients_text_out = _extract_only_ingredients(ingredients_text)
    return ingredients_text_out


def _extract_only_ingredients(input_text: str) -> list:
    output_list_ingredients = []
    s = io.StringIO(input_text)
    for line in s:
        if line.strip():
            if line[0].isdigit():
                output_list_ingredients.append(line)
    return output_list_ingredients


def correct_llm_dictionary_output(
    llm_parse_categorize_ingredients: str, key_names: list
) -> str:
    checked_llm_parse_categorize_ingredients = ""
    keys_found_position = []
    for idx_keys in key_names:
        position_key = llm_parse_categorize_ingredients.find(idx_keys)
        keys_found_position.append(position_key)

    X = key_names
    Y = keys_found_position
    key_names_reordered = [x for _, x in sorted(zip(Y, X))]

    num_keys = len(key_names)
    for idx, key_name in enumerate(key_names_reordered):
        key_start_pos = keys_found_position[idx]
        if key_start_pos < 0:
            value = ""
        else:
            value_start = key_start_pos + len(key_name) + len('": "')
            if idx < num_keys - 1:
                next_key_start = keys_found_position[idx + 1]
                value_end = next_key_start - len('", "')
                value = '"{}", '.format(
                    llm_parse_categorize_ingredients[value_start:value_end]
                )
            else:
                value_end = len(llm_parse_categorize_ingredients) - len('"}')
                value = '"{}"'.format(
                    llm_parse_categorize_ingredients[value_start:value_end]
                )

        checked_llm_parse_categorize_ingredients += f'"{key_name}": {value}'
    checked_llm_parse_categorize_ingredients = "{%s}" % (
        checked_llm_parse_categorize_ingredients
    )
    return checked_llm_parse_categorize_ingredients


def format_list_to_textlist(
    list_of_ailes: str, string_before: str = "", string_after: str = ""
) -> str:
    output_textlist = ""
    for aile_item in list_of_ailes:
        output_textlist += string_before + aile_item + string_after + " \n"

    return output_textlist


def _import_list_recipes(file_recpie_name: str) -> list:
    output_path, output_name = get_latest_file(file_recpie_name)
    file_path_name = output_path + output_name
    list_recipes = read_file(file_path_name)
    first_braket = list_recipes.find("[")
    list_recipes = list_recipes[first_braket:]
    return ast.literal_eval(list_recipes)


def extract_strings_from_list(
    string_recipes_ingredients: str, list_recipes: list
) -> str:
    strings_to_trim = list_recipes.append("INGREDIENSER")
    trimmed_ingredients = ""
    for rec_ing_line in string_recipes_ingredients:
        if rec_ing_line not in strings_to_trim:
            print(rec_ing_line)

    #         trimmed_ingredients.
    # return trimmed_ingredients


def main():
    string_recipes = "out_extractRecipeNames"
    list_recipes = _import_list_recipes(string_recipes)

    input_file = "w28_plan.txt"
    input_Ingredients_path, _ = get_latest_file()
    path_recipes_ingredients = input_Ingredients_path + input_file

    # string_recipes_ingredients = read_file(path_recipes_ingredients)
    list_string_recipes_ingredients = read_file_line_to_list(path_recipes_ingredients)
    trimmed_text = extract_strings_from_list(
        list_string_recipes_ingredients, list_recipes
    )

    print((list_string_recipes_ingredients))

    pass


if __name__ == "__main__":
    main()
