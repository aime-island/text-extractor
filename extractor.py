from util.argparser import create_parser
from util.modules import (get_file_directories, reynir_tidy_text,
    create_file, open_file, extract_multible_xml, normalization, 
    Counter, Timer, clean_text_from_xml_multiple)


parser = create_parser()

def main():
    #Start a timer
    timer = Timer()

    #Generate a list of file paths from the output of extract_multble_xml
    list_of_file_paths = get_file_directories(args)

    extract_multible_xml(args, list_of_file_paths)

    #Generate a list of file paths from the output of extract_multble_xml
    list_of_file_paths = get_file_directories(args, from_where='./outPut/raw')
    print(list_of_file_paths)
    #Clean up and create new txt files.    
    clean_text_from_xml_multiple(args, list_of_file_paths)

    print(timer.showTimer())
    print('Finished task')

if __name__ == "__main__":
    args = parser.parse_args()
    main()