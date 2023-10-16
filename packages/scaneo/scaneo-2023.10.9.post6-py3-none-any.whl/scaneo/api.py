from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import os

from routers import geojson, images, labels, sam

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(images.router)
app.include_router(geojson.router)
app.include_router(labels.router)
app.include_router(sam.router)

# this needs to be last in order to not override other routes
# ui is in same directory as this file
# in order for this to work with multipage apps, make sure to use trailingSlash = 'always' in svelte layout
app.mount(
    "/",
    StaticFiles(
        directory=os.path.dirname(os.path.realpath(__file__)) + "/ui", html=True
    ),
    name="ui",
)
