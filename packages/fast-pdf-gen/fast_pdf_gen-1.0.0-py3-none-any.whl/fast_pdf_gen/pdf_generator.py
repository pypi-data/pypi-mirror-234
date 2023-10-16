import asyncio
import logging
import os
from fast_pdf_gen.handlebars_compiler import compile_handlebars_template
from pyppeteer import launch

logger = logging.getLogger(__name__)

def configure_logging(log_level=logging.INFO):
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

async def generate_pdf_from_template(template_key, template_path_or_string, output_path, context=None, pdf_options=None):

    try:
        compiled_html = compile_handlebars_template(template_key, template_path_or_string, context)
        if compiled_html:
            browser = await launch()
            page = await browser.newPage()
            await page.setContent(compiled_html)

            default_pdf_options = {
                'path': output_path,
                'format': 'A4',
                'margin': {
                    'top': '20mm',
                    'right': '20mm',
                    'bottom': '20mm',
                    'left': '20mm'
                }
            }

            # Merge default options with custom options, if provided
            if pdf_options:
                default_pdf_options.update(pdf_options)

            await page.pdf(default_pdf_options)
            await browser.close()
            logger.info(f"PDF generated successfully at: {output_path}")
        else:
            logger.error(f"Error generating PDF: Template '{template_key}' compilation failed.")
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise

def generate_pdf(template_key, template_path_or_string, output_path, context=None, pdf_options=None):
    configure_logging()
    try:
        asyncio.get_event_loop().run_until_complete(generate_pdf_from_template(template_key, template_path_or_string, output_path, context=context, pdf_options=pdf_options))
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
