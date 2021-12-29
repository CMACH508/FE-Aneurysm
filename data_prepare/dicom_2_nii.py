import os
import pydicom as dicom
import numpy as np
import SimpleITK
import nibabel as nib
import matplotlib
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
import scipy
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure, feature



folder_name = "./data/DICOM/"
out_path = "./data/nii_file"

def load_scan(path):
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key = lambda x: float(x.ImagePositionPatient[2]))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
 
    for s in slices:
        s.SliceThickness = slice_thickness
    return slices

def get_pixels_hu(slices):
    image = np.stack([s.pixel_array for s in slices])
    image = image.astype(np.int16)
    image[image == -2000] = 0
    for slice_number in range(len(slices)):
 
        intercept = slices[slice_number].RescaleIntercept
        slope = slices[slice_number].RescaleSlope
 
        if slope != 1:
            image[slice_number] = slope * image[slice_number].astype(np.float64)
            image[slice_number] = image[slice_number].astype(np.int16)
 
        image[slice_number] += np.int16(intercept)
 
    return np.array(image, dtype=np.int16)



folders = os.listdir(folder_name)

for folder in folders:
    print(folder)
    try:
        patient = load_scan(folder_name + folder)
        patient_pixels = get_pixels_hu(patient)
        print(patient_pixels.shape)
        image_refer = patient_pixels.copy()
        c,w,h = patient_pixels.shape
        for i in range(c):
            patient_pixels[i] = image_refer[c-i-1]
        new_img = nib.Nifti1Image(patient_pixels,np.eye(4))
        nib.save(new_img,out_path + "/" + folder + ".nii.gz")
    except:
        continue
