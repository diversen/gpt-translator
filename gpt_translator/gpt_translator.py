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
        max_tokens=1024,
        model="gpt-3.5-turbo",
    ):
        self.prompt = prompt
        self.failure_sleep = failure_sleep
        self.from_file = from_file
        self.working_dir = working_dir
        self.temperature = temperature
        self.presence_penalty = presence_penalty
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.model = model
        self.total_tokens = 0
        self.failure_iterations = 1

        self.paragraphs_src = file_utils.file_get_src_paragraphs(
            self.from_file, self.max_tokens
        )

        # create working directory if it doesn't exist
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)

        # init sqlite database
        self.db = DB(self.working_dir)

        # Insert all paragraphs into database that don't already exist
        for idx, para in enumerate(self.paragraphs_src):
            self.db.insert_paragraph(idx + 1, para)

    def _get_params(self, message):
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

    def _translate_endpoint(self, message):
        params = self._get_params(message)
        result = openai.ChatCompletion.create(**params)

        tokens_used = int(result["usage"]["total_tokens"])
        if tokens_used == 0:
            raise Exception("No tokens were returned from API endpoint.")

        content = result["choices"][0]["message"]["content"]
        return content, tokens_used

    def _translate_single_paragraph(self, idx):
        failure_iterations = 1
        para = self.db.get_paragraph(idx)

        while True:
            try:
                content, tokens_used = self._translate_endpoint(para)
                self.total_tokens += tokens_used
                return content

            except Exception as e:
                logger.exception(e)
                logger.error(f"Exception. Retry with key: {idx + 1}")

                sleep = self.failure_sleep * failure_iterations
                logger.info(f"Sleeping for {sleep} seconds before retrying.")
                time.sleep(sleep)

                failure_iterations *= 2  # exponential backoff

    def translate(self):
        if self.db.all_translated():
            logger.info("All paragraphs have been translated.")

        else:
            total = self.db.get_count_paragraphs()
            idxs = self.db.get_idxs()

            for idx in idxs:
                if self.db.idx_is_translated(idx):
                    logger.info(f"Paragraph {idx} has already been translated.")
                    continue

                logging.info(f"Translating paragraph {idx} of {total}")
                content = self._translate_single_paragraph(idx)
                self.db.update_paragraph_translation(idx, content)
                logger.info(f"(Total tokens used: {self.total_tokens})")

        self.export()

    def translate_idxs(self, idxs):
        """
        Translate paragraphs by index.
        """
        for idx in idxs:
            if not self.db.idx_exists(idx):
                logger.error(f"Paragraph {idx} does not exist.")
                continue

            logging.info(f"Translating paragraph {idx}")
            content = self._translate_single_paragraph(idx)
            self.db.update_paragraph_translation(idx, content)
            logger.info(f"(Total tokens used: {self.total_tokens})")

        self.export()

    def export(self):
        """
        Export translated paragraphs to file.
        """

        # generate filename from source filename
        filename = os.path.basename(self.from_file)

        # get extension
        filename, ext = os.path.splitext(filename)

        # append _translated to filename
        filename = filename + "_translated" + ext

        # get output_dir + filename
        filename = os.path.join(self.working_dir, filename)

        paragraphs = self.db.get_all_rows()
        file_utils.file_put_paragraphs(filename, paragraphs)
