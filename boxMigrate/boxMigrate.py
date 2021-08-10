from boxsdk import OAuth2, Client
import numpy as np
import netCDF4 as nc
import os

def iterate_download(folder,name):
    directories = folder.get_items()
    for directory in directories:
        if directory.name == name:
            return directory
        
def filterNC_latlon(dsetName,keys,lat,lon,laty,lonx):
    
    print(dsetName)
    
    dset = nc.Dataset(dsetName)
    dim_len = len(dset.dimensions)
#     print(dim_len)
    
    if dim_len == 3:
        lonx = []
        laty = []
        
        idx = np.abs(dset['Longitude'][:] - lon.min()).argmin()
        if idx > 0:
            idx = idx - 1
        lonx.append(idx)   
        idx = np.abs(dset['Longitude'][:] - lon.max()).argmin()
        if idx < len(dset['Longitude'][:]):
            idx = idx + 1
        lonx.append(idx)
    #     print(lonx)

        idx = np.abs(dset['Latitude'][:] - lat.min()).argmin()
        if idx < len(dset['Latitude'[:]]):
            idx = idx + 1
        laty.append(idx)
        idx = np.abs(dset['Latitude'][:] - lat.max()).argmin()
        if idx > 0:
            idx = idx - 1
        laty.append(idx)
    #     print(laty)
    
    ds = nc.Dataset(os.path.splitext(dsetName)[0]+'_filt.nc','w',format='NETCDF4_CLASSIC')
    Longitude = ds.createDimension('Longitude',lonx[1]-lonx[0])
    var = ds.createVariable('Longitude', 'f4', ('Longitude',))
    var[:] = dset['Longitude'][lonx[0]:lonx[1]]
    Latitude = ds.createDimension('Latitude',laty[0]-laty[1])
    var = ds.createVariable('Latitude', 'f4', ('Latitude',))
    var[:] = dset['Latitude'][laty[1]:laty[0]]
    
    countUp = 0
    for key in keys:
        try:
            test = dset[key]
            countUp += 1
            if dim_len == 3:
                value = dset[key][:,lonx[0]:lonx[1],laty[1]:laty[0]]
                if countUp == 1:
                    Day = ds.createDimension('Day',len(dset[key][:,1,1]))
                var = ds.createVariable(key, 'f4', ('Day', 'Longitude', 'Latitude',))
                var[:,:,:] = value
            else:
                value = dset[key][:,:,lonx[0]:lonx[1],laty[1]:laty[0]]
                if countUp == 1:
                    Day = ds.createDimension('Day',len(dset[key][:,1,1,1]))
                    Stats = ds.createDimension('Stats',len(dset[key][1,:,1,1]))
                var = ds.createVariable(key, 'f4', ('Day', 'Stats', 'Longitude', 'Latitude',))
                var[:,:,:,:] = value
        except:
            print("An exception occurred")
    
    print(lonx)
    print(laty)
    dset.close()
    ds.close()
    
    os.remove(dsetName)
    
    return lonx, laty
    

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
    
    def download_data(root_directory,subdirs,client,out_path,**kwargs):
        folder = root_directory
        for subdir in subdirs:
            folder = iterate_download(folder,subdir)
        files = folder.get_items()
        lonx = []
        laty = []
        for file in files:
            with open(out_path+file.name,'wb') as open_file:
                client.file(file.id).download_to(open_file)
                
                if kwargs.get('filter', None) == 'latlon':
                    keys = kwargs.get('keys')
                    lon = kwargs.get('lon')
                    lat = kwargs.get('lat')
                    
                    fname = open_file.name
                    open_file.close()
                    lonx,laty = filterNC_latlon(fname,keys,lat,lon,laty,lonx)
        return
    

    
