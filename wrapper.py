#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Version: v1.0
Date: 2023-03-09
Authors: Chen G.
Description: A wrapper function to derive the Landsat images
"""

import ee
import geemap
import os
import helper
import cal_index as ci

# VPN port
geemap.set_proxy(port=5188)
try:
    ee.Initialize()
except:
    ee.Authenticate()
    ee.Initialize()


###########################################
# DO THE JOB
###########################################

def landsat_preprocess(params):
    """
    Applies preprocessing to a collection of landsat images to return an analysis ready landsat data.

    Parameters
    ----------
    params : Dictionary
        These parameters determine the data selection and image processing parameters.

    Raises
    ------
    ValueError


    Returns
    -------
    ee.ImageCollection
        A processed Landsat image collection

    """

    START_DATE = params['START_DATE']
    END_DATE = params['END_DATE']
    BANDS = params['BANDS']
    ROI = params['ROI']
    CLOUD_COVER_PERCENT = params['CLOUD_COVER_PERCENT']
    REMOVE_CLOUD = params['REMOVE_CLOUD']
    CAL_NDVI = params['CAL_NDVI']
    CAL_NDMI = params['CAL_NDMI']
    CLIP_TO_ROI = params['CLIP_TO_ROI']
    EXPORT_CRS = params['EXPORT_CRS']
    EXPORT_SCALE = params['EXPORT_SCALE']
    SAVE_ASSET = params['SAVE_ASSET']
    ASSET_ID = params['ASSET_ID']
    SAVE_LOCAL = params['SAVE_LOCAL']
    RENDER = params['RENDER']
    RENDER_SCALE = params['RENDER_SCALE']
    LOCAL_DIR = params['LOCAL_DIR']

    ###########################################
    # 0. CHECK PARAMETERS
    ###########################################

    if CLOUD_COVER_PERCENT is None:
        CLOUD_COVER_PERCENT = 100
    if REMOVE_CLOUD is None:
        REMOVE_CLOUD = False
    if CAL_NDVI is None:
        CAL_NDVI = False
    if CAL_NDMI is None:
        CAL_NDMI = False
    if EXPORT_CRS is None:
        EXPORT_CRS = 'EPSG:4326'
    if EXPORT_SCALE is None:
        EXPORT_SCALE = 30
    if RENDER is None:
        RENDER = False
    if RENDER_SCALE is None:
        RENDER_SCALE = 100

    bands_required = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2']
    if not any(band in bands_required for band in BANDS):
        raise ValueError("ERROR!!! Parameter BANDS not correctly defined")

    if CLOUD_COVER_PERCENT < 0 or CLOUD_COVER_PERCENT > 100:
        raise ValueError("ERROR!!! Parameter CLOUD_COVER_PERCENT not correctly defined")

    ###########################################
    # 1. DATA SELECTION
    ###########################################

    # import Landsat image collection
    l9_sr = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")
    l8_sr = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
    l7_sr = ee.ImageCollection("LANDSAT/LE07/C02/T1_L2") 
    l5_sr = ee.ImageCollection("LANDSAT/LT05/C02/T1_L2")
    l4_sr = ee.ImageCollection("LANDSAT/LT04/C02/T1_L2")
    
    # select image collection by cloud coverage
    l9Col = l9_sr.filterDate(START_DATE, END_DATE) \
                 .filterBounds(ROI) \
                 .filter(ee.Filter.lte('CLOUD_COVER', CLOUD_COVER_PERCENT))

    l8Col = l8_sr.filterDate(START_DATE, END_DATE) \
                 .filterBounds(ROI) \
                 .filter(ee.Filter.lte('CLOUD_COVER', CLOUD_COVER_PERCENT))
    
    l7Col = l7_sr.filterDate(START_DATE, END_DATE) \
                 .filterBounds(ROI) \
                 .filter(ee.Filter.lte('CLOUD_COVER', CLOUD_COVER_PERCENT))
    
    l5Col = l5_sr.filterDate(START_DATE, END_DATE) \
                 .filterBounds(ROI) \
                 .filter(ee.Filter.lte('CLOUD_COVER', CLOUD_COVER_PERCENT))
    
    l4Col = l4_sr.filterDate(START_DATE, END_DATE) \
                 .filterBounds(ROI) \
                 .filter(ee.Filter.lte('CLOUD_COVER', CLOUD_COVER_PERCENT))

    ###########################################
    # 2. REMOVE CLOUD
    ###########################################

    if REMOVE_CLOUD:
        # remove cloud function
        l9Col = l9Col.map(helper.srCloudMask89)
        l8Col = l8Col.map(helper.srCloudMask89)
        l7Col = l7Col.map(helper.srCloudMask457)
        l5Col = l5Col.map(helper.srCloudMask457)
        l4Col = l4Col.map(helper.srCloudMask457)
    
    ###########################################
    # 3. SCALE FACTOR
    ###########################################

    # scale function
    l9Col = l9Col.map(helper.scaleImage89)
    l8Col = l8Col.map(helper.scaleImage89)
    l7Col = l7Col.map(helper.scaleImage457)
    l5Col = l5Col.map(helper.scaleImage457)
    l4Col = l4Col.map(helper.scaleImage457)

    ###########################################
    # 4. SELECT BANDS
    ###########################################

    # bands correspondence
    bands89 = []
    bands457 = []
    spectrum_bands = []
    if 'blue' in BANDS:
        bands89.append('SR_B2')
        bands457.append('SR_B1')
        spectrum_bands.append('blue')
    if 'green' in BANDS:
        bands89.append('SR_B3')
        bands457.append('SR_B2')
        spectrum_bands.append('green')
    if 'red' in BANDS:
        bands89.append('SR_B4')
        bands457.append('SR_B3')
        spectrum_bands.append('red')
    if 'nir' in BANDS:
        bands89.append('SR_B5')
        bands457.append('SR_B4')
        spectrum_bands.append('nir')
    if 'swir1' in BANDS:
        bands89.append('SR_B6')
        bands457.append('SR_B5')
        spectrum_bands.append('swir1')
    if 'swir2' in BANDS:
        bands89.append('SR_B7')
        bands457.append('SR_B7')
        spectrum_bands.append('swir2')
    
    l9Col = l9Col.select(bands89, spectrum_bands)
    l8Col = l8Col.select(bands89, spectrum_bands)
    l7Col = l7Col.select(bands457, spectrum_bands)
    l5Col = l5Col.select(bands457, spectrum_bands)
    l4Col = l4Col.select(bands457, spectrum_bands)
    
    ###########################################
    # 5. CALCULATE VEGETATION INDEX
    ###########################################
 
    if CAL_NDVI:
        l9Col = l9Col.map(ci.cal_ndvi)
        l8Col = l8Col.map(ci.cal_ndvi)
        l7Col = l7Col.map(ci.cal_ndvi)
        l5Col = l5Col.map(ci.cal_ndvi)
        l4Col = l4Col.map(ci.cal_ndvi)
    if CAL_NDMI:
        l9Col = l9Col.map(ci.cal_ndmi)
        l8Col = l8Col.map(ci.cal_ndmi)
        l7Col = l7Col.map(ci.cal_ndmi)
        l5Col = l5Col.map(ci.cal_ndmi)
        l4Col = l4Col.map(ci.cal_ndmi)
    
    ###########################################
    # 6. MERGE IMAGE COLLECTION
    ###########################################
 
    lxCol = l9Col.merge(l8Col) \
             .merge(l7Col) \
             .merge(l5Col) \
             .merge(l4Col) \
             .sort('system:time_start')
    print('Toal Images Count:', lxCol.size().getInfo())
    
    # Get ImageCollection footprint list
    sizeRaw = lxCol.size().getInfo()
    imlistRaw = lxCol.toList(sizeRaw)
    footprintList = []
    for idx in range(0, sizeRaw):
        img = imlistRaw.get(idx)
        img = ee.Image(img)
        footprint = ee.Geometry(img.get('system:footprint'))
        footprintList.append(footprint)

    ###########################################
    # 4. OUTPUT
    ###########################################

    # clip to roi
    if CLIP_TO_ROI:
        lxCol = lxCol.map(lambda image: image.clip(ROI))

    # save to asset
    if SAVE_ASSET:
        size = lxCol.size().getInfo()
        imlist = lxCol.toList(size)
        for idx in range(0, size):
            img = imlist.get(idx)
            img = ee.Image(img)
            name = str(img.id().getInfo()).split("L")[1]
            name = "L" + name
            description = name
            assetId = ASSET_ID + '/' + name

            task = ee.batch.Export.image.toAsset(image=img,
                                                 assetId=assetId,
                                                 description=description,
                                                 region=lxCol.geometry(),
                                                 scale=EXPORT_SCALE,
                                                 maxPixels=1e13)
            task.start()
            print('Exporting {} to {}'.format(name, assetId))

    # save to local
    if SAVE_LOCAL:

        size = lxCol.size().getInfo()
        imlist = lxCol.toList(size)
        for idx in range(0, size):
            img = imlist.get(idx)
            img = ee.Image(img)
            name = str(img.id().getInfo()).split("L")[1]
            name = "L" + name
            print(name)

            # save raw images to local
            if not os.path.exists(LOCAL_DIR):
                os.makedirs(LOCAL_DIR)
            filename_raw = os.path.join(LOCAL_DIR, name + '.tif')
            print('Downloading Raw Image: {} to {}'.format(name, filename_raw))
            if CLIP_TO_ROI:
                geemap.download_ee_image(img, filename_raw, region=ROI, crs=EXPORT_CRS, scale=EXPORT_SCALE)
            else:
                geemap.download_ee_image(img, filename_raw, region=footprintList[idx], crs=EXPORT_CRS,
                                         scale=EXPORT_SCALE)

            # save visualization images to local
            if RENDER:
                rgb_bands = ['red', 'green', 'blue']
                if not any(i in rgb_bands for i in BANDS):
                    raise ValueError("ERROR!!! Only can convert RGB bands image into an 32-int RGB image")
                img_rgb = img.select(rgb_bands)
                rgbImage = img_rgb.visualize(**{
                    'bands': rgb_bands,
                    'min': 0.0,
                    'max': 0.3
                })
                filename_rgb = os.path.join(LOCAL_DIR, name + '_render_RGB.tif')
                print('Downloading Visualization RGB Image to {}'.format(filename_rgb))
                if CLIP_TO_ROI:
                    geemap.ee_export_image(rgbImage, filename=filename_rgb, scale=RENDER_SCALE, crs=EXPORT_CRS, region=ROI)
                else:
                    geemap.ee_export_image(rgbImage, filename=filename_rgb, scale=RENDER_SCALE, crs=EXPORT_CRS, region=footprintList[idx])

                if CAL_NDVI:
                    img_ndvi = img.select('NDVI')
                    ndviImage = img_ndvi.visualize(**{
                        'bands': ['NDVI'],
                        'min': 0.0,
                        'max': 1.0,
                        'palette': ['FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163',
                                    '99B718', '74A901', '66A000', '529400', '3E8601',
                                    '207401', '056201', '004C00', '023B01', '012E01',
                                    '011D01', '011301']
                    })
                    filename_vis_ndvi = os.path.join(LOCAL_DIR, name + '_render_NDVI.tif')
                    print('Downloading Visualization NDVI Image to {}'.format(filename_vis_ndvi))
                    if CLIP_TO_ROI:
                        # geemap.download_ee_image(ndviImage, filename_vis_ndvi, region=ROI, crs=EXPORT_CRS, scale=RENDER_SCALE, dtype='int32')
                        geemap.ee_export_image(ndviImage, filename=filename_vis_ndvi, scale=RENDER_SCALE, crs=EXPORT_CRS, region=ROI)
                    else:
                        # geemap.download_ee_image(ndviImage, filename_vis_ndvi, region=footprintList[idx], crs=EXPORT_CRS, scale=RENDER_SCALE, dtype='int32')
                        geemap.ee_export_image(ndviImage, filename=filename_vis_ndvi, scale=RENDER_SCALE, crs=EXPORT_CRS, region=footprintList[idx])
    return lxCol
