"""
Detect which app the python interpreter is running in. use detect_app()
"""

import types
import contextlib
from typing import Optional
import logging
import importlib
import importlib.util
import os
import sys


def attempt_import(module_name: str) -> Optional[types.ModuleType]:
    """attempt to import a module, return True if it succeeded"""
    return bool(importlib.util.find_spec(module_name))


apps = []


class __AppMeta(type):
    """meta class for App, used to track all apps. adds the class to the apps list if it has an id"""
    # any app class that inherits this meta class, will be added to the apps list
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
      
    @staticmethod 
    def version():
        raise NotImplementedError


class Ansible(App):
    id = "ansible"
    action = lambda: attempt_import("ansible")
    
    # @staticmethod 
    # def version():
    #     import subprocess
    #     process = subprocess.run(['ansible', '--version'], capture_output=True, text=True)
    #     version = process.stdout
        

class AutoCAD(App):
    id = "autocad"
    action = lambda: attempt_import("pyautocad")  # 3rd party module

    @staticmethod 
    def version():
        import win32com.client
        acad = win32com.client.Dispatch("AutoCAD.Application")
        return acad.Version


class Blender(App):
    id = "blender"
    action = lambda: attempt_import("bpy")
    
    @staticmethod 
    def version():
        import bpy
        return bpy.app.version_string  # str e.g. '2.83.2'
        return bpy.app.version  # tuple e.g. (2, 76, 0)


class Calibre(App):
    id = "calibre"
    action = lambda: attempt_import("calibre")

    # @staticmethod 
    # def version():
    #     import subprocess
    #     # Run the 'calibre' command with the '--version' option
    #     process = subprocess.run(['calibre', '--version'], capture_output=True, text=True)
    #     version = process.stdout


class Cinema4D(App):
    id = "cinema4d"
    action = lambda: attempt_import("c4d")
    
    @staticmethod 
    def version():
        import c4d
        c4d.GetC4DVersion()  # int e.g. 12016


class Clarisse(App):
    id = "clarisse"
    action = lambda: attempt_import("clarisse_helper")
    
    @staticmethod 
    def version():
        import clarisse_helper
        return clarisse_helper.get_version()


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

    @staticmethod 
    def version():
        import FreeCAD
        version = FreeCAD.Version()
        return version


class Fusion(App):
    id = "fusion"
    action = lambda: attempt_import("adsk.fusion")


class Gaffer(App):
    id = "gaffer"
    action = lambda: attempt_import("Gaffer")

    @staticmethod 
    def version():
        import gaffer
        return gaffer.__version__


class Gimp(App):
    id = "gimp"
    action = lambda: attempt_import("gimp")

    @staticmethod 
    def version():
        import gimp
        return (gimp.major_version, gimp.minor_version)
        # TODO is there a patch version?


class Houdini(App):
    id = "houdini"
    action = lambda: attempt_import("hou")

    @staticmethod 
    def version():
        import hou
        return hou.applicationVersion()


class Inkscape(App):
    id = "inkscape"
    action = lambda: attempt_import("inkex")
    
    @staticmethod 
    def version():
        import inkex
        return inkex.inkscape.version


class Katana(App):
    id = "katana"
    action = lambda: attempt_import("Katana")


class Krita(App):
    id = "krita"
    action = lambda: attempt_import("krita")

    @staticmethod 
    def version():
        from krita import Krita
        krita_app = Krita.instance()
        return krita_app.version()


class Mari(App):
    id = "mari"
    action = lambda: attempt_import("mari")


class Marmoset(App):
    id = "marmoset"
    action = lambda: attempt_import("mset")

    @staticmethod 
    def version():
        import mset
        return mset.getToolbagVersion()  # int, e.g. 4062


class Maya(App):
    id = "maya"
    action = lambda: attempt_import("maya")

    @staticmethod 
    def version():
        import maya.cmds as cmds
        version = cmds.about(version=True)  # str

        # handle preview releases, where cmds.about(version=True) doesn't return the year
        if version == "Preview Release":
            product = cmds.about(product=True)  # str e.g. 'Maya 2025'
            # preview releases usually are 1 year ahead of the version number
            year = product.split()[-1]  # str e.g. '2025'
            version = int(year) + 1

        return version
        

class Max3ds(App):
    id = "max3ds"
    _name = "3ds Max"
    action = lambda: attempt_import("pymxs")
    
    @staticmethod 
    def version():
        import pymxs
        return pymxs.runtime.maxversion()  # <Array<#(22000, 55, 0, 22, 2, 0, 2126, 2020, ".2 Update ")>>
        # TODO convert from maxscript to int or string


class MotionBuilder(App):
    id = "motion_builder"
    action = lambda: attempt_import("pyfbsdk")
    
    @staticmethod 
    def version():
        from pyfbsdk import FBApplication
        mb_app = FBApplication()
        return mb_app.Version


class Nuke(App):
    id = "nuke"
    action = lambda: attempt_import("nuke")
    
    @staticmethod 
    def version():
        import nuke
        return nuke.NUKE_VERSION_STRING


class Revit(App):
    id = "revit"
    action = lambda: attempt_import("Autodesk.Revit")

    @staticmethod 
    def version():
        import clr
        clr.AddReference("RevitAPI")  # allow Python to use classes & functions defined in the Revit .NET API
        from Autodesk.Revit.Application import Application
        revit_app = Application()
        return revit_app.VersionNumber


class RV(App):
    id = "rv"
    action = lambda: attempt_import("rv")

    @staticmethod 
    def version():
        import rv.commands
        return rv.commands.appVersion()


class Shotgun(App):
    id = "shotgun"
    action = lambda: attempt_import("shotgun_api3")
    
    @staticmethod 
    def version():
        from shotgun_api3 import __version__
        return __version__  # version of the py API, not shotgun itself


class Scribus(App):
    id = "scribus"
    action = lambda: attempt_import("scribus")
    
    @staticmethod 
    def version():
        import scribus
        return scribus.version()


class Softimage(App):
    id = "softimage"
    action = lambda: attempt_import("PySoftimage")
    
    @staticmethod 
    def version():
        import win32com.client
        app = win32com.client.Dispatch('XSI.Application')
        return app.Version


class SubstanceDesigner(App):
    id = "substance_designer"
    action = lambda: attempt_import("pysbs")

    @staticmethod 
    def version():
        import sd
        return sd.getContext().getSDApplication().getAppVersion()


class SubstancePainter(App):
    id = "substance_painter"
    action = lambda: attempt_import("substance_painter")

    @staticmethod 
    def version():
        import substance_painter._version
        return substance_painter._version.__version_info__  # tuple e.g. (0, 2, 10)


class Unreal(App):
    id = "unreal"
    action = lambda: attempt_import("unreal")

    @staticmethod 
    def version():
        import unreal
        return unreal.SystemLibrary.get_engine_version()


def detect_app_from_interpreter() -> Optional[App]:
    """
    detect which app the python interpreter is running in.
    and use this to detect the app
    """
    python_exe = sys.executable.lower()  # C:\\Users\\...\\venv\\Scripts\\python.exe'
    python_basename = os.path.basename(python_exe)  # python.exe
    exe_name = os.path.splitext(python_basename)[0].lower()  # ('python', '.exe')

    apps_sys_exe_check = {
        Maya: ["maya", "mayapy"],
        Max3ds: ["3dsmax"],
        RV: ["rv"],
        SubstancePainter: ["adobe substance 3d painter"],
        Unreal: ["ue4editor", "unrealeditor"]
    }

    for app, possible_names in apps_sys_exe_check.items():
        if exe_name in possible_names:
            logging.debug(f"App detected '{app.id}' from interpreter")
            return app


def detect_app_from_env_var() -> Optional[App]:
    """
    enables overwriting the detected app, e.g. for complex pipelines, or debugging purpose
    set DETECT_APP_FORCE_ID env var to the app id you want to force
    """
    app_id = os.getenv("DETECT_APP_FORCE_ID")
    # return the class with the name, check apps
    if app_id:
        for app in apps:
            if app.id == app_id:
                logging.debug(f"App OVERWRITTEN from env var: '{app.id}'")
                return app
        else:
            logging.warning(f"App from env var '{app_id}' could not be found")
            return None


def detect_app() -> Optional[App]:
    """
    detect which app is currently running
    """
    app = detect_app_from_env_var()
    if app:
        return app

    app = detect_app_from_interpreter()
    if app:
        return app

    global apps
    for app in apps:
        if app.action():
            logging.debug(f"App detected '{app.id}'")
            return app


if __name__ == "__main__":
    import cProfile
    import time

    start_time = time.time()
    cProfile.run('detect_app()', sort='tottime')
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
