### gpt-translator

This can translate large (and small) text files using the OpenAI API.

Examle usage:

* Convert complex text to simple text.
* Translate text between different languages.

How It Works:

The text is divided into sections, separated by two or more newlines.
A paragraph is a collection of sections, with a default size limit of e.g. 1024 tokens.

Each paragraph is translated using the OpenAI API. The original text and the translated text is
inserted into a sqlite3 database.

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
	pipx install git+https://github.com/diversen/gpt-translator@v0.2.5

```bash
gpt-translator translate --help
 ```
    Usage: gpt-translator translate [OPTIONS]

    Options:
    -f, --from-file TEXT      Source file for translation.  [required]
    -p, --prompt TEXT         Prompt for translation.  [required]
    -d, --working-dir TEXT    Working directory. Default is 'output'
    -m, --max-tokens INTEGER  Max tokens per paragraph. Default is 1024
    -i, --idxs INTEGER        Translate specific paragraphs by index. Default is
                                None
    --failure-sleep INTEGER   Failure sleep time. Default is 10 seconds
    --temperature FLOAT       Temperature. Default is 0.7
    --presence-penalty FLOAT  Presence penalty. Default is 0.1
    --top-p FLOAT             Top P. Default is 0.99
    --model TEXT              Model to use. Default is gpt-3.5-turbo
    --separator BOOLEAN       When exporting text, include part separator.
                                Default is False
    --help                    Show this message and exit.

Example: 

Translate a text file (markdown in this case):

```bash
gpt-translator translate -f input/hamlet_part.md -p "Translate the following two scenes from Hamlet by Shakespeare to a modern version so that it is easier to understand. It should be as simple as possible, but no simpler."
```

The translation will be placed in the `output` directory. In this case the translated text will be placed in a file named `hamlet_part_translated.md`.

Update a translation by idxs:

```bash
gpt-translator translate -f input/hamlet_part.md --separator true --prompt  "Please translate a part of Hamlet to Sindarin (Tolkien dialect). Here is the text you should translate: " --idxs 2
```

Remove database:

```bash
gpt-translator cleanup
```

### Usage as requirement

<!-- LATEST-VERSION-PIP -->
	pip install git+https://github.com/diversen/gpt-translator@v0.2.5

For usage see [translate.py](translate.py)

### License

MIT © [Dennis Iversen](https://github.com/diversen)