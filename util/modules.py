import os
from reynir import Reynir
import PyPDF2 
from bs4 import BeautifulSoup, SoupStrainer
import re
import enlighten


class Counter():
    def __init__(self):
        self.count_object = 0

    def iterate(self):
        self.count_object = self.count_object +1
    
    def show(self):
        return self.count_object

def get_file_directories(args):
    #Scarapes all files in the rootDir and its subfolders. 
    print(f'Geting list of files form {args.root_dir} and its subfolders')
    counter = Counter() 
    filepath_list = []
    for dirName, _subdirList, fileList in os.walk(args.root_dir, topdown=False):
        for fname in fileList:
            counter.iterate()
            filepath_list.append(dirName + '\\' + fname)

    print(f'Found {counter.show()} files')
    create_file(filepath_list, filename=f'List of file paths for {args.root_name}.txt')
    return filepath_list

def reynir_tidy_text(data):
    #Takes a list or a string and returns a list of str with a text representation of the sentence, with correct spacing between tokens, and em- and en-dashes substituted for regular hyphens as appropriate.

    list_to_return = []

    if type(data) == list:
        #print('Tidying list of sentences')

        # Initialize Reynir and submit the text as a parse job
        r = Reynir() 
        for line in data:
            job = r.submit(line)

            # Iterate through sentences and parse each one
            for item in job:
                item.parse()
                list_to_return.append(item.tidy_text)

    elif type(data) == str:
        #print('Tidying a string')
        r = Reynir()
        job = r.submit(data)
        for item in job:
            item.parse()
            list_to_return.append(item.tidy_text)
    else:
        print('reynir_tidy_text only takes a list or a string\nFor this blasphemy I return you a empty list')
    
    return list_to_return

def create_file(list_of_some_variables, filename='output.txt', mode='w'):
    #Save a list to a file. Defult is "output.txt"
    #print(f'Writing a file named: {filename}')
    with open(filename, mode, encoding='utf8') as file:
        for line in list_of_some_variables:
            file.write(line + '\n')

def open_flie(filename, mode='r'):
    #Opens a file named and returns a list with irs variables.
    print(f'Opening file: {filename}')
    list_to_return =[]
    with open(filename, mode, encoding='utf8') as file:
        for line in file:
            list_to_return.append(line.rstrip())
    return list_to_return   

def xml_extractor(file_directory):
    #print(f'Extracting sentences from {file_directory}')
    
    with open(file_directory, encoding="utf-8") as file:
        #Beacause s contains all the sentences
        soup = BeautifulSoup(file, 'lxml')
    
    sentences = soup.find_all('s') #Beacause s contains all the sentences 

    return [sentence.get_text().replace('\n', ' ') for sentence in sentences]

def extract_multible_xml(args, data, tidy=True):
    '''
    A specify extractor for multible xml files that keep their text in the 's' mark.
    The function extracts text form mulitble files and exports .txt files that have the names of the 
    subfolders in rootfolder.
    The function will call to a formating function called reynir_tidy_text by defult as tidy=True this can 
    be turned of by turning it to False. You might want to turn of reynir_tidy_text as it is quite slow.
    '''
    pbar = enlighten.Counter(total=len(data), desc='Extracting files') 
    name = get_subfolder_name(data[0], args.root_name)
    
    list_to_create = []
    for path in data:
        current_subfolder = get_subfolder_name(path, args.root_name)
        
        
        if name != current_subfolder:
            filename = '.\outPut\\' + name +'.txt'
            create_file(list_to_create, filename)
            list_to_create = []
            name = current_subfolder


        for item in xml_extractor(path):
            if tidy:
                list_to_create.extend(reynir_tidy_text(item))
            else:
                list_to_create.append(item)

        #Compare current subfolder to name. Given that the list_of_file_paths 
        #is linear this will create files with the names of the subfolder and
        #then reset the list_to_create

        #if name == current_subfolder and path 
        pbar.update()
    filename = '.\outPut\\' + name +'.txt'
    create_file(list_to_create, filename)

def get_subfolder_name(directory, rootfolder):
    firstIndex = directory.index(rootfolder) + len(rootfolder)+1
    try:
        secondIndex = directory.index('\\', firstIndex)
    except:
        secondIndex = len(directory)
        
    return directory[firstIndex:secondIndex]


def pdf_extractor(filename):
    #Opens a pdf file and returns the text    

    # creating a pdf file object 
    pdfFileObj = open(filename, 'rb') 
    
    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    
    # printing number of pages in pdf file 
    print(pdfReader.numPages) 
    
    # creating a page object 
    pageObj = pdfReader.getPage(0) 
    
    # extracting text from page 
    #rint(pageObj.extractText()) 
    stringToReturn = pageObj.extractText()
    
    # closing the pdf file object 
    pdfFileObj.close() 
    return stringToReturn 