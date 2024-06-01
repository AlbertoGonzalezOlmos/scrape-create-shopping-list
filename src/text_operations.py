from _file_read_write import read_file, read_file_line_to_list
from _file_paths import get_latest_file
import ast


def _import_list_recipes(file_recpie_name: str) -> list:
    output_path, output_name = get_latest_file(file_recpie_name)
    file_path_name = output_path + output_name
    list_recipes = read_file(file_path_name)
    first_braket = list_recipes.find("[")
    list_recipes = list_recipes[first_braket:]
    return ast.literal_eval(list_recipes)


def trim_strings(string_recipes_ingredients: str, list_recipes: list) -> str:
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
    trimmed_text = trim_strings(list_string_recipes_ingredients, list_recipes)

    print((list_string_recipes_ingredients))

    pass


if __name__ == "__main__":
    main()
