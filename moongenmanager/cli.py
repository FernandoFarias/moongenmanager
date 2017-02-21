import click
import moongenmanager
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - [%(name)s]:[%(levelname)s] - %(message)s')
logger = logging.getLogger("moongenmanager.cli")

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
              nargs=3, help='The database configuration e.g: 127.0.0.1 user password',
              required=True)
def cmd_eval(operating_system, type_evaluation,
             lua_trafficgen_dir, description, database):

    descr = moongenmanager.evaluation.Description()
    descr.os_descr = operating_system
    descr.type_descr = type_evaluation
    descr.eval_descr = description

    m_dir = lua_trafficgen_dir

    config_db = {'host': database[0], 'user': database[1],
                 'password': database[2], 'database': 'moongen'}

    eval_env = {'config_db': config_db,
                'descr_obj': descr, 'm_dir': m_dir}

    evalu = moongenmanager.evaluation.Evaluation(**eval_env)
    logger.info("######## New Evaluation Starting #########")
    evalu.start()

@cli.command('consult')
def consult():
    pass


if __name__ == '__main__':
    
    
    cli()
