import json
import os
from pyproj import pyproj
import rasterio as rio
import os
from samgeo import SamGeo
from src.image.image_utils import to_uint8
import shutil


sam = None


def generate_mask(storage, image_path, bands, points, pointsLabel, label):
    image_name = os.path.basename(image_path)
    image_url = storage.get_url(image_path)
    # sam temporary files
    sam_tmp_folder = "/tmp/sam/"
    os.makedirs(sam_tmp_folder, exist_ok=True)
    image_name = os.path.splitext(image_name)[0]
    rgb_file = sam_tmp_folder + "rgb" + "_" + image_name + ".tif"
    mask_tif_file = sam_tmp_folder + "mask" + "_" + image_name + ".tif"
    mask_geojson_file = sam_tmp_folder + "mask" + "_" + image_name + ".geojson"
    # generate RGB image
    red = int(bands["bands"]["red"])
    green = int(bands["bands"]["green"])
    blue = int(bands["bands"]["blue"])
    stretch_maximum = int(bands["stretch"]["maximum"])
    stretch_minimum = int(bands["stretch"]["minimum"])
    ds = rio.open(image_url)
    bands = ds.read((red, green, blue))
    rgb = to_uint8(bands, stretch_minimum, stretch_maximum)
    # save RGB as local tif
    profile = ds.profile
    profile.update(count=3, dtype="uint8")
    if not os.path.exists(rgb_file):
        with rio.open(rgb_file, "w", **profile) as dst:
            dst.write(rgb)
    # initialize sam
    global sam
    if sam is None:
        sam = SamGeo(
            checkpoint="sam_vit_h_4b8939.pth",
            model_type="vit_h",
            automatic=False,
            sam_kwargs=None,
        )
    # generate mask
    sam.set_image(rgb_file)
    sam.predict(
        points,
        point_labels=pointsLabel,
        point_crs="EPSG:4326",  # validar ???
        output=mask_tif_file,
    )
    sam.raster_to_vector(
        mask_tif_file,
        mask_geojson_file,
    )
    # adapt reponse to the format expected by the front-end
    transformed_geojson = transform_geojson(mask_geojson_file, ds.crs, label)
    # shutil.rmtree(sam_tmp_folder)
    return transformed_geojson


def transform_geojson(mask_geojson_file, crs, label):
    with open(mask_geojson_file, "r") as f:
        geojson_data = json.load(f)
    transformed_geometries = []
    for feature in geojson_data["features"]:
        coordinates_set = feature["geometry"]["coordinates"]
        transformed_coordinates_collection = []
        for coordinates in coordinates_set:
            transformed_coordinates = []
            for coordinate in coordinates:
                transformed_array = transform_coords(
                    coordinate[0],
                    coordinate[1],
                    crs,
                    "EPSG:4326",
                )
                transformed_coordinates.append(transformed_array)
            transformed_coordinates_collection.append(transformed_coordinates)
        transformed_geometries.append(transformed_coordinates_collection)
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": transformed_geometries,
                },
                "properties": {"labels": [label], "tasks": ["segmentation"]},
            }
        ],
    }
    return geojson_data


def transform_coords(x, y, src_crs, dst_crs, **kwargs):
    transformer = pyproj.Transformer.from_crs(
        src_crs, dst_crs, always_xy=True, **kwargs
    )
    tuple = transformer.transform(x, y)
    return [tuple[0], tuple[1]]
