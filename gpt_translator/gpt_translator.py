import openai
import time
import logging
import os
from dotenv import load_dotenv
from gpt_translator import file_utils


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# log to stdout
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class GPTTranslator:
    def __init__(
        self,
        from_file,
        pre_prompt,
        working_dir="./output",
        idx_begin=0,  # idx to start from
        failure_sleep=10,
        temperature=0.7,
        presence_penalty=0.1,
        top_p=0.99,
        max_tokens_paragraph=1024,
        model="gpt-3.5-turbo",
    ):

        self.pre_prompt = pre_prompt
        self.idx_begin = idx_begin
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

    def get_params(self, message):
        message = self.pre_prompt + message
        params = {
            "model": self.model,
            "temperature": self.temperature,
            "presence_penalty": self.presence_penalty,
            "top_p": self.top_p,
            "stream": False,
            "messages": [{"role": "user", "content": message}],
        }
        return params

    def translate_string(self, message):
        params = self.get_params(message)
        result = openai.ChatCompletion.create(**params)
        return result

    def translate(self):
        paragraphs = file_utils.read_source_file(
            self.from_file, self.max_tokens_paragraph
        )

        file_utils.save_markdown(self.working_dir, "input.md", paragraphs)
        paragraphs_translated = file_utils.get_paragraphs(
            self.working_dir, "output.json"
        )

        position = len(paragraphs_translated)

        logging.info(f"Total paragraphs to translate: {len(paragraphs)}")
        logging.info(f"Starting from paragraph: {position + 1}")

        for idx, para in enumerate(paragraphs[position:], position):
            retry = True
            failure_iterations = 1

            while retry:
                try:
                    logging.info(
                        f"Translating paragraph {idx + 1} of {len(paragraphs)}"
                    )

                    result = self.translate_string(para)
                    tokens_used = int(result["usage"]["total_tokens"])
                    if tokens_used == 0:
                        raise Exception("No tokens were returned from API endpoint.")

                    content = result["choices"][0]["message"]["content"]
                    self.total_tokens += tokens_used

                    paragraphs_translated.append(content.strip())
                    file_utils.save_markdown(
                        self.working_dir, "output.md", paragraphs_translated
                    )
                    file_utils.save_json(
                        self.working_dir, "output.json", paragraphs_translated
                    )

                    logger.info(f"(Total tokens used: {self.total_tokens})")
                    retry = False  # Translation successful, exit while-loop

                except Exception as e:
                    logger.exception(e)
                    logger.error(f"Exception. Retry with key: {idx}")
                    sleep = self.failure_sleep * failure_iterations
                    logger.info(f"Sleeping for {sleep} seconds before retrying.")
                    time.sleep(sleep)
                    failure_iterations *= 2  # exponential backoff
