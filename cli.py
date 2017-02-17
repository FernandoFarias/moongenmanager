import click


@click.group()
def cli():
    pass


@cli.command('evaluate')
@click.option('-o', '--operating-system', nargs=1,
              default='Linux', type=click.STRING,
              help='Operating System name')
@click.option('-t', '--type-evaluation',
              type=click.Choice(['latency', 'throughput']),
              help='Evaluation type latency or throughput')
@click.option('-l', '--lua-trafficgen-dir', default='/usr/src/lua-trafficgen/',
              type=click.Path(exists=True), help='The lua trafficgen directory ')
@click.option('-d', '--description', nargs=1, required=True,
              type=click.STRING, help='The evaluation description e.g (case1 or kernel 4.9)')
@click.option('-b', '--database', type=click.STRING,
              nargs=3, help='The database configuration e.g: 127.0.0.1 user password')
def cmd_eval(operating_system, type_evaluation,
             lua_trafficgen_dir, description, databas):
    pass


@cli.command('consult')
def consult():
    pass


if __name__ == '__main__':
    cli()
