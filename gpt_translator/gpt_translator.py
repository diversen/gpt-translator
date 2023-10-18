import openai
import time
import logging
import tempfile

from gpt_translator.file_utils import read_txt

temp_dir = tempfile.gettempdir()

# log to stdout
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class GPTTranslator:
    def __init__(
        self,
        api_key,
        from_file,
        to_file,
        pre_prompt,
        idx_begin=0,  # idx to start from
        failure_sleep=1,
        temperature=0.7,
        presence_penalty=0.1,
        top_p=0.99,
        max_words_paragraph=1024,
        model="gpt-3.5-turbo",
    ):

        # Read api key from file
        with open(api_key, "r") as file:
            api_key = file.read().strip()

        openai.api_key = api_key

        self.pre_prompt = pre_prompt
        self.idx_begin = idx_begin
        self.failure_sleep = failure_sleep
        self.from_file = from_file
        self.to_file = to_file
        self.temperature = temperature
        self.presence_penalty = presence_penalty
        self.top_p = top_p
        self.max_words_paragraph = max_words_paragraph
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
        paragraphs = read_txt(self.from_file, self.max_words_paragraph)

        logging.info(f"Total paragraphs to translate: {len(paragraphs)}")
        logging.info(f"Starting from paragraph index: {self.idx_begin}")

        for idx, para in enumerate(paragraphs[self.idx_begin:], self.idx_begin):
            retry = True
            failure_iterations = 1

            while retry:
                try:
                    logging.info(f"Translating paragraph index {idx} of {len(paragraphs)}")

                    result = self.translate_string(para)
                    tokens_used = int(result["usage"]["total_tokens"])
                    if tokens_used == 0:
                        raise Exception("No tokens were returned from API endpoint.")

                    self.total_tokens += tokens_used
                    with open(self.to_file, "a") as file:
                        file.write(result["choices"][0]["message"]["content"] + "\n\n")

                    logger.info(f"(Total tokens used: {self.total_tokens})")
                    retry = False  # Translation successful, exit while-loop

                except Exception:
                    logger.error("Exception. Retry with key: {idx}")
                    sleep = self.failure_sleep * failure_iterations
                    logger.info(f"Sleeping for {sleep} seconds before retrying.")
                    time.sleep(sleep)
                    failure_iterations *= 2
