import argparse

def create_parser():
    parser = argparse.ArgumentParser(
        description='Text exctractor for RMH',
        add_help=True,
        formatter_class=argparse.MetavarTypeHelpFormatter)

    parser.add_argument(
        '--root_dir', required=True, type=str, help='path to folder')
    parser.add_argument(
        '--root_name', required=True, type=str, help='name of rootfolder in dir')
   
    return parser