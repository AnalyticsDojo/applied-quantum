# The goal of this script is to use the included OS package to read in the site files and generate a sitemap
# This sitemap is necessary for the build process of the website

import os
import platform
import subprocess
from pathlib import Path
from collections import OrderedDict
import time


def get_files(fileList, dirTemp, notebookIndex):
    temp_list = []
    for file in fileList:
        print('     -%s' % file)
        tempString = '  - file: '
        # first we format the string with dir list
        for directoryLevel in dirTemp[notebookIndex:]:
            tempString = tempString + directoryLevel + '/'

        # take only notebook files and append them to output
        fileSplit = file.split('.')
        # we need to handle the case where files are typeless ex: LICENSE files
        if len(fileSplit) == 2 and fileSplit[1] == 'ipynb':
            tempString = tempString + file + '\n'
            temp_list.append(tempString)
    return temp_list

# given a directory, recursively parse and index its files and subdirectories
def traverse_filetree(directory, outputList, os_type):
    print('STARTING TREE AT ROOT: %s' % directory)
    for dirName, subdirList, fileList in os.walk(directory):
        print('STATS: subDirs: %s | files: %s' % (subdirList, fileList))
        # handling case of file systems
        if os_type == 'Windows':
            dirTemp = dirName.split('\\')
        else:
            dirTemp = dirName.split('/')

        # find the index of the 'notebooks' level
        notebookIndex = dirTemp.index('notebooks')

        # making a path out of the directory
        # dirPath = Path(dirName)

        # if there are subdirectories and no file list
        # ex: sub1/    sub2/    subN/
        if subdirList and not fileList:
            print('  ONLY SUBDIRECTORIES FOUND:')
            # for each directory, recurse
            for subDirectory in subdirList:
                print('    -%s' % subDirectory)
                directory_next = Path(directory)
                directory_next = directory_next / subDirectory
                return traverse_filetree(directory_next, outputList, os_type)

        # if there are files and no subdirectories (leaf directory)
        # ex: file1.ipynb    file2.ipynb    fileN.ipynb
        elif fileList and not subdirList:
            print('   ONLY FILES FOUND:')
            files = get_files(fileList, dirTemp, notebookIndex)
            if files:
                outputList.extend(files)
                print('\n\n')
            return outputList

        # if there are both files and dubdirectories
        # ex: sub1/    subN/    file2.ipynb    fileN.ipynb
        elif fileList and subdirList:
            print('   FILES AND SUBDIRS FOUND:')
            # first handle the files in the repo
            print('    FILES:')
            files = get_files(fileList, dirTemp, notebookIndex)
            if files:
                print('      FILES RETURNED: %s |||| TYPE: %s' % (files, type(files)))
                outputList.extend(files)
                print('\n')

            # then recurse on the subdirectories
            for subDirectory in subdirList:
                print('     SUBDIR: - %s' % subDirectory)
                directory_next = Path(directory)
                directory_next = directory_next / subDirectory
                return traverse_filetree(directory_next, outputList, os_type)

        # if there are no files and no subdirectories
        # ex:  [empty directory]
        else:
            print('NOTHING FOUND, EMPTY DIRECTORY')
            return outputList


def notebooks_read():
    os_type = platform.system()
    current_wd = str(os.getcwd())

    # because this automation must be able to run agnostic of the server environment we can pull the os type
    # and switch implementation based on this
    if os_type == "Windows":
        dir_list = current_wd.split('\\')
        site_list = dir_list.copy()
        site_list[len(site_list) - 1] = "site"
        current_wd = site_list.copy()
        site_list.append("notebooks")
        site_dir = ""
        site_path_dir = ""
        # parse to notebooks
        for path in site_list:
            site_dir += path + "\\"

        # parse to site root for later
        for path in current_wd:
            site_path_dir += path + "\\"

    elif os_type == "Linux" or os_type == "Darwin":
        dir_list = current_wd.split('/')
        site_list = dir_list.copy()
        site_list[len(site_list) - 1] = "site"
        current_wd = site_list.copy()
        site_list.append("notebooks")
        site_dir = ""
        site_path_dir = ""
        for path in site_list:
            site_dir += path + "/"

        # parse to site root for later
        for path in current_wd:
            site_path_dir += path + "/"
    else:
        site_path_dir = ""
        site_dir = ""

    # append the notebooks files to the end of the yml following structure defined
    # in the update_yaml function. Because this is a long list, it should appear
    # at the end of the yaml file for structure purposes.
    try:
        site_directory = Path(site_path_dir)
        with open(site_directory / '_toc.yml', "a") as text_file:
            #text_file.write('# =============THE ALGO WROTE THIS ==============================\n')
            text_file.write('- part: NOTEBOOKS\n')
            text_file.write('  numbered: true\n')
            text_file.write('  chapters:\n')
            # with our path set, we can now pull the data and construct our tree

            rootDir = site_dir  # this will start in .../site/notebooks
            # kick off the recursion
            print('STARTING RECURSION')
            outputlist = []
            for dirName, subdirList, fileList in os.walk(rootDir):
                tempList = []
                tempList = traverse_filetree(dirName, outputlist, os_type)
                if tempList:
                    outputlist.extend(tempList)
            filtered_results = list(OrderedDict.fromkeys(outputlist))
            if filtered_results:
                for file in filtered_results:
                    text_file.write(file)
    except subprocess.CalledProcessError as e:
        print("error: " + e)
        return
    time.sleep(60.0)
    print('COMPLETED SUCESSFULLY')
