# from wrap_openai import openai_client_initialize, prompt_chain
from _file_paths import get_latest_file, create_output_path

from _file_read_write import read_file, write_file, write_pdf
from llm_proxy import LlmProxy


def main():

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

    pass


if __name__ == "__main__":
    main()
