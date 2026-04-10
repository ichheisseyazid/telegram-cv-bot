# pdf_generator.py

import os
import tempfile
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# Load templates from the templates/ folder
env = Environment(loader=FileSystemLoader("templates"))


def generate_pdf(data: dict) -> str:
    """
    Takes the completed CV data dict, renders the HTML template,
    converts it to PDF, saves to a temp file, and returns the file path.
    """

    # Parse comma-separated fields into lists for the template
    data["skills_list"] = [s.strip() for s in data.get("skills", "").split(",")]
    data["languages_list"] = [l.strip() for l in data.get("languages", "").split(",")]

    # Render HTML with Jinja2
    template = env.get_template("cv_template.html")
    html_content = template.render(**data)

    # Write to a temp PDF file
    tmp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf",
        prefix=f"cv_{data.get('full_name', 'output').replace(' ', '_')}_"
    )
    tmp_path = tmp.name
    tmp.close()

    # Convert HTML → PDF
    HTML(string=html_content).write_pdf(tmp_path)

    return tmp_path
