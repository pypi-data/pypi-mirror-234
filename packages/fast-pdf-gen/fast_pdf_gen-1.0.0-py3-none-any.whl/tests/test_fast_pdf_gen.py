import os
from fast_pdf_gen import generate_pdf

def test_generate_pdf_with_custom_options():
    # Define test input parameters
    template_key = 'test_template'
    template_string = '<html><body><h1>{{title}}</h1></body></html>'
    output_path = 'output_with_options.pdf'
    context = {'title': 'Test PDF'}
    
    # Custom PDF options
    pdf_options = {
        'format': 'A3',
        'margin': {
            'top': '10mm',
            'right': '10mm',
            'bottom': '10mm',
            'left': '10mm'
        }
    }

    # Call the function to generate PDF with custom options
    generate_pdf(template_key, template_string, output_path, context=context, pdf_options=pdf_options)

    # Perform assertions or validation checks here
    assert os.path.exists(output_path)

    # Clean up generated files (optional)
    os.remove(output_path)
