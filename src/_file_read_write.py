from fpdf import FPDF
from _file_paths import create_output_path


def read_file(file_path_name: str) -> str:
    with open(file_path_name, "r") as f:
        content = f.read()
    return content


def write_file(file_path_name: str, response: str) -> None:
    if not file_path_name.endswith(".txt"):
        file_path_name = f"{file_path_name}.txt"

    with open(file_path_name, "w") as f:
        f.write(response)


def write_pdf(input_file: str, output_name: str) -> None:
    output_path = f"{output_path}_PDF"
    output_path = create_output_path(output_name)
    # Create a new FPDF object
    pdf = FPDF()

    # Open the text file and read its contents
    with open(input_file, "r") as f:
        text = f.read()

    # Add a new page to the PDF
    pdf.add_page()

    # Set the font and font size
    pdf.set_font("Arial", size=12)

    # Write the text to the PDF
    pdf.write(5, text)

    if output_name.find(".txt") > 0:
        output_name = output_name[:-4]
    if output_name.find(".pdf") < 0:
        output_name = f"{output_name}.pdf"

    print(f"pdf output path: {output_path} and ")
    print(f"output name: {output_name}")
    # Save the PDF
    pdf.output(output_path + output_name)
