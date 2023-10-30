from gpt_translator.gpt_translator import GPTTranslator
import logging

# set logging level
logging.basicConfig(level=logging.INFO)

pre_prompt = """Translate the following two scenes from Hamlet by Shakespeare 
to a modern version so that it is easier to understand. It should be as simple as possible, but no simpler. """

# Initialize the GPTTranslate class and call the translate method
gpt_translate = GPTTranslator(
    "./output/hamlet_part.md",
    pre_prompt,
    working_dir="./output",
    idx_begin=0,
    model="gpt-3.5-turbo",
    max_tokens_paragraph=1024,
)

gpt_translate.translate()
