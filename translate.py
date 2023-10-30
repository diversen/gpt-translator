from gpt_translator.gpt_translator import GPTTranslator
import logging

# set logging level
logging.basicConfig(level=logging.INFO)

pre_prompt = """Translate the following H. P. Lovecraft text to English so that I child aged 12 will have no 
problem reading it. Add some humor to the text if possible. """

# Initialize the GPTTranslate class and call the translate method
gpt_translate = GPTTranslator(
    "./output/winged-death.md",
    pre_prompt,
    working_dir="./output",
    idx_begin=0,
    model="gpt-3.5-turbo",
    max_tokens_paragraph=256,
)

gpt_translate.translate()
