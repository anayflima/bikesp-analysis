import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

class TravelSurveyAnalysis:
    def __init__(self, source_folder_path, destination_folder_path,
                 expansion_factor_trip, expansion_factor_person):
        self.source_folder_path = source_folder_path
        self.destination_folder_path = destination_folder_path
        self.expansion_factor_trip = expansion_factor_trip
        self.expansion_factor_person = expansion_factor_person
    
    def read_data(self, filename, sep = ','):
        data = pd.read_csv(self.source_folder_path + filename, encoding = "ISO-8859-1",
                           sep = sep)
        return data
    
    def treat_csv_file_generated_from_dbf_and_save(self, filename):
        '''
            Site used to convert original dbf file to the csv format:
            https://onlineconvertfree.com/convert/dbf/

            The columns names of the generated csv file had an additional ",N,X,0" in front of it.
            For example:
            ZONA,N,3,0	-> instead of ZONA
            SZ,N,1,0	-> instead of SZ

            Thus, we want to treat the column names to remove everything after the first colon.
        '''
        data = pd.read_csv(self.source_folder_path + filename)
        new_names = [name.split(",")[0] for name in data.columns]
        data.columns = new_names
        data.to_csv(self.source_folder_path + filename[:-4] + '_treated.csv', index=False)
    
    def get_specific_mode_trips(self, df_trips, mode_column, filter_list):
        '''
            filter is a list with the values of the mode_column
            that should be included in the output
        '''
        filter_trips = df_trips[(df_trips[mode_column].isin(filter_list))]
        return filter_trips
    
    def calculate_distribution(self, df, variable_column, expansion_factor, index_map = {}, normalize=True):
        '''
            the parameter "expansion_factor" is either False (boolean)
            or a string with the column that contains the expansion factor
        '''
        
        new_variable_column = variable_column + '_new'
        if index_map != {}:
            df[new_variable_column] = df[variable_column].map(index_map)
        else:
            new_variable_column = variable_column
        
        if expansion_factor:
            df_grouped  = df.groupby(new_variable_column)[expansion_factor].sum()
            if index_map != {}:
                df_grouped = df_grouped[df_grouped.index.isin(list(index_map.values()))]
            if normalize: # if normalize is True, calculate the percentage. Otherwise return the values.
                df_percentage = df_grouped / df_grouped.sum() * 100
            else:
                df_percentage = df_grouped
        else: # expansion_factor is False. Simply calculate the distribution in the column
            df_percentage = df[new_variable_column].value_counts(normalize=normalize) * 100
        
        df_percentage = pd.DataFrame(df_percentage)

        for value in index_map.values():
            if value and value not in df_percentage.index:
                    df_percentage.loc[value] = 0

        return df_percentage

    def treat_duration_column(self, data, duration_column, new_duration_column):
        
        # the duration column must be int (sometimes it's a string). It could also be float
        data[new_duration_column] = data[duration_column].replace('#NULL!', None)
        # Int64 keeps the null values
        data[new_duration_column] = data[new_duration_column].astype('Int64')
        data[new_duration_column].fillna(int(data[new_duration_column].mean()), inplace=True)

        return data

    def plot_histogram_age(self, trips, variable_column, expansion_factor = False,
                            list_bins = [0,15,25,35,45,55,65,75,100],
                            mode = 'bike', save = False):
        '''
            the parameter "expansion_factor" is either False (boolean)
            or a string with the column that contains the expansion factor
        '''
        
        fig, ax = plt.subplots(figsize=(22, 11))

        if expansion_factor:
            sns.histplot(data = trips, x = variable_column, stat = 'percent', bins = list_bins, weights = expansion_factor)
        else:
            ax = sns.histplot(data = trips, x = variable_column, stat = 'percent', bins = list_bins)
        
        for i in ax.containers:
            ax.bar_label(i,fmt='%.1f', fontsize=25)
        
        ax.set_xticks(list_bins)

        ax.set_ylim(bottom = 0, top = 20)

        ax.axes.set_title('Age distribution for ' + mode, fontsize=30, pad = 15)
        ax.set_xlabel('Age (years)',fontsize=25, labelpad = 15)
        ax.set_ylabel('Percentage of trips (%)',fontsize=25, labelpad = 15)
        ax.set_yticklabels(ax.get_yticks(), size=25)
        ax.set_xticklabels(ax.get_xticks(), size=25)

        plt.show()

        if save:
            fig_filename = variable_column + '_expand_' + str(expansion_factor)+ '_' + mode 
            fig_filename = fig_filename.replace(' ', '_')
            ax.figure.savefig(self.destination_folder_path + 'charts/histograms/' + fig_filename, bbox_inches='tight')
    
    def plot_percentage_class(self, data, social_class_column, index_map, bike = False, save = False):
        df = self.calculate_distribution(data, social_class_column, self.expansion_factor_person, index_map)
        plt.figure(figsize=(22, 11))
        ax = df[self.expansion_factor_person].plot(kind='pie', autopct='%1.1f%%', fontsize = 20, ylabel=None)
        ax.set_ylabel(None)
        if bike:
            ax.set_title('Percentage of each class for bike trips', fontsize = 25)
        else:
            ax.set_title('Percentage of each class for all trips', fontsize = 25)
        
        if save:
            fig_filename = 'percentage_class_' + social_class_column + '_expand_' + str(self.expansion_factor_person)
            if bike:
                fig_filename = fig_filename + '_bike'
            else:
                fig_filename = fig_filename + '_all_modes'

            fig_filename = fig_filename.replace(' ', '_')
            ax.figure.savefig(self.destination_folder_path + 'charts/pies/' + fig_filename, bbox_inches='tight')
    
    def plot_mode_separated_by_class(self, data, social_class_column, mode_column, mode_index_map, classes_index_map, save=False):

        nrow=3
        ncol=2
        classes = {1: 'A', 2:'B1', 3:'B2', 4: 'C1', 5:'C2', 6:'D-E'}

        fig, axes = plt.subplots(nrow, ncol)

        fig.patch.set_facecolor('white')
        fig.set_size_inches(11, 18.5)
        fig.suptitle('Percentage of each mode of transportation, separated by class', fontsize = 25)

        count = 1

        percentages_social_class = self.calculate_distribution(data, social_class_column, self.expansion_factor_person, classes_index_map)

        new_variable_column = social_class_column + '_new'
        data[new_variable_column] = data[social_class_column].map(classes_index_map)

        for r in range(nrow):
            for c in range(ncol):
                social_class = classes[count]
                
                if int(percentages_social_class.loc[social_class]) == 0:
                    axes[r,c].axis('equal')  # Set aspect ratio to make it a circle
                    axes[r,c].pie([1], labels=[''], autopct='%1.1f%%', colors = colors)
                else:
                    data_class = data[data[new_variable_column] == social_class]

                    data_plot = self.calculate_distribution(data_class, mode_column, self.expansion_factor_trip, mode_index_map)

                    colors = ['sandybrown', 'limegreen', 'cornflowerblue','hotpink', 'darkorchid']

                    if count == 1:
                        data_plot.plot(ax=axes[r,c], kind='pie', autopct='%1.1f%%', fontsize = 15, colors = colors, y=self.expansion_factor_trip)
                    else:
                        data_plot.plot(ax=axes[r,c],  labels = None, kind='pie', autopct='%1.1f%%', fontsize = 15, colors = colors, y=self.expansion_factor_trip)
                    axes[r,c].get_legend().remove()
                
                percentage_social_class = round(float(percentages_social_class.loc[social_class]),1)
                axes[r,c].set_title('Class ' + social_class +
                                    ': ' + str(percentage_social_class) + '%', fontsize = 15)
                                
                    
                axes[r,c].set(ylabel=None)
                count+=1
        
        plt.subplots_adjust(right=1)

        if save:
            fig_filename = 'mode_per_class_' + social_class_column + '_expand_' + str(self.expansion_factor_person)
            fig_filename = fig_filename.replace(' ', '_')
            fig.savefig(self.destination_folder_path + 'charts/pies/' + fig_filename, bbox_inches='tight')


    def plot_duration_separated_by_class(self, data, duration_column, social_class_column,
                                         classes_index_map, bike=False, expansion_factor = True, save = False):
        nrow=3
        ncol=2

        classes = {0: 'NA', 1: 'A', 2:'B1', 3:'B2', 4: 'C1', 5:'C2', 6:'D-E'}
        # classes = {1: 'A', 2:'B1', 3:'B2', 4: 'C1', 5:'C2', 6:'D-E'}

        fig, axes = plt.subplots(nrow, ncol)

        fig.patch.set_facecolor('white')
        fig.set_size_inches(11, 16)
        if bike:
            fig.suptitle('Duration of bicycle trips, separated by class', fontsize = 25)
        else:
            fig.suptitle('Duration of all trips, separated by class', fontsize = 25)

        new_variable_column = social_class_column + '_new'
        data[new_variable_column] = data[social_class_column].map(classes_index_map)

        expansion_factor =  self.expansion_factor_person if expansion_factor else False

        percentages_social_class = self.calculate_distribution(data, social_class_column,
                                                               expansion_factor,
                                                               classes_index_map)
        count = 1

        for r in range(nrow):
            for c in range(ncol):

                social_class = classes[count]
        
                data_class = data[data[new_variable_column] == social_class]

                data_class.boxplot(ax=axes[r,c],column=[duration_column], fontsize=18)
                
                percentage_social_class = round(float(percentages_social_class.loc[social_class]),1)
                axes[r,c].set_title('Class ' + social_class + ': ' + str(percentage_social_class) + '%', fontsize = 20)
                axes[r,c].set(ylabel=None)
                if bike:
                    axes[r,c].set_ylim(0,120)
                else:
                    axes[r,c].set_ylim(0,180)
                
                start, end = axes[r,c].get_ylim()
                stepsize = 20
                axes[r,c].yaxis.set_ticks(np.arange(start, end+1, stepsize))
                count+=1

        if save:
            fig_filename = 'duration_per_class_' + social_class_column + '_expand_' + str(self.expansion_factor_person)
            if bike:
                fig_filename = fig_filename + '_bike'
            else:
                fig_filename = fig_filename + '_all_modes'
            fig_filename = fig_filename.replace(' ', '_')
            fig.savefig(self.destination_folder_path + 'charts/boxplots/' + fig_filename, bbox_inches='tight')

