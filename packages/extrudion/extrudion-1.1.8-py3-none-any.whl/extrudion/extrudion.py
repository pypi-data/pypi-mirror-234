# Copyright 2023 Paride Azzari
#
# Licensed under the MIT License. See LICENSE

import pandas as pd

def analyzeDirectory(folder_path: str = '.', cut_off = True, sample_area = 100) -> pd.DataFrame:
    '''
    Give a folder path as a relative or absolute path, the script will analyze all the .TAR files found in the directory and return a DataFrame containing the results.
    Leaving returns the Current Working Directory.
    '''
    from .files import Folder
    import os
    
    results = pd.DataFrame()
    
    try:
        files = Folder.getList(folder_path)
       
        if not os.path.exists('plots'):
            os.makedirs('plots')
        
        for file in files:
            dataFile = getFile(file, folder_path, sample_area)
            result = analyzeFile(dataFile, cut_off)
            results = pd.concat([results, result])
            
        results = results.rename_axis(index='File')
        results.to_csv(folder_path+'/analysis.csv')
        return results
    
    except FileNotFoundError as e:
        print("File not found error:", e)
    
def analyzeFile(file, cut_off: bool = True):
    '''
    Give a filename and a folder as a relative or absolute path, the script will analyze the .TAR files found and return a DataFrame containing the results.
    '''    
    from .stress import Stress
        
    analysis = Stress(file, cut_off)
    analysis.plot()
    
    results = analysis.results
    results.index = [file.filename.replace('.TRA', '')]
    return results

def getFile(filename: str, folder: str, sample_area = 100):
    from .files import File
    return File(filename, folder, sample_area)    