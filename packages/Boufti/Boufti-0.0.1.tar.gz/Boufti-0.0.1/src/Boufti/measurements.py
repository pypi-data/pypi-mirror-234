# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:39:07 2023

@author: Bart Steemans. Govers Lab. 
"""
# Helper functions for extracting features
import numpy as np
import math
from shapely.geometry import Polygon
from skimage.draw import polygon2mask
from scipy.signal import find_peaks
from scipy.stats import kurtosis, skew
# Contour Feature functions ------------------------------------------------------------------------
def get_step_length(x1, y1, x2, y2, px):
    dx = x1[1:] + x2[1:] - x1[:-1] - x2[:-1]
    dy = y1[1:] + y2[1:] - y1[:-1] - y2[:-1]
    return (np.sqrt(dx**2 + dy**2) / 2)*px
def get_length(step_length):
    return np.sum(step_length)

def get_avg_width(x1, y1, x2, y2, px):
    width_not_ordered = np.sqrt((x1-x2)**2+(y1-y2)**2)
    sorted_width = sorted(width_not_ordered, reverse = True)
    width = (sum(sorted_width[:math.floor(len(sorted_width)/3)]) / math.floor(len(sorted_width)/3))
    return width*px, width_not_ordered*px

def get_area(contour, px):
    poly = Polygon(contour)
    area = poly.area
    return area*px*px

def get_volume(x1, y1, x2, y2, step_length, px):
    d = np.sqrt((x1-x2)**2+(y1-y2)**2)
    volume = np.trapz((np.pi*(d/2)**2) , dx = step_length)
    return volume*px*px

def get_surface_area(width_no, step_length):
    widths = width_no[1:]
    surface_areas = 2 * np.pi * (widths / 2) * step_length
    total_surface_area = np.sum(surface_areas)
    return total_surface_area
def get_surface_area_over_volume(sa, vol):
    return (sa/vol)

def get_cell_perimeter_measurements(contour, area, px):
    v1 = contour[:-1]
    v2 = contour[1:]
    d = v2-v1
    perimeter = np.sum(np.sqrt(np.sum(d**2,axis=1)))*px
    circularity = (4*np.pi*area)/(perimeter)**2
    compactness = (perimeter ** 2) / area
    sphericity = (np.pi * 1.5 * (perimeter / (2 * np.pi)) ** 1.5) / area
    return perimeter, circularity, compactness, sphericity

#cell width variability calculated based on the 50% highest cell widths
def get_cell_width_variability(width_no):
    sorted_width = sorted(width_no, reverse = True)
    half_idx = len(sorted_width) // 2
    half_width = sorted_width[:half_idx]
    width_var = np.std(half_width) / np.mean(half_width)    
    return width_var

#ask Sander what the difference is between this and 3 consecutive points (MATLAB code)
def get_curvature_characteristics(contour, px):
    dx = np.gradient(contour[:, 0]*px)
    dy = np.gradient(contour[:, 1]*px)
    d2x = np.gradient(dx)
    d2y = np.gradient(dy)
    curvature = np.abs(dx*d2y - dy*d2x) / (dx**2 + dy**2)**1.5
    max_c = np.max(curvature)
    min_c = np.min(curvature)
    mean_c = np.nanmean(curvature)
    return max_c, min_c, mean_c

def get_total_phaco_intensity(contour, shape, interp2d):
    mask = polygon2mask(shape, contour)
    coords = np.column_stack(np.where(mask)).astype(int)
    values = interp2d.ev(coords[:,0], coords[:,1])
    return np.sum(values), np.max(values), np.mean(values)
    # Calculate the total phase intensity within the contour mask

def get_contour_intensity(contour, interp2d):
    data =  interp2d.ev(contour.T[0], contour.T[1])
    return data

def find_signal_peaks(signal, maximum):
    peaks, _ = find_peaks(signal, prominence= 0.5, height = (maximum * 0.5))
    return len(peaks)

def measure_contour_variability(signal):
    extra_contour_intensities = np.concatenate([signal, signal[:10]])
    contour_intensities_variability = np.array([np.std(extra_contour_intensities[ss:ss+10]) for ss in range(1, len(extra_contour_intensities)-10)])
    return contour_intensities_variability

def get_kurtosis(signal):
    return kurtosis(signal)

def get_skew(signal):
    return skew(signal)