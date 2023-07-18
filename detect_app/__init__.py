"""
Detect which app the python interpreter is running in. use detect_app()
"""

import types
import contextlib
from typing import Optional
import logging
import importlib
import os
import sys

def attempt_import(module_name: str) -> Optional[types.ModuleType]:
    """attempt to import a module, return True if it succeeded"""
    with contextlib.suppress(ImportError):
        importlib.import_module(module_name)
        return True
    return False


apps = []

_apps_sys_exe_check = {
    "Maya": ["maya", "mayapy"],
    "Max3ds": "3dsmax",
    "RV": "rv",
    "SubstancePainter": "adobe substance 3d painter",
    "Unreal": ["ue4editor", "unrealeditor"]
}

class __AppMeta(type):
    """meta class for App, used to track all apps. adds the class to the apps list if it has an id"""
    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        if name != "App":
            global apps
            apps.append(cls)
        return cls


class App(metaclass=__AppMeta):
    id: str  # id follows python module name conventions, name should not start with int, useinstead of spaces
    _name: str
    action: callable  # if returns True, the app is detected

    @classmethod
    def get_name(cls):
        return cls.id.replace("_", " ").title() if not cls._name else cls._name


class Ansible(App):
    id = "ansible"
    action = lambda: attempt_import("ansible")


class AutoCAD(App):
    id = "autocad"
    action = lambda: attempt_import("pyautocad")  # 3rd party module


class Blender(App):
    id = "blender"
    action = lambda: attempt_import("bpy")


class Calibre(App):
    id = "calibre"
    action = lambda: attempt_import("calibre")


class Cinema4D(App):
    id = "cinema4d"
    action = lambda: attempt_import("c4d")


class Clarisse(App):
    id = "clarisse"
    action = lambda: attempt_import("clarisse_helper")


class CryEngine(App):
    id = "cry_engine"
    action = lambda: attempt_import("SandboxBridge")  # todo is there a better module to use?


class Flame(App):
    id = "flame"
    action = lambda: attempt_import("flame")


class FreeCAD(App):
    id = "freecad"
    action = lambda: attempt_import("FreeCAD")
    _name = "FreeCAD"


class Fusion(App):
    id = "fusion"
    action = lambda: attempt_import("adsk.fusion")


class Gaffer(App):
    id = "gaffer"
    action = lambda: attempt_import("Gaffer")


class Gimp(App):
    id = "gimp"
    action = lambda: attempt_import("gimp")


class Houdini(App):
    id = "houdini"
    action = lambda: attempt_import("hou")


class Inkscape(App):
    id = "inkscape"
    action = lambda: attempt_import("inkex")


class Katana(App):
    id = "katana"
    action = lambda: attempt_import("Katana")


class Krita(App):
    id = "krita"
    action = lambda: attempt_import("krita")


class Mari(App):
    id = "mari"
    action = lambda: attempt_import("mari")


class Marmoset(App):
    id = "marmoset"
    action = lambda: attempt_import("mset")


class Maya(App):
    id = "maya"
    action = lambda: attempt_import("maya")


class Max3ds(App):
    id = "max3ds"
    _name = "3ds Max"
    action = lambda: attempt_import("pymxs")


class MotionBuilder(App):
    id = "motion_builder"
    action = lambda: attempt_import("pyfbsdk")


class Nuke(App):
    id = "nuke"
    action = lambda: attempt_import("nuke")


class Revit(App):
    id = "revit"
    action = lambda: attempt_import("Autodesk.Revit")


class RV(App):
    id = "rv"
    action = lambda: attempt_import("rv")


class Shotgun(App):
    id = "shotgun"
    action = lambda: attempt_import("shotgun_api3")


class Scribus(App):
    id = "scribus"
    action = lambda: attempt_import("scribus")


class Softimage(App):
    id = "softimage"
    action = lambda: attempt_import("PySoftimage")


class SubstanceDesigner(App):
    id = "substance_designer"
    action = lambda: attempt_import("pysbs")


class SubstancePainter(App):
    id = "substance_painter"
    action = lambda: attempt_import("substance_painter")


class Unreal(App):
    id = "unreal"
    action = lambda: attempt_import("unreal")


def detect_app() -> Optional[App]:
    """
    detect which app is currently running
    """
    python_exe = sys.executable.lower()
    exe_name = os.path.splitext(os.path.basename(python_exe))[0].lower()

    for app, possible_name in _apps_sys_exe_check.items():
        if isinstance(possible_name, (tuple, list)):
            if exe_name in possible_name:
                return getattr(sys.modules[__name__], app)
        else:
            if exe_name == possible_name:
                return getattr(sys.modules[__name__], app)

    global apps
    for app in apps:
        if app.action():
            logging.debug(f"app detected {app.id}")
            return app

