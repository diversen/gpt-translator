from gpt_translator.gpt_translator import GPTTranslator
import logging

# set logging level
logging.basicConfig(level=logging.INFO)

prompt = """Objective: Translate a selected passage from Shakespeare's 'Hamlet' into modern English.
Audience Engagement: Ensure the translation is clear, engaging, and accessible to contemporary readers while maintaining the spirit and tone of the original.
Preservation of Essence: Retain the core elements of the scenes, characters, and structure found in the original text.
Selective Translation: Focus on translating sections that are obscure or challenging for a modern audience. Exclude parts that are already clear and understandable in their original form.
Format Consistency: Adhere closely to the original formatting, including line breaks and line width. Each line of text in the original should correspond to one line of text in the translation, ensuring that each paragraph has the same number of lines.
Paragraph Line Count: Emphasize that one line of text in the original should equate to one line of text in the translation, preserving the paragraph structure exactly.
Markdown Compatibility: Maintain markdown formatting for both the original text and the translated version to ensure ease of reading and compatibility with markdown readers.

Here is the original text you will translate:"""

# Initialize the GPTTranslate class and call the translate method
gpt_translate = GPTTranslator(
    "./input/hamlet_part.md",
    prompt,
    working_dir="./output",
    model="gpt-3.5-turbo",
    max_tokens=512,
)

gpt_translate.translate()

# update by a list of idxs. Idx corresponds to the paragraph number (or database idx)
# gpt_translate.translate_idxs([2])
