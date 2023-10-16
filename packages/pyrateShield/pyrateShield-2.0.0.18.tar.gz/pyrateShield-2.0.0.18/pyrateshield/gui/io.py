import os
import imageio

from PyQt5.QtWidgets  import QFileDialog, QErrorMessage, QMessageBox

from pyrateshield.model import Model



def safe_load_model(filename=None):
    # filename only used to extract current folder
    confirm = confirm_changes("Load Project")
    if not confirm:
        return
    
    newfile = select_project_file(filename, must_exist=True)

    if newfile is not None:
        try:
            model = Model.load_from_project_file(newfile)
        except IOError:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(f'Could not read from {filename}!')
            error_dialog.exec_()
            model = None
            raise
    else:
        model = None
        
    return model

def show_help(title="title", text="Help?"):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setText("Help")
    msg.setInformativeText(text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setWindowTitle(title)
    msg.exec_()
    
    
    

def safe_write_model(model=None, filename=None):
    if filename is None:
        filename = select_project_file(model.filename)
        
    if filename is not None:
        
        try:
            model.save_to_project_file(filename)
            model.filename = filename
        except:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(f'Could not write to {filename}!')
            error_dialog.exec_()
            raise
    

def safe_load_image():

    
    filename = ask_image_file('Open bitmap image')
    image = None
    if filename:
        try:
            with open(filename, 'rb') as f:                
                image = imageio.imread(filename)
        except:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(f'Could not read from {filename}!')
            error_dialog.exec_()
            

    return image
        
       
def ask_image_file(title):
    extensions = "Image Files (*.png *.jpg *.jpeg *.tiff *.bmp)"
    file = ask_existing_file(title, extensions)
    if file == '':
        file = None
    return file

def ask_new_image_file(title):
    extensions = "Image Files (*.png *.jpg *.jpeg *.tiff *.bmp)"
    file = ask_new_file(title, extensions)
    if file == '':
        file = None
    return file

def ask_existing_file(title, extensions, directory=None):
    filedialog = QFileDialog(directory=directory)
    filedialog.setFileMode(QFileDialog.ExistingFile)
    file = str(QFileDialog.getOpenFileName(filedialog, title, "",
                                           extensions)[0])
    if file == '': # Cancel
        file = None
    return file

def ask_new_file(title, extensions, directory=None):
    filedialog = QFileDialog(directory=directory)
    filedialog.setFileMode(QFileDialog.AnyFile)
    file = str(QFileDialog.getSaveFileName(filedialog, title, "",
                                           extensions)[0])
    
    if file == '': # Cancel
        file = None
    
    return file
           
def select_project_file(filename=None, must_exist=False):
    # filename only used for finding current folder
    
    if filename is not None:
        folder = os.path.split(filename)[0]
        if not os.path.exists(folder):
            folder = None
    else:
        folder = None
        
    if must_exist:
        file_selector = ask_existing_file
    else:
        file_selector = ask_new_file
        
        
    project_file = file_selector("Select Project File", 
                                 "PyrateShield Projects (*.zip *.psp)",
                                 directory=folder)
    
    return project_file

def confirm_new_project():
    confirm = confirm_changes("New Project")
    if confirm:
        return True
    else:
        return False

def pixelsize_error(title=None):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Error!")
    txt = 'Real world distance in cm must be positive and greater than 0!'
    msg.setInformativeText(txt)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setWindowTitle(title)
    msg.exec_()
    

def confirm_changes(title=None):
   msg = QMessageBox()
   msg.setIcon(QMessageBox.Warning)
   msg.setText("Warning!")
   msg.setInformativeText("Any unsaved changes will be lost!")
   msg.setWindowTitle(title)
   msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
   
  
   confirm = msg.exec_()
   if confirm == QMessageBox.Ok:
       return True
   else:
       return False
  
        
    

    

        


      
        
