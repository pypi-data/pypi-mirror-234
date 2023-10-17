import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.interpolate import griddata
import matplotlib.cm as cm
from matplotlib.ticker import ScalarFormatter,AutoMinorLocator
import matplotlib as mpl
plt.style.use('plt_style.txt')



os.chdir(os.path.expanduser('Z:/single_objective_synth/inner_again'))

paran_data = "set_data.csv"
param_data_df = pd.read_csv(paran_data)
problem_number = 5
folders = param_data_df[param_data_df['problem_number'] ==problem_number]
folders = folders.index.values
spread_checker = 100000
for i in folders:
   
    file = str(i) +"/log.csv"
    try:
        
        df = pd.read_csv(file, on_bad_lines='skip')
        # Only keep the rows where the pvalue_exceed column is 0
        df = df[df['incumbent_pval_exceed'] == 0]
        df = df.reset_index(drop =True)
        print('good', i)
        x = df['incumbent_bic']
        
        
      

# Calculate weighted average
       

        
        
        if param_data_df['algorithm'][i] == 'de':
            param_1 = param_data_df['_hms'][i]
            param_2 = param_data_df['crossover'][i]
            val =min(x)
         
        if param_data_df['algorithm'][i] == 'hs':
            param_1 = param_data_df['_hms'][i]
            param_2 = param_data_df['_hmcr'][i]
            param_3 = param_data_df['_par'][i]
            
            val = min(x)
            
         
        if param_data_df['algorithm'][i] == 'sa':
            param_1 = param_data_df['crossover'][i]
            param_2 = param_data_df['temp_scale'][i]
            param_3 = param_data_df['steps'][i]
            
            val = min(x)
            
        
            
        if min(x) < spread_checker:
            spread_checker = min(x)
            print('best_folder is', i, 'with', spread_checker)
            store_2 = file
       
    except:
        print(i)
        