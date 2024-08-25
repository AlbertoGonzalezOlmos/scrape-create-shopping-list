from llm_proxy.initialize_provider import LlmProxy, TandemProxy
from tqdm import tqdm
from string_formatting import (
    format_list_to_textlist,
    correct_llm_dictionary_output,
    parse_ingredients_between_recipes,
)

from printing_output_evaluation import _col_text

from typing import Union
import ast
import asyncio


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


def llm_categorize_ingredient_by_aile_extract_quantity(
    llm_obj: Union[LlmProxy, TandemProxy],
    input_ingredient: str,
    textlist_of_ailes: str = "",
) -> str:

    if not textlist_of_ailes:
        list_of_ailes = get_list_of_ailes()
        string_before = "        - "
        string_after = ", "
        textlist_of_ailes = format_list_to_textlist(
            list_of_ailes, string_before, string_after
        )

    user_prompt_parse_categorize_ingredients = f"""

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

    system_prompt_parse_categorize_ingredients = (
        "You are a useful and concise inventory manager in a grocery store."
    )

    llm_prompt_parse_categorize_ingredients = llm_obj.get_completion(
        system_prompt=system_prompt_parse_categorize_ingredients,
        user_prompt=user_prompt_parse_categorize_ingredients,
    )
    key_names = ["ingredient", "quantity", "aile"]
    checked_llm_prompt_parse_categorize_ingredients = correct_llm_dictionary_output(
        llm_prompt_parse_categorize_ingredients, key_names
    )

    return checked_llm_prompt_parse_categorize_ingredients


def pipeline_get_grocery_list(
    llm_obj: Union[LlmProxy, TandemProxy], list_with_quantity_ingredients: list[dict]
) -> list:
    out_grocery_list = []

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

    for iIngredient in tqdm(list_with_quantity_ingredients):

        print(
            _col_text(
                string="  - working on ingredient: ",
                fore_colour="yellow",
                back_colour="black",
            )
        )
        print(iIngredient["ingredient"])

        aile = llm_categorize_ingredient_by_aile(
            llm_obj, iIngredient["ingredient"], textlist_of_ailes
        )
        out_grocery_list.append(
            {
                "quantity": iIngredient["quantity"],
                "ingredient": iIngredient["ingredient"],
                "aile": aile,
            }
        )
    return out_grocery_list


def pipeline_get_grocery_list_from_text(
    llm_obj: Union[LlmProxy, TandemProxy], text_with_recipes: str
) -> tuple[str, str]:
    out_grocery_list = []

    string_recipes = llm_extract_recipe_names(llm_obj, text_with_recipes)
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
            llm_obj, iIngredient, textlist_of_ailes
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
        print("\n")

    print(
        _col_text(
            string="Adding together same ingredients in each category... ",
            fore_colour="black",
            back_colour="green",
        )
    )
    print("\n")

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
                llm_obj, ingredients_aile
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
            print("\n")

    return out_grocery_list, format_list_to_textlist(list_recipes)


def get_text_of_llm_categorize_ingredient_by_aile(
    input_ingredient: str,
    textlist_of_ailes: str,
) -> tuple[str, str]:

    user_prompt_parse_categorize_ingredients = f"""

    Follow the instructions below to categorize the Ingredient between <> and output the corresponding aile:
    1. Associate the Ingredient between < and > to one of the Ailes between ''' and ''':
    
    Ingredient:
<
{input_ingredient}
>

    Ailes:
'''
{textlist_of_ailes} 
'''

    2. Output only the name of the aile.
        
    3. Do not say anything else.
    
    """

    system_prompt_parse_categorize_ingredients = (
        "You are a useful and concise inventory manager in a grocery store."
    )

    return (
        system_prompt_parse_categorize_ingredients,
        user_prompt_parse_categorize_ingredients,
    )


def get_text_llm_sum_same_ingredients(ingredients_aile: str) -> tuple[str, str]:

    user_prompt_sum_ingredients = f"""

    Sum the quantities of the same Ingredients between <>:
    
    Ingredients:
<
{ingredients_aile} 
>

    Output your response in the same format as the list of ingredients.
    Do not say anything else.
    
    """

    system_prompt_sum_ingredients = (
        "You are a useful and concise inventory manager in a grocery store."
    )

    return system_prompt_sum_ingredients, user_prompt_sum_ingredients


async def create_list_of_list_of_groceries_from_dict(
    llm_obj: Union[LlmProxy, TandemProxy],
    list_with_quantity_ingredients: list[dict],
) -> dict:

    list_of_ailes = get_list_of_ailes()
    string_before = "        - "
    string_after = ", "
    textlist_of_ailes = format_list_to_textlist(
        list_of_ailes, string_before, string_after
    )

    list_of_user_system_prompts_list_of_groceries = []
    for iIngredient in list_with_quantity_ingredients:
        list_of_user_system_prompts_list_of_groceries.append(
            get_text_of_llm_categorize_ingredient_by_aile(
                iIngredient["ingredient"],
                textlist_of_ailes,
            )
        )

    # print(list_of_user_system_prompts_list_of_groceries[0])

    # for system_prompt, user_prompt in list_of_user_system_prompts_list_of_groceries[:2]:
    #     print(user_prompt)
    #     print(system_prompt)
    #     print("\n")

    list_ingredients_sorted_ailes = await asyncio.gather(
        *[
            llm_obj.get_async_completion(
                system_prompt=system_prompt, user_prompt=user_prompt, queue_number=idx
            )
            for idx, (system_prompt, user_prompt) in enumerate(
                list_of_user_system_prompts_list_of_groceries
            )
        ]
    )

    out_list_dict_quant_ingredient_aile = {}
    for aile in list_of_ailes:
        for idx, iIngredient in enumerate(list_with_quantity_ingredients):
            list_ingredient_aile = []
            if list_ingredients_sorted_ailes[idx] == aile:
                list_ingredient_aile.append(
                    {
                        "quantity": iIngredient["quantity"],
                        "ingredient": iIngredient["ingredient"],
                    }
                )
        out_list_dict_quant_ingredient_aile[aile] = list_ingredient_aile
    return out_list_dict_quant_ingredient_aile


async def async_pipeline_get_grocery_list_from_dict(
    llm_obj: Union[LlmProxy, TandemProxy], list_with_quantity_ingredients: list[dict]
) -> list:

    print(
        _col_text(
            string="Categorizing ingredients by aile/ creating dictionary ... ",
            fore_colour="black",
            back_colour="green",
        )
    )

    list_of_ingredients_by_aile = await create_list_of_list_of_groceries_from_dict(
        llm_obj=llm_obj, list_with_quantity_ingredients=list_with_quantity_ingredients
    )

    return list_of_ingredients_by_aile

    print(
        _col_text(
            string="Adding together same ingredients in each category... ",
            fore_colour="black",
            back_colour="green",
        )
    )
    print("\n")

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
        for i in list_dict_quant_ing_aile:
            if i["aile"] == aile:
                ingredients_aile += "{} {} \n".format(i["quantity"], i["ingredient"])
        if ingredients_aile.strip():

            grouped_ingredients_aile = llm_sum_same_ingredients(
                llm_obj, ingredients_aile
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
            print("\n")

    return out_grocery_list


def get_week_number(week_title: str) -> str:
    uge_string = "uge"
    number_starts = week_title.lower().find(uge_string) + len(uge_string)
    week_number = week_title[number_starts : number_starts + 4].strip()
    out_week_number = week_number.replace(",", "")
    return out_week_number


async def main():

    tandem_llm = TandemProxy(model="llama-3.1-70b")

    quantity_ingredients_dict_path = "./noSubmit/example_list_scraped_ingredients.txt"
    with open(quantity_ingredients_dict_path, "r") as file:
        quantity_ingredients_dict = file.read()

    quant_ing_dict = ast.literal_eval(quantity_ingredients_dict[1:-1])
    grocery_list = await async_pipeline_get_grocery_list_from_dict(
        tandem_llm, quant_ing_dict
    )

    print(grocery_list)


if __name__ == "__main__":
    asyncio.run(main())
