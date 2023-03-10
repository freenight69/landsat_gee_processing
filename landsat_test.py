#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: landsat_test.py
Version: v1.0
Date: 2023-03-10
Authors: Chen G.
Description: This script creates downloading and processing Landsat 45789 images based on Google Earth Engine.
License: This code is distributed under the MIT License.

    Parameter:
        START_DATE: The earliest date to include images for (inclusive).
        END_DATE: The latest date to include images for (exclusive).
        BANDS: The Landsat image bands to select for processing.
            'blue' - selects the SR_B2 band (0.452-0.512 μm) of Landsat 89; the SR_B1 band (0.45-0.52 μm) of Landsat 457.
            'green' - selects the SR_B3 band (0.533-0.590 μm) of Landsat 89; the SR_B2 band (0.52-0.60 μm) of Landsat 457.
            "red' - selects the SR_B4 band (0.636-0.673 μm) of Landsat 89; the SR_B3 band (0.63-0.69 μm) of Landsat 457.
            'nir' - selects the SR_B5 band (0.851-0.879 μm) of Landsat 89; the SR_B4 band (0.77-0.90 μm) of Landsat 457.
            'swir1' - selects the SR_B6 band (1.566-1.651 μm) of Landsat 89; the SR_B5 band (1.55-1.75 μm) of Landsat 457.
            "swir2' - selects the SR_B7 band (2.107-2.294 μm) of Landsat 89; the SR_B7 band (2.08-2.35 μm) of Landsat 457.
        ROI: The boundry to select for processing.
        CLOUD_COVER_PERCENT: (Optional) cloud cover percentage to apply landsat image collection filter.
        REMOVE_CLOUD: (Optional) whether to do the cloud removal operation.
        CAL_NDVI: (Optional) calculate the Normalized Difference Vegetation Index (NDVI) from multiband s2 images.
        CAL_NDMI: (Optional) calculate the Normalized Difference Moisture Index (NDMI) from multiband s2 images.
        CLIP_TO_ROI: (Optional) clip the processed image to the region of interest.
        EXPORT_CRS : (Optional) the coordinate system of processed collection to export.
        EXPORT_SCALE : (Optional) the scale factor of processed collection to export.
        SAVE_ASSETS : (Optional) exports the processed collection to an asset.
        ASSET_ID : (Optional) the user id path to save the assets
        SAVE_LOCAL : (Optional) download the processed images to local.
        RENDER : (Optional) convert raw image to RGB image and download the processed images to local.
        RENDER_SCALE : (Optional) the scale factor of RGB or NDVI image collection to export.
        LOCAL_DIR : (Optional) where to save downloaded images.
        
    Returns:
        An ee.ImageCollection with an analysis ready Landsat imagery with the cloud masked images and vegetation index band.


    """

import ee
import datetime
import wrapper as wp

# /***************************/
# // MAIN
# /***************************/
# Parameters
roi = ee.Geometry.Polygon(
    [
        [
            [115.16834215367976, 33.701872369004235],
            [115.17627043570991, 33.70131946914559],
            [115.17652898790209, 33.696708742504754],
            [115.19270219396873, 33.695469141510074],
            [115.19269776135631, 33.69603538868455],
            [115.19635419318811, 33.69560736836466],
            [115.19536871569764, 33.688972181515396],
            [115.21243366830475, 33.68769689871397],
            [115.21305799376336, 33.68953402829715],
            [115.20616420338078, 33.69058193647584],
            [115.2065387881696, 33.696369831239814],
            [115.21456072975056, 33.69592841602659],
            [115.21603668394272, 33.699732020060445],
            [115.18431015244617, 33.70197050776158],
            [115.16892178430702, 33.70637164762904],
            [115.16834215367976, 33.701872369004235],
        ]
    ]
)
parameter = {'START_DATE': '2023-01-01',
             'END_DATE': '2023-03-10',
             'BANDS': ['blue', 'green', 'red', 'nir'],
             # 'ROI': ee.Geometry.Rectangle([-47.1634, -3.00071, -45.92746, -5.43836]),
             'ROI': roi,
             'CLOUD_COVER_PERCENT': 50,
             'REMOVE_CLOUD': False,
             'CAL_NDVI': True,
             'CAL_NDMI': False,
             'CLIP_TO_ROI': False,
             'EXPORT_CRS': 'EPSG:4326',
             'EXPORT_SCALE': 30,
             'SAVE_ASSET': False,
             'ASSET_ID': "users/gongchen9369",
             'SAVE_LOCAL': True,
             'RENDER': True,
             'RENDER_SCALE': 100,
             'LOCAL_DIR': "G:/test"
             }

# /***************************/
# // MAIN
# /***************************/
if __name__ == "__main__":
    start_time = datetime.datetime.now()

    # processed s1 collection
    landsat_processed = wp.landsat_preprocess(parameter)

    end_time = datetime.datetime.now()
    # 输出程序运行所需时间
    print("Elapsed Time:", end_time - start_time)
