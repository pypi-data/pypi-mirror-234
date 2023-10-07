# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 13:46:15 2023

@author: Bart Steemans. Govers Lab. 
"""
import os
import shutil
import tifffile

import numpy as np
import cv2 as cv
import networkx as nx
import math

import skimage
import scipy.ndimage
from scipy import interpolate
from scipy.ndimage import gaussian_filter1d, gaussian_filter, minimum_filter

from skimage.filters import threshold_otsu, rank
from skimage.draw import polygon2mask
from skimage.morphology import skeletonize, ball
#-------------------------------------------------------------------------------------------------------
#FUNCTIONS
def smallest_path(x_coords, y_coords, start_x, start_y):
    G = nx.Graph()
    for i in range(len(x_coords)):
        G.add_node(i, x=x_coords[i], y=y_coords[i])
    for i in range(len(x_coords)):
        for j in range(i + 1, len(x_coords)):
            G.add_edge(i, j, weight=np.sqrt((x_coords[i] - x_coords[j])**2 + (y_coords[i] - y_coords[j])**2))
    start = None
    for i in range(len(x_coords)):
        if x_coords[i] == start_x and y_coords[i] == start_y:
            start = i
            break
    T = nx.minimum_spanning_tree(G)
    path = nx.dfs_postorder_nodes(T, source=start)
    sorted_points = list(path)
    return [x_coords[i] for i in sorted_points],[y_coords[i] for i in sorted_points]

def skeleton_endpoints(skel):
    # Make our input nice, possibly necessary.
    skel = skel.copy()
    skel[skel!=0] = 1
    skel = np.uint8(skel)
    
    # Apply the convolution.
    kernel = np.uint8([[1,  1, 1],
                       [1, 10, 1],
                       [1,  1, 1]])

    filtered = cv.filter2D(skel, -1 ,kernel)

    out = np.zeros_like(skel)
    out[np.where(filtered==11)] = 1
    return out

def get_ordered_list(points, x, y):
   distance = (((x-points[1])**2 + ( y- points[0])**2)** 0.5)
   args = np.argsort(distance)
   return args

#@jit(nopython=True, cache=True)
def line_intersect(x1, y1, x2, y2, x3, y3, x4, y4):  # Ax+By = C
    A1 = y2 - y1
    B1 = x1 - x2
    C1 = A1 * x1 + B1 * y1
    A2 = y4 - y3
    B2 = x3 - x4
    C2 = A2 * x3 + B2 * y3
    intersect_x = (B1 * C2 - B2 * C1) / (A2 * B1 - A1 * B2)
    intersect_y = (A1 * C2 - A2 * C1) / (B2 * A1 - B1 * A2)
    return intersect_x, intersect_y

def line_contour_intersection(p1, p2, contour):
    v1, v2 = contour[:-1], contour[1:]
    x1, y1 = v1.T
    x2, y2 = v2.T
    x3, y3 = p1
    x4, y4 = p2
    xy = np.array(line_intersect(x1, y1, x2, y2, x3, y3, x4, y4)).T
    dxy_v1 = xy - v1
    dxy_v2 = xy - v2
    dxy = dxy_v1 * dxy_v2
    intersection_points = xy[np.where(np.logical_and(dxy[:, 0] < 0, dxy[:, 1] < 0))]
    if len(intersection_points) > 2:
        dist = np.sum(np.square(np.tile(p1, (len(intersection_points), 1)) - intersection_points),
                      axis=1)
        intersection_points = intersection_points[np.argsort(dist)[0:2]]
    return intersection_points

def unit_perpendicular_vector(data, closed= True):

    p1 = data[1:]
    p2 = data[:-1]
    dxy = p1 - p2
    ang = np.arctan2(dxy.T[1], dxy.T[0]) + 0.5 * np.pi
    dx, dy = np.cos(ang), np.sin(ang)
    unit_dxy = np.array([dx, dy]).T
    if not closed:
        unit_dxy = np.concatenate([[unit_dxy[0]], unit_dxy])
    else:
        unit_dxy = np.concatenate([unit_dxy,[unit_dxy[-1]]])
    return unit_dxy

def get_contour(cell, masks, smoothing = 13):
    temp_mask = np.where( masks == cell, 1, 0)
    contour, coord =  cv.findContours(cv.convertScaleAbs(temp_mask), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    
    contour = np.array(contour)
    
    contourx = contour.squeeze()[:, 1] 
    contoury = contour.squeeze()[:, 0] 
    
    s = int(len(contourx) / smoothing) if len(contourx) > smoothing else 1
    
    tck, u =interpolate.splprep([contourx,contoury], u = None, s = s, per=1)  #3; 12
    u_new = np.linspace(u.min(), u.max(), len(contourx))
    outx,outy = interpolate.splev(u_new, tck, der = 0)
    
    return np.array([outx,outy]).T

def extract_skeleton(contour, masks):
    
    contour = contour.copy()
    contour = contour.astype(int)
    img = polygon2mask(masks.shape, contour)
    # Get the bounding rectangle of the largest contour
    x, y, w, h = cv.boundingRect(contour)
    # Create the cropped image
    padding = 5  # Adjust the padding value as per your needs
    x -= padding
    y -= padding
    w += 2 * padding
    h += 2 * padding
    
    cropped_img = img[x:x+w, y:y+h]
    
    # Apply skeletonization on the cropped image
    skeleton = skeletonize(cropped_img, method='lee')
    
    # Retrieve the skeleton coordinates in the original image space
    skeleton_coords = np.column_stack(np.where(skeleton)).astype(int)
    skeleton_coords[:, 0] += x  # Add the x-offset
    skeleton_coords[:, 1] += y  # Add the y-offset
    
    x_skel = skeleton_coords[:, 0]
    y_skel = skeleton_coords[:, 1]
    
    skel_mask = np.zeros_like(masks)
    skel_mask[x_skel,y_skel] = 1
    
    #Sort coordinates based on distance
    skel_end = skeleton_endpoints(skel_mask)
    end_coords = np.argwhere(skel_end == 1)[0]
    sorted_skelx,sorted_skely = (smallest_path(x_skel, y_skel, end_coords[0], end_coords[1]))
    #Smoothen the skeleton
    if len(y_skel)<=3:
        return []
    elif 4 <=len(y_skel)<= 13:
        fkc, u = interpolate.splprep([sorted_skelx,sorted_skely], k=1, s=1, per=0)
    else:
        fkc, u = interpolate.splprep([sorted_skelx,sorted_skely], k=2, s=10, per=0)
    smoothed_skel = np.asarray(interpolate.splev(np.linspace(u.min(), u.max(), 200), fkc, der=0)).T
    return smoothed_skel

def find_poles(smoothed_skeleton,
               smoothed_contour,
               find_pole1=True,
               find_pole2=True):
    # find endpoints and their nearest neighbors on a midline
    length = len(smoothed_skeleton)
    extended_pole1 = [smoothed_skeleton[0]]
    extended_pole2 = [smoothed_skeleton[-1]]
    i = 0
    j = 0
    if find_pole1:
        for i in range(10):
            p1 = smoothed_skeleton[i]
            p2 = smoothed_skeleton[i + 1]
            # find the two intersection points between
            # the vectorized contour and line through pole1
            intersection_points_pole1 = line_contour_intersection(p1, p2, smoothed_contour)
            # find the interesection point with the same direction as the outward pole vector
            dxy_1 = p1 - p2
            p1_tile = np.tile(p1, (len(intersection_points_pole1), 1))
            p1dot = (intersection_points_pole1 - p1_tile) * dxy_1
            index_1 = np.where((p1dot[:, 0] > 0) & (p1dot[:, 1] > 0))[0]
            if len(index_1) > 0:
                extended_pole1 = intersection_points_pole1[index_1]
                break
    else:
        i = 1

    if find_pole2:
        for j in range(10):
            p3 = smoothed_skeleton[-1 - j]
            p4 = smoothed_skeleton[-2 - j]
            # find the two intersection points between
            # the vectorized contour and line through pole1
            intersection_points_pole2 = line_contour_intersection(p3, p4, smoothed_contour)
            # find the interesection point with the same direction as the outward pole vector
            dxy_2 = p3 - p4
            p3_tile = np.tile(p3, (len(intersection_points_pole2), 1))
            p3dot = (intersection_points_pole2 - p3_tile) * dxy_2
            index_2 = np.where((p3dot[:, 0] > 0) & (p3dot[:, 1] > 0))[0]
            if len(index_2) > 0:
                extended_pole2 = intersection_points_pole2[index_2]
                break
    else:
        j = 1
    trimmed_midline = smoothed_skeleton[i:length - j]
    return extended_pole1, extended_pole2, trimmed_midline

def extend_skeleton(smoothed_skeleton, smoothed_contour,
                    find_pole1=True, find_pole2=True):
    # initiate approximated tip points
    new_pole1, new_pole2, trimmed_skeleton = find_poles(smoothed_skeleton,
                                                         smoothed_contour,
                                                         find_pole1=find_pole1,
                                                         find_pole2=find_pole2)
    extended_skeleton = np.concatenate([new_pole1,
                                        trimmed_skeleton,
                                        new_pole2])

    extended_skeleton = spline_approximation(extended_skeleton, n = 200, smooth_factor = 1, closed = False)
    return extended_skeleton, new_pole1, new_pole2                           

def distance_matrix(data1, data2):
    x1, y1 = data1.T
    x2, y2 = data2.T
    dx = x1[:, np.newaxis] - x2
    dy = y1[:, np.newaxis] - y2
    dxy = np.sqrt(dx ** 2 + dy ** 2)
    return dxy

def intersect_matrix(line, contour,
                     orthogonal_vectors=None):
    if orthogonal_vectors is None:
        dxy = unit_perpendicular_vector(line, closed=False)
    else:
        dxy = orthogonal_vectors
    v1, v2 = contour[:-1], contour[1:]
    x1, y1 = v1.T
    x2, y2 = v2.T
    x3, y3 = line.T
    perp_xy = line + dxy
    x4, y4 = perp_xy.T
    A1 = y2 - y1
    B1 = x1 - x2
    C1 = A1 * x1 + B1 * y1
    A2 = y4 - y3
    B2 = x3 - x4
    C2 = A2 * x3 + B2 * y3

    A1B2 = A1[:, np.newaxis] * B2
    A1C2 = A1[:, np.newaxis] * C2
    B1A2 = B1[:, np.newaxis] * A2
    B1C2 = B1[:, np.newaxis] * C2
    C1A2 = C1[:, np.newaxis] * A2
    C1B2 = C1[:, np.newaxis] * B2
    #can give outliers when B1A2 = A1B2, division by zero or close to zero
    intersect_x = (B1C2 - C1B2) / (B1A2 - A1B2)
    intersect_y = (A1C2 - C1A2) / (A1B2 - B1A2)
    return intersect_x, intersect_y

def spline_approximation(init_contour, n=200, smooth_factor=1, closed = True):
    if closed:
        tck, u = interpolate.splprep(init_contour.T, u=None, s=smooth_factor, per=1)
    else:
        tck, u = interpolate.splprep(init_contour.T, u=None, s=smooth_factor)
    u_new = np.linspace(u.min(), u.max(), n)
    x_new, y_new = interpolate.splev(u_new, tck, der=0)
    return np.array([x_new, y_new]).T
#min dist has influence on extreme points (lower works good for some cases)
def orthogonal_intersection_point(midline,
                                  outerline,
                                  precomputed_orthogonal_vector=None,
                                  min_dist=1e-100):
    v1, v2 = outerline[:-1], outerline[1:]
    skel_x, skel_y = midline.T
    if precomputed_orthogonal_vector is None:
        intersect_x, intersect_y = intersect_matrix(midline, outerline)
    else:
        intersect_x, intersect_y = intersect_matrix(midline, outerline,
                                                    orthogonal_vectors=precomputed_orthogonal_vector)
    dx_v1 = intersect_x - v1.T[0][:, np.newaxis]
    dx_v2 = intersect_x - v2.T[0][:, np.newaxis]
    dy_v1 = intersect_y - v1.T[1][:, np.newaxis]
    dy_v2 = intersect_y - v2.T[1][:, np.newaxis]
    dx = dx_v1 * dx_v2
    dy = dy_v1 * dy_v2

    dist_x = skel_x[np.newaxis, :] - intersect_x
    dist_y = skel_y[np.newaxis, :] - intersect_y
    #influence on extreme points
    non_bounadry_points = np.where(np.logical_and(dy >= 0, dx >= 0))
    dist_matrix = np.sqrt(dist_x ** 2 + dist_y ** 2)
    dist_matrix[non_bounadry_points] = np.inf
    dist_matrix[dist_matrix <= min_dist] = np.inf
    
    nearest_id_x = np.argsort(dist_matrix, axis=0)[:1]
    nearest_id_y = np.linspace(0, dist_matrix.shape[1]-1, dist_matrix.shape[1]).astype(int)
    pos_list = np.array([intersect_x[nearest_id_x[0], nearest_id_y],
                         intersect_y[nearest_id_x[0], nearest_id_y]]).T
    return pos_list

def straighten_by_orthogonal_lines(contour, midline, length, width, unit_micron= 0.5):
    # estimate profile mesh size
    median_width = np.median(width)
    N_length = int(round(length / unit_micron))
    N_width = int(round(median_width / unit_micron))
    midline = spline_approximation(midline, n= N_length, smooth_factor=1, closed=False)

    # divide contour
    # if contour[-1] == contour[-2]:
    #     contour = contour[:-1]
    half_contour_1, half_contour_2 = divide_contour_by_midline(midline, contour)#[:-1]
    # infer orthogonal vectors
    ortho_unit_vectors = unit_perpendicular_vector(midline)
    # generate orthogonal profile lines for all midline points except for the polar ones
    l1 = orthogonal_intersection_point(midline, half_contour_1,
                                       precomputed_orthogonal_vector= ortho_unit_vectors)

    l2 = orthogonal_intersection_point(midline, half_contour_2,
                                       precomputed_orthogonal_vector=ortho_unit_vectors)

    dl = (l2 - l1) / N_width
    mult_mat = np.tile(np.arange(N_width + 1), (len(l1), 1))
    mat_x = l1[:, 0][:, np.newaxis] + mult_mat * dl[:, 0][:, np.newaxis]
    mat_y = l1[:, 1][:, np.newaxis] + mult_mat * dl[:, 1][:, np.newaxis]
    profile_mesh = np.array([mat_x, mat_y])
    return l1, l2, profile_mesh, midline



def divide_contour_by_midline(midline, contour):
    dist1 = distance_matrix(contour, midline[0]).flatten()
    dist2 = distance_matrix(contour, midline[-1]).flatten()

    id1, id2 = np.argsort(dist1)[:2]
    id3, id4 = np.argsort(dist2)[:2]

    contour_cp = contour.copy()
    if max(id1, id2) < max(id3, id4):
        term_p1 = max(id1, id2)
        if abs(id3 - id4) == 1:
            term_p2 = max(id3, id4) + 1
        elif abs(id3 - id4) > 1:
            term_p2 = max(id3, id4) + 2
        contour_cp = np.insert(contour_cp, term_p1, midline[0], axis=0)
        contour_cp = np.insert(contour_cp, term_p2, midline[-1], axis=0)

    else:
        term_p1 = max(id3, id4)
        if abs(id1 - id2) == 1:
            term_p2 = max(id1, id2) + 1
        elif abs(id1 - id2) > 1:
            term_p2 = max(id1, id2) + 2
        contour_cp = np.insert(contour_cp, term_p1, midline[-1], axis=0)
        contour_cp = np.insert(contour_cp, term_p2, midline[0], axis=0)

    if term_p1 == term_p2:
        raise ValueError('Two endpoints are identical!')
    else:
        pos1, pos2 = sorted([term_p1, term_p2])
        #print(id1, id2, id3, id4, pos1, pos2, len(contour_cp))
        half_contour_1 = contour_cp[pos1:min(pos2 + 1, len(contour_cp) - 1)]
        half_contour_2 = np.concatenate([contour_cp[pos2:], contour_cp[:pos1 + 1]])
    return half_contour_1, half_contour_2

def line_length(line):
    v1 = line[:-1]
    v2 = line[1:]
    d = v2-v1
    return np.sum(np.sqrt(np.sum(d**2,axis=1)))

def direct_intersect_distance(skeleton, contour):
    v1, v2 = contour[:-1], contour[1:]
    skel_x, skel_y = skeleton[1:-1].T
    intersect_x, intersect_y = intersect_matrix(skeleton[1:-1], contour)
    dx_v1 = intersect_x - v1.T[0][:, np.newaxis]
    dx_v2 = intersect_x - v2.T[0][:, np.newaxis]
    dy_v1 = intersect_y - v1.T[1][:, np.newaxis]
    dy_v2 = intersect_y - v2.T[1][:, np.newaxis]
    dx = dx_v1 * dx_v2
    dy = dy_v1 * dy_v2
    dist_x = skel_x[np.newaxis, :] - intersect_x
    dist_y = skel_y[np.newaxis, :] - intersect_y

    non_boundry_points = np.where(np.logical_and(dy > 0, dx > 0))
    dist_matrix = np.sqrt(dist_x ** 2 + dist_y ** 2)
    dist_matrix[non_boundry_points] = np.inf
    nearest_id_x = np.argsort(dist_matrix, axis=0)[:2]
    nearest_id_y = np.linspace(0, dist_matrix.shape[1] - 1, dist_matrix.shape[1]).astype(int)
    dists = dist_matrix[nearest_id_x[0], nearest_id_y] + dist_matrix[nearest_id_x[1], nearest_id_y]
    return np.concatenate([[0], dists, [0]])

def distance(v1, v2):
    #Euclidean distance of two points
    return np.sqrt(np.sum((np.array(v1) - np.array(v2)) ** 2))

def measure_width(extended_skeleton, smoothed_contour):
    length = line_length(extended_skeleton)
    d_perp = unit_perpendicular_vector(extended_skeleton, closed=False)
    width_list = []
    for i in range(1, len(extended_skeleton)-1):
        xy = line_contour_intersection(extended_skeleton[i],
                                       d_perp[i] + extended_skeleton[i],
                                       smoothed_contour)
        coords = np.average(xy, axis=0)
        if (len(xy) == 2) and (np.isnan(coords).sum() == 0):
            width_list.append(distance(xy[0], xy[1]))
        else:
            raise ValueError('Error encountered while computing line intersection points!')
    return np.array([0]+width_list+[0]), length

def add_poles(coords1, coords2, pole1, pole2):
    coords1 = np.vstack([pole1, coords1[1:-1], pole2])
    coords2 = np.vstack([pole1, coords2[1:-1], pole2])
    result = np.stack([coords1[:,0], coords1[:,1], coords2[:,0], coords2[:,1]], axis=1)
    return result, coords1, coords2

def get_cell_pairs(pole_1, pole_2, cell_ID, maxdist = None):
    dm11 = distance_matrix(pole_1, pole_1)
    dm22 = distance_matrix(pole_2, pole_2)
    dm12 = distance_matrix(pole_1, pole_2)
    for i in cell_ID:
        dm11 = np.insert(dm11, i-1, values=np.zeros((1, dm11.shape[1]), dtype=int), axis=0)
        dm11 = np.insert(dm11, i-1, values=np.zeros(dm11.shape[0], dtype=int), axis=1)
        dm22 = np.insert(dm22, i-1, values=np.zeros((1, dm22.shape[1]), dtype=int), axis=0)
        dm22 = np.insert(dm22, i-1, values=np.zeros(dm22.shape[0], dtype=int), axis=1)
        dm12 = np.insert(dm12, i-1, values=np.zeros((1, dm12.shape[1]), dtype=int), axis=0)
        dm12 = np.insert(dm12, i-1, values=np.zeros(dm12.shape[0], dtype=int), axis=1)
    if maxdist != None:
        maxdistance = maxdist
        neighboring_cells_dm11 = np.argwhere(np.logical_and(dm11 > 0, dm11 <= maxdistance))
        neighboring_cells_dm22 = np.argwhere(np.logical_and(dm22 > 0, dm22 <= maxdistance))
        neighboring_cells_dm12 = np.argwhere(np.logical_and(dm12 > 0, dm12 <= maxdistance))
        nc_concat = np.concatenate((neighboring_cells_dm11, neighboring_cells_dm22, neighboring_cells_dm12), axis=0)
        unique_nc1 = np.unique(nc_concat, axis=0)
        unique_nc2 = unique_nc1[unique_nc1[:, 0] != unique_nc1[:, 1]]
    else:
        #get index list of cell couples. Loop decides the distance for when more than 2 cells from couples with other cells
        maxdistance = 1
        while True: #or maxdist = 8
            neighboring_cells_dm11 = np.argwhere(np.logical_and(dm11 > 0, dm11 <= maxdistance))
            neighboring_cells_dm22 = np.argwhere(np.logical_and(dm22 > 0, dm22 <= maxdistance))
            neighboring_cells_dm12 = np.argwhere(np.logical_and(dm12 > 0, dm12 <= maxdistance))
            nc_concat = np.concatenate((neighboring_cells_dm11, neighboring_cells_dm22, neighboring_cells_dm12), axis=0)
            unique_nc1 = np.unique(nc_concat, axis=0)
            unique_nc2 = unique_nc1[unique_nc1[:, 0] != unique_nc1[:, 1]]
            unique_values, inverse_indices = np.unique(unique_nc2, return_inverse=True)
            counts = np.bincount(inverse_indices)
            # Check if the current neighboring cells are already in the set of unique cells
            if counts == []:
                print("No neighboring cells present in the image")
                break
            try:
                if np.max(counts) > 2:
                    print(f"Found triple neighboring cells after {maxdistance} distance units")
                    maxdistance = maxdistance
                    break
            except ValueError:
                pass
                    
            
            # Increment the maximum distance to search for
            maxdistance += 1
            if maxdistance > 10:
                print('pole distance to reach 4 stitched cells exceeds 20')
                break
            if counts == []:
                unique_nc2 = []
            else:
                neighboring_cells_dm11 = np.argwhere(np.logical_and(dm11 > 0, dm11 <= maxdistance))
                neighboring_cells_dm22 = np.argwhere(np.logical_and(dm22 > 0, dm22 <= maxdistance))
                neighboring_cells_dm12 = np.argwhere(np.logical_and(dm12 > 0, dm12 <= maxdistance))
                nc_concat = np.concatenate((neighboring_cells_dm11, neighboring_cells_dm22, neighboring_cells_dm12), axis=0)
                unique_nc1 = np.unique(nc_concat, axis=0)
                unique_nc2 = unique_nc1[unique_nc1[:, 0] != unique_nc1[:, 1]]
    return unique_nc2

def mesh2contour(x1, y1, x2, y2):
    x2f = np.flip(x2)
    y2f = np.flip(y2)
    # Concatenate the x and y coordinates
    xspline = np.concatenate((x2f[1:], x1[1:]))
    yspline = np.concatenate((y2f[1:], y1[1:]))

    tck, u = interpolate.splprep(np.array([xspline, yspline]), k=3, s=2, per = 1)
    u_new = np.linspace(u.min(), u.max(), 200)
    outx, outy = interpolate.splev(u_new, tck)
    
    return np.array([outx, outy]).T

def split_point(x1, y1, x2, y2, ctpos):
    dx = x2 - x1
    dy = y2 - y1
    dist = np.sqrt(dx**2 + dy**2)
    # ctpos is the index at which the cell is most constricted and where the algorith will split the cell
    xc1 = x1[ctpos]
    yc1 = y1[ctpos]
    xc2 = x2[ctpos]
    yc2 = y2[ctpos]
    newpole_x = (xc1 + xc2) / 2
    newpole_y = (yc1 + yc2) / 2
    
    xt1, yt1 = x1[ctpos+1], y1[ctpos+1]
    distt = dist[ctpos+1]
    # Use indexing to get the x and y coordinates separately
    xt13, yt13 = np.array([xt1, yt1]) + (distt/3) * np.array([dx[ctpos+1], dy[ctpos+1]]) / distt
    xt23, yt23 = np.array([xt1, yt1]) + (distt*(2/3)) * np.array([dx[ctpos+1], dy[ctpos+1]]) / distt
    
    xs1, ys1 = x1[ctpos-1], y1[ctpos-1]
    dists = dist[ctpos-1]
    
    # Use indexing to get the x and y coordinates separately
    xs13, ys13 = np.array([xs1, ys1]) + (dists/3) * np.array([dx[ctpos-1], dy[ctpos-1]]) / dists
    xs23, ys23 = np.array([xs1, ys1]) + (dists*(2/3)) * np.array([dx[ctpos-1], dy[ctpos-1]]) / dists
    
    return newpole_x, newpole_y, np.array([[xt13, yt13, xt23, yt23]]), np.array([[xs13, ys13, xs23, ys23]])

# calculates the constriction degree in relative and absolute value, 
# and the relative position along the length of the cell
# absolute constr degree needs to be multiplied by the width
def constr_degree_single_cell_min(intensity, new_step_length):
    # if intensity == []:
    #     minsize = 0
    #     minsizeabs = 0
    #     ctpos = []
    # else:
    minima = np.concatenate(([False], (intensity.T[1:-1] < intensity.T[:-2]) & (intensity.T[1:-1] < intensity.T[2:]), [False]))
    if all(not x for x in minima) or sum(intensity.T) == 0: 
        minsize = 0
        minsizeabs = 0
        ctpos = []
    else:
        index = np.where(minima)[0]
        dh = np.zeros(index.shape)
        dhi = np.zeros(index.shape)
        hgt = np.zeros(index.shape)
        for i in range(len(index)):
            k = index[i]
            half1 = intensity.T[:k-1]
            half2 = intensity.T[k+1:]
            try:
                dh1 = np.max(half1)-intensity.T[k]
                dh2 = np.max(half2)-intensity.T[k]
                dh[i] = np.min([dh1, dh2])
                dhi[i] = np.mean([dh1, dh2])
                hgt[i] = intensity.T[k]+dhi[i]
            except ValueError:
                minsize = 0
                minsizeabs = 0
                ctposr = []
            fix = np.argmax(dh)
            minsizeabs = dhi[fix]
            minsize = minsizeabs / hgt[fix]
            ctpos = index[fix]
            ctposr = np.cumsum(new_step_length)[ctpos] / np.sum(new_step_length)
        if not minsize:
            minsize = 0
            minsizeabs = 0
    constrDegree = minsize
    constrDegree_abs = minsizeabs
    if not ctpos:
        ctposr = np.nan
    relPos = ctposr
    return constrDegree, relPos, constrDegree_abs, ctpos

# This function calculates the interpolated intensity values at the position of each midline
# This is required for creating the intensity-profile
def intensity_profile(midline, width, ff):
    # x = (x1 + x2) / 2
    # y = (y1 + y2) / 2
    # create the interpolation function using bilinear interpolation
    # interpolate the image at the points given by the mesh grid
    # prf = ff.ev(x, y)
    prf = ff.ev(midline.T[0], midline.T[1])
    sigma = 2  # standard deviation of Gaussian filter
    prf = gaussian_filter1d(prf, sigma)  # apply Gaussian filter
    weighted_prf = prf * width
    return prf, weighted_prf

def get_profilemesh_intensity(profile_mesh):
    prf = np.average(profile_mesh, axis = 0)
    sigma = 2  # standard deviation of Gaussian filter
    prf = gaussian_filter1d(prf, sigma)  # apply Gaussian filter
    return prf

# This function iterates over each segment and sums up the pixel intensities within that segment
# this function is not used in calculating the intensity profile
def measure_intensity(x1, y1, x2, y2, step_length, image, bgr, width):
    #weight the intensity with the length of each branch
    mesh = np.array([x1, y1, x2, y2], dtype=np.int32)
    step_intensity = []
    bgr_image = np.maximum(image - bgr, 0)
    for i in range(1, len(x1)):
        rect = np.array([mesh[:, i - 1], mesh[:, i]])
        rect_reshaped = rect.reshape(-1, 2)
        rect_reshaped = rect_reshaped[np.lexsort((rect_reshaped[:, 1], rect_reshaped[:, 0]))]
        rect_reshaped = rect_reshaped.reshape(-1, 2)
        rect_reshaped = np.append(rect_reshaped, rect_reshaped[0]).reshape(-1, 2)
        x_coords = rect_reshaped[:,1]
        y_coords = rect_reshaped[:,0]
        
        rr, cc = skimage.draw.polygon(y_coords, x_coords)
        mask = np.zeros_like(bgr_image, dtype= bool)
        mask[rr, cc] = True
        intensity = np.sum(bgr_image[mask])
        step_intensity.append(intensity)
    sigma = 2  # standard deviation of Gaussian filter
    inten = gaussian_filter1d(step_intensity, sigma)  # apply Gaussian filter
    weighted_inten = inten * width[:-1]
    return np.array(weighted_inten).T, np.array(inten).T

def interp2d(image):
    ff = interpolate.RectBivariateSpline(range(image.shape[0]), range(image.shape[1]), image, kx=1, ky=1)
    return ff

# def phase_background(image, se_size=3, bgr_erode_num=1):
#     cropped_image = image[int(image.shape[0]*0.05):int(image.shape[0]*0.95), int(image.shape[1]*0.05):int(image.shape[1]*0.95)]
#     thres = skimage.filters.threshold_otsu(cropped_image)
#     mask = cv.threshold(image, thres, 255, cv.THRESH_BINARY_INV)[1]
#     kernel = cv.getStructuringElement(cv.MORPH_RECT, (se_size, se_size))
#     mask = cv.erode(mask, kernel, iterations=bgr_erode_num)
#     bgr_mask = mask.astype(bool)
#     bgr = np.mean(image[bgr_mask])
#     return bgr

def phase_background(image, cell_mask):
    background_mask = np.logical_not(cell_mask)
    bgr = np.mean(image[background_mask])
    return bgr

def get_bbox(x1, y1, x2, y2):
    mesh1 = [x1, x2]
    mesh2 = [y1, y2]
    ymin = int(np.min(mesh1)-10)
    ymax = int(np.max(mesh1)+10)
    xmin = int(np.min(mesh2)-10)
    xmax = int(np.max(mesh2)+10)
    # Crop the image using the boundaries
    return (xmin, xmax, ymin, ymax)

def get_step_length(x1, y1, x2, y2):
    dx = x1[1:] + x2[1:] - x1[:-1] - x2[:-1]
    dy = y1[1:] + y2[1:] - y1[:-1] - y2[:-1]
    return (np.sqrt(dx**2 + dy**2) / 2)

def get_image_for_frame(df_nr, images):
    return images[df_nr]

def separate_meshdata(df_nr, cell_nr, data):
    x1 = data[df_nr]['mesh'][cell_nr][:,0]
    y1 = data[df_nr]['mesh'][cell_nr][:,1]
    x2 = data[df_nr]['mesh'][cell_nr][:,2]
    y2 = data[df_nr]['mesh'][cell_nr][:,3]
    contour = data[df_nr]['contour'][cell_nr]
    return x1, y1, x2, y2, contour

def separate_singleframe_meshdata(cell_nr, data):
    x1 = data['mesh'][cell_nr][:,0]
    y1 = data['mesh'][cell_nr][:,1]
    x2 = data['mesh'][cell_nr][:,2]
    y2 = data['mesh'][cell_nr][:,3]
    contour = data['contour'][cell_nr]
    midline = data['midline'][cell_nr]
    return x1, y1, x2, y2, contour, midline

def distribute_tiff_files(folder_path, batch_size=5):
    tiff_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.tif', '.tiff'))]
    
    if len(tiff_files) <= batch_size:
        print("No need to distribute files, as there are 5 or fewer TIFF files.")
        return

    # Calculate the number of new folders needed
    num_folders = len(tiff_files) // batch_size
    if len(tiff_files) % batch_size != 0:
        num_folders += 1

    # Create new folders with incremental names
    for i in range(num_folders):
        new_folder_name = f"{folder_path}_{i + 1}"
        os.makedirs(new_folder_name, exist_ok=True)

        # Copy batch_size TIFF files to the new folder or fewer if it's the last folder
        start_index = i * batch_size
        end_index = min((i + 1) * batch_size, len(tiff_files))
        
        for j in range(start_index, end_index):
            source_file = os.path.join(folder_path, tiff_files[j])
            destination_file = os.path.join(new_folder_name, tiff_files[j])
            shutil.copy2(source_file, destination_file)

    print(f"{len(tiff_files)} TIFF files distributed into {num_folders} folders with a batch size of {batch_size}.")


def read_channels(folder_path, channel_list=None):
    if channel_list is None:
        # If no suffixes are provided, assume an empty list
        channel_list = []

    # Get a list of all TIFF files in the folder matching the provided suffixes
    images_dict = {}  # Create a dictionary to store channel images with specified suffixes as keys
    
    for channel in channel_list:
        matching_files = [f for f in os.listdir(folder_path) if f.endswith(f'{channel}.tif') or f.endswith(f'{channel}.tiff')]
        
        if matching_files:
            images_dict[channel] = [tifffile.imread(os.path.join(folder_path, tiff_file)) for tiff_file in matching_files]

    if not any(images_dict.values()):
        raise ValueError(f'\nNo images with specified suffixes ({channel_list}) found in folder: {folder_path}')

    print(f'\nImages with specified suffixes ({channel_list}) found in folder: {folder_path}')
    
    return images_dict


def read_tiff_folder(folder_path, suffix='', include_paths=False):
    # Get a list of all TIFF files in the folder
    tiff_files = [f for f in os.listdir(folder_path) if f.endswith(f'{suffix}.tif') or f.endswith(f'{suffix}.tiff')]
    
    if not tiff_files:
        # Raise an exception if no TIFF files are found in the folder
        raise ValueError('\nNo TIFF files found in folder: ' + folder_path)
    
    images = []
    file_names = []
    paths = [] if include_paths else None

    for tiff_file in tiff_files:
        tiff_path = os.path.join(folder_path, tiff_file)
        image = tifffile.imread(tiff_path)
        images.append(image)
        file_names.append(tiff_file)
        if include_paths:
            paths.append(tiff_path)

    if len(images) == 1:
        print(f'\nOnly one TIFF file found in folder: {folder_path}')
        images = np.expand_dims(images[0], axis=0)
        file_names = [file_names[0]]
        if include_paths:
            paths = [paths[0]]
        
    else:
        print(f'\n{len(images)} TIFF files found in folder: {folder_path}')

    if include_paths:
        return np.array(images), file_names, paths
    else:
        return np.array(images), file_names
        
# Better use the midline attribute instead of the mesh for such purposes
def mesh2midline(x1, y1, x2, y2):
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    line = np.array([x, y]).T
    line = spline_approximation(line, n = len(x1), smooth_factor = 3, closed = False)
    return line

def get_weighted_intprofile(intensity, width):
    if intensity.shape[0] == width.shape[0]:
        return intensity * width
    else:
        return []
    
def measure_along_midline_interp2d(midline, im_interp2d, width = 7, subpixel = 0.5):

    unit_dxy = unit_perpendicular_vector(midline, closed=False)
    width_normalized_dxy = unit_dxy * subpixel
    
    data = im_interp2d.ev(midline.T[0], midline.T[1])
    for i in range(1, 1+int(width * 0.5 / subpixel)):
        dxy = width_normalized_dxy * i
        v1 = midline + dxy
        v2 = midline - dxy
        p1 = im_interp2d.ev(v1.T[0], v1.T[1])
        p2 = im_interp2d.ev(v2.T[0], v2.T[1])
        data = np.vstack([p1, data, p2])
    prf = np.average(data, axis=0)
    sigma = 2  # standard deviation of Gaussian filter
    prf = gaussian_filter1d(prf, sigma)
    return prf

def get_width(x1, y1, x2, y2):
    width_not_ordered = np.sqrt((x1-x2)**2+(y1-y2)**2)
    return width_not_ordered

def split_mesh2mesh(x1, y1, x2, y2):
    
    contour = mesh2contour(x1, y1, x2, y2)
    width = get_width(x1, y1, x2, y2)
    length = np.sum(get_step_length(x1, y1, x2, y2))
    
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    line = np.array([x, y]).T
    midline, pole1, pole2 = extend_skeleton(line[3:-3], contour)
    l1, l2, profile_mesh, midline = straighten_by_orthogonal_lines(contour, midline, length, width, unit_micron= 0.5)
    result, l1, l2 = add_poles(l1, l2, pole1, pole2)
    return result, contour, midline

def get_profile_mesh(mesh, width, micron_unit = 1):
    l1 = mesh[:,:2]
    l2 = mesh[:,2:]
    sorted_width = sorted(width, reverse = True)
    width = (sum(sorted_width[:math.floor(len(sorted_width)/3)]) / math.floor(len(sorted_width)/3))
    N_width = int(round(np.median(width) / 0.05))
    dl = (l2 - l1) / N_width
    mult_mat = np.tile(np.arange(N_width + 1), (len(l1), 1))
    mat_x = l1[:, 0][:, np.newaxis] + mult_mat * dl[:, 0][:, np.newaxis]
    mat_y = l1[:, 1][:, np.newaxis] + mult_mat * dl[:, 1][:, np.newaxis]
    profile_mesh = np.array([mat_x, mat_y])
    return profile_mesh

def expand_contour(contour, scale= 1):
    """
    enlarges contour
    :param contour:
    :param scale:
    :return:
    """
    area = 0.5 * np.sum(np.diff(contour[:, 0]) * (contour[:-1, 1] + contour[1:, 1]))
    if area < 0:
        # If the area is negative, flip the sign of the unit perpendicular vector
        dxy = unit_perpendicular_vector(contour, closed=True) 
    else:
        # Otherwise, use the unit perpendicular vector as is
        dxy = unit_perpendicular_vector(contour, closed=True) * (-1)
    #dxy = unit_perpendicular_vector(contour, closed=True)

    return contour - (scale * dxy)

def erode_contour(contour, scale= 1):
    """
    shrinks contour
    :param contour:
    :param scale:
    :return:
    """
    area = 0.5 * np.sum(np.diff(contour[:, 0]) * (contour[:-1, 1] + contour[1:, 1]))
    if area < 0:
        # If the area is negative, flip the sign of the unit perpendicular vector
        dxy = unit_perpendicular_vector(contour, closed=True) 
    else:
        # Otherwise, use the unit perpendicular vector as is
        dxy = unit_perpendicular_vector(contour, closed=True) * (-1)
    #dxy = unit_perpendicular_vector(contour, closed=True)

    return contour + (scale * dxy)

def crop_image(contour, image, pad = 10):
    contour = contour.copy()
    contour = contour.astype(int)
    mask = polygon2mask(image.shape, contour)
    
    padding =10
    x, y, w, h = cv.boundingRect(contour)
    x = np.clip(x - padding, 0, image.shape[0])
    y = np.clip(y - padding, 0, image.shape[1])
    w = np.clip(w + 2 * padding, 0, image.shape[0] - x)
    h = np.clip(h + 2 * padding, 0, image.shape[1] - y)

    cropped_img = image[x:x+w, y:y+h]
    cropped_mask = mask[x:x+w, y:y+h]
    return cropped_img, cropped_mask, x, y



def get_object_contours(mask, x_offset, y_offset, smoothing=10):
    contours, _ = cv.findContours(mask.astype(np.uint8), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    interpolated_contours = []

    for contour in contours:
        contour = np.array(contour)
        contourx = contour[:, 0, 1]
        contoury = contour[:, 0, 0]
        s = int(len(contourx) / smoothing) if len(contourx) > smoothing else 1
        tck, u = interpolate.splprep([contourx, contoury], u=None, s=s, per=1)
        u_new = np.linspace(u.min(), u.max(), len(contourx))
        outx, outy = interpolate.splev(u_new, tck, der=0)
        
        interpolated_contour = np.array([outx+x_offset, outy+y_offset]).T
        interpolated_contours.append(interpolated_contour)

    return interpolated_contours

def keep_significant_masks(nucleoid_mask, cropped_mask, min_overlap_ratio=0.01, max_external_ratio=0.1):
    # Find connected components (blobs) in the nucleoid_mask
    num_labels, labels, stats, _ = cv.connectedComponentsWithStats(nucleoid_mask.astype(np.uint8))

    # Create a mask to keep blobs with significant overlap
    significant_mask = np.zeros_like(nucleoid_mask, dtype=np.uint8)

    # Get the total area of the cropped_mask
    total_cropped_mask_area = np.sum(cropped_mask)

    for label in range(1, num_labels):  # Skip label 0 as it represents the background
        # Extract the blob region for the current label
        blob_mask = (labels == label).astype(np.uint8)

        # Calculate the overlap with the cropped_mask
        overlap_area = np.sum(np.logical_and(blob_mask, cropped_mask))

        # Calculate the overlap ratio
        overlap_ratio = overlap_area / total_cropped_mask_area

        # Calculate the external ratio (portion outside of cropped_mask)
        external_area = np.sum(np.logical_and(blob_mask, ~cropped_mask))
        external_ratio = external_area / np.sum(blob_mask)
        # Keep blobs that have a significant overlap with the cropped_mask
        # and don't exceed the maximum external ratio
        if overlap_ratio >= min_overlap_ratio and external_ratio <= max_external_ratio:
            significant_mask |= blob_mask

    return significant_mask


def get_subcellular_objects(contour, signal, cell_id, 
                            log_sigma, 
                            kernel_width, 
                            min_overlap_ratio=0.01, 
                            max_external_ratio=0.1):
    
    cropped_img, cropped_mask, x_offset, y_offset = crop_image(contour, signal)
    bgr = phase_background(cropped_img, cropped_mask)
    cropped_img_bgr = np.maximum(cropped_img - bgr, 0)

    # Apply Laplacian of Gaussian (LoG) filter to the cropped_img
    log_filtered_img = scipy.ndimage.gaussian_laplace(cropped_img_bgr, sigma=log_sigma)

    threshold_value = threshold_otsu(log_filtered_img)
    nucleoid_mask = log_filtered_img < threshold_value
    kernel = np.ones((kernel_width, kernel_width), np.uint8)  # You can adjust the kernel size as needed
    nucleoid_mask = cv.dilate(nucleoid_mask.astype(np.uint8), kernel, iterations=1)

    nucleoid_mask = keep_significant_masks(nucleoid_mask, cropped_mask, min_overlap_ratio, max_external_ratio)

    if np.any(nucleoid_mask == 1):
        object_contours = get_object_contours(nucleoid_mask, x_offset, y_offset)

    else:
        object_contours = None
        print(f'No nucleoids detected in cell {cell_id}')
    return object_contours





