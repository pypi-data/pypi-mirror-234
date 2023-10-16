import os
import re
import shutil
import hashlib
import fileinput

def get_list_of_files_in_cur_folder(dir_path : str, pattern : str):
    """
        For the given path, get the List of all files in the current folder

        Parameters
        -----------
        dir_path : str
            The directory path to look into

        Returns
        -----------
        The list of file complete paths
    """
    # create a list of file and sub directories
    # names in the given directory 
    cur_file_list = os.listdir(dir_path)
    file_list = list()
    # Iterate over all the entries
    for entry in cur_file_list:
        # Create full path
        fullPath = os.path.join(dir_path, entry)
        if not os.path.isdir(fullPath):
            if pattern is not None :
                # Checks if the pattern is matching the file
                if re.search(re.compile(pattern), entry) is not None:
                    file_list.append(fullPath)
            else:
                file_list.append(fullPath)
    return file_list

def get_list_of_files(dir_path):
    """
        For the given path, get the List of all files in the directory tree recursively

        Parameters
        -----------
        dir_path : str
            The directory path to look into

        Returns
        -----------
        The list of file complete paths

    """
    # create a list of file and sub directories 
    # names in the given directory 
    cur_file_list = os.listdir(dir_path)
    file_list = list()
    # Iterate over all the entries
    for entry in cur_file_list:
        # Create full path
        fullPath = os.path.join(dir_path, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            file_list = file_list + get_list_of_files(fullPath)
        else:
            file_list.append(fullPath)
    return file_list

"""
    For the given path, get the List of all files in the directory tree 
    Recursive function
"""
def get_list_of_files_in_relative_path(dirName, relativePath='.'):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        currentRelativePath = os.path.join(relativePath, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_list_of_files_in_relative_path(fullPath, currentRelativePath)
        else:
            allFiles.append(currentRelativePath)
                
    return allFiles

"""
    For the given path, get the List of all files in the directory tree 
    Recursive function
"""
def get_list_of_directories_in_relative_path(dirName, relativePath='.'):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allDirectories = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        currentRelativePath = os.path.join(relativePath, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allDirectories.append(currentRelativePath)
            allDirectories = allDirectories + get_list_of_directories_in_relative_path(fullPath, currentRelativePath)           
    return allDirectories

def get_list_of_directories(dir_name):
    """
        For the given path, get the List of all files in the directory tree 
        Recursive function

        Parameters
        -----------
        dir_name : str
            The directory absolute path to look into
        
        Returns
        -----------
        directory_list : list
            A list containing all the folders found in the directory provided
    """
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dir_name)
    directory_list = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            directory_list.append(fullPath)
            directory_list = directory_list + get_list_of_directories(fullPath)           
    return directory_list

"""
    Removes all the files in the provided directory
"""
def remove_all_files_in_directory(dirName):
    listOfFiles = get_list_of_files_in_relative_path(dirName)
    for fileRelativePath in listOfFiles:
        os.remove(os.path.join(dirName, fileRelativePath))

def get_file_base_name(filePath) -> str:
    """
        Get the base name of a file

        Parameters
        -----------
        filePath : str
            The file complete path

        Returns
        -----------
        baseName : str
            The base name of the file without the extension
    """
    splitFileName = os.path.basename(filePath).split('.')
    splitFileName.pop(len(splitFileName) - 1)
    return '.'.join(splitFileName)

 
def unpack_archive(archiveFilePath, extractionFolder, removeArchiveAfterUnpack : bool =False) -> str:
    """
        Unpacks an archive in a folder with the same base name as the archive located in 
        the extraction folder provided

        Parameters
        -----------
        archiveFilePath : str
            The archive complete path

        extractionFolder : str
            The folder to extraction the archive into
        
        removeArchiveAfterUnpack : bool
            A flag to force the deletion of the archive after the unpack

        Returns
        -----------
        archiveExtractionFolder : str
            The complete path of the extracted archive
    """
    archiveFileBaseName = get_file_base_name(archiveFilePath)
    archiveExtractionFolder = os.path.join(extractionFolder, archiveFileBaseName)
    os.makedirs(archiveExtractionFolder, exist_ok=False)
    shutil.unpack_archive(archiveFilePath, archiveExtractionFolder)
    if removeArchiveAfterUnpack:
        os.remove(archiveFilePath)
    return archiveExtractionFolder

def make_archive_from_folder(archiveGenerationFolderPath, folderToArchive, removeFolderAfterPack : bool =False) -> str:
    """
        Makes an archive from the folder provided into the generation folder path provided

        Parameters
        -----------
        archiveGenerationFolderPath : str
            The folder path to generate the archive into

        folderToArchive : str
            The folder to archive

        removeFolderAfterPack : bool
            A flag to force the deletion of the packed folder after archive is created

        Returns
        -----------
        generatedArchivePath : str
            The complete path of the generated archive

    """
    folderToArchiveCompletePath = os.path.join(archiveGenerationFolderPath, folderToArchive)
    generatedArchivePath = shutil.make_archive(archiveGenerationFolderPath, 'zip', folderToArchiveCompletePath)
    if removeFolderAfterPack:
        shutil.rmtree(folderToArchiveCompletePath)
    return generatedArchivePath

def hash(filePath):
    """
        Returns the standard hash of a file 

        Parameters
        -----------
        filePath : str
            The file path

        Returns
        -----------
        fileHash : _Hash
            The file hash

    """
    with open(filePath, 'rb') as f:
        h = hashlib.sha256(f.read()).hexdigest()
    return h.upper()

def replace_text_in_file(filePath : str, originalStr : str, newStr : str) -> None:
    """
        Replace a text inside an existing file

        Parameters
        -----------
        filePath : str
            The file path
        
        originalStr : str
            The original string
        
        newStr : str
            The new string

        Returns
        -----------
        None

    """
    with fileinput.FileInput(filePath, inplace=True) as file:
        for line in file:
            print(line.replace(originalStr, newStr))

def replace_strings_in_file(file_path : str, replacement_dict : dict) -> None:
    """
        Replace one to multiple string inside an existing file

        Parameters
        -----------
        filePath : str
            The file path
        
        replacement_dict : str
            The replacement dictionnary linking an original string to the new string that it should be replaced with

        Returns
        -----------
        None

    """
    # Read in the file
    with open(file_path, 'r') as file :
        filedata = file.read()

    # Replace the target string
    for original_value, new_value in replacement_dict.items():
        filedata = filedata.replace(original_value, new_value)

    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(filedata)

def is_text_in_file(filePath, strToFind : str) -> bool:
    with open(filePath, 'r') as fileReader:
        if strToFind in fileReader.read():
            return True
    return False


def merge_files(mergeFilePath, filesToMerge : list) -> None:
    with open(mergeFilePath, 'w') as outfile:  
        for file in filesToMerge:
            with open(file) as infile:
                outfile.write(infile.read())
