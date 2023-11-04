### gpt-translator

This can translate large (and small) text files using the OpenAI API.

Examle usage:

* Convert complex text to simple text.
* Translate text between different languages.

How It Works:

The text is divided into sections, separated by two or more newlines.
A paragraph is a collection of sections, with a default size limit of max 1024 tokens.

Set a custom token limit for paragraphs with `--max-tokens-paragraph`.
Adjust the wait time after errors using `--failure-sleep`. The wait time doubles with each consecutive error, starting from 10 seconds.

Output is saved to `output` dir, which is created if it does not exist. This can be changed setting the `--working-dir`. Default output translation file is `output/output.md`.

### Usage

You need to have an openai API key. 

Add your openai API key to your environment, e.g. in .bashrc 

```bash
export OPENAI_API_KEY=your-api-key
```

Or add the openai API key to a `.env` file in the directory where you execute `gpt-translator`

```bash
OPENAI_API_KEY=your-api-key
```

### Usage as command line tool

Install latest version using pipx

<!-- LATEST-VERSION-PIPX -->
	pipx install git+https://github.com/diversen/gpt-translator@v0.0.9

```bash
gpt-translator translate --help
```
    Usage: gpt-translator translate [OPTIONS]

    Options:
    -f, --from-file TEXT            Source file for translation.  [required]
    -p, --prompt TEXT               Prompt for translation.  [required]
    -d, --working-dir TEXT          Working directory. Default is 'output'
    -m, --max-tokens-paragraph INTEGER
                                    Max tokens per paragraph. Default is 1024
    --failure-sleep INTEGER         Failure sleep time. Default is 10 seconds
    --temperature FLOAT             Temperature. Default is 0.7
    --presence-penalty FLOAT        Presence penalty. Default is 0.1
    --top-p FLOAT                   Top P. Default is 0.99
    --model TEXT                    Model to use. Default is gpt-3.5-turbo
    --help                          Show this message and exit.

Example: 

```bash
gpt-translator translate -f output/hamlet_part.md -p "Translate the following two scenes from Hamlet by Shakespeare to a modern version so that it is easier to understand. It should be as simple as possible, but no simpler."

```

The output file is saved to `output` dir, which is 

Cleanup output:

```bash
gpt-translator cleanup
```

### Usage as requirement

<!-- LATEST-VERSION-PIP -->
	pip install git+https://github.com/diversen/gpt-translator@v0.0.9

For usage see [translate.py](translate.py)

### License

MIT © [Dennis Iversen](https://github.com/diversen)