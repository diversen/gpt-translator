from gpt_translator.gpt_translator import GPTTranslator
import logging

# set logging level
logging.basicConfig(level=logging.INFO)

prompt = """Objective: Translate a passage from Shakespeare's 'Hamlet' into contemporary English that is engaging and clear for toda
y's readers. Don't translate what makes sense to modern readers. Don't make any meta-comments about the translation.

Keep the formatting: Translate line by line. Each line in the input should correspond to a single line in the output. A
single line is defined as some text that ends with a newline character. Never combine two lines into one. Never split a
single line into two. Translate each line independently.

The translated text should have the same number of lines as the input text.

Markdown: Input is markdown. Output should also be markdown. Always keep the markdown formatting from the input. E.g. al
l lines in the dialogs begins with '> '. And also any headings, lists, etc.

Here is the original text you will translate:"""

# Initialize the GPTTranslate class and call the translate method
gpt_translate = GPTTranslator(
    "./output/hamlet_part.md",
    prompt,
    working_dir="./output",
    model="gpt-3.5-turbo",
    max_tokens=512,
)

gpt_translate.translate()

# update by a list of idxs. Idx corresponds to the paragraph number (or database idx)
# gpt_translate.translate_idxs([2])
