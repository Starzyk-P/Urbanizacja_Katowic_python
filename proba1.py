import ee
import numpy as np
import pandas as pd

ee.Initialize(project="proba1-454320")

katowice_bbox = ee.Geometry.Rectangle([18.94, 50.19, 19.08, 50.32])

sentinel_2024 = ee.ImageCollection("COPERNICUS/S2_HARMONIZED") \
    .filterBounds(katowice_bbox) \
    .filterDate("2024-01-01", "2024-12-31") \
    .median()  

sentinel_2015 = ee.ImageCollection("COPERNICUS/S2_HARMONIZED") \
    .filterBounds(katowice_bbox) \
    .filterDate("2015-01-01", "2015-12-31") \
    .median()  


def calculate_ndbi(image):
    swir = image.select("B11")  #SWIR
    nir = image.select("B8")  # NIR
    ndbi = swir.subtract(nir).divide(swir.add(nir)).rename("NDBI")
    return image.addBands(ndbi)

ndbi_2024 = calculate_ndbi(sentinel_2024)
ndbi_2015 = calculate_ndbi(sentinel_2015)

import matplotlib.pyplot as plt
ndbi_diff = ndbi_2024.select("NDBI").subtract(ndbi_2015.select("NDBI"))

task = ee.batch.Export.image.toDrive(
    image=ndbi_diff,
    description="NDBI_Katowice",
    scale=30,
    region=katowice_bbox,
    fileFormat="GeoTIFF"
)
task.start()

