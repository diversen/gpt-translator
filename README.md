### gpt-translator

A simple tool for translating text using the openai API.

Give a text file and a prompt the tool will translate the text file using a given prompt.

You can translate a complicated text to a simple text. Or you can translate a text to a different language. Or in short: Translate a text to another text.

Each text is split into sections defined as text separated by at least two newlines. A paragraph is defined as a number of sections with a maximum number of tokens. The default is 1024 tokens. You can change this by using the `--max-tokens-paragraph` option.

The tool keeps track of what paragraphs have been translated and will continue from the last translated paragraph if the tool is stopped or interrupted.

If there is an error the tool will back off exponentially. The default is to sleep 10 second on the first error, 20 seconds on the second error, 40 seconds on the third error, and so on. You can change this by using the `--failure-sleep` option.

### Usage

You need to have an openai API key.

Add this to a `.env` file in your environment:

```bash
OPENAI_API_KEY=your-api-key
```

Or just add it to your environment.

### Install as requirement

<!-- LATEST-VERSION-PIP -->
	pip install git+https://github.com/diversen/gpt-translator@v0.0.9

For usage see [translate.py](translate.py)

### As command line tool

Install latest version using pipx

<!-- LATEST-VERSION-PIPX -->
	pipx install git+https://github.com/diversen/gpt-translator@v0.0.9


```bash
gpt-translator translate --help
```
    Usage: python -m gpt_translator translate [OPTIONS]

    Options:
    -f, --from-file TEXT            Source file for translation.  [required]
    -p, --prompt TEXT               Prompt for translation.  [required]
    -d, --working-dir TEXT          Working directory. Default is 'output'
    -m, --max-tokens-paragraph INTEGER
                                    Max tokens per paragraph. Default 1024
    --failure-sleep INTEGER         Failure sleep time. Default is 10 seconds.
    --temperature FLOAT             Temperature.
    --presence-penalty FLOAT        Presence penalty.
    --top-p FLOAT                   Top P.
    --model TEXT                    Model to use.
    --help                          Show this message and exit.

Translat example: 

```bash
gpt-translator translate -f output/hamlet_part.md -p "Translate the following two scenes from Hamlet by Shakespeare to a modern version so that it is easier to understand. It should be as simple as possible, but no simpler."

```

Cleanup output:

```bash
gpt-translator cleanup
```

### License

MIT © [Dennis Iversen](https://github.com/diversen)