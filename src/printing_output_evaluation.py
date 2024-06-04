from colorama import Fore, Back, Style
from typing import Union


def _highlight_text(input_text: str, search_text_input: Union[str, list]) -> None:

    search_text_print = ""
    is_context = True
    if not search_text_input:
        search_text_input = ["ffffffffffffffff NO CONTEXT FOUND ffffffffffffffffff"]
        is_context = False
    elif isinstance(search_text_input, str):
        search_text_input = [search_text_input]

    search_text = []
    search_text_not_found = []
    context_color = f"{Fore.WHITE}{Back.BLACK}"
    for text_item in search_text_input:
        # search_text.append(_correct_string_format(text_item))
        search_text.append(text_item)

    start_start = 0
    return_text = ""
    found_text_order_list = []
    for search_idx, search_text_item in enumerate(search_text):
        if isinstance(search_text_item, list):
            search_text_item = str(search_text_item[0])
            search_text[search_idx] = str(search_text_item[0])

        found_text_order_list.append(input_text.find(search_text_item))
    X = search_text
    Y = found_text_order_list
    search_text_reordered = search_text
    if found_text_order_list:
        search_text_reordered = [x for _, x in sorted(zip(Y, X))]

    for search_text_item in search_text_reordered:
        search_text_print += search_text_item + "\n"
        start_end = input_text.find(search_text_item)

        if not is_context:
            search_text_print = ""
            search_text_item = ""
        if start_end < 0:
            search_text_not_found.append(search_text_item)

        else:

            context_color = f"{Fore.BLACK}{Back.GREEN}"
            return_text += (
                input_text[start_start:start_end]
                + f"{Fore.GREEN}{search_text_item}{Style.RESET_ALL}"
            )
            start_start = start_end + len(search_text_item)

    print(
        f"{Fore.BLACK}{Back.BLUE}search text:{Style.RESET_ALL} "
        + f"{Fore.BLUE}{search_text_print}{Style.RESET_ALL}"
    )
    if search_text_not_found:
        print(f"{Fore.BLACK}{Back.RED} TEXT NOT FOUND ... {Style.RESET_ALL}")
        for text_not_found in search_text_not_found:
            print(text_not_found)

    print(f"")
    print(f"{context_color}CONTEXT:{Style.RESET_ALL} ")
    print(return_text + input_text[start_start:])


def _col_bool_int(input_string: str = "") -> str:

    if not input_string:
        return input_string
    col_bool_int = ""
    if input_string.find("True") >= 0:
        str_opt = len("True")
        col_bool_int = _col_text("True", "black", "green") + input_string[str_opt:]
    elif input_string == "5":
        col_bool_int = _col_text(input_string, "black", "green")

    elif input_string.find("Partially included") >= 0:
        str_opt = len("Partially included")
        col_bool_int = (
            _col_text("Partially included", "black", "yellow") + input_string[str_opt:]
        )
    elif input_string == "4":
        col_bool_int = _col_text(input_string, "black", "yellow")

    elif input_string.find("False") >= 0:
        str_opt = len("False")
        col_bool_int = _col_text("False", "black", "red") + input_string[str_opt:]
    elif input_string == "0":
        col_bool_int = _col_text(input_string, "black", "red")

    else:
        col_bool_int = _col_text(input_string, "magenta", "black")

    return col_bool_int


def _col_text(
    string: str = "", fore_colour: str = "white", back_colour: str = "black"
) -> str:
    coloured_string = ""
    fore_colour = fore_colour.upper()
    back_colour = back_colour.upper()
    fore_eval = f"Fore.{fore_colour}"
    back_eval = f"Back.{back_colour}"
    coloured_string += f"{eval(fore_eval)}{eval(back_eval)}{string}{Style.RESET_ALL}"
    return coloured_string


def _print_evaluation_results(output_evaluation: dict) -> None:
    str_yellow_stripe = "################################################"
    yellow_stripe = _col_text(str_yellow_stripe, "black", "yellow")

    print(yellow_stripe)
    _highlight_text(
        output_evaluation["context"], output_evaluation["llm_response"]["context"]
    )

    print(_col_text(" GT CONTEXT: ", "black", "cyan"))
    print(output_evaluation["gt_context"])

    print("")
    print(_col_text(" QUESTION: ", "black", "cyan"))
    print(output_evaluation["question"])
    print(_col_text(" GT_ANSWER: ", "black", "cyan"))
    print(output_evaluation["gt_answers"])
    print(_col_text(" LLM RESPONSE: ", "black", "cyan"))
    print(output_evaluation["llm_response"])

    for evaluation_item in output_evaluation["evaluation_list"]:
        if evaluation_item["evaluation_description"]:
            print(
                (
                    _col_text(
                        evaluation_item["evaluation_description"], "black", "cyan"
                    )
                    + _col_bool_int(evaluation_item["evaluation_result"])
                )
            )

    print(yellow_stripe)
    print("")
