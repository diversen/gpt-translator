import click
from gpt_translator.gpt_translator import GPTTranslator


@click.group()
def cli():
    pass

@click.command()
@click.option('--from-file', default='', help='Source file for translation.')
@click.option('--pre-prompt', default='', help='Pre-prompt for translation.')
@click.option('--working-dir', default='./output', help='Working directory.')
@click.option('--idx-begin', default=0, help='Index to start from.')
@click.option('--failure-sleep', default=10, help='Failure sleep time.')
@click.option('--temperature', default=0.7, help='Temperature.')
@click.option('--presence-penalty', default=0.1, help='Presence penalty.')
@click.option('--top-p', default=0.99, help='Top P.')
@click.option('--max-tokens-paragraph', default=1024, help='Max tokens per paragraph.')
@click.option('--model', default='gpt-3.5-turbo', help='Model to use.')
def translate(from_file, pre_prompt, working_dir, idx_begin, failure_sleep, temperature, presence_penalty, top_p, max_tokens_paragraph, model):
    translator = GPTTranslator(
        from_file=from_file,
        pre_prompt=pre_prompt,
        working_dir=working_dir,
        idx_begin=idx_begin,
        failure_sleep=failure_sleep,
        temperature=temperature,
        presence_penalty=presence_penalty,
        top_p=top_p,
        max_tokens_paragraph=max_tokens_paragraph,
        model=model
    )
    translator.translate()

cli.add_command(translate)

if __name__ == '__main__':
    cli()
