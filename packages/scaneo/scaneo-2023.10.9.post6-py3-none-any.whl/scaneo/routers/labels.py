from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.stac import (
    is_stac,
    Stac,
)
from src.storage import Storage


router = APIRouter(prefix="/labels", tags=["labels"])


class Body(BaseModel):
    labels: list


@router.post("")
def save_labels(body: Body):
    try:
        storage = Storage()
        if is_stac(storage):
            stac = Stac()
            stac.save_labels(body.labels)
        else:
            storage.save("labels.json", body.json())
        return {"status": "201 Created", "labels": body.labels}
    except Exception as e:
        print("error labels:save_labels", e)
        return HTTPException(status_code=500, detail="Could not save new label")


@router.get("")
def get_labels():
    try:
        storage = Storage()
        if is_stac(storage):
            stac = Stac()
            labels_and_colors = stac.get_labels_and_colors()
            return {"labels": labels_and_colors}
        labels_file = [f for f in storage.list() if f.endswith("labels.json")]
        if len(labels_file) > 0:
            return storage.read(labels_file[0])
        return HTTPException(status_code=404, detail="Labels file not found")

    except Exception as e:
        print("error labels:get_labels", e)
        return HTTPException(status_code=500, detail="Could not get labels")
