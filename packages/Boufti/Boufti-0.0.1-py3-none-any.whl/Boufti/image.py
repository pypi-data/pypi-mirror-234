# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 09:45:53 2023

@author: Bart Steemans. Govers Lab.
"""
from .features import Features
from . import utilities as u

from tqdm import tqdm
import numpy as np
import pandas as pd  
import warnings
warnings.filterwarnings("ignore")

class Image:
    
    
    def __init__(self, image, image_name, 
                 frame, mask = None, 
                 processed_mesh_dataframe = None, 
                 px = 0.065):
        
        
        self.mask = mask
        self.cells = []
        self.px = px
        self.image_name = image_name
        self.frame = frame
        self.image = image
        self.channel = None
        
        self.joined_mask = None
        self.mesh_dataframe = None
        self.processed_mesh_dataframe = processed_mesh_dataframe
        
        self.im_interp2d = None
        self.inverted_image = None
        
        
    def calculate_features(self, add_profiling_data=True, svm=False):
        
        self.features = Features(self)
        result_df = None
    
        for cell in self.cells:
            if svm:
                self.features.get_svm_features(cell)
            else:
                self.features.get_all_features(cell, add_profiling_data)
    
        if svm:
            result_df = self.svm_features_to_dataframe()
        else:
            result_df = self.features_to_dataframe()
    
        self.im_interp2d = None
        self.inverted_image = None
        del self.features
    
        return result_df
    
    def features_to_dataframe(self):
        
        contour_df = self.dataframe_from_dict("contour_features")
        
        phaco_df = self.dataframe_from_dict("phaco_features")
        
        nucleoid_df = self.dataframe_from_dict("nucleoid_features")
        
        # Combine all feature dictionaries in 
        features_df = pd.concat([contour_df, phaco_df, nucleoid_df], axis=1)
        
        self.add_info_feature_df(features_df)
        
        return features_df
    
    def svm_features_to_dataframe(self):

        svm_df = self.dataframe_from_dict("svm_features")

        self.add_info_feature_df(svm_df)
        
        return svm_df    
    
    def dataframe_from_dict(self, feature_dictionary):
        
        data = {cell.cell_id: getattr(cell, feature_dictionary)
                for cell in self.cells if not cell.discard}
        
        df = pd.DataFrame.from_dict(data, orient='index')
        
        return df
    

    
    def add_info_feature_df(self, dataframe):
        
        dataframe.insert(0, 'image_name', self.image_name)
        dataframe.insert(0, 'cell_id', [cell.cell_id for cell in self.cells if not cell.discard])
        dataframe.insert(0, 'frame', self.frame)
        
    def join_split_pipeline(self, join_thresh = 4, split_thresh = 0.3):
        
        """
        Method used in the ic.batch_mesh_process() method.
        Returns 'processed_mesh_dataframe' which is used to created Cell objects.

        """
        self.join_cells(join_thresh)
        self.mask2mesh()
        self.split_cells(split_thresh)
        self.create_cell_object()
            
    def create_cell_object(self, verbose=True):
        self.cells = []
    
        if self.processed_mesh_dataframe is None:
            try:
                dataframe = self.mesh_dataframe
                message = 'Cell objects are created from unprocessed meshes'
    
            except AttributeError:
                print('No meshes from the masks. Either process the masks or load in mesh data from a .pkl file.')
                return
    
        else:
            dataframe = self.processed_mesh_dataframe
            message = 'Cell objects are created from processed meshes'
    
        for i, row in dataframe.iterrows():
            cell_ID = i
            contours = np.array(row['contour'])
            meshes = np.array(row['mesh'])
            midlines = np.array(row['midline'])
            cell = Cell(contours, meshes, midlines, self.image.shape, cell_ID)
            self.add_cell(cell)
    
        if verbose:
            print(message)
    
          
    def add_cell(self, cell):
        
        self.cells.append(cell)
        
    def get_inverted_image(self):
        
        inverted_image = np.subtract(np.max(self.image),self.image)
        bgr = u.phase_background(inverted_image,self.mask) #
        self.inverted_image = np.maximum(inverted_image - bgr, 0)
        self.im_interp2d = u.interp2d(self.inverted_image)
            
    def join_cells(self, thresh = None):
        
        print('Joining cells ...')    
        
        if self.mask is None:
            raise ValueError('Mask image is not loaded')
        
        pole_1 = []
        pole_2 = []
        cell_ID = []
        
        #loop through all cells in the frame
        for cell in tqdm(range(1,np.max(self.mask))): #50
            try:
                contour = u.get_contour(cell, self.mask, smoothing = 13)
                skeleton = u.extract_skeleton(contour, self.mask)
            except Exception:
                
                skeleton = []
                cell_ID.append(cell)
                continue
            
            if np.any(skeleton):
                extended_skeleton, pole1, pole2  = u.extend_skeleton(skeleton,
                                                            contour,
                                                            find_pole1=True,
                                                            find_pole2=True)
                pole_1.append(pole1)
                pole_2.append(pole2)
            else:
                cell_ID.append(cell)   
        pole_1 = np.vstack(np.array(pole_1))
        pole_2 = np.vstack(np.array(pole_2))
        
        cell_pairs = u.get_cell_pairs(pole_1, pole_2, cell_ID, thresh)
        
        if not np.any(cell_pairs):
            self.joined_mask = np.copy(self.mask)
        else:
            # Create a copy of the original masks array to store the new masks
            new_masks = np.copy(self.mask)
            dsu = {}
            for mask in np.unique(cell_pairs):
                dsu[mask + 1] = mask + 1
            # Merge masks that belong to the same group
            for mask1, mask2 in cell_pairs:
                root1 = mask1 + 1
                while root1 != dsu[root1]:
                    root1 = dsu[root1]
                root2 = mask2 + 1
                while root2 != dsu[root2]:
                    root2 = dsu[root2]
                if root1 != root2:
                    dsu[root1] = root2
    
            # Update the masks with the merged values
            for mask, root in dsu.items():
                new_masks[new_masks == mask] = root
            unique_masks = np.unique(new_masks)
            # Create a dictionary that maps unique mask values to new mask values starting from 1
            mask_dict = {mask: i for i, mask in enumerate(unique_masks)}
    
            # Use the dictionary to relabel the new_masks array and the new_labels array
            new_masks_relabel = np.vectorize(mask_dict.get)(new_masks)
            self.joined_mask = new_masks_relabel
        
    
    def mask2mesh(self):
        
        contour_fit = []
        mesh = []
        midlines = []
        
        if self.joined_mask is not None:
            mask = self.joined_mask
            print('Creating meshes from joined masks ...')
        else:
            mask = self.mask
            print('Creating meshes from raw masks ...')
        #loop through all cells in the frame
        for cell in tqdm(range(1,np.max(mask))):
            #contour and skeleton generation
            try:
                contour = u.get_contour(cell, mask, smoothing = 13)
                skeleton = u.extract_skeleton(contour, mask)
            except Exception:
                skeleton = []
                
            if np.any(skeleton):
                
                extended_skeleton, pole1, pole2  = u.extend_skeleton(skeleton,
                                                                        contour,
                                                                        find_pole1=True,
                                                                        find_pole2=True)
                try:
                    length = u.line_length(extended_skeleton)
                    width = u.direct_intersect_distance(extended_skeleton,contour)
                except Exception:
                    width = []
                if np.any(width):
                    l1, l2, profile_mesh, midline = u.straighten_by_orthogonal_lines(contour, extended_skeleton, length, width, unit_micron= 0.5)
                    result, l1, l2 = u.add_poles(l1, l2, pole1, pole2)
                    contour_fit.append(contour)
                    mesh.append(result)             
                    midlines.append(midline)
        
        self.mesh_dataframe = pd.DataFrame({'contour': contour_fit, 'mesh': mesh, 'midline': midlines})
        self.mesh_dataframe['frame'] = self.image_name
        
    def split_cells(self, thresh = 0.3):
        
        self.get_inverted_image()
        print('Splitting cells ...')
        
        new_meshes = []
        new_contours = []
        new_midlines = []
        
        for j in tqdm(range(len(self.mesh_dataframe))):
            
            x1, y1, x2, y2, contour, midline = u.separate_singleframe_meshdata(j, self.mesh_dataframe)
            
            complete_mesh = np.array(np.column_stack((x1, y1, x2, y2)))
            
            step_length_px = u.get_step_length(x1, y1, x2, y2)*self.px
            
            width_px = u.get_width(x1, y1, x2, y2)*self.px
            
            intprofile = u.measure_along_midline_interp2d(midline, self.im_interp2d, width = 5)
            
            weighted_intprofile = u.get_weighted_intprofile(intprofile, width_px)
            
            constrDegree, relPos, constrDegree_abs, ctpos = u.constr_degree_single_cell_min(weighted_intprofile, step_length_px)
            
            if constrDegree > thresh:
                x, y, left, right = u.split_point(x1, y1, x2, y2, ctpos)
                
                mesh1rec = np.concatenate((complete_mesh[:(ctpos-2)], right , np.array([[x, y, x, y]])))
                mesh2rec = np.concatenate((np.array([[x, y, x, y]]), left ,complete_mesh[(ctpos+2):]))
                
                try:
                    mesh1, contour1, midline1 = u.split_mesh2mesh(mesh1rec[:,0], mesh1rec[:,1], mesh1rec[:,2], mesh1rec[:,3])
                    mesh2, contour2, midline2 = u.split_mesh2mesh(mesh2rec[:,0], mesh2rec[:,1], mesh2rec[:,2], mesh2rec[:,3])
                except Exception:
                    continue
                if 4 <= len(mesh1) and len(mesh2) <= 500:
                    new_meshes.append(mesh1)
                    new_meshes.append(mesh2)
                    
                    new_contours.append(contour1)
                    new_contours.append(contour2)
                    
                    new_midlines.append(midline1)
                    new_midlines.append(midline2)
            else:
                new_meshes.append(complete_mesh)
                new_contours.append(contour)
                new_midlines.append(midline)
        self.processed_mesh_dataframe = pd.DataFrame({'mesh': new_meshes, 'contour': new_contours, 'midline': new_midlines})
        self.processed_mesh_dataframe['frame'] = self.image_name

    def object_detection(self, folder_path, channel_suffix = '', log_sigma = 3, kernel_width = 4, min_overlap_ratio=0.01, max_external_ratio=0.1):
                    
        detections = []
        cell_ids = []
        
        for cell in self.cells:
            cell.object_contours = u.get_subcellular_objects(cell.contour, self.channel[channel_suffix], 
                                                             cell.cell_id, log_sigma, 
                                                             kernel_width, min_overlap_ratio, 
                                                             max_external_ratio)
        
            detections.append(cell.object_contours)
            cell_ids.append(cell.cell_id)
        
        self.detections_df = pd.DataFrame({'cell_id' : cell_ids, 'object_contours': detections})
        self.detections_df.insert(0, 'frame', self.frame)
        return self.detections_df
        
        
        
        
class Cell:
    
    def __init__(self, contour, mesh, midline, shape, cell_id):
        
        self.discard = False
        self.contour = contour
        self.mesh = mesh
        self.midline = midline
        self.cell_id = cell_id
        
        self.x1 = self.mesh[:,0]
        self.y1 = self.mesh[:,1]
        self.x2 = self.mesh[:,2]
        self.y2 = self.mesh[:,3]
        
        self.profile_mesh = None
        self.object_contours = None
        
        self.contour_features = {}
        self.phaco_features = {}
        self.nucleoid_features = {}
        self.profiling_data = {}
        self.svm_features = {}    


    