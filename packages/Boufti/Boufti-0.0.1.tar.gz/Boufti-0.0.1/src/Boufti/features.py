# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 09:45:56 2023

@author: Bart Steemans. Govers Lab.
"""
from .measurements import *
from . import utilities as u
import numpy as np

class Features:
    
    def __init__(self, image_obj):
        
        self.image_obj = image_obj
    
    def get_all_features(self, cell, add_profiling_data):
        
        self.get_contour_features(cell)
        self.get_phaco_features(cell, add_profiling_data)
        self.get_nucleoid_features(cell, add_profiling_data)
        
    
        
    def get_contour_features(self, cell):
        cell.contour_features = {}
        if 4 <= len(cell.mesh) <= 500:              
            cell.profile_mesh = u.get_profile_mesh(cell.mesh, u.get_width(cell.x1, cell.y1, cell.x2, cell.y2))
            
            self.step_length = get_step_length(cell.x1, cell.y1, cell.x2, cell.y2, self.image_obj.px)
            cell.contour_features['cell_length'] = get_length(self.step_length)
            cell.contour_features['cell_width'], self.width_not_ordered = get_avg_width(cell.x1, cell.y1, cell.x2, cell.y2, self.image_obj.px)
            cell.profiling_data['cell_widthno'] = self.width_not_ordered 
            cell.contour_features['cell_area'] = get_area(cell.contour, self.image_obj.px)
            cell.contour_features['cell_volume'] = get_volume(cell.x1, cell.y1, cell.x2, cell.y2, self.step_length, self.image_obj.px)
            cell.contour_features['cell_surface_area'] = get_surface_area(self.width_not_ordered, self.step_length)
            cell.contour_features['cell_SOV'] = get_surface_area_over_volume(cell.contour_features['cell_surface_area'], cell.contour_features['cell_volume'])
            cell.contour_features['cell_perimeter'], cell.contour_features['cell_circularity'], cell.contour_features['cell_POA'], cell.contour_features['cell_sphericity'] = get_cell_perimeter_measurements(cell.contour, cell.contour_features['cell_area'], self.image_obj.px)
            cell.contour_features['cell_width_variability'] = get_cell_width_variability(self.width_not_ordered)
            cell.contour_features['max_curvature'], cell.contour_features['min_curvature'], cell.contour_features['mean_curvature'] = get_curvature_characteristics(cell.contour, self.image_obj.px)
        else:
            cell.discard = True
            
    def get_phaco_features(self, cell, add_profiling_data):
        cell.phaco_features = {}
        if self.image_obj.im_interp2d is None:
            self.image_obj.get_inverted_image()
        if 4 <= len(cell.mesh) <= 500 and add_profiling_data:    
            try:
                cell.profiling_data['phaco_axial_intensity'] = u.measure_along_midline_interp2d(cell.midline, self.image_obj.im_interp2d, width = 5)
                cell.profiling_data['phaco_midline_intensity'] = u.measure_along_midline_interp2d(cell.midline, self.image_obj.im_interp2d, width = 1)

                cell.profiling_data['phaco_mesh_intensity'] = self.image_obj.im_interp2d.ev(cell.profile_mesh[0],cell.profile_mesh[1]).T
                cell.profiling_data['phaco_average_mesh_intensity'] = u.get_profilemesh_intensity(cell.profiling_data['phaco_mesh_intensity'])
                cell.profiling_data['phaco_weighted_intensity'] = u.get_weighted_intprofile(cell.profiling_data['phaco_axial_intensity'], self.width_not_ordered )
                cell.profiling_data['CD'], cell.profiling_data['relpos'], constrDegree_abs, ctpos = u.constr_degree_single_cell_min(cell.profiling_data['phaco_weighted_intensity'], self.step_length)
                
            except Exception:
                print(f'The mesh of Cell number {cell.cell_id} is incorrect')
                cell.discard = True
        else:
            cell.discard = True
            
    def get_svm_features(self, cell):
        cell.svm_features = {}
        cell.profiling_data = {}
        if self.image_obj.im_interp2d is None:
            self.image_obj.get_inverted_image()
            
        if 4 <= len(cell.mesh) <= 500: 
            try:
                cell.profile_mesh = u.get_profile_mesh(cell.mesh, u.get_width(cell.x1, cell.y1, cell.x2, cell.y2))
                self.step_length = get_step_length(cell.x1, cell.y1, cell.x2, cell.y2, self.image_obj.px)
                
                # Contour is added here for labeling purposes
                cell.svm_features['contour'] = cell.contour
                
                # Morphological features
                cell.svm_features['cell_length'] = get_length(self.step_length)
                cell.svm_features['cell_width'], self.width_not_ordered = get_avg_width(cell.x1, cell.y1, cell.x2, cell.y2, self.image_obj.px)
                cell.svm_features['cell_area'] = get_area(cell.contour, self.image_obj.px)
                cell.svm_features['cell_volume'] = get_volume(cell.x1, cell.y1, cell.x2, cell.y2, self.step_length, self.image_obj.px)
                cell.svm_features['cell_surface_area'] = get_surface_area(self.width_not_ordered, self.step_length)
                cell.svm_features['max_curvature'], cell.svm_features['min_curvature'], cell.svm_features['mean_curvature'] = get_curvature_characteristics(cell.contour, self.image_obj.px)
                cell.svm_features['cell_perimeter'], cell.svm_features['cell_circularity'], cell.svm_features['cell_POA'], cell.svm_features['cell_sphericity'] = get_cell_perimeter_measurements(cell.contour, cell.svm_features['cell_area'], self.image_obj.px)
                
                # Cell surface intensity features
                total_int, max_int, mean_int = get_total_phaco_intensity(cell.contour, self.image_obj.image.shape, self.image_obj.im_interp2d)
                cell.svm_features['phaco_total_intensity'] = total_int
                cell.svm_features['phaco_max_intensity'] = max_int
                cell.svm_features['phaco_mean_intensity'] = mean_int
            
                # Contour intensity features
                cell.profiling_data['phaco_contour_intensity'] = get_contour_intensity(cell.contour, self.image_obj.im_interp2d)
                cell.profiling_data['phaco_contour_intensity_variability'] = measure_contour_variability(cell.profiling_data['phaco_contour_intensity'])
                
                sorted_phaco_contour_intensity = sorted(cell.profiling_data['phaco_contour_intensity'])
                cell.svm_features['phaco_contour_peaks'] = find_signal_peaks(cell.profiling_data['phaco_contour_intensity'], max_int)
                cell.svm_features['phaco_max_contour_intensity'] = np.max(cell.profiling_data['phaco_contour_intensity'])
                cell.svm_features['phaco_mean_contour_intensity'] = np.mean(cell.profiling_data['phaco_contour_intensity'])
                cell.svm_features['phaco_min_contour_intensity'] = np.mean(sorted_phaco_contour_intensity[:10])
                cell.svm_features['phaco_max_contour_variability'] = np.max(cell.profiling_data['phaco_contour_intensity_variability'])
                cell.svm_features['phaco_mean_contour_variability'] = np.mean(cell.profiling_data['phaco_contour_intensity_variability'])
    
                # Midline intensity features
                # If no midline available calculate it with mesh2midline( ).
                cell.profiling_data['phaco_axial_intensity'] = u.measure_along_midline_interp2d(cell.midline, self.image_obj.im_interp2d, width = 5)
                
                cell.svm_features['midline_kurtosis'] = get_kurtosis(cell.profiling_data['phaco_axial_intensity'])
                cell.svm_features['midline_skewness'] = get_skew(cell.profiling_data['phaco_axial_intensity'])
                
                
                # Expanded contour intensity features
                expanded_contour = u.expand_contour(cell.contour, scale = 2)
                eroded_contour = u.erode_contour(cell.contour, scale = 2)
                cell.profiling_data['phaco_expanded_contour_intensity'] = get_contour_intensity(expanded_contour, self.image_obj.im_interp2d)
                cell.profiling_data['phaco_eroded_contour_intensity'] = get_contour_intensity(eroded_contour, self.image_obj.im_interp2d)
                
                cell.svm_features['phaco_max_expanded_contour_intensity'] = np.max(cell.profiling_data['phaco_expanded_contour_intensity'])
                cell.svm_features['phaco_mean_expanded_contour_intensity'] = np.mean(cell.profiling_data['phaco_expanded_contour_intensity'])
                
                #Mesh gradient features
                cell.svm_features['phaco_cell_edge_gradient'] = np.average(cell.profiling_data['phaco_eroded_contour_intensity'] - cell.profiling_data['phaco_expanded_contour_intensity'])
            except Exception:
                print(f'The mesh of Cell number {index} is incorrect')
                cell.discard = True
        else:
            cell.discard = True
            print(f'The mesh of Cell number {cell.cell_id} is too small or large')
            
    def get_nucleoid_features(self, cell, add_profiling_data):
        """
        Under construction.
        Input: channel containing nucleoid information

        Returns
        -------
        Dictionary of features for that cell object.

        """
        if cell.object_contours:
            nucleoid_areas = []  # Initialize a list to store nucleoid areas for each contour
            for contour in cell.object_contours:
                area = get_area(contour, self.image_obj.px)  # Calculate area for each contour
                nucleoid_areas.append(area)
            cell.nucleoid_features['nucleoid_area'] = nucleoid_areas
    
    
    
    