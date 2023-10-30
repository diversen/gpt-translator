### gpt-translator

A simple tool for translating text using the openai API.

Give a text file and a prompt and the tool will translate the text file using the prompt.

Translate is in the broadest sense. The tool will use the prompt to generate text that is similar to the text in the file. You can translate a complicated text to a simple text. Or you can translate a text to a different language.

You need to have an openai API key.

Add this to a `.env` file in your environment:

```bash
OPENAI_API_KEY=your-api-key
```

### Install as requirement


```bash
pip install git+https://github.com/diversen/gpt-translator.git
```

For usage see [translate.py](translate.py)

### As command line tool

```bash
pipx install git+https://github.com/diversen/gpt-translator.git
```

```bash
gpt-translator translate --help
```

    Usage: gpt-translator translate [OPTIONS]

    Options:
    -f, --from-file TEXT            Source file for translation.  [required]
    -p, --pre-prompt TEXT           Pre-prompt for translation.  [required]
    -d, --working-dir TEXT          Working directory.
    -i, --idx-begin INTEGER         Index to start from.
    --failure-sleep INTEGER         Failure sleep time.
    --temperature FLOAT             Temperature.
    --presence-penalty FLOAT        Presence penalty.
    --top-p FLOAT                   Top P.
    --max-tokens-paragraph INTEGER  Max tokens per paragraph.
    --model TEXT                    Model to use.
    --help                          Show this message and exit.

Example: 

```bash
gpt-translator translate -f output/winged-death.md -p "Translate the following text to a simple English so that a child aged 12 could read it with ease"
```

### License

MIT © [Dennis Iversen](https://github.com/diversen)