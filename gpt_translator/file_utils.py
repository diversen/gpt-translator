import re


def read_txt(filename, max_words_paragraph=0):
    """
    Read txt and markdown files and return a list of paragraphs as a list of strings.
    """
    with open(filename, "r") as file:
        content = file.read()

    # Normalize all line endings to \n
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    # Transform multiple newlines into max two
    content = re.sub('\n{3,}', '\n\n', content)

    # Split on double line endings
    paragraphs = content.split("\n\n")

    # Expand paragraphs
    if max_words_paragraph:
        paragraphs = expand_paragraphs(paragraphs, max_words_paragraph)

    # Trim
    paragraphs = [para.strip() for para in paragraphs if para.strip()]

    return paragraphs


def expand_paragraphs(paragraphs, max_words_paragraph):
    """
    Expand paragraphs to a maximum number of words per paragraph.
    """
    new_paragraphs = []
    new_paragraph = ""
    for paragraph in paragraphs:
        new_paragraph += paragraph + "\n\n"
        if len(new_paragraph) > max_words_paragraph:
            new_paragraphs.append(new_paragraph)
            new_paragraph = ""
    return new_paragraphs
