import ee
import os

# =====================================================
# GOOGLE EARTH ENGINE – SERVICE ACCOUNT AUTHENTICATION
# =====================================================

# 🔴 CHANGE THIS LINE ONLY
# Replace with your EXACT service account email
SERVICE_ACCOUNT = "gee-fastapi@satellite-vision-project.iam.gserviceaccount.com"

# 🔹 DO NOT CHANGE THIS (file already placed correctly)
KEY_FILE = os.path.join(os.path.dirname(__file__), "gee-key.json")

# Initialize Earth Engine with service account
credentials = ee.ServiceAccountCredentials(
    SERVICE_ACCOUNT,
    KEY_FILE
)
ee.Initialize(credentials)

# =====================================================
# NDVI + RGB IMAGE (SAME SENTINEL-2 IMAGE)
# =====================================================
def get_ndvi_and_rgb(geometry, start_date, end_date):

    try:
        collection = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(geometry)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
            .sort("CLOUDY_PIXEL_PERCENTAGE")
        )

        image = ee.Image(collection.first())

        # ================= NDVI =================
        ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")

        ndvi_value = ndvi.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=10,
            maxPixels=1e13
        ).get("NDVI").getInfo()

        # ================= WATER DETECTION =================
        # NDWI (better for water)
        ndwi = image.normalizedDifference(["B3", "B8"]).rename("NDWI")

        water_mask = ndwi.gt(0)

        water_area = water_mask.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=10,
            maxPixels=1e13
        ).getInfo()

        water_percent = int(water_area.get("NDWI", 0) * 100)

        # ================= RGB =================
        thumbnail_params = {
            "bands": ["B4", "B3", "B2"],
            "min": 300,
            "max": 2200,
            "gamma": 1.4,
            "dimensions": 350,
            "region": geometry,
            "format": "png"
        }

        rgb_url = image.getThumbURL(thumbnail_params)

        return {
            "ndvi": ndvi_value,
            "water": water_percent,   # 🔥 NEW
            "rgb_url": rgb_url
        }

    except Exception as e:
        print("Earth Engine Error:", e)
        return {
            "ndvi": None,
            "water": 0,
            "rgb_url": None
        }