import numpy as np


import pandas as pd
import csv
import matplotlib.pyplot as plt
#from matplotlib import style
# using the style for the plot


plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

def drop_correlations(x_df, percentage = 0.85):
    cor_matrix = x_df.corr().abs()
    upper_tri = cor_matrix.where(np.triu(np.ones(cor_matrix.shape), k=1).astype(bool))  # type: ignore
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > percentage)]
    return x_df.drop(x_df[to_drop].columns, axis=1)

def remove_files(yes = 1):
    if not yes:
        return
    else:
        import os

        directory = "./"
        files_in_directory = os.listdir(directory)
        filtered_files = [file for file in files_in_directory if file.endswith(".tex")]
        filtered_csv_files = [file for file in files_in_directory if 'log' in file and file.endswith(".csv")]

        for file in filtered_files:
            path_to_file = os.path.join(directory, file)
            os.remove(path_to_file)
        for file in filtered_csv_files:
            path_to_file = os.path.join(directory, file)
            os.remove(path_to_file)
        if os.path.exists('log.csv'):
            os.remove('log.csv')
        if os.path.exists('pop_log.csv'):
            os.remove('pop_log.csv')
            
def as_wide_factor(x_df, yes =1, min_factor = 2, max_factor = 8, keep_original = 0, exclude = []):
    if not yes:
        return x_df
    else:
        for col in x_df.columns:
            if col not in exclude:
                factor = len(set(x_df[col]))
                if factor > min_factor and factor < max_factor:
                    if keep_original:
                        x_df[col + str('orig')] = x_df[col]
                    x_df = pd.get_dummies(x_df, columns=[col], prefix=[col], prefix_sep='_')
        return x_df             



def interactions(df, keep = None, drop_this_perc = 0.6):
    interactions = 0
    if interactions:
        interactions = []
        for i, var_i in enumerate(df.columns):
            for j, var_j in enumerate(df.columns):
                if i <= j:
                    continue
                interaction = df[var_i] * df[var_j]
                interactions.append(interaction)
                
        df_interactions = pd.concat(interactions, axis=1)
        df_interactions.columns = [f'{var_i}_{var_j}' for i, var_i in enumerate(df.columns) for j, var_j in enumerate(df.columns) if i < j]
        corr_matrix = df_interactions.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

    # Find features with correlation greater than 0.95
        to_drop = [column for column in upper.columns if any(upper[column] > 0.3)]

    # Drop features 
        df_interactions.drop(to_drop, axis=1, inplace=True)
        #to_drop = [column for column in correlation_matrix.columns if any(correlation_matrix[column] > 0.9)]
        
        #df_interactions = df_interactions.drop(to_drop, axis=1)
        df = pd.concat([df, df_interactions], axis=1, sort = False)
    
    
    #second
    
    corr_matrix = df.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

# Find features with correlation greater than 0.6
    to_drop = [column for column in upper.columns if any(upper[column] > drop_this_perc)]
    if keep is not None:
        to_drop = [column for column in to_drop if column not in keep]
# Drop features 
    df.drop(to_drop, axis=1, inplace=True)
    
    
    return df
    
def check_list_type(lst, check_type):
    for element in lst:
        if not isinstance(element, check_type):
            raise TypeError(f"All elements in the list must be of type {check_type}")


def results_printer(results, algorithm = 'hs', is_multi = 1, obj_1 = 'bic', obj_2 = 'MSE'):
    if algorithm == 'hs':
        plt.scatter([x['bic'] for x in results.harmony_memories], [x['MAE'] for x in results.harmony_memories])
        plt.savefig('bic.svg', format='svg', dpi=1200)
        print('Elapsed time: {}\nBest harmony: {}\nBest fitness: {}\nHarmony memories: {}'.format(results.elapsed_time,
                                                                                                  results.best_harmony,
                                                                                              results.best_fitness,
                                                                                             results.harmony_memories))
    elif algorithm == 'de':
        if is_multi:
            
            plt.plot([x[obj_1] for x in results.best_solutions], [x[obj_2] for x in results.best_solutions], 'o-r')
            plt.xlabel(f'{obj_1.upper()}') #x label
            plt.ylabel(f'{obj_2.upper()}') #y label
            plt.savefig(f'{obj_1}_vs_{obj_2}.svg', format='svg', dpi=1200)
            print('Elapsed time: {}\nPareto Solutions: {} \nPopulation Solutions: {}'.format(results.elapsed_time, results.best_solutions, results.population_solutions))
        else:
            
            print('Elapsed time: {}\nIterations: {}\nIteration_Fitnesses: {}\nBest Fitnessses: {}\nBest Fitness: {}\nBest Struct: {}\nAverage Fitness: {}'.format(
                results.elapsed_time,
                results.iteration, results.iter_solution, results.best_solutions, results.best_fitness, #type: ignore
                results.best_struct, results.average_best)) #type: ignore
    elif algorithm == 'sa':
        print(
            'Elapsed time: {}\nIterations: {}'.format(
                results['elapsed_time'], results['Iteration']
        ))       
                
                
    


def algorithm_set_data(algorithm = 'de'):
    POPULATION = 50; MAX_ITER = 3600;  ADJ_INDX = 1; CR_R = 0.2; INTL_ACCEPT = 0.5;
    STEPS = 20; SWAP_PERC = 0.05; ALPHA_TEMP = 0.99; NUM_INTL_SLNS = 25; IS_MULTI = 1;
    SHARED = list()
    if algorithm == 'de':
       
        with open('set_data.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    algorithm = row['algorithm']
                    POPULATION = int(row['population'])
                    CR_R = float(row['crossover'])
                    MAX_TIME = float(row['max_time'])
                    SEED = int(row['seed'])
                    MAX_ITER = int(row['max_iter'])
                    IS_MULTI = int(row['is_multi'])
                    TEST_SET_SIZE = float(row['test_size'])
                    OBJ_1 = str(row['obj1'])
                    OBJ_2 = str(row['obj2'])
                    if TEST_SET_SIZE == 0:
                        TEST_SET_SIZE = 0
        csv_file.close()
        hyperparameters =  [POPULATION, MAX_ITER, ADJ_INDX, CR_R]
        return hyperparameters
    elif algorithm == 'sa':
        with open('set_data.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    algorithm = row['algorithm']
                    ALPHA_TEMP = float(row['temp_scale'])
                    STEPS = int(row['steps'])
                    MAX_TIME = float(row['max_time'])
                    SEED = int(row['seed'])
                    MAX_ITER = int(row['max_iter'])
                    SWAP_PERC = float(row['crossover'])
                    IS_MULTI = int(row['is_multi'])
                    TEST_SET_SIZE = float(row['test_size'])
                    OBJ_1 = str(row['obj1'])
                    OBJ_2 = str(row['obj2'])
                    if TEST_SET_SIZE == 0:
                        TEST_SET_SIZE = 0
        csv_file.close()
        hyperparameters = [ALPHA_TEMP, MAX_ITER, INTL_ACCEPT, STEPS, SWAP_PERC, NUM_INTL_SLNS, IS_MULTI]
        return hyperparameters
    elif algorithm == 'hs':
        with open('set_data.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    algorithm = row['algorithm']
                    POPULATION = int(row['population'])
                    CR_R = float(row['crossover'])
                    MAX_TIME = float(row['max_time'])
                    SEED = int(row['seed'])
                    MAX_ITER = int(row['max_iter'])
                    HMCR = float(row['hmcr'])
                    PAR = float(row['par'])
                    IS_MULTI = int(row['is_multi'])
                    TEST_SET_SIZE = float(row['test_size'])
                    OBJ_1 = str(row['obj1'])
                    OBJ_2 = str(row['obj2'])
                    if TEST_SET_SIZE == 0:
                        TEST_SET_SIZE = 0
        csv_file.close()
        
def entries_to_remove(entries, the_dict):
    for key in entries:
        if key in the_dict:
            del the_dict[key]