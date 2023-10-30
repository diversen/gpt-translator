from gpt_translator.gpt_translator import GPTTranslator
import logging

# set logging level
logging.basicConfig(level=logging.INFO)

pre_prompt = """You WILL modernize an H.P. lovecraft text to a more modern and easy readable English.
Words that are outdated or not very common anymore should be replaced with words that convey the same meaning.
You MUST not use any meta-comments.
You MUST keep any markdown formatting intact when possible, e.g. markdown header like '#' or '##'.
The text may be a headline or a full paragraph. You MUST translate from English to a more Modern English.
The text to modernize begins after the next colon: """

# pre_prompt = """
# You are an agent that is fluent in both English and Danish.
# You should internally translate to a modern English first. And then translate this modern English to Danish.
# You MUST not use any meta-comments.
# You MUST keep any markdown formatting intact when possible, e.g. markdown header like '#' or '##'.
# The text may be a headline or a full paragraph.
# The text to translate to Danish begins after the next colon: """

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
