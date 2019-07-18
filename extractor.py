from util.argparser import create_parser
from util.modules import (get_file_directories, reynir_tidy_text,
    create_file, open_flie, extract_multible_xml, Counter)


parser = create_parser()

def main():
    #Generate a list of file
    list_of_file_paths = get_file_directories(args)

    #Exctract the text in these files 
    extract_multible_xml(args, list_of_file_paths, tidy=True)


    print('Finished task')
if __name__ == "__main__":
    args = parser.parse_args()
    main()