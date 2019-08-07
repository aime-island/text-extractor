import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description='Text exctractor for RMH',
        add_help=True,
        formatter_class=argparse.MetavarTypeHelpFormatter)

    parser.add_argument(
        '--root_dir', required=False, type=str, help='path to folder')
    
    parser.add_argument(
        '--abbr', required=False, type=bool, default=True, help='Change abbriviations ex. m.a. will be meðal annars')

    parser.add_argument(
        '--nums', required=False, type=bool, default=True, help='Change numbers ex. 123 will be hundrað tuttugu og þrír')

    return parser