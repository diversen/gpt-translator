import click
from gpt_translator.gpt_translator import GPTTranslator
from gpt_translator import file_utils
from gpt_translator import __version__
import logging
import os


# set logging level
logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    pass


@click.command()
@click.option('-f', '--from-file', help='Source file for translation.', required=True)
@click.option('-p', '--prompt', help='Prompt for translation.', required=True)
@click.option('-d', '--working-dir', default='output', help="Working directory. Default is 'output'")
@click.option('-m', '--max-tokens', default=1024, help='Max tokens per paragraph. Default is 1024')
@click.option('-i', '--idxs', default=None, multiple=True, type=int, help='Translate specific paragraphs by index. Default is None')
@click.option('--failure-sleep', default=10, help='Failure sleep time. Default is 10 seconds')
@click.option('--temperature', default=0.7, help='Temperature. Default is 0.7')
@click.option('--presence-penalty', default=0.1, help='Presence penalty. Default is 0.1')
@click.option('--top-p', default=0.99, help='Top P. Default is 0.99')
@click.option('--model', default='gpt-3.5-turbo', help='Model to use. Default is gpt-3.5-turbo')
@click.option('--separator', default=False, help='When exporting text, include part separator. Default is False')
def translate(from_file, prompt, idxs, working_dir, failure_sleep, temperature, presence_penalty, top_p, max_tokens, model, separator):

    translator = GPTTranslator(
        from_file=from_file,
        prompt=prompt,
        working_dir=working_dir,
        failure_sleep=failure_sleep,
        temperature=temperature,
        presence_penalty=presence_penalty,
        top_p=top_p,
        max_tokens=max_tokens,
        model=model,
        part_separator=separator,
    )

    if idxs:
        translator.translate_idxs(idxs)
    else:
        translator.translate()


cli.add_command(translate)


@click.command()
@click.option('-d', '--working-dir', default='output', help='Working directory. Default is output')
def cleanup(working_dir):
    if os.path.exists(working_dir):
        file_utils.cleanup(working_dir)


cli.add_command(cleanup)


@click.command()
def version():
    print(__version__)
    exit(0)


cli.add_command(version)

if __name__ == '__main__':
    cli()
