import ee

def get_air_pollution(geometry, start_date, end_date):
    try:
        # Load NO2 dataset
        collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2") \
            .filterBounds(geometry) \
            .filterDate(start_date, end_date) \
            .select("tropospheric_NO2_column_number_density")

        # Check if collection is empty
        count = collection.size().getInfo()
        if count == 0:
            return {
                "no2_value": None,
                "level": "No Data (Empty Collection)"
            }

        # Mean image
        image = collection.mean()

        # Reduce region
        stats = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=1000,
            bestEffort=True,
            maxPixels=1e9
        )

        no2 = stats.get("tropospheric_NO2_column_number_density")

        # Handle None safely
        if no2 is None:
            return {
                "no2_value": None,
                "level": "No Data"
            }

        # Convert to number
        no2_value = ee.Number(no2).getInfo()

        if no2_value is None:
            return {
                "no2_value": None,
                "level": "No Data"
            }

        # Classification
        if no2_value < 0.00005:
            level = "Low"
        elif no2_value < 0.0001:
            level = "Moderate"
        else:
            level = "High"

        return {
            "no2_value": round(no2_value, 8),
            "level": level
        }

    except Exception as e:
        return {
            "no2_value": None,
            "level": "Error",
            "error": str(e)
        }