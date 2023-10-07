
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 16:47:19 2023

@author: Bart Steemans. Govers Lab.
"""

import os
import pickle
from . import utilities as u
from tqdm import tqdm
from .image import Image
from .omni import Omnipose
from .curation import Curation
import pandas as pd   
import torch
import multiprocessing


class ImageCollection: 
    
    def __init__(self, image_folder_path = None):
        
        self.images = None
        self.masks = None
        self.channel_images = None
        self.channel_list = None
        self.image_filenames = None
        self.image_folder_path = image_folder_path
        self.name = os.path.basename(self.image_folder_path)
        self.image_objects = []
        
        self.mesh_df_collection = pd.DataFrame()
        
        self.all_features_df = None
        self.svm_features_df = None
        
        
    def load_masks(self):
        self.masks, self.mask_filenames = u.read_tiff_folder(self.image_folder_path + '/masks')
        
    def load_phase_images(self, phase_channel = ''):
        self.images, self.image_filenames, self.paths = u.read_tiff_folder(self.image_folder_path, phase_channel, include_paths = True)
    
    def load_channel_images(self, channel_list):
        self.channel_list = channel_list
        self.channel_images = u.read_channels(self.image_folder_path, self.channel_list)
        
    def create_image_objects(self, channel_list = None, phase_channel=''):
        
        if self.masks is None:
            self.load_masks()
            self.load_phase_images(phase_channel)
            
        if channel_list:
            self.channel_images = self.load_channel_images(channel_list)
            
        self.image_objects = []
    
        for i, image_name in enumerate(self.image_filenames):
            
            image = self.images[i]
            mask = self.masks[i]
            mesh_df = self.get_mesh_dataframe(image_name)
    
            img_obj = self.create_image_object(image, image_name, i, mask, mesh_df)
            
            self.add_channels(img_obj, self.channel_images, i)

            self.image_objects.append(img_obj)
            
    def add_channels(self,img_obj, channel_images, i):
        channel_single_image_dict = {}
        if self.channel_images is not None:  # Check if self.channel_images is not None
            for channel, images in self.channel_images.items():
                channel_single_image_dict[channel] = images[i]
        img_obj.channel = channel_single_image_dict
        
        
    def get_mesh_dataframe(self, image_name):
        
        if not self.mesh_df_collection.empty:
            return self.mesh_df_collection[self.mesh_df_collection['frame'] == image_name].reset_index(drop=True)
        else:
            return None
    
    def create_image_object(self, image, image_name, index, mask, mesh_df):
        img_obj = Image(image, image_name, index, mask, mesh_df)
        if mesh_df is not None:
            img_obj.create_cell_object(verbose=False)
        return img_obj
            
# Methods for batch processing of images ----------------------------------------------  
    def segment_images(self, mask_thresh, minsize, n, model_name = 'bact_phase_omni'):
        omni = Omnipose(self.images, self.paths)
        omni.load_models(model_name)
        
        omni.compiled_process(n, mask_thresh, minsize)
        torch.cuda.empty_cache()
        del omni
    
    def batch_detect_objects(self, folder_path, channel_suffix = '', channel_list = None, log_sigma = 3, kernel_width = 4, 
                             min_overlap_ratio=0.01, max_external_ratio=0.1):
        
        if self.channel_images is None:
            self.load_channel_images(channel_list)
            
            for i, image_obj in enumerate(self.image_objects):
                self.add_channels(image_obj, self.channel_images, i)
                
        print("\nDetecting objects within cell ...")
        
        dfs = (image.object_detection(folder_path, channel_suffix, 
                                      log_sigma, kernel_width, 
                                      min_overlap_ratio, 
                                      max_external_ratio) for image in tqdm(self.image_objects))
        self.object_detection_df = pd.concat(dfs, axis=0)
        
        return self.object_detection_df
    
    def batch_process_mesh(self, pkl_name = None, object_list = None, phase_channel = '', join_thresh = 4, split_thresh = 0.35):
        
        self.mesh_df_collection = pd.DataFrame()
        
        if isinstance(object_list, Image):
            
            print(f'\nProcessing image: {object_list.image_name}')
            
            object_list.join_split_pipeline(join_thresh, split_thresh)
            
            self.mesh_df_collection = getattr(object_list, 'processed_mesh_dataframe')
            
            object_list.create_cell_object(verbose=False)
            
        else:
            
            if object_list is None:
                self.create_image_objects(phase_channel = phase_channel)  
                
                object_list = self.image_objects

            for img_obj in object_list:
                print(f'\nProcessing image: {img_obj.image_name}')
                
                img_obj.join_split_pipeline(join_thresh, split_thresh)
                
                self.mesh_df_collection = pd.concat([self.mesh_df_collection, getattr(img_obj, 'processed_mesh_dataframe')])
                
                img_obj.create_cell_object(verbose=False)

        if pkl_name is not None:
            
            self._to_pickle(pkl_name, self.mesh_df_collection)
            
        self._to_pickle("{}_meshdata.pkl".format(self.name), self.mesh_df_collection)
        
        
    def batch_load_mesh(self, pkl_name, pkl_path = None, phase_channel = ''):
        
        self.mesh_df_collection = pd.DataFrame()
        
        if pkl_path is None:
            
            pkl_path = self.image_folder_path
            
        with open(os.path.join(pkl_path, pkl_name), 'rb') as f:
            self.mesh_df_collection = pickle.load(f)
            
        print(f'\nMeshes are loaded from a pickle file named {pkl_name}')  
        
        self.create_image_objects(phase_channel = phase_channel)
         
        
    def batch_mask2mesh(self, pkl_name = None, object_list = None, phase_channel=''):
        
        self.mesh_df_collection = pd.DataFrame()

        if isinstance(object_list, Image):
            print(f'\nProcessing image: {object_list.image_name}')
            
            object_list.mask2mesh()
            self.mesh_df_collection = getattr(object_list, 'mesh_dataframe')
            object_list.create_cell_object(verbose=False)
        else:
            
            if object_list is None:
                self.create_image_objects(phase_channel=phase_channel)
                object_list = self.image_objects
            
            for img_obj in object_list:
                print(f'\nProcessing image: {img_obj.image_name}')
                
                img_obj.mask2mesh()
                self.mesh_df_collection = pd.concat([self.mesh_df_collection, getattr(img_obj, 'mesh_dataframe')])
                
                img_obj.create_cell_object(verbose=False)
        
        if pkl_name is not None:
            self._to_pickle(pkl_name, self.mesh_df_collection)

        self._to_pickle("{}_meshdata.pkl".format(self.name), self.mesh_df_collection)

    def batch_calculate_features(self, add_profiling_data=True, svm=False):
        
        feature_dfs = []
    
        for image in tqdm(self.image_objects):
            df = image.calculate_features(add_profiling_data, svm)
            feature_dfs.append(df)
    
        combined_df = pd.concat(feature_dfs, axis=0)
    
        if svm:
            self.svm_features_df = combined_df
        else:
            self.all_features_df = combined_df

        return combined_df
    
    def curate_dataset(self, path_to_model, cols = 4):
        
        self.batch_calculate_features(svm=True)
        cur = Curation(self.svm_features_df)
        self.curated_df = cur.compiled_curation(path_to_model, cols)
        
        p1, p0 = cur.get_label_proportions()
        print(f"\nProportion of label 1: {p1}")
        print(f"Proportion of label 0: {p0}")

        for index, row in self.curated_df.iterrows():
            frame = row['frame']
            cell_id = row['cell_id']
            label = row['label']
            
            # Find the Image object in the list based on the 'frame' index
            image = self.image_objects[frame]
            
            # Find the Cell object in the Image object based on the 'cell_id' index
            cell = next((c for c in image.cells if c.cell_id == cell_id), None)
            
            if cell is not None and label == 0:
                # Remove the Cell object from the list of Cells within the Image object
                image.cells.remove(cell)
    
    
    
    def dataframe_to_pkl(self, dataframe = 'features'):
        
        if dataframe == 'features':
            
            self._to_pickle("{}_features.pkl".format(self.name), self.all_features_df)
            
        elif dataframe == 'svm_features':
            
            self._to_pickle("{}_svm_features.pkl".format(self.name), self.svm_features_df)
        
        elif dataframe == 'channel_objects':
            
            self._to_pickle("{}_channel_objects.pkl".format(self.name), self.object_detections)
            

    def _to_pickle(self, pkl_name, data):
        """
        Save data to a pkl file.

        """
        file_path = os.path.join(self.image_folder_path, pkl_name)
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
    

class Pipeline:
    
    def __init__(self):
        self.exp_folder_path = None
    

    #@profile
    def general_pipeline(self, exp_folder_path, **kwargs):
        
        self.exp_folder_path = exp_folder_path
        
        subfolder_paths = [os.path.join(exp_folder_path, directory) for directory in os.listdir(exp_folder_path) if os.path.isdir(os.path.join(exp_folder_path, directory))]
        print(f'\nProcessed folders are: {subfolder_paths}')
        
        for image_path in subfolder_paths:  
            ic = ImageCollection(image_path)
            
            if 'segment' in kwargs and kwargs['segment']:
                ic.load_phase_images(phase_channel=kwargs.get('phase_channel', ''))
                i = len(ic.images)
                ic.segment_images(kwargs.get('mask_thresh', 1), kwargs.get('minsize', 300), n=range(i))
            
            if 'load_mesh' in kwargs and kwargs['load_mesh']:
                filename = ic.name + '_meshdata.pkl'
                ic.batch_load_mesh(filename, phase_channel=kwargs.get('phase_channel', ''))
            else:
                ic.batch_process_mesh(
                    object_list=None,
                    phase_channel=kwargs.get('phase_channel', ''),
                    join_thresh=kwargs.get('join_thresh', 4),
                    split_thresh=kwargs.get('split_thresh', 0.4)
                )
            
            if 'curation' in kwargs and kwargs['curation'] is not None:
                ic.curate_dataset(kwargs['curation'])
            
            feature_type = kwargs.get('feature_type', 'all')
            if feature_type == 'svm':
                
                print("\nCalculating SVM features ...")
                ic.batch_calculate_features(svm=True)
                ic.dataframe_to_pkl(dataframe='svm_features')
            elif feature_type == 'nucleoid':
                ic.batch_detect_objects(
                    image_path,
                    channel_suffix=kwargs.get('channel_suffix', ''),
                    channel_list = kwargs.get('channel_list'),
                    min_overlap_ratio=kwargs.get('min_overlap_ratio', 0.01),
                    max_external_ratio=kwargs.get('max_external_ratio', 0.1)
                )
                print("\nCalculating nucleoid features ...")
                ic.batch_calculate_features(svm=False)
                ic.dataframe_to_pkl(dataframe='features')
            else:
                print("\nCalculating features")
                ic.batch_calculate_features(svm=False)
                ic.dataframe_to_pkl(dataframe='features')
            
            del ic
         
    def process_image_folder(self, image_path, kwargs):
        ic = ImageCollection(image_path)

        if 'segment' in kwargs and kwargs['segment']:
            print('Segmenting ...')
            ic.load_phase_images(phase_channel=kwargs.get('phase_channel', ''))
            i = len(ic.images)
            ic.segment_images(kwargs.get('mask_thresh', 1), kwargs.get('minsize', 300), n=range(i))

        if 'load_mesh' in kwargs and kwargs['load_mesh']:
            filename = ic.name + '_meshdata.pkl'
            ic.batch_load_mesh(filename, phase_channel=kwargs.get('phase_channel', ''))
        else:
            ic.batch_process_mesh(
                object_list=None,
                phase_channel=kwargs.get('phase_channel', ''),
                join_thresh=kwargs.get('join_thresh', 4),
                split_thresh=kwargs.get('split_thresh', 0.4)
            )

        if 'curation' in kwargs and kwargs['curation'] is not None:
            ic.curate_dataset(kwargs['curation'])

        feature_type = kwargs.get('feature_type', 'all')
        if feature_type == 'svm':
            print("\nCalculating SVM features ...")
            ic.batch_calculate_features(svm=True)
            ic.dataframe_to_pkl(dataframe='svm_features')
        elif feature_type == 'nucleoid':
            ic.batch_detect_objects(
                image_path,
                channel_suffix=kwargs.get('channel_suffix', ''),
                channel_list=kwargs.get('channel_list'),
                min_overlap_ratio=kwargs.get('min_overlap_ratio', 0.01),
                max_external_ratio=kwargs.get('max_external_ratio', 0.1)
            )
            print("\nCalculating nucleoid features ...")
            ic.batch_calculate_features(svm=False)
            ic.dataframe_to_pkl(dataframe='features')
        else:
            print("\nCalculating features")
            ic.batch_calculate_features(svm=False)
            ic.dataframe_to_pkl(dataframe='features')

        del ic

    def general_pipeline_parallel(self, exp_folder_path, **kwargs):
        self.exp_folder_path = exp_folder_path

        subfolder_paths = [os.path.join(exp_folder_path, directory) for directory in os.listdir(exp_folder_path) if os.path.isdir(os.path.join(exp_folder_path, directory))]
        print(f'\nProcessed folders are: {subfolder_paths}')

        # Create a multiprocessing pool with the specified number of cores (default: 2)
        pool = multiprocessing.Pool(kwargs.get('n_cores', 2))

        # Map the function to process each image folder in parallel
        pool.starmap(self.process_image_folder, [(image_path, kwargs) for image_path in subfolder_paths])

        # Close the pool and wait for all processes to complete
        pool.close()
        pool.join()
    
    
    
    
    
    
    
    