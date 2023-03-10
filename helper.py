#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Version: v1.0
Date: 2023-03-09
Authors: Chen G.
"""


# ---------------------------------------------------------------------------//
# Cloud Mask
# ---------------------------------------------------------------------------//
def srCloudMask89(image):
    """
    mask cloud for Landsat 89 images

    Parameters
    ----------
    image : ee.Image
        image to apply the cloud masking

    Returns
    -------
    ee.Image
        Masked image

    """
    qa = image.select('QA_PIXEL')
    cloudShadowBitMask = (1 << 4)
    cloudsBitMask = (1 << 3)
    cirrusBitMask = (1 << 2)
    dilatedBitMask = (1 << 1)
    mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0) \
             .And(qa.bitwiseAnd(cloudsBitMask).eq(0)) \
             .And(qa.bitwiseAnd(cirrusBitMask).eq(0)) \
             .And(qa.bitwiseAnd(dilatedBitMask).eq(0))
    return image.updateMask(mask) \
                .copyProperties(image) \
                .copyProperties(image, ["system:time_start",'system:time_end','system:footprint'])


def srCloudMask457(image):
    """
    mask cloud for Landsat 457 images

    Parameters
    ----------
    image : ee.Image
        image to apply the cloud masking

    Returns
    -------
    ee.Image
        Masked image

    """
    qa = image.select('QA_PIXEL')
    dilatedBitMask = (1 << 1)
    cloudsBitMask = (1 << 3) 
    cloudShadowBitMask = (1 << 4)
    mask = qa.bitwiseAnd(cloudsBitMask).eq(0) \
             .And(qa.bitwiseAnd(cloudShadowBitMask).eq(0)) \
             .And(qa.bitwiseAnd(dilatedBitMask).eq(0))
    return image.updateMask(mask) \
                .copyProperties(image) \
                .copyProperties(image, ["system:time_start",'system:time_end','system:footprint'])


# ---------------------------------------------------------------------------//
# Scale images by scale and offset factor
# ---------------------------------------------------------------------------//
def scaleImage89(image):
    """
    scale Landsat 89 images by scale factor and offset factor

    Parameters
    ----------
    image : ee.Image
        image to apply scale

    Returns
    -------
    ee.Image
        Scaled image

    """
    time_start = image.get("system:time_start") 
    opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
    thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0)
    image = image.addBands(opticalBands, None, True).addBands(thermalBands, None, True)
    image = image.set("system:time_start", time_start); 
    return image


def scaleImage457(image):
    """
    scale Landsat 457 images by scale factor and offset factor

    Parameters
    ----------
    image : ee.Image
        image to apply scale

    Returns
    -------
    ee.Image
        Scaled image

    """
    time_start = image.get("system:time_start") 
    opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
    thermalBands = image.select('ST_B6').multiply(0.00341802).add(149.0)
    image = image.addBands(opticalBands, None, True).addBands(thermalBands, None, True)
    image = image.set("system:time_start", time_start); 
    return image
