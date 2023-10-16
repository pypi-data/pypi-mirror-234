from pystac import Catalog, MediaType, Collection
import os
import json
from src.storage import Storage
import shutil
import numpy as np


geotiff_type = "image/tiff; application=geotiff"
allowed_media_types = [media_type.value for media_type in MediaType]
label_extension = "https://stac-extensions.github.io/label/v1.0.1/schema.json"
scaneo_asset = "labels"
scaneo_properties_key = "labels"
scaneo_labels_and_colors = "scaneo:colors"
image_mode = os.getenv("IMAGE")
asset_name_appendix = "_labels.geojson"


def is_stac(storage):
    return storage.exists("catalog.json")


def get_stac_catalog() -> Catalog:
    storage = Storage()
    catalog_file = [f for f in storage.list() if f.endswith("catalog.json")]
    if not catalog_file:
        return None
    catalog_path = storage.get_url(catalog_file[0])
    catalog = Catalog.from_file(catalog_path)
    return catalog


def save_json(file_path, json_file):
    with open(file_path, "w") as f:
        json.dump(json_file, f)


def get_asset_path(label_item, asset_href):
    is_relative = asset_href.startswith("./")
    if is_relative:
        return os.path.normpath(os.path.join(os.path.dirname(label_item), asset_href))
    else:
        return asset_href


class Stac:
    def __init__(self, catalog=get_stac_catalog()):
        self.catalog = catalog

    def get_catalog(self):
        return self.catalog

    def collections(self):
        return list(self.catalog.get_children())

    def collection_links(self):
        return self.catalog.get_child_links()

    def get_items_paths(self, collection):
        collection_path = collection.get_self_href()
        with open(collection_path, "r") as collection_item:
            collection_json = json.load(collection_item)
        relative_hrefs = [
            link["href"] for link in collection_json["links"] if link["rel"] == "item"
        ]
        folder_path = os.path.dirname(collection_path)
        paths = [
            os.path.normpath(os.path.join(folder_path, relative_href))
            for relative_href in relative_hrefs
        ]
        return paths

    def find_label_collection(self):
        return next(
            filter(
                lambda collection: label_extension in collection.stac_extensions,
                self.collections(),
            )
        )

    def create_label_collection(self):
        catalog_path = self.catalog.self_href
        labels_dir = catalog_path.replace("catalog.json", "labels")
        print("INFO: no label collection found, creating one in", labels_dir)
        if not os.path.exists(labels_dir):
            os.makedirs(labels_dir)
        source_collection_path = self.source_collection().self_href
        shutil.copy(source_collection_path, labels_dir)
        label_collection_path = labels_dir + "/collection.json"
        with open(label_collection_path, "r") as collection_item:
            collection_json = json.load(collection_item)
            collection_json["id"] = "labels"
            collection_json["description"] = "Labels"
            collection_json["links"] = []
            collection_json["stac_extensions"] = [label_extension]
            collection_json["summaries"] = {
                scaneo_labels_and_colors: [],
                "label:classes": [{"classes": [], "name": "labels"}],
                "label:type": image_mode,
            }
            save_json(label_collection_path, collection_json)
            collection = Collection.from_dict(collection_json)
            self.catalog.add_child(collection)
            self.catalog.save()
        return collection

    def label_collection(self):
        try:
            return self.find_label_collection()
        except StopIteration:
            return self.create_label_collection()

    def get_labels(self):
        label_collection = self.label_collection().get_self_href()
        if label_collection is None:
            return []
        with open(label_collection, "r") as item:
            collection_json = json.load(item)
            summaries = collection_json["summaries"]
            label_classes = summaries["label:classes"]
            if len(label_classes) > 1:
                print("WARNING: more than one label set found, using the first one")
            target_labels = label_classes[0]
            return target_labels["classes"]

    def get_label_colors(self):
        label_collection = self.label_collection().to_dict()
        summaries = label_collection["summaries"]
        return (
            summaries[scaneo_labels_and_colors]
            if scaneo_labels_and_colors in summaries
            else []
        )

    def get_scaneo_labels_and_colors(self):
        storage = Storage()
        labels_file = [f for f in storage.list() if f.endswith("labels.json")]
        if len(labels_file) > 0:
            labels_and_colors_json = storage.read(labels_file[0])["labels"]
            self.save_labels(labels_and_colors_json)
            print(
                "INFO: labels.json found, using it as labels and colors for the STAC catalog"
            )
            return labels_and_colors_json
        return []

    def get_labels_and_colors(self):
        labels = self.get_labels()
        colors = self.get_label_colors()
        if len(labels) < 1:
            return self.get_scaneo_labels_and_colors()
        labels_and_colors = [{"name": label} for label in labels]
        for i, label in enumerate(labels_and_colors):
            if label["name"] in colors:
                labels_and_colors[i]["color"] = colors[label["name"]]
        return labels_and_colors

    def find_label_item(self, image_path):
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        label_paths = self.get_items_paths(self.label_collection())
        if not label_paths:
            return None
        for path in label_paths:
            item_name = os.path.splitext(os.path.basename(path))[0]
            if item_name == image_name:
                return path
        return None

    def create_label_item(self, image_path):
        name = os.path.splitext(os.path.basename(image_path))[0]
        collection_path = self.label_collection().get_self_href()
        label_dir = collection_path.replace("collection.json", name)
        if not os.path.exists(label_dir):
            os.makedirs(label_dir)
        source_item = self.find_source_item(image_path)
        shutil.copy(source_item, label_dir)
        label_path = label_dir + f"/{name}.json"
        with open(label_path, "r") as label_item:
            label = json.load(label_item)
            label["stac_extensions"].append(label_extension)
            label["collection"] = "labels"
            label["assets"] = {}
            label["properties"]["label:properties"] = ["labels"]
            label["properties"]["label:description"] = "Item label"
            label["properties"]["label:type"] = "vector"
            label["properties"]["label:classes"] = self.get_labels()
            links = []
            links.append(
                {
                    "rel": "root",
                    "href": os.path.relpath(self.catalog.self_href, label_dir),
                    "type": "application/json",
                }
            )
            links.append(
                {
                    "rel": "collection",
                    "href": os.path.relpath(collection_path, label_dir),
                    "type": "application/json",
                }
            )
            links.append(
                {
                    "rel": "source",
                    "href": os.path.relpath(source_item, label_dir),
                    "type": "application/json",
                }
            )
            label["links"] = links
            save_json(label_path, label)

        ## Add item link to collection
        with open(collection_path, "r") as collection_item:
            collection_json = json.load(collection_item)
            collection_json["links"].append(
                {
                    "rel": "item",
                    "href": "./" + name + "/" + name + ".json",
                    "type": "application/json",
                }
            )
            save_json(collection_path, collection_json)
        return label_dir + f"/{name}.json"

    def save_labels(self, labels):
        label_names = [label["name"] for label in labels]
        label_collection = self.label_collection().get_self_href()
        with open(label_collection, "r") as item:
            collection_json = json.load(item)
            labels_and_colors = [{label["name"]: label["color"]} for label in labels]
            labels_and_colors_dictionary = {}
            for pair in labels_and_colors:
                for key, value in pair.items():
                    labels_and_colors_dictionary[key] = value
            collection_json["summaries"]["label:classes"][0]["classes"] = label_names
            collection_json["summaries"][
                scaneo_labels_and_colors
            ] = labels_and_colors_dictionary
            save_json(label_collection, collection_json)
        label_items = self.get_items_paths(self.label_collection())
        for label_item in label_items:
            item_json = json.load(open(label_item))
            item_json["properties"]["label:classes"] = label_names
            save_json(label_item, item_json)

    def get_annotations(self, image_path):
        label_item = self.find_label_item(image_path)
        if not label_item:
            label_item = self.create_label_item(image_path)
        item_json = json.load(open(label_item))
        assets = item_json["assets"]
        if scaneo_asset in assets:
            asset_path = get_asset_path(label_item, assets[scaneo_asset]["href"])
            asset_json = json.load(open(asset_path))
            asset_tasks = []
            first_feature = asset_json["features"][0]
            if "properties" in first_feature:
                if "tasks" in first_feature["properties"]:
                    asset_tasks = first_feature["properties"]["tasks"]
            tasks = []
            if "label:tasks" in item_json["properties"]:
                tasks = item_json["properties"]["label:tasks"]
            if len(asset_tasks) < 1 and len(tasks) > 0:
                for feature in asset_json["features"]:
                    feature["properties"]["tasks"] = tasks
            properties_key = item_json["properties"]["label:properties"]
            if type(properties_key) == list:
                if len(properties_key) > 1:
                    print(
                        "WARNING: more than one label property found, using the first one"
                    )
                properties_key = properties_key[0]
            for feature in asset_json["features"]:
                if properties_key in feature["properties"]:
                    value = feature["properties"].pop(properties_key)
                    flattened_value = np.array([value]).flatten()
                    feature["properties"][
                        scaneo_properties_key
                    ] = flattened_value.tolist()
            return asset_json
        else:
            geojson = {
                "type": "FeatureCollection",
                "features": [item_json],
            }
            return geojson

    def find_source_item(self, image_path):
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        source_paths = self.get_items_paths(self.source_collection())
        for path in source_paths:
            item_name = os.path.splitext(os.path.basename(path))[0]
            if item_name == image_name:
                return path

    def source_collection(self):
        collections = self.collections()
        return next(
            filter(
                lambda collection: not label_extension in collection.stac_extensions,
                collections,
            )
        )

    def add_bboxes(self, source_items_paths):
        names_and_bboxes = []
        for image_item_path in source_items_paths:
            with open(image_item_path, "r") as item:
                json_item = json.load(item)
                image_name = json_item["id"]
                image_info = json_item["assets"][image_name]
                image_bbox = json_item["bbox"]
                image_relative_path = image_info["href"]
                image_path = os.path.normpath(
                    os.path.join(os.path.dirname(image_item_path), image_relative_path)
                )
                dict = {"name": image_path, "bbox": image_bbox}
                names_and_bboxes.append(dict)
        return names_and_bboxes

    def get_images_info(self, source_items_paths):
        image_paths_and_bboxes = []
        for image_item_path in source_items_paths:
            with open(image_item_path, "r") as item:
                json_item = json.load(item)
                image_name = json_item["id"]
                image_info = json_item["assets"][image_name]
                image_relative_path = image_info["href"]
                image_path = os.path.normpath(
                    os.path.join(os.path.dirname(image_item_path), image_relative_path)
                )
                path_bbox = {"name": image_path, "bbox": json_item["bbox"]}
                image_paths_and_bboxes.append(path_bbox)
        return image_paths_and_bboxes

    def save_classification(self, image_path, feature):
        label_item = self.find_label_item(image_path)
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        if not label_item:
            label_item = self.create_label_item(image_path)
        with open(label_item, "r") as item:
            json_item = json.load(item)
            json_item["properties"]["labels"] = feature.properties["labels"]
            asset = {
                scaneo_asset: {
                    "href": "./" + image_name + asset_name_appendix,
                    "title": "Label",
                    "type": "application/geo+json",
                }
            }
            json_item["assets"] = asset
            save_json(label_item, json_item)

    def add_scaneo_asset(self, image_path):
        label_item = self.find_label_item(image_path)
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        if label_item is None:
            label_item = self.create_label_item(image_path)
        with open(label_item, "r") as item:
            json_item = json.load(item)
            if scaneo_asset not in json_item["assets"]:
                asset = {
                    "href": "./" + image_name + asset_name_appendix,
                    "title": "Label",
                    "type": "application/geo+json",
                }
                json_item["assets"][scaneo_asset] = asset
            save_json(label_item, json_item)

    def save(self, name, geojson_string):
        geojson = json.loads(geojson_string.json())
        image_path = name
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        self.add_scaneo_asset(image_path)
        label_item = self.find_label_item(image_path)
        label_item_dir = os.path.dirname(label_item)
        storage = Storage()
        storage.save(
            label_item_dir + "/" + image_name + asset_name_appendix,
            json.dumps(geojson),
        )
