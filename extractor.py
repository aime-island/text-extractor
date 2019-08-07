from util.argparser import create_parser
from util.modules import (get_file_directories, reynir_tidy_text,
    create_file, open_file, extract_multible_xml, fixNumsAbbrive, 
    Counter, clean_multiple_files, Timer)


parser = create_parser()

def main():
    #Start a timer
    timer = Timer()
    
    #Generate a list of file paths form the driectory hold the xml files
    #list_of_file_paths = get_file_directories(args)

    #Exctract the text in these files 
    #extract_multible_xml(args, list_of_file_paths)
    
    #Generate a list of file paths from the output of extract_multble_xml
    #new_list_of_file_paths = get_file_directories(args)
    
    #print(new_list_of_file_paths)
    #Clean up and create new txt files.    
    #clean_multiple_files(args, new_list_of_file_paths)

    sentence = 'Árið 1231 var konugur danmörks m.a. 1. maðurinn til að brugga bjór\nÁrið 21'
    print(sentence)
    print(fixNumsAbbrive(sentence, args))
    
    print(timer.showTimer())
    print('Finished task')

if __name__ == "__main__":
    args = parser.parse_args()
    main()