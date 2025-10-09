##TODO - how to make it useful for the user to use this ? desktop app with a ui ?
# worth checking - https://code-b.dev/blog/building-desktop-applications-using-python

import os
import shutil
import logging

from enum import Enum

logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  
)

logger = logging.getLogger(__name__)

#### Assignment 1
# create different folders and put the contents of the folder in respective folders 

'''
What it does 
On a particular folder location , it will scan all the files in the location and move the files to appropriate folders 

It can revert the changes made as well in the same session 
logging implementation - use log instead of print - basic logging implemented 

Future implementations:
-Effective try catch / exception handling 
-Extracting this out as its own utility or could it be run as a script ?
-May be creating another utility function to extract all the files outside of all the folders ( a pre-requisite for further sorting )
-Providing the ways to the user to customize the folder names as per their requirement 



'''


class FolderName(Enum):
    TEXT = ".txt"
    PDF = ".pdf"
    WORD = ".docx"
    IMAGES = (".png", ".jpeg", ".jpg", ".gif", ".bmp")
    VIDEO = ".mp4"
    AUDIO = ".mp3"
    CERTIFICATES = ".crt"
    WORKBOOKS = (".xls",".xlsx")
    OTHER = "other"
    
    def get_enum_name_by_value(value):
        for folder in FolderName:
            if isinstance(folder.value, tuple):
                # Check if the value is in the tuple of image formats
                if value in folder.value:
                    return folder.name  # Return the name of the enum member
            elif folder.value == value:
                return folder.name  # Return the name if it matches directly1
        return FolderName("other").name
        


def get_files_list_from_location(base_location):
    
    initial_list = os.listdir(base_location)
    files_list = []
    for item in initial_list:
        if os.path.isdir(os.path.join(base_location,item)):
            logger.info(f"This is a directory: {item}")
        else:
            files_list.append(item)
            logger.info("-----appended--------")
    return sorted(files_list)
    
def extract_file_extension_from_folder(sorted_listdir):
    extension_list = []

    for files in sorted_listdir:
        print(os.path.splitext(files))
        extension_list.append(os.path.splitext(files)[1])
    
    print(f"extension set extracted successfully {extension_list} ")  # TODO replace with logs 
        
    return set(extension_list)

# todo - check if not used now ?
def strip_off_particular_character_from_list(list_for_sanitization,character_to_strip):
        sanitized_extracted_extensions = []
    
        for extension in list_for_sanitization:
            sanitized_extracted_extensions.append(extension.strip(character_to_strip))
        
        logger.info(f"stripping off {character_to_strip} from list. sanitized list is : {sanitized_extracted_extensions} ") # TODO replace with logs 
        
        return sanitized_extracted_extensions
        

def create_folder_based_on_list_items(input_list,path_where_folder_is_required_to_be_created):
    # sanitize input_list and replace it with the values 
    folder_names = get_unique_folder_names(input_list)
     
    # create folder based on the new list 
    for file in folder_names:
         logger.info(f"----folder_name is : {file}")
         directory_path = os.path.join(path_where_folder_is_required_to_be_created,file)
         if not os.path.exists(directory_path):
             os.mkdir(directory_path)
             logger.info(f"folder created for {file} ")  # TODO replace with logs 
         else:
             logger.info(f"Directory '{directory_path}' already exists, skipping creation.")        


def get_unique_folder_names(folder_list):
    folder_names = []
    for name in folder_list:
         folder_names.append(FolderName.get_enum_name_by_value(name))
    
    logger.info(f"folder names extracted are : {set(folder_names)}") 
    return set(folder_names)

def move_files_to_related_folders(file_extensions,files_to_move,base_path):
        for ext in file_extensions:
            destination_folder = os.path.join(base_path,FolderName.get_enum_name_by_value(ext))
            for file in files_to_move:
                source_path = os.path.join(base_path,file)
                destination_path = os.path.join(destination_folder,file)
                if os.path.splitext(file)[1]== ext:
                    shutil.move(source_path,destination_path)
                
        logger.info("---Moving files to related folders completed---, Awesome Job!! ")  # TODO replace with logs  

    
    
    
def reverting_changes(folder_list,files_to_move,base_path):
     unique_folder_names = get_unique_folder_names(folder_list)
     
     for name in unique_folder_names:
         source_base_path = os.path.join(base_path,name)
         # find the number of files 
         for file in os.listdir(source_base_path):
             destination_path = os.path.join(base_path,file)
             source_path = os.path.join(source_base_path,file)
             shutil.move(source_path,destination_path) 
             if os.path.exists(source_base_path) and os.path.isdir(source_base_path):
                 entries = os.listdir(source_base_path)
                 if not entries:
                     os.rmdir(source_base_path)
                     logger.info(f" the directory {source_base_path} is deleted") 
                 else:
                     logger.info(f" the directory {source_base_path} is still not empty") 
     logger.info("------------Changes Reverted Successfully--------------------")
                
   
   
def glued(folder_path):
    files_under_consideration = get_files_list_from_location(folder_path)
            
    logger.info(f" your sorted file names are {files_under_consideration}")
    
    extracted_extensions=extract_file_extension_from_folder(files_under_consideration)
    logger.info(f"extracted extensions from the files are : {extracted_extensions}")
    
    create_folder_based_on_list_items(extracted_extensions,folder_path)
    
    move_files_to_related_folders(extracted_extensions,files_under_consideration,folder_path)
    
    revert_changes = input("Do you want to revert the changes ? Answer Y or N: ")
    
    if revert_changes.upper() == "Y":
        reverting_changes(extracted_extensions,files_under_consideration,folder_path)


def main():
    
    name = input("Hi There , What is your awesome name ? :")
    want_to_use = input(f"Hi {name} ! Are you ready to use the cleanup utility ? : Y or N : ")
    if want_to_use.upper()=="Y":
        folder_path = input("Please Enter the path where you want the cleanup :")
        glued(folder_path)
    else:
        print("Sorry to hear you don't want to use this awesome utility")
        
        
        
    

# test the working code
    #folder_path = "xx"
   
    
 ##---------------------working---------------------------- 
    # files_under_consideration = get_files_list_from_location(folder_path)
            
    # print(f" your sorted file names are {files_under_consideration}")
    
    # extracted_extensions=extract_file_extension_from_folder(files_under_consideration)
    # print(f"extracted extensions from the files are : {extracted_extensions}")
 ##---------------------working----------------------------
 
    # sanitize the list to remove the . from the front
        
    # sanitized_extension_list= strip_off_particular_character_from_list(extracted_extensions,'.')
    
    
    ##---------------------working----------------------------
    # create_folder_based_on_list_items(extracted_extensions,folder_path)
    
    # move_files_to_related_folders(extracted_extensions,files_under_consideration,folder_path)

    
    #reverting_changes(extracted_extensions,files_under_consideration,folder_path)

  
  
if __name__ == "__main__":
    main()





