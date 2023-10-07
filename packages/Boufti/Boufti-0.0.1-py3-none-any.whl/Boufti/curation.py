# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 16:46:21 2023

@author: Bart Steemans. Govers Lab.
"""
import pickle
import pandas as pd
import numpy as np

class Curation:
    
    def __init__(self, svm_df):
        
        self.svm_df = svm_df
        self.features = None
        self.curated_df = None
        self.svm_model = None
    
    def compiled_curation(self, path_to_model, cols):
        self.load_model(path_to_model)
        self.prepare_dataframe(cols)
        curated_df = self.make_predictions()
        return curated_df
        
    def load_model(self, path_to_model):
        with open(path_to_model, 'rb') as f:
            self.svm_model = pickle.load(f)
    
    def prepare_dataframe(self, cols):

        self.features = self.svm_df.iloc[:, cols:]
        
        self.features[self.features.select_dtypes(include=[np.number]).columns] = \
            self.features.select_dtypes(include=[np.number]).astype(float)
    
        # Check for infinite values and NaNs
        has_infinite = np.any(np.isinf(self.features.select_dtypes(include=[np.number])))
        has_nan = np.any(np.isnan(self.features.select_dtypes(include=[np.number])))
    
        if has_infinite or has_nan:
            # Create a boolean mask for rows without infinite or NaN values
            mask = ~(np.isinf(self.features.select_dtypes(include=[np.number])).any(axis=1) |
                     np.isnan(self.features.select_dtypes(include=[np.number])).any(axis=1))
    
            # Filter the DataFrame to keep only rows without infinite or NaN values
            svm_training_filtered = self.features[mask]
            
            # Print the number of removed rows
            num_removed_rows = len(self.features) - len(svm_training_filtered)
            print(f"\nNumber of removed rows: {num_removed_rows}")
    
            # Update svm_training with the filtered DataFrame
            self.features = svm_training_filtered
            self.svm_df = self.svm_df[mask]
            
        else:    
            print("\nNo rows removed")         
        
    def get_label_proportions(self):
        label_counts = self.curated_df['label'].value_counts()
        total_samples = len(self.curated_df)
        
        proportion_label_1 = label_counts.get(1, 0) / total_samples
        proportion_label_0 = label_counts.get(0, 0) / total_samples
        
        return proportion_label_1, proportion_label_0
    
    def make_predictions(self):
        # Make predictions using the SVM model
        predictions = self.svm_model.predict(self.features)
    
        # Assuming 'label' column is missing in the DataFrame, add the predicted labels
        self.curated_df = self.svm_df.copy()
        self.curated_df['label'] = predictions
    
        return self.curated_df
    
    def get_control(self, num_pos=5, num_neg=5):
        # Get the cell IDs of positive and negative classes from curated_df
        positive_cell_ids = self.curated_df[self.curated_df['label'] == 1]['cell_id'].tolist()
        negative_cell_ids = self.curated_df[self.curated_df['label'] == 0]['cell_id'].tolist()
        positive_cell_ids_random = np.random.choice(positive_cell_ids, size=num_pos, replace=False)
        negative_cell_ids_random = np.random.choice(negative_cell_ids, size=num_neg, replace=False)
    
        return np.array(positive_cell_ids_random, dtype = int), np.array(negative_cell_ids_random, dtype = int)