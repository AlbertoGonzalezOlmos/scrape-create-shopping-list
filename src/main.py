def main():
    from file_paths import get_latest_file, create_output_path
    from file_read_write import read_file, write_file, write_pdf
    from string_formatting import (
        format_recipe_names_list_to_text,
        format_quantity_ingredients_listtext_to_listdictionary,
    )
    from llm_proxy import LlmProxy
    from language_processing import (
        get_week_number,
        pipeline_get_grocery_list,
        pipeline_get_grocery_list_from_text,
    )
    from scrape_recipes import get_most_recent_week_url, scrape_recipe_names_ingredients

    week_title, most_recent_week_url = get_most_recent_week_url("flexitarisk")

    week_number = get_week_number(week_title)

    recipe_names_url_list, list_quantity_ingredients = scrape_recipe_names_ingredients(
        most_recent_week_url
    )

    recipe_names_url_text = format_recipe_names_list_to_text(recipe_names_url_list)

    output_recipe_names_name = "out_extract_recipe_names_PDF"
    output_recipe_names_path = create_output_path(output_recipe_names_name)
    output_recipe_name = f"w{week_number}_recipe_names"
    output_recipe_names_path_name = output_recipe_names_path + output_recipe_name
    write_file(output_recipe_names_path_name, recipe_names_url_text)

    quantity_ingredient_listdict = (
        format_quantity_ingredients_listtext_to_listdictionary(
            list_quantity_ingredients
        )
    )

    print(quantity_ingredient_listdict)
    print(recipe_names_url_text)

    try:
        llmObj = LlmProxy("together")
    except:
        llmObj = LlmProxy("groq")

    grocery_list = pipeline_get_grocery_list(llmObj, quantity_ingredient_listdict)

    # # input_week_path, input_week_name = get_latest_file()
    # # input_week_path_name = input_week_path + input_week_name
    # # text_with_recipes = read_file(input_week_path_name)

    # # grocery_list, recipe_names = pipeline_get_grocery_list_from_text(llmObj, text_with_recipes)

    # output_grocery_list_PDF = "out_grocery_list_PDF"
    # output_grocery_list_PDF_path = create_output_path(output_grocery_list_PDF)
    # output_grocery_list_PDF_name = f"w{week_number}_grocery_list"
    # output_grocery_list_PDF_path_name = (
    #     output_grocery_list_PDF_path + output_grocery_list_PDF_name
    # )
    # write_pdf(output_grocery_list_PDF_path_name, grocery_list)


if __name__ == "__main__":

    main()
