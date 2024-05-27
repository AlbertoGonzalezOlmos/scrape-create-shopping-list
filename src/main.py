# from wrap_openai import openai_client_initialize, prompt_chain
from _file_paths import get_latest_file, create_output_path

from _file_read_write import read_file, write_pdf
from llm_proxy import LlmProxy


def main():

    llmObj = LlmProxy("groq")
    input_Ingredients_path, input_Ingredients_name = get_latest_file()

    input_context = input_Ingredients_path + input_Ingredients_name

    prompt = f"""

    From the list of recipes and ingredients between <>, perform the following tasks: \

    1. Extract the titles of the recipes.
    2. Output the titles as a list of strings.
    
    Output only the list of strings.

    List of recipes:
    """

    output_file = "out_extractRecipeNames"
    response = llmObj.prompt_chain(
        prompt=prompt,
        output_response_name=output_file,
        input_context_path_name=input_context,
    )

    print(response)

    is_continue = False
    if is_continue:
        output_path, output_name = get_latest_file(output_file, extension="txt")

        prompt = f"""

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
        """

        output_file = "out_groupIngredients"
        response = llmObj.prompt_chain(
            prompt=prompt,
            output_response_name=output_file,
            input_context_path_name=input_context,
        )

        output_path, output_name = get_latest_file(output_file, extension="txt")
        output_file = output_path + output_name
        write_pdf(output_file, input_Ingredients_name)

    pass


if __name__ == "__main__":
    main()
