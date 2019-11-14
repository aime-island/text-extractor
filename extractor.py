from util.argparser import create_parser
from util.modules import (call_extract_multible_xml,
    Counter, Timer, call_xml_cleaner, call_nomrmalization_functions, 
    call_segregation, create_directory, call_combiner, segregation_for_language_model)


parser = create_parser()

def main():
    #Start a timer
    timer = Timer()
    create_directory()

    #call_extract_multible_xml(args)

    #Clean up and create new txt files. Takes in 
    #raw send into clean
    #args.input_dir = r'.\data\05 - raw'
    call_xml_cleaner(args)  


    #Cleaning numbers abbrivitaions and other stuff. Takes in 
    #clean sends to normalized
    args.input_dir = r'.\data\04 - clean'
    call_nomrmalization_functions(args)
    

    #Segregat into a group to use and not to use. Takes in
    #normalized sends into keep/notToKeep
    args.input_dir = r'.\data\03 - normalized'
    call_segregation(args)
    

    args.input_dir = r'.\data\01 - Keep'
    call_combiner(args)

    print(timer.showTimer())
    print('Finished task')

if __name__ == "__main__":
    args = parser.parse_args()
    main()