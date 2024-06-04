from llm_proxy import LlmProxy
from tqdm import tqdm
from string_formatting import (
    format_list_to_textlist,
    correct_llm_dictionary_output,
    parse_ingredients_between_recipes,
)

from printing_output_evaluation import _col_text


from llm_proxy import LlmProxy
import ast


def get_list_of_ailes(add_to_list: list = []) -> list:
    output_list = [
        "produce",
        "meat",
        "canned goods",
        "eggs, milk, yogurt, sour cream",
        "cheese",
        "cold cuts",
        "nuts",
        "spices",
    ]

    if add_to_list:
        if isinstance(add_to_list, str):
            add_to_list = [add_to_list]
        for item in add_to_list:
            output_list.append(item)

    return output_list


def llm_extract_recipe_names(llmObj: LlmProxy, text_with_recipes: str) -> list:

    ########################################################
    ########################################################
    ###############        STEP        #####################
    ########################################################
    #########        EXTRACT RECIPES         ###############
    ########################################################

    user_prompt_recipe_names = f"""
    From the list of recipes and ingredients between <>, perform the following tasks:

    1. Extract the titles of the recipes.
    2. Output the titles as a list of strings.

    List of recipes:
    <{text_with_recipes}>
    
    Output only the list of ingredients as a python list.
    Do not say anything else.
    """
    system_prompt_recipe_names = (
        "You are a concise inventory manager in a grocery store"
    )

    llm_response_recipe_names = llmObj.get_completion(
        system_prompt=system_prompt_recipe_names, user_prompt=user_prompt_recipe_names
    )

    return llm_response_recipe_names


def llm_categorize_ingredient_by_aile_extract_quantity(
    llmObj: LlmProxy, input_ingredient: str, textlist_of_ailes: str = ""
) -> str:

    if not textlist_of_ailes:
        list_of_ailes = get_list_of_ailes()
        string_before = "        - "
        string_after = ", "
        textlist_of_ailes = format_list_to_textlist(
            list_of_ailes, string_before, string_after
        )

    user_parse_categorize_ingredients = f"""

    Follow the instructions below to parse the information between <> and output a python dictionary:
    1. Extract the ingredient and enter it as a value under the key "ingredient".
    3. Extract the quantity and enter it as a value under the key "quantity".
    2. Associate the ingredient to one of the following categories and enter it as a value under the key "aile":
{textlist_of_ailes} 

    4. Output your response as a python dictionary with the keys:
        - "ingredient":
        - "quantity":
        - "aile":
        
    Information:
    <
    {input_ingredient}
    >
    
    Only output a python dictionary.
    Do not say anything else.
    
    """

    system_parse_categorize_ingredients = (
        "You are a useful and concise inventory manager in a grocery store."
    )

    llm_parse_categorize_ingredients = llmObj.get_completion(
        system_prompt=system_parse_categorize_ingredients,
        user_prompt=user_parse_categorize_ingredients,
    )
    key_names = ["ingredient", "quantity", "aile"]
    checked_llm_parse_categorize_ingredients = correct_llm_dictionary_output(
        llm_parse_categorize_ingredients, key_names
    )

    return checked_llm_parse_categorize_ingredients


def llm_sum_same_ingredients(llmObj, ingredients_aile):

    user_sum_ingredients = f"""

    Add the quantities of the following ingredients:
{ingredients_aile} 

    Output your response in the same format as the list of ingredients.
    Do not say anything else.
    
    """

    system_sum_ingredients = (
        "You are a useful and concise inventory manager in a grocery store."
    )

    llm_sum_ingredients = llmObj.get_completion(
        system_prompt=system_sum_ingredients,
        user_prompt=user_sum_ingredients,
    )

    return llm_sum_ingredients


def pipeline_get_grocery_list(
    llmObj: LlmProxy, text_with_recipes: str
) -> tuple[str, str]:
    out_grocery_list = []

    string_recipes = llm_extract_recipe_names(llmObj, text_with_recipes)
    list_recipes = ast.literal_eval(string_recipes)

    print(
        _col_text(
            string="Extracting recipe names... ",
            fore_colour="black",
            back_colour="green",
        )
    )
    print(list_recipes)

    ingredients_text = parse_ingredients_between_recipes(
        text_with_recipes, list_recipes
    )
    print(
        _col_text(
            string="Extracting ingredients... ",
            fore_colour="black",
            back_colour="green",
        )
    )

    print(ingredients_text)

    list_of_ailes = get_list_of_ailes()
    string_before = "        - "
    string_after = ", "
    textlist_of_ailes = format_list_to_textlist(
        list_of_ailes, string_before, string_after
    )

    print(
        _col_text(
            string="Categorizing ingredients by aile/ creating dictionary ... ",
            fore_colour="black",
            back_colour="green",
        )
    )

    ingredients_list_dict = []
    for iIngredient in tqdm(ingredients_text):

        print(
            _col_text(
                string="  - working on ingredient: ",
                fore_colour="yellow",
                back_colour="black",
            )
        )
        print(iIngredient)

        ingredient = llm_categorize_ingredient_by_aile_extract_quantity(
            llmObj, iIngredient, textlist_of_ailes
        )
        eval_ingredient = ast.literal_eval(ingredient)
        ingredients_list_dict.append(eval_ingredient)

        print(
            _col_text(
                string="  - output: ",
                fore_colour="green",
                back_colour="black",
            )
        )
        print(ingredient)

    print(
        _col_text(
            string="Adding together same ingredients in each category... ",
            fore_colour="black",
            back_colour="green",
        )
    )

    out_grocery_list = ""
    for aile in list_of_ailes:

        print(
            _col_text(
                string="  - Aile:",
                fore_colour="green",
                back_colour="black",
            )
            + _col_text(
                string=f"{aile}",
                fore_colour="black",
                back_colour="blue",
            )
        )

        ingredients_aile = ""
        for i in ingredients_list_dict:
            if i["aile"] == aile:
                ingredients_aile += "{} {} \n".format(i["quantity"], i["ingredient"])
        if ingredients_aile.strip():

            grouped_ingredients_aile = llm_sum_same_ingredients(
                llmObj, ingredients_aile
            )

            out_grocery_list += f"** {aile} **: \n"
            out_grocery_list += "{} \n".format(grouped_ingredients_aile)

            print(
                _col_text(
                    string="  - Before sum:",
                    fore_colour="yellow",
                    back_colour="black",
                )
            )

            print(ingredients_aile)

            print(
                _col_text(
                    string="  - After sum:",
                    fore_colour="yellow",
                    back_colour="black",
                )
            )

            print(grouped_ingredients_aile)

            print("")

    return out_grocery_list, format_list_to_textlist(list_recipes)


def main():
    from _file_paths import get_latest_file
    from _file_read_write import read_file

    llmObj = LlmProxy("groq")

    debugmode = True

    if debugmode:

        ingredients_string_string_list_dict_string = read_file(
            "./src/text_list_dicts_ingredients.txt"
        )

        ingredients_string_list_dict_string = ast.literal_eval(
            ingredients_string_string_list_dict_string
        )

        ingredients_list_dict = ast.literal_eval(ingredients_string_list_dict_string)

        list_of_ailes = get_list_of_ailes()

    else:

        input_week_path, input_week_name = get_latest_file()
        input_week_path_name = input_week_path + input_week_name
        text_with_recipes = read_file(input_week_path_name)

        grocery_list = pipeline_get_grocery_list(llmObj, text_with_recipes)

        print("output from grocery list:")
        print(grocery_list)

        ingredients_list_dict = grocery_list

    ingredients_list = ""
    for aile in list_of_ailes:

        ingredients_aile = ""
        for i in ingredients_list_dict:
            if i["aile"] == aile:
                ingredients_aile += "{} {} \n".format(i["quantity"], i["ingredient"])
        if ingredients_aile.strip():
            print("################################")
            print("Before sum:")
            print(ingredients_aile)
            grouped_ingredients_aile = llm_sum_same_ingredients(
                llmObj, ingredients_aile
            )
            print("After sum:")
            print(grouped_ingredients_aile)

            print("")

            ingredients_list += f"** {aile} **: \n"
            ingredients_list += "{} \n".format(grouped_ingredients_aile)

        # # print(aile)
        # textlist_ingredients_grouped = [
        #     "{} {} \n".format(i["quantity"], i["ingredient"])
        #     for i in ingredients_list_dict
        #     if i["aile"] == aile
        # ]
        # print(textlist_ingredients_grouped)
        # ingredients_list.append()
    # print(ingredients_list)
    pass


if __name__ == "__main__":
    main()
