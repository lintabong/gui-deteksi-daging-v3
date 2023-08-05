import numpy
import cv2
from skimage.feature import graycomatrix, graycoprops

def GLCM(img, props=['dissimilarity', 'correlation', 'homogeneity', 'contrast', 'ASM', 'energy'], dists=[5], agls=[0, numpy.pi/4, numpy.pi/2, 3*numpy.pi/4], lvl=256, sym=True, norm=True):
    glcm = graycomatrix(img, 
                        distances=dists, 
                        angles=agls, 
                        levels=lvl,
                        symmetric=sym, 
                        normed=norm)
    result = []
    glcm_props = [propery for name in props for propery in graycoprops(glcm, name)[0]]
    for item in glcm_props:
        result.append(round(item, 3))
    
    contrastMean = round((result[12] + result[13] + result[14] + result[15])/4 ,3)
    corrMean = round((result[4] + result[5] + result[6] + result[7])/4 ,3)
    energyMean = round((result[20] + result[21] + result[22] + result[23])/4 ,3)
    homogenityMean = round((result[8] + result[9] + result[10] + result[11])/4 ,3)

    return [["", "0", "45", "90", "135", "rata-rata"],
            ["Kontras", result[12], result[13], result[14], result[15], contrastMean],
            ["Korelasi", result[4], result[5], result[6], result[7], corrMean],
            ["Energi", result[20], result[21], result[22], result[23], energyMean],
            ["Homogenitas", result[8], result[9], result[10], result[11], homogenityMean]]
