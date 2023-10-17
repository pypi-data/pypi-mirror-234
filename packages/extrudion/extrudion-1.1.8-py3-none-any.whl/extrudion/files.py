class Folder:
    class FolderNotFound(Exception):
        pass
    
    @staticmethod
    def getList(folder_path: str) -> str:
        import os
            
        try:
            dir_list = os.listdir(folder_path)
            
            try:
                file_list = [filename for filename in dir_list if filename.endswith('.TRA')]

                if not file_list:
                    print('No .TRA files found in the folder.')
                    return []
                else:
                    return file_list
            
            except FileNotFoundError:
                print('An error occurred while filtering files.')
                raise
            
        except FileNotFoundError:
            raise Folder.FolderNotFound('Folder not found') 
        

class File:
    import pandas as pd
    
    def __init__(self, filename: str, folder: str, sample_area = 100):
        self.filename = filename
        self.folder = folder
        self.sample_area = sample_area
        self.data = self.calculate()
                
    def openFile(self) -> pd.DataFrame:
        import os 
        file = os.path.join(self.folder, self.filename)
        
        import pandas as pd
        return pd.read_table(file, header = [3], encoding = 'ANSI', sep = ',')
        
    def calculate(self) -> pd.DataFrame:
        import pandas as pd
        data = self.openFile()
        
        strain = self.getStrain(data)
        stress = self.getStress(data)
        
        return pd.DataFrame({'strain': strain, 'stress': stress})
        
    def getStress(self, data) -> pd.Series:
        # Divide force by surface in mm to get Pascals, divide by 1000 to get KPascals
        return data['N'] / (self.sample_area) * 1_000_000 / 1000

    
    def getStrain(self, data) -> pd.Series:
        import numpy as np
        return np.log(data['mm.1'] / data['mm.1'][0])