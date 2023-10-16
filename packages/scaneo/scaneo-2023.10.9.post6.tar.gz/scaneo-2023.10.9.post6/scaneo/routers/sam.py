from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.storage import Storage
from src.sam import generate_mask

router = APIRouter(prefix="/sam", tags=["sam"])


class Body(BaseModel):
    points: list
    pointsLabel: list
    image: str
    label: str
    bands: dict  # esto contiene bands y stretch, renombrar


@router.post("")
def sam_points(body: Body):
    try:
        storage = Storage()
        geojson_data = generate_mask(
            storage, body.image, body.bands, body.points, body.pointsLabel, body.label
        )
        return geojson_data
    except Exception as e:
        return HTTPException(
            status_code=500, detail="Could not generate a predictive mask"
        )
