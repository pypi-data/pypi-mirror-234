Python Package to extract information about the Stress, Strain and Young Modulus from a set of `.TRA` files

# Set up Instructions

Run the following command in the conda/miniconda terminal to install the package:
`pip install extrudion` 

Import the package in your Jupyter project or Python script:
`import extrudion as ex`


# Available commands:
**Analyze a whole directory**
`ex.analyzeDirectory(folder_path, cut_off = True, sample_thickness = 10)` 
plots all the `.TRA` files in the given directory. 


returns a pandas DataFrame containing 

Arguments:
- `folder_path` can be left empty to analyze the current working directory (e.g. `ex.analyzeDirectory()` )
- `folder_path` can be a relative path to a folder within the current working directory (e.g. `ex.analyzeDirectory('data')` )
- `folder_path` can be the absolute path (e.g. `ex.analyzeDirectory('C:\Users\Desktop\extrusion_data')` )

- `cut_off` is by default `True` and must not be specified. If it is true, cuts the data at the max value of Stress
- `sample_thickeness` is the value in `mm` of the size of the sample. The surface of the sample is `sample_thickeness * 10` converted in meters squared. If not specified, a value of 10 mm is assumed.

The results are saved in `analysis.csv` file in the same directory.

**Analyze a single file**
`ex.analyzeFile(*file_path*, folder=[], cut_off = True, sample_thickeness = 10)`

`analyzeFile`, analyzes a single file and returns the pandas.Dataframe with the results as shown below. 
-`folder` must be specified as a second argument
-`cut_off` and `sample_thickness` can be specified as a third argument as shown above.

# Mathematical Formulas

`Stress` = Force['N'] / `sample_thickness` / 10 * 10^3 

returns gives the `stress` in `kPa`

`Strain` = ln( length['mm'] / initial length ['mm'] )

`Young Modulus` = slope of the best line fit for the curve

`Intercept` = the incercet of the previous fit

`Yield Stress and Strain` are the point of intersection for the Young modulus line shifted by 0.02 in the Strain and the data.
# Example
![image](https://github.com/azzarip/extrudion/assets/116155557/f4cefd4a-50b2-45b2-a603-f0fc15f6e8cc)
