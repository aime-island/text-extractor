import argparse
import multiprocessing as mp


def create_parser():
    parser = argparse.ArgumentParser(
        description='Text exctractor for RMH',
        add_help=True,
        formatter_class=argparse.MetavarTypeHelpFormatter)

    parser.add_argument(
        '--root_dir', default =r"C:\Users\dmollberg\OneDrive - Deloitte (O365D)\Aime\CC_BY\althingislog\1933\06", required=False, type=str, help='path to folder')
    parser.add_argument(
        '--root_name', default= '06', required=False, type=str, help='name of rootfolder in dir')
    parser.add_argument(
        '--cores', default= 2, required=False, type=int, help='how many cores to use, default 2')

    return parser