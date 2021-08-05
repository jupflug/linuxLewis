from boxsdk import OAuth2, Client

def iterate_download(folder,name):
    directories = folder.get_items()
    for directory in directories:
        if directory.name == name:
            return directory

class boxMigrate:
    
    def target_directory(id,secret,token,target_dir):
        auth = OAuth2(client_id=id,
                      client_secret=secret,
                      access_token=token)
        client = Client(auth)
        root_folder = client.root_folder().get()
        
        directories = root_folder.get_items()
        
        for directory in directories:
            if directory.name == target_dir:
                target = directory
                break
        
        return client, target
    
    def download_data(root_directory,subdirs,client,out_path):
        folder = root_directory
        for subdir in subdirs:
            folder = iterate_download(folder,subdir)
        files = folder.get_items()
        for file in files:
            with open(out_path+file.name,'wb') as open_file:
                client.file(file.id).download_to(open_file)
    

    
