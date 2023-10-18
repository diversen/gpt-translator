from gpt_translator.gpt_translator import GPTTranslator
import logging

# set logging level
logging.basicConfig(level=logging.ERROR)

pre_prompt = """You WILL modernize an English text to a more modern and more readable English text.
Words that maybe appear outdated should be replaced with more modern versions of the words.
You MUST not use any meta-comments.
You MUST keep any markdown formatting intact when possible, e.g. markdown header like '#' or '##'. 
The text may be a headline or a full paragraph. You MUST translate from English to a more Modern English. 
The text to modernize begins after the next colon: """

# Initialize the GPTTranslate class and call the translate method
gpt_translate = GPTTranslator(
    "/home/dennis/.config/shell-gpt-php/api_key.txt",
    "./example/ashes.md",
    "./example/ashes-modern.md",
    pre_prompt,
    idx_begin=1,
    model="gpt-3.5-turbo",
)
gpt_translate.translate()
