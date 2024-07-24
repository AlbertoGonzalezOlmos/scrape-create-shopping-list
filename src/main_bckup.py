# from wrap_openai import openai_client_initialize, prompt_chain


def main():

    from file_paths import get_latest_file, create_output_path

    from file_read_write import read_file, write_file, write_pdf
    from llm_proxy import LlmProxy

    llmObj = LlmProxy("groq")

    ########################################################
    ########################################################
    ###############        STEP        #####################
    ########################################################
    ######### GET WEEK RECIPES + INGREDIENTS ###############
    ########################################################

    input_week_path, input_week_name = get_latest_file()
    input_week_path_name = input_week_path + input_week_name
    input_week_text = read_file(input_week_path_name)

    ########################################################
    ########################################################
    ###############        STEP        #####################
    ########################################################
    #########        EXTRACT RECIPES         ###############
    ########################################################

    user_prompt_recipe_names = f"""

    From the list of recipes and ingredients between <>, perform the following tasks: \

    1. Extract the titles of the recipes.
    2. Output the titles as a list of strings.
    
    

    List of recipes:
    <{input_week_text}>
    
    Output only the list of ingredients.
    Do not output anything else.
    
    """
    system_prompt_recipe_names = (
        "You are a useful and concise inventory manager in a grocery store"
    )

    llm_response_recipe_names = llmObj.get_completion(
        system_prompt=system_prompt_recipe_names, user_prompt=user_prompt_recipe_names
    )

    output_recipe_names_name = "out_extract_recipe_names"

    output_recipe_names_path = create_output_path(output_recipe_names_name)
    output_recipe_names_path_name = (
        output_recipe_names_path + input_week_name[:-4] + "_recipe_names"
    )

    print(f"output path + name: {output_recipe_names_path_name}")

    print(f" - List of recipes: \n {llm_response_recipe_names}")

    write_file(output_recipe_names_path_name, llm_response_recipe_names)

    ########################################################
    ########################################################
    ###############        STEP        #####################
    ########################################################
    ########        GROUP INGREDIENTS         ##############
    ########################################################

    # output_path, output_name = get_latest_file(output_response_path, extension="txt")

    # output_path_name = output_path + output_name

    user_prompt_group_ingredients = f"""

    From the list of ingredients between <>, perform the following tasks: \

    1. make a shopping list grouping the type of ingredient using the following categories: \
    - produce. \
    - meat. \
    - canned goods. \
    - eggs, milk, yogurt, sour cream. \
    - cheese. \
    - cold cuts. \
    - nuts. \
    - spices. \
    - 
    
    2. add up the quantities of the same type of ingredient. \

    If there are no ingredients in one category, do not list the category in the shopping list.

    Output only the shopping list.

    List of ingredients:
    <
    {input_week_text}
    >
    """

    system_prompt_group_ingredients = (
        "You are a useful and concise inventory manager in a grocery store"
    )

    llm_response_group_ingredients = llmObj.get_completion(
        system_prompt=system_prompt_group_ingredients,
        user_prompt=user_prompt_group_ingredients,
    )

    output_group_ingredients_name = "out_group_ingredients"

    output_group_ingredients_path = create_output_path(output_group_ingredients_name)

    output_group_ingredients_path_name = (
        output_group_ingredients_path + input_week_name[:-4] + "_grouped_ingredients"
    )

    print(f"output path + name: {output_group_ingredients_path_name}")

    print(f" - Group ingredients: \n {llm_response_group_ingredients}")

    write_file(output_group_ingredients_path_name, llm_response_group_ingredients)

    ########################################################
    ########################################################
    ###############        STEP        #####################
    ########################################################
    ##########          WRITE PDF           ################
    ########################################################

    output_PDF = "out_group_ingredients_PDF"

    output_PDF_path = create_output_path(output_PDF)

    input_group_ingredients_text = read_file(output_group_ingredients_path_name)

    output_PDF_path_name = (
        output_PDF_path + input_week_name[:-4] + "_grouped_ingredients"
    )

    print(f" - output path for PDF: {output_PDF_path}")

    write_pdf(input_group_ingredients_text, output_PDF_path_name)

    ##################################################
    ##################################################
    ##################################################
    ##################################################
    ##################################################
    ##################################################
    ##################################################

    from file_paths import get_latest_file, create_output_path

    from file_read_write import read_file, write_file, write_pdf

    from llm_proxy import LlmProxy
    import ast

    llmObj = LlmProxy("groq")

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

        string_recipes = llm_extract_recipe_names(llmObj, text_with_recipes)
        list_recipes = ast.literal_eval(string_recipes)

        print("Recipe names: ")
        print(list_recipes)

        ingredients_text = parse_ingredients_between_recipes(
            text_with_recipes, list_recipes
        )
        print("List of ingredients: ")
        print(ingredients_text)

        print("Parsing ingredients:")
        list_of_ailes = get_list_of_ailes()
        string_before = "        - "
        string_after = ", "
        textlist_of_ailes = format_list_to_textlist(
            list_of_ailes, string_before, string_after
        )

        ingredients_list_dict = []
        for iIngredient in tqdm(ingredients_text):
            print(" - working on ingredient:")
            print(iIngredient)
            ingredient = llm_categorize_ingredient_by_aile_extract_quantity(
                llmObj, iIngredient, textlist_of_ailes
            )
            print(" - output: ")
            print(ingredient)
            print("")
            eval_ingredient = ast.literal_eval(ingredient)
            ingredients_list_dict.append(eval_ingredient)

        print(ingredients_list_dict)

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

    pass


if __name__ == "__main__":
    main()
