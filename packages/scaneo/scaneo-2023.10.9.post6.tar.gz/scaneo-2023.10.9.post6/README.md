# scan

This repo contains the code for SCAN

- scaneo: includes the cli, lib and api
- ui: includes the web ui

The CLI runs the API, which in turns servers the static files for the UI.

The library can be installed with

```
pip install scaneo
```

## Instructions

### Developement

Run the api with the cli

```
cd scaneo
python main.py run --reload --data <<folder>>
```

Then, run the ui

```
cd ui
yarn dev
```

### Production

Build the ui, copy the build inside scaneo and build the python package

```
make build v=<version>
make publish
```

## Notes

Do not add scaneo/ui to gitignore since the build process will fail (missing entry folder)
