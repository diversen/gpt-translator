import re
import os
import json
import tiktoken
import logging

# log to stdout
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def count_tokens(string: str) -> int:
    """
    Returns the number of tokens in a text string.
    cl100k_base: gpt-4, gpt-3.5-turbo, text-embedding-ada-002
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens


def read_source_file(filename, max_tokens_paragraph):
    """
    Read txt and markdown files and return a list of paragraphs as a list of strings.
    """
    with open(filename, "r") as file:
        content = file.read()

    # Normalize all line endings to \n
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    # trim all lines
    content = "\n".join([line.strip() for line in content.split("\n")])

    # Transform multiple newlines into max two
    content = re.sub("\n{3,}", "\n\n", content)

    # Split on double line endings
    paragraphs = content.split("\n\n")

    # replace only single newlines wit spaces, but not multiple newlines
    paragraphs = [re.sub("(?<!\n)\n(?!\n)", " ", para) for para in paragraphs]

    # replace any double space with a single space
    paragraphs = [re.sub(" +", " ", para) for para in paragraphs]

    # Expand paragraphs
    paragraphs = _expand_paragraphs(paragraphs, max_tokens_paragraph)

    # Trim
    paragraphs = [para.strip() for para in paragraphs if para.strip()]

    return paragraphs


def save_markdown(working_dir, filename, paragraphs):
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    save_file = os.path.join(working_dir, filename)
    with open(save_file, "w") as file:
        file.write("\n\n".join(paragraphs))


def save_json(working_dir, filename, paragraphs):
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    save_file = os.path.join(working_dir, filename)
    with open(save_file, "w") as file:
        json.dump(paragraphs, file, indent=4, ensure_ascii=False)


def get_paragraphs(working_dir, filename):
    json_file = os.path.join(working_dir, filename)
    if not os.path.exists(json_file):
        return []

    try:
        with open(json_file, "r") as file:
            paragraphs = json.load(file)
    except json.decoder.JSONDecodeError:
        paragraphs = []

    return paragraphs


def _expand_paragraphs(paragraphs, max_tokens_paragraph):
    """
    Expand paragraphs to a maximum number of words per paragraph.
    """
    new_paragraphs = []
    new_paragraph = ""

    for paragraph in paragraphs:
        token_count = count_tokens(paragraph)
        if token_count > max_tokens_paragraph:
            raise Exception(
                f"Paragraph contains {token_count} tokens, which is more than the maximum of {max_tokens_paragraph} tokens per paragraph."
            )

    for paragraph in paragraphs:
        token_count = count_tokens(paragraph)
        if token_count > max_tokens_paragraph:
            raise Exception(
                f"Paragraph contains {token_count} tokens, which is more than the maximum of {max_tokens_paragraph} tokens per paragraph."
            )

        new_paragraph += paragraph + "\n\n"
        if count_tokens(new_paragraph) > max_tokens_paragraph:
            new_paragraphs.append(new_paragraph)
            new_paragraph = ""
    return new_paragraphs


def cleanup(directory):
    files_to_remove = ["input.md", "input.json", "output.md"]
    
    for filename in files_to_remove:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Removed {file_path}")

    logger.info("Cleanup complete.")
