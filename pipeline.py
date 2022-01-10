import logging
logging.basicConfig(level=logging.INFO)
import subprocess

logger = logging.getLogger(__name__)
file = 'heroes'

def _extract():
    logger.info('Starting extract process')
    subprocess.run(['python3', 'main.py'], cwd='./extract')
    subprocess.run(['find', '.', '-name', '{}*'.format(file), '-exec', 'mv', '{}', '../transform/{}_.csv'.format(file), ';'], cwd='./extract')

def _transform():
    logger.info('Starting transform process')
    dirty_data_filename = '{}_.csv'.format(file)
    clean_data_filename = 'clean_{}'.format(dirty_data_filename)
    subprocess.run(['python3', 'main.py', dirty_data_filename], cwd='./transform')
    subprocess.run(['rm', dirty_data_filename], cwd='./transform')
    subprocess.run(['mv', clean_data_filename, '../load/{}.csv'.format(file)], cwd='./transform')

def _load():
    logger.info('Starting load process')
    clean_data_filename = '{}.csv'.format(file)
    subprocess.run(['python3', 'main.py', clean_data_filename], cwd='./load')
    subprocess.run(['rm', clean_data_filename], cwd='load')



def main():
    _extract()
    _transform()
    _load()

if __name__ == '__main__':
    main()