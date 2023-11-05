import openai
import time
import logging
import os

from dotenv import load_dotenv
from gpt_translator import file_utils
from gpt_translator.db import DB

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# log to stdout
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class GPTTranslator:
    def __init__(
        self,
        from_file,
        prompt,
        working_dir="output",
        failure_sleep=10,
        temperature=0.7,
        presence_penalty=0.1,
        top_p=0.99,
        max_tokens_paragraph=1024,
        model="gpt-3.5-turbo",
    ):
        self.prompt = prompt
        self.failure_sleep = failure_sleep
        self.from_file = from_file
        self.working_dir = working_dir
        self.temperature = temperature
        self.presence_penalty = presence_penalty
        self.top_p = top_p
        self.max_tokens_paragraph = max_tokens_paragraph
        self.model = model
        self.total_tokens = 0
        self.failure_iterations = 1

        # create working directory if it doesn't exist
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)

        # init sqlite database
        self.db = DB(self.working_dir)

    def get_params(self, message):
        message = self.prompt + message
        params = {
            "model": self.model,
            "temperature": self.temperature,
            "presence_penalty": self.presence_penalty,
            "top_p": self.top_p,
            "stream": False,
            "messages": [{"role": "user", "content": message}],
        }
        return params

    def translate_endpoint(self, message):
        params = self.get_params(message)
        result = openai.ChatCompletion.create(**params)

        tokens_used = int(result["usage"]["total_tokens"])
        if tokens_used == 0:
            raise Exception("No tokens were returned from API endpoint.")

        content = result["choices"][0]["message"]["content"]
        return content, tokens_used

    def translate(self):
        paragraphs_src = file_utils.file_get_src_paragraphs(
            self.from_file, self.max_tokens_paragraph
        )

        # Insert all paragraphs into database that don't already exist
        for idx, para in enumerate(paragraphs_src):
            self.db.insert_paragraph(idx, para)

        # get total count of paragraphs
        total = self.db.get_count_paragraphs()

        # if all paragraphs have been translated, exit
        if self.db.all_translated():
            logger.info("All paragraphs have been translated.")
            return

        # iterate all paragraphs
        for idx, para in enumerate(paragraphs_src):
            # if paragraph has already been translated, skip
            if self.db.idx_is_translated(idx):
                continue

            # translate paragraph
            content = self.translate_single_paragraph(idx, total, para)

            # save translated paragraph to database
            self.db.update_paragraph(idx, content)
            logger.info(f"(Total tokens used: {self.total_tokens})")

    def translate_single_paragraph(self, idx, total, para):
        retry = True
        failure_iterations = 1

        while retry:
            try:
                logging.info(f"Translating paragraph {idx + 1} of {total}")

                content, tokens_used = self.translate_endpoint(para)
                self.total_tokens += tokens_used

                retry = False  # Translation successful, exit while-loop
                return content

            except Exception as e:
                logger.exception(e)
                logger.error(f"Exception. Retry with key: {idx}")
                sleep = self.failure_sleep * failure_iterations
                logger.info(f"Sleeping for {sleep} seconds before retrying.")
                time.sleep(sleep)
                failure_iterations *= 2  # exponential backoff
