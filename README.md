# detect-app

[![PyPI Downloads](https://img.shields.io/pypi/v/detect-app?color=0)](https://pypi.org/project/detect-app/)

Detect which app the python interpreter is running in. Usefull for cross app scripts

Supports:
```
    Blender,
    Fusion,
    Houdini,
    Krita,
    MotionBuilder,
    Marmoset,
    Maya,
    Max3ds,
    Nuke,
    SubstancePainter,
    SubstanceDesigner,
    Softimage,
    Unreal,
```

## Instructions

e.g. if run in Blender, will print `Blender"`
```python
import detect_app
app_info = detect_app.detect_app()
print(app_info.id)
```
right now app_info is very simple
- **id**: `str` a unique identifier for the app, lowercase, underscores, not start with nr
- **action**: `callable` that returns true if run in the app. usually just attempts to import an app specific module
- **get_name()**: `method` to return a pretty name.
