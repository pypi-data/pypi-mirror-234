import os
import logging
from pybars import Compiler as HandlebarsCompiler

logger = logging.getLogger(__name__)

template_cache = {}

def configure_logging(log_level=logging.INFO):
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def normalize_path(template_path):
    # Normalize the path separators based on the operating system
    return os.path.abspath(os.path.expanduser(template_path.replace('/', os.path.sep).replace('\\', os.path.sep)))

def compile_handlebars_template(template_key, template_path_or_string, context=None):
    
    if template_path_or_string.endswith('.html'):
        # If the path ends with .html, normalize the path
        template_path = normalize_path(template_path_or_string)
    else:
        # Otherwise, use the template_path_or_string as is
        template_path = template_path_or_string

    
    if template_key not in template_cache:
        try:
            if template_path.endswith('.html') and os.path.isfile(template_path):
                # Read template from HTML file
                with open(template_path, 'r') as file:
                    template_source = file.read()
                    logger.info(f"Reading template from HTML file: {template_path}")
            else:
                # Use template_path_or_string as a string template
                template_source = template_path
                logger.info("Using provided template string.")

            compiler = HandlebarsCompiler()
            
            compiled_template = compiler.compile(template_source)
            compiled_html = compiled_template(context)
            template_cache[template_key] = compiled_html
            logger.info(f"Template '{template_key}' compilation successful.")
        except Exception as e:
            logger.error(f"Error: {e}")
            template_cache[template_key] = None

    compiled_html = template_cache[template_key]
    return compiled_html
