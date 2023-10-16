from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication
from pyrateshield.gui.main_controller import MainController
from pyrateshield.gui.graphics import Graphics
from pyrateshield.dosemapper import Dosemapper
from pyrateshield.model import Model
from pyrateshield import labels
from pyrateshield import __pkg_root__, __version__
from PyQt5.QtGui import QIcon


    
import requests
import os
import multiprocessing
import argparse
import sys

if getattr(sys, 'frozen', False):
    import pyi_splash

_LICENCE_FILE = os.path.join(__pkg_root__, 'LICENSE')

DISCLAIMER =\
("PyrateShield is free to use under the GNU GPLv3 license. The developers do "
 "not take any responsibility for any damages that might arise from using this "
 "software.\n\n"
 "This is a beta version, distributed for the purpose of testing and "
 "validation. Use at your own risk!\n\n"
 "Marcel Segbers (m.segbers@erasmusmc.nl)\n"
 "Rob van Rooij (r.vanrooij-3@umcutrecht.nl)\n\n"
 "Pyrateshield version: " + __version__)

URL = 'https://bitbucket.org/MedPhysNL/pyrateshield/downloads/'

NEW_VERSION =\
    (f"You are currently running version {__version__}, a newer version "
     " is available. Please obtain the latest version!\n\n"
     f"<a href='{URL}'>Latest execuatable</a>\n"
     "or use pip install --upgrade pyrateshield")
     
    
     
     

def approve_disclaimer():
    with open (_LICENCE_FILE, "r") as fn:
        LICENCE=''.join(fn.readlines())

    msg = QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText("Disclaimer!")
    msg.setInformativeText(DISCLAIMER)
    msg.setWindowTitle("Disclaimer")
    msg.setDetailedText(LICENCE)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    approvement = msg.exec() == QMessageBox.Ok
    
    return approvement


def version_dialog(latest_version):    
    msg = QMessageBox()
    msg.setWindowTitle("New version available!")
    msg.setIcon(QtWidgets.QMessageBox.Information)
    #msg.setText("New version!")
    msg.setTextFormat(Qt.RichText) # this is what makes the links clickable)
    msg.setText(NEW_VERSION)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()

def get_latest_version():
    package = 'pyrateshield'  # replace with the package you want to check
    response = requests.get(f'https://pypi.org/pypi/{package}/json')
    latest_version = response.json()['info']['version']
    return latest_version

def get_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--pyshield', action='store_true')
    group.add_argument('--radtracer', action='store_true')
    parser.add_argument('project', nargs='*')
    args = parser.parse_args()
    
    project_path = args.project[0] if len(args.project) else None
    if project_path is not None and not os.path.exists(project_path):
        raise ValueError(f"Path does not exist: {project_path}")
    
    if args.radtracer:
        engine = labels.RADTRACER
    elif args.pyshield:
        engine = labels.PYSHIELD
    else:
        engine = None
    
    return project_path, engine

def launch_app(dm, project):
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    
    app = QtWidgets.QApplication([])   
    icon = os.path.join(os.path.split(__file__)[0], 'gui', 'icon.png')
    app.setWindowIcon(QIcon(icon))  
    
    if getattr(sys, 'frozen', False):
        pyi_splash.close()


    
    if not approve_disclaimer():
        return None
    
    try:
        latest_version = get_latest_version()
    except:
        latest_version is not None
        
    if latest_version is not None and latest_version > __version__:
        version_dialog(latest_version)
        
    controller = MainController(dosemapper=dm, model=project)
    window = controller.view
    window.showMaximized()
    window.show()
    app.exec_()
    return controller


def stand_alone(dm, project, engine):
    project.dosemap.engine = engine
    dosemap = dm.get_dosemap(project)
    report = dm.get_critical_points(project)    
    print(report)
    
    
    app = QApplication([])
    window = QMainWindow()
    
    view = Graphics(model=project)
    view.scene().dosemap().setDosemap(dosemap)

    window.setCentralWidget(view)
    
    # view.legend.setBottomRight()

    window.show()
    

    app.exec_()
    
    
    # ax = plt.axes()    
    # if project.floorplan.image is not None:
    #     ax.imshow(project.floorplan.image, extent=project.floorplan.extent)
    # MplItemsPlotter(model=project, axes=ax)
    # plot_dosemap(ax, project, dosemap)
    # plt.show()
    

def main():
    project_path, engine = get_arguments()
    
    if project_path:
        project = Model.load_from_project_file(project_path)
    else:
        project = None
    
    if engine and project is None:
        print("Nothing to execute, specify project file")
        exit()

    controller = None
    with Dosemapper(multi_cpu=True) as dm:
        if engine:
            stand_alone(dm, project, engine)
        else:
            controller = launch_app(dm, project)
        
    return controller

if __name__ == "__main__":
    multiprocessing.freeze_support()
    controller = main()
    

