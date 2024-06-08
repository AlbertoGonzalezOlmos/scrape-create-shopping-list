from fpdf import FPDF
from _file_paths import create_output_path

def check_file_exist(file_path_name: str) -> bool:
    pass
    


def read_file(file_path_name: str) -> str:

    if not file_path_name.endswith(".txt"):
        file_path_name = f"{file_path_name}.txt"

    with open(file_path_name, "r") as f:
        content = f.read()
    return content



def read_file_line_to_list(file_path_name: str) -> list:
    # list_content = []
    # with open(file_path_name, "r") as f:
    #     for
    #     list_content.append(f.readline())
    # return list_content

    with open(file_path_name) as f:
        return [line.rstrip() for line in f]


def write_file(file_path_name: str, response: str) -> None:
    if not file_path_name.endswith(".txt"):
        file_path_name = f"{file_path_name}.txt"

    with open(file_path_name, "w") as f:
        f.write(response)


def write_pdf(output_path_name: str, input_file: str) -> None:

    if output_path_name.endswith(".txt"):
        output_path_name = output_path_name[:-4]

    if not output_path_name.endswith(".pdf") < 0:
        output_path_name = f"{output_path_name}.pdf"

    # Create a new FPDF object
    pdf = FPDF()

    # Add a new page to the PDF
    pdf.add_page()

    # Set the font and font size
    pdf.set_font("Arial", size=12)

    # Write the text to the PDF
    pdf.write(5, input_file)

    # Save the PDF
    pdf.output(output_path_name)
