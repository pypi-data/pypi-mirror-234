# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 14:02:27 2023

@author: Bart Steemans. Govers Lab.
"""

import matplotlib.pyplot as plt
import numpy as np

dpi = 300
def plot_contour(cell, image, title = None):
    fig=plt.figure(figsize=(12,12))
    cellobj = image.cells[cell]
    contour = cellobj.contour
    midline = cellobj.midline
    #ori_contour = image.mesh_dataframe['contour'][cell]
    xmin = np.min(contour.T[1]-10)
    xmax = np.max(contour.T[1]+10)
    ymin = np.min(contour.T[0]-10)
    ymax = np.max(contour.T[0]+10)
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.imshow(image.image, cmap = 'gist_gray')
    
    
    plt.plot(contour.T[1], contour.T[0],'-', c = 'w', lw = 5)
    
    
    #plt.plot(ori_contour.T[1], ori_contour.T[0],'-', c = 'y')
    #plt.plot(midline.T[1], midline.T[0], c = 'cyan')
    plt.title(f"Cell {cellobj.cell_id}")
    if title != None:
        plt.title(f'{title}', fontsize = 16)#
    # plt.savefig('C:/Users/u0158103/Documents/PhD/Pictures/contour_plot.png', dpi=dpi)
    plt.show()

def plot_contour_scientific(cell, image,crop_size=300):
    fig=plt.figure(figsize=(12,12))
    cellobj = image.cells[cell]
    contour = cellobj.contour
    midline = cellobj.midline
    
    # Calculate the center of the contour
    center_x = np.mean(contour.T[1])
    center_y = np.mean(contour.T[0])

    # Calculate the new cropping boundaries based on the fixed crop size
    half_crop_size = crop_size / 2
    xmin = center_x - half_crop_size
    xmax = center_x + half_crop_size
    ymin = center_y - half_crop_size
    ymax = center_y + half_crop_size

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.imshow(image.image, cmap='gist_gray')
    
    plt.plot(contour.T[1], contour.T[0],'-', c = 'w', lw = 5)
    
    
    #plt.plot(ori_contour.T[1], ori_contour.T[0],'-', c = 'y')
    #plt.plot(midline.T[1], midline.T[0], c = 'cyan')
    plt.title(f"Cell {cellobj.cell_id}")
    # Add scale bar
    scale_length_um = 1
    scale_length_px = scale_length_um / 0.065  # Convert µm to pixels
    scale_x = (xmin + xmax) / 2 - scale_length_px / 2  # Center the scale bar
    scale_y = ymin + (ymax - ymin) * 0.02  # Adjust the position of the scale bar
    plt.plot([scale_x, scale_x + scale_length_px], [scale_y, scale_y], color='white', lw=5)

    plt.savefig('C:/Users/u0158103/Documents/PhD/Pictures/contour_plot2.svg', dpi=400)
    plt.show()



def plot_objects(cell, image,chann, title = None):
    fig=plt.figure(figsize=(12,12))
    cellobj = image.cells[cell]
    contour = cellobj.contour
    
    xmin = np.min(contour.T[1]-10)
    xmax = np.max(contour.T[1]+10)
    ymin = np.min(contour.T[0]-10)
    ymax = np.max(contour.T[0]+10)
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.imshow(image.channel[chann], cmap = 'gist_gray')
    plt.plot(contour.T[1], contour.T[0],'-', c = 'yellow', lw = 2)
    if cellobj.object_contours is not None:
        for nuc_contour in cellobj.object_contours:
            plt.plot(nuc_contour.T[1], nuc_contour.T[0],'-', c = 'cyan', lw = 2)
            
    plt.title(f"Cell {cellobj.cell_id}")
    plt.axis('off')
    
    plt.show()

def plot_mesh_scientific(cell, image, crop_size = 300):
    fig=plt.figure(figsize=(12,12))
    cellobj = image.cells[cell]
    profile_mesh = cellobj.profile_mesh
    # Calculate the center of the contour
    center_x = np.mean(cellobj.contour.T[1])
    center_y = np.mean(cellobj.contour.T[0])

    # Calculate the new cropping boundaries based on the fixed crop size
    half_crop_size = crop_size / 2
    xmin = center_x - half_crop_size
    xmax = center_x + half_crop_size
    ymin = center_y - half_crop_size
    ymax = center_y + half_crop_size

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.imshow(image.image, cmap='gist_gray')
    plt.plot(cellobj.contour.T[1], cellobj.contour.T[0],'-', c = 'w')
    
    plt.plot([cellobj.y1[::2], cellobj.y2[::2]], [cellobj.x1[::2], cellobj.x2[::2]], c = 'cyan')
    # Add scale bar
    scale_length_um = 1
    scale_length_px = scale_length_um / 0.065  # Convert µm to pixels
    scale_x = (xmin + xmax) / 2 - scale_length_px / 2  # Center the scale bar
    scale_y = ymin + (ymax - ymin) * 0.02  # Adjust the position of the scale bar
    plt.plot([scale_x, scale_x + scale_length_px], [scale_y, scale_y], color='white', lw=5)
    #plt.scatter(profile_mesh[1][::2].T, profile_mesh[0][::2].T, s = 3, c = 'cyan')
    plt.title(f'Cell number: {cellobj.cell_id} with contour and profiling mesh', fontsize = 16)
    plt.savefig('C:/Users/u0158103/Documents/PhD/Pictures/mesh_plot_scientific2.svg', dpi=400)
    plt.show()
    
def plot_mesh(cell, image, title):
    fig=plt.figure(figsize=(12,12))
    cellobj = image.cells[cell]
    profile_mesh = cellobj.profile_mesh
    xmin = np.min(profile_mesh[1]-10)
    xmax = np.max(profile_mesh[1]+10)
    ymin = np.min(profile_mesh[0]-10)
    ymax = np.max(profile_mesh[0]+10)
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.imshow(image.image, cmap = 'gist_gray')
    plt.plot(cellobj.contour.T[1], cellobj.contour.T[0],'-', c = 'w')
    
    plt.plot([cellobj.y1[::2], cellobj.y2[::2]], [cellobj.x1[::2], cellobj.x2[::2]], c = 'cyan')
    #plt.scatter(profile_mesh[1][::2].T, profile_mesh[0][::2].T, s = 3, c = 'cyan')
    plt.title(f'Cell number: {cellobj.cell_id} with contour and profiling mesh', fontsize = 16)
    plt.savefig('C:/Users/u0158103/Documents/PhD/Pictures/mesh_plot.png', dpi=dpi)
    plt.show()
    
def plot_comparison(cell, image):    
    cellobj = image.cells[cell]    
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    profile_mesh = cellobj.profile_mesh
    profiling_data = cellobj.profiling_data
    
    
    int_midline = profiling_data['phaco_midline_intensity']
    int_axial = profiling_data['phaco_axial_intensity']
    int_average_mesh = profiling_data['phaco_average_mesh_intensity']
    # weighted_intensity = profiling_data['phaco_weighted_intensity']
    # CD = round(profiling_data['CD'], 3)
    # relpos = round(profiling_data['relpos'], 3)
    xmin = np.min(profile_mesh[1]-10)
    xmax = np.max(profile_mesh[1]+10)
    ymin = np.min(profile_mesh[0]-10)
    ymax = np.max(profile_mesh[0]+10)
    axs[0].set_position([0.05, 0.05, 0.4, 0.9])
    axs[0].imshow(image.image, cmap='gist_gray')
    axs[0].plot(cellobj.contour.T[1], cellobj.contour.T[0],'-', c = 'r')
    axs[0].plot(cellobj.midline.T[1],cellobj.midline.T[0],'-', c = 'y')
    #plt.scatter(profile_mesh[1].T, profile_mesh[0].T, s = 3, c = 'cyan')
    # axs[0].set_title(f'Constriction Degree: {CD} \n Relative Position: {relpos}')
    axs[0].set_xlabel(f'Cell Number: {cell}')
    axs[0].set_xlim(xmin, xmax)
    axs[0].set_ylim(ymin, ymax)
    
    # axs[1].plot(int_axial/25000, c = 'y') 
    # axs[1].plot(weighted_intensity/25000)
    # axs[1].plot(cellobj.contour_features['cell_widthno'], c = 'r')
    
    axs[1].plot(int_midline, c = 'r')
    axs[1].plot(int_axial, c = 'm')
    axs[1].plot(int_average_mesh, c = 'b')
   
    axs[1].set_xlabel('Cell Length')
    axs[1].set_ylabel('Intensity [pixel value]')    
    axs[1].legend(['strip (1) intensity', 'strip (7) intensity', 'profile intensity'], frameon = False)

    # axs[1].set_ylabel('Normalized values')
    # axs[1].legend(['Intensity', 'Weighted Intensity', 'Width'], frameon = False)
    plt.show()

def plot_exp_contour(cell, image):    
    cellobj = image.cells[cell]    
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    profile_mesh = cellobj.profile_mesh
    profiling_data = cellobj.profiling_data
    contour_intensity = profiling_data['phaco_expanded_contour_intensity']
    exp_contour = profiling_data['expanded_contour']

    
    # int_traditional = profiling_data['phaco_intensity']
    # int_mesh_midline = profiling_data['phaco_axial_intensity']
    # int_midline = profiling_data['phaco_average_mesh_intensity']
    
    xmin = np.min(profile_mesh[1]-10)
    xmax = np.max(profile_mesh[1]+10)
    ymin = np.min(profile_mesh[0]-10)
    ymax = np.max(profile_mesh[0]+10)
    axs[0].set_position([0.05, 0.05, 0.4, 0.9])
    axs[0].imshow(image.image, cmap='gist_gray')
    axs[0].plot(exp_contour.T[1], exp_contour.T[0],'-', c = 'r')
    axs[0].plot(cellobj.midline.T[1],cellobj.midline.T[0],'-', c = 'y')
    #plt.scatter(profile_mesh[1].T, profile_mesh[0].T, s = 3, c = 'cyan')
    axs[0].set_title('profiling mesh')
    axs[0].set_xlabel(f'Cell Number: {cell}')
    axs[0].set_xlim(xmin, xmax)
    axs[0].set_ylim(ymin, ymax)
    
    #axs[1].plot(int_traditional, c = 'y')
    # axs[1].plot(int_mesh_midline, c = 'k')
    # axs[1].plot(int_midline, c = 'b')
    axs[1].plot(contour_intensity, c = 'b')
    axs[1].set_ylim(0, 27000)

    #axs[1].plot(cellobj.features.width_not_ordered, c = 'cyan')
    #axs[1].legend(['midline intensity', 'strip intensity', 'profile intensity'])
    axs[1].legend(['expaned_contour_intensity'], frameon = False)
    plt.show()
    
def plot_width(cell, image, crop_size = 70):    
    cellobj = image.cells[cell]   
    other_cellobj = image.cells[cell + 44]

    fig1, axs1 = plt.subplots(figsize=(12, 12))
    profile_mesh = cellobj.profile_mesh

    center_x = np.mean(cellobj.contour.T[1])
    center_y = np.mean(cellobj.contour.T[0])

    # Calculate the new cropping boundaries based on the fixed crop size
    half_crop_size = crop_size / 2
    xmin = center_x - half_crop_size
    xmax = center_x + half_crop_size
    ymin = center_y - half_crop_size
    ymax = center_y + half_crop_size

    axs1.set_position([0.1, 0.1, 0.5, 0.8])
    axs1.imshow(image.image, cmap='gist_gray')
    axs1.plot(cellobj.contour.T[1], cellobj.contour.T[0], lw=3, c='orange')

    axs1.set_xlim(xmin, xmax)
    axs1.set_ylim(ymin, ymax)
    # Add scale bar
    scale_length_um = 1
    scale_length_px = scale_length_um / 0.065  # Convert µm to pixels
    scale_x = (xmin + xmax) / 2 - scale_length_px / 2  # Center the scale bar
    scale_y = ymin + (ymax - ymin) * 0.02  # Adjust the position of the scale bar
    axs1.plot([scale_x, scale_x + scale_length_px], [scale_y, scale_y], color='white', lw=5)
    axs1.set_xticks([])
    axs1.set_yticks([])
    axs1.set_title('Cell ' + str(cell), fontname='Arial', fontsize=14)
    
    fig2, axs2 = plt.subplots(figsize=(6, 4))

    # Plot the cell width for the first cell (red curve)
    axs2.plot(cellobj.profiling_data['cell_widthno'], c='orange')
    
    # Plot the cell width for the other cell (green curve)
    axs2.plot(other_cellobj.profiling_data['cell_widthno'], c='b')
    
    # Set x-axis ticks and labels
    newxticks = [np.round(cellobj.contour_features['cell_length'] * (tick / profile_mesh.shape[1]), 1) for tick in axs2.get_xticks()]
    axs2.set_xticks(axs2.get_xticks())
    axs2.set_xticklabels(newxticks, fontname='Arial', fontsize=12)
    
    # Set y-axis ticks and label
    newyticks = [np.round(tick, 1) for tick in axs2.get_yticks()]
    axs2.set_yticks(axs2.get_yticks())
    axs2.set_yticklabels(newyticks, fontname='Arial', fontsize=12)
    
    # Set x-axis to start at 0
    axs2.set_xlim(left=0)
    axs2.set_ylim(bottom=0)
    # Set x and y axis labels
    axs2.set_xlabel('cell length [µm]', fontname='Arial', fontsize=12)
    axs2.set_ylabel('cell width [µm]', fontname='Arial', fontsize=12)

    axs2.legend(['overlapping cell', 'single cell'], frameon=False)

    fig3, axs3 = plt.subplots(figsize=(12, 12))
    other_profile_mesh = other_cellobj.profile_mesh

    center_x = np.mean(other_cellobj.contour.T[1])
    center_y = np.mean(other_cellobj.contour.T[0])

    # Calculate the new cropping boundaries based on the fixed crop size
    half_crop_size = crop_size / 2
    xmin = center_x - half_crop_size
    xmax = center_x + half_crop_size
    ymin = center_y - half_crop_size
    ymax = center_y + half_crop_size

    axs3.set_position([0.1, 0.1, 0.5, 0.8])
    axs3.imshow(image.image, cmap='gist_gray')
    axs3.plot(other_cellobj.contour.T[1], other_cellobj.contour.T[0], lw=3, c='b')

    axs3.set_xlim(xmin, xmax)
    axs3.set_ylim(ymin, ymax)

    axs3.set_xticks([])
    axs3.set_yticks([])
    axs3.set_title('Other Cell', fontname='Arial', fontsize=14)
    scale_length_um = 1
    scale_length_px = scale_length_um / 0.065  # Convert µm to pixels
    scale_x = (xmin + xmax) / 2 - scale_length_px / 2  # Center the scale bar
    scale_y = ymin + (ymax - ymin) * 0.02  # Adjust the position of the scale bar
    axs3.plot([scale_x, scale_x + scale_length_px], [scale_y, scale_y], color='white', lw=5)
    
    fig1.savefig('C:/Users/u0158103/Documents/PhD/Pictures/bad_cell_image.svg', dpi=300)
    fig2.savefig('C:/Users/u0158103/Documents/PhD/Pictures/width.svg', dpi=300)
    fig3.savefig('C:/Users/u0158103/Documents/PhD/Pictures/good_cell_image.svg', dpi=300)
    plt.show()



def plot_signal_profile(cell, image):
    cellobj = image.cells[cell]
    profile_mesh = cellobj.profile_mesh
    profiling_mesh = cellobj.profiling_data['phaco_mesh_intensity']
    fig, ax = plt.subplots(2,1, figsize = (10, 10))
    xmin = np.min(profile_mesh[1]-10)
    xmax = np.max(profile_mesh[1]+10)
    ymin = np.min(profile_mesh[0]-10)
    ymax = np.max(profile_mesh[0]+10)
    ax[0].imshow(profiling_mesh, aspect='auto')
    ax[0].get_xticks()
    xticks = (ax[0].get_xticks())
    newxticks = [np.round(cellobj.contour_features['cell_length'] * (tick / profiling_mesh.shape[1]), 1) for tick in
                 xticks]
    ax[0].set_xticklabels(newxticks, fontname='Arial', fontsize=12)
    ax[0].set_yticks([])
    ax[0].set_ylabel('signal\nstraighten image\n', fontname='Arial', fontsize=12)
    ax[0].set_xlabel('cell length [µm]', fontname='Arial', fontsize=12)
    
    
    ax[1].imshow(image, cmap='gist_gray', aspect = 'auto')
    ax[1].plot(cellobj.contour.T[1], cellobj.contour.T[0],'-', c = 'r')
    ax[1].plot(cellobj.midline.T[1],cellobj.midline.T[0],'-', c = 'y')
    ax[1].set_xlim(xmin, xmax)
    ax[1].set_ylim(ymin, ymax)
    plt.show()