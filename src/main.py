def main():
    from _file_paths import get_latest_file, create_output_path
    from _file_read_write import read_file, write_file, write_pdf
    from llm_proxy import LlmProxy
    from language_processing import pipeline_get_grocery_list

    llmObj = LlmProxy("groq")

    input_week_path, input_week_name = get_latest_file()
    input_week_path_name = input_week_path + input_week_name
    text_with_recipes = read_file(input_week_path_name)

    grocery_list, recipe_names = pipeline_get_grocery_list(llmObj, text_with_recipes)

    output_recipe_names_name = "out_extract_recipe_names_PDF"
    output_recipe_names_path = create_output_path(output_recipe_names_name)
    output_recipe_names_path_name = (
        output_recipe_names_path + input_week_name[:-4] + "_recipe_names"
    )
    write_file(output_recipe_names_path_name, recipe_names)

    output_grocery_list_PDF = "out_grocery_list_PDF"
    output_grocery_list_PDF_path = create_output_path(output_grocery_list_PDF)
    output_grocery_list_PDF_path_name = (
        output_grocery_list_PDF_path + input_week_name[:-4] + "_grocery_list"
    )
    write_pdf(output_grocery_list_PDF_path_name, grocery_list)

    pass


if __name__ == "__main__":

    main()
