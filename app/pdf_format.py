import streamlit as st
from markdown2 import markdown
import pdfkit
import tempfile
import os

def pdf_format(markdown_input):

    # CSS for styling the HTML
    custom_css = """
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        pre {
            font-family: monospace;
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            white-space: pre-wrap; /* Wrap long lines */
            word-wrap: break-word;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        blockquote {
            font-style: italic;
            color: #7f8c8d;
            padding-left: 10px;
            border-left: 4px solid #bdc3c7;
        }
        ul {
            margin-left: 20px;
        }
        li {
            margin-bottom: 5px;
        }
    </style>
    """

    # Convert Markdown to HTML and wrap in <pre> for spacing
    if markdown_input.strip():
        html_content = f"""
        <html>
            <head>
                {custom_css}
            </head>
            <body>
                <pre>{markdown(markdown_input)}</pre>
            </body>
        </html>
        """
        st.markdown("### Preview:")
        st.components.v1.html(html_content, height=400, scrolling=True)

        # Generate PDF button
        # if st.button("Generate PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            pdfkit.from_string(html_content, tmp_pdf.name)
            
            with open(tmp_pdf.name, "rb") as pdf_file:
                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name="markdown_output.pdf",
                    mime="application/pdf",
                )
                if st.download_button:
                    st.success("PDF generated successfully!")
            os.remove(tmp_pdf.name)
    else:
        st.info("Enter Markdown text above to generate a preview and PDF.")

    return markdown_input