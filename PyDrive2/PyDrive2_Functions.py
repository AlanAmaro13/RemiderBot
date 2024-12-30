#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Just functions
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

def authentication(cred: str = "mycreds.txt"):
    '''
    Do the authentication using credencials and returns the drive objetc

    Args: 
        cred (str) - Path to save the credentials

    Return: Drive object 
    '''
    try:
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(cred)  # Load previously saved credentials
        if not gauth.credentials:
            gauth.LoadClientConfigFile()  # Use the downloaded credentials.json
            gauth.LocalWebserverAuth()  # Authenticate using a local web server
            gauth.SaveCredentialsFile(cred)  # Save the credentials for future use
        return GoogleDrive(gauth)
    except Exception as e:
        print(e)

def get_file_id_from_link(link: str):
    '''
    Returns the object id of a folder or document 
    '''
    if "id=" in link:
        return link.split("id=")[1]
    elif "d/" in link:
        return link.split("d/")[1].split("/")[0]
    elif "folders/" in link:
        return link.split("folders/")[1].split("?")[0]
    else:
        raise ValueError("Invalid Google Drive link")

def download_folder_files(folder_id, download_path: str = './DriveFiles'):
    '''
    Download all the files in a Drive folder:

    Args:
        folder_id (str): The id in the link path 
        download_pat (str): This path will create a folder to save the files

    Return: True if all the documents were downloaded
    '''
    os.makedirs(download_path, exist_ok = True)
    
    # Query for files in the folder
    query = f"'{folder_id}' in parents and trashed=false"
    file_list = drive.ListFile({'q': query}).GetList()
    
    # Download each file
    try:    
        for file in file_list:
            print(f"Downloading {file['title']}...")
            file.GetContentFile( f"{download_path}/{file['title']}"   )
        print('True')
    except Exception as e:
        print('False: ', e)

def download_just_one(file_id: str):
    file = drive.CreateFile({'id': file_id})
    file_name = file['title']  # Get the file name
    data = file.GetContentFile(file_name)  # Download the file
    print(f"File '{file_name}' downloaded successfully!")

def update_a_file(path_to_file: str, file_id: str):
    try:
        file = drive.CreateFile({'id': file_id})
        file.SetContentFile(path_to_file)
        file.Upload()

        return print(True)

    except Exception as e:
        return print(False, e)
    
