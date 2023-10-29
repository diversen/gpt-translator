### Install

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

```bash
gpt-translator translate -f output/winged-death.md -p "Translate the following text to a simple English so that a child aged 12 could read it with ease"
```