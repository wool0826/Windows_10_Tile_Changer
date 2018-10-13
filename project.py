import sys
import os
import getpass
import xml.etree.cElementTree as ET
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from shutil import copyfile


form_class = uic.loadUiType("layout.ui")[0]
dialog_class = uic.loadUiType("dlayout.ui")[0]

class MyDialog(QDialog, dialog_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.addEventListener()
        self.visible = True
        self.language = "ko"
        
        data = open('strings.json', encoding="utf-8").read()
        self.strings = json.loads(data)
        self.str = self.strings[self.language]
        
          
    def addEventListener(self):
        self.targetBtn.clicked.connect(self.fileDialogEvent)
        self.bigLogoBtn.clicked.connect(self.fileDialogEvent)
        self.smallLogoBtn.clicked.connect(self.fileDialogEvent)
        self.colorBtn.clicked.connect(self.colorPicker)
        self.executeBtn.clicked.connect(self.execute)
        self.refreshBtn.clicked.connect(self.refresh)
        self.bigTileCheck.clicked.connect(self.changeTitle)
        self.fgLight.clicked.connect(self.changeTitle)
        self.fgDark.clicked.connect(self.changeTitle)
        self.actionKorean.triggered.connect(self.chageLanguage)
        self.actionEnglish.triggered.connect(self.chageLanguage)
        self.actionMade_By.triggered.connect(self.madeBy)

    def madeBy(self):
        d = MyDialog()
        d.dLabel.setText("wool0826\nchanwool94@gmail.com\nhttps://github.com/wool0826")
        d.exec()

    def tempMsg(self, icon, title, text, informative):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(text)
        msg.setInformativeText(informative)
        msg.setWindowTitle(title)
        msg.exec()
    
    def chageLanguage(self):
        caller = self.sender().objectName()

        if caller == 'actionKorean':
            if(self.language == "ko"): return None

            self.language = "ko"            
        elif caller == 'actionEnglish':
            if(self.language == "en"): return None
            self.language = "en"  

        self.str = self.strings[self.language]
        self.actionMade_By.setText(self.str["made"])
        self.menuLanguage.setTitle(self.str["lang"])
        self.example150.setText(self.str["ex_150"])
        self.example40.setText(self.str["ex_40"])
        self.pixmap150.setText(self.str["example"])
        self.pixmap40.setText(self.str["example"])
        self.executeBtn.setText(self.str["execute"])
        self.refreshBtn.setText(self.str["refresh"])
        self.fgtext150.setText(self.str["ex_title"])
        self.targetLabel.setText(self.str["target_location"])
        self.bigLogoLabel.setText(self.str["logo150"])
        self.smallLogoLabel.setText(self.str["logo40"])
        self.foregroundLabel.setText(self.str["title_color"])
        self.backgroundLabel.setText(self.str["background_color"])
        self.bigTileLabel.setText(self.str["show_title"])


    def changeTitle(self):
        caller = self.sender().objectName()

        if caller == 'fgDark':
            self.fgtext150.setStyleSheet("color: black")
        elif caller == 'fgLight':
            self.fgtext150.setStyleSheet("color: white")
        elif caller == 'bigTileCheck':
            self.visible = not self.visible
            self.fgtext150.setVisible(self.visible)
            

    def colorPicker(self):
        color = QColorDialog.getColor()
        self.colorBtn.setStyleSheet("background-color: " + color.name())
        self.colorBtn.setText(color.name())
        self.pixmap40.setStyleSheet("background-color: " + color.name())
        self.pixmap150.setStyleSheet("background-color: " + color.name())


    def fileDialogEvent(self,e):
        caller = self.sender().objectName()
        
        if caller == 'targetBtn':
            location = QFileDialog.getOpenFileName(self, "Select Target File", "C:/")
            if location[0] != '':
                self.targetLine.setText(location[0])
        elif caller == 'bigLogoBtn':
            location = QFileDialog.getOpenFileName(self, "Select 150X150 Image", "C:/", "Images(*.png *.jpg)")
            if location[0] != '':
                self.bigLogoLine.setText(location[0])
                pixmap = QPixmap(location[0])
                self.pixmap150.setPixmap(pixmap.scaled(150,150))
        elif caller == 'smallLogoBtn':
            location = QFileDialog.getOpenFileName(self, "Select 40X40 Image", "C:/", "Images(*.png *.jpg)")
            if location[0] != '':
                self.smallLogoLine.setText(location[0])
                pixmap = QPixmap(location[0])
                self.pixmap40.setPixmap(pixmap.scaled(40,40))

    def createXML(self, smallExt, bigExt):
        root = ET.Element("Application")
        root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        ET.register_namespace("xsi", 'http://www.w3.org/2001/XMLSchema-instance')

        bCheck = self.bigTileCheck.isChecked()
        bFgColor = self.fgDark.isChecked()
        sBgColor = self.colorBtn.text()

        ET.SubElement(root, 'VisualElements', ShowNameOnSquare150x150Logo='on' if bCheck else 'off', Square150x150Logo='VisualElements/Logo' + bigExt,
            Square70x70Logo='VisualElements/SmallLogo' + smallExt, Square44x44Logo='VisualElements/SmallLogo' + smallExt,
            ForegroundText='dark' if bFgColor else 'light', BackgroundColor=sBgColor)
       
        return root

    def execute(self):
        targetLoc = self.targetLine.text()
        logo40Loc = self.smallLogoLine.text()
        logo150Loc = self.bigLogoLine.text()

        if targetLoc == "":
            self.tempMsg(QMessageBox.Critical, self.str["error_title"], self.str["error_text"], self.str["error_target"])
            return None
        elif logo40Loc == "":
            self.tempMsg(QMessageBox.Critical, self.str["error_title"], self.str["error_text"], self.str["error_40"])
            return None
        elif logo150Loc == "":
            self.tempMsg(QMessageBox.Critical, self.str["error_title"], self.str["error_text"], self.str["error_150"])
            return None

        targetName = os.path.basename(targetLoc).split(".")[0]
        targetLoc = os.path.dirname(targetLoc)
        imageFolder = os.path.join(targetLoc , 'VisualElements')

        print(targetName, targetLoc, imageFolder)

        if not os.path.exists(imageFolder):
            try:
                os.makedirs(imageFolder)
            except:
                self.tempMsg(QMessageBox.Critical, self.str["error_title"], self.str["error_mkdir"], self.str["admin"] )
                return None

        logo40Ext = os.path.splitext(logo40Loc)[1]
        logo150Ext = os.path.splitext(logo150Loc)[1]

        print(logo40Ext, logo150Ext)

        tree = ET.ElementTree(self.createXML(logo40Ext, logo150Ext))
        try:
            tree.write(os.path.join(targetLoc , targetName +'.VisualElementsManifest.xml'))
        except:
            self.tempMsg(QMessageBox.Critical, self.str["error_title"], self.str["error_write"], self.str["admin"] )
            return None
      
        try:      
            copyfile(logo40Loc, os.path.join(imageFolder,"smallLogo"+ logo40Ext))
            copyfile(logo150Loc,os.path.join(imageFolder,"Logo"+ logo150Ext))
        except:
            self.tempMsg(QMessageBox.Critical, self.str["error_title"], self.str["error_copy"], self.str["admin"] )
            return None

        try:
            os.chmod(os.path.join(targetLoc , targetName +'.VisualElementsManifest.xml'),644)
            os.chmod(os.path.join(imageFolder,"Logo"+ logo150Ext),644)
            os.chmod(os.path.join(imageFolder,"smallLogo"+ logo40Ext),644)
        except:
            self.tempMsg(QMessageBox.Critical, self.str["error_title"], self.str["error_chmod"], self.str["admin"] )
            return None
            
        self.tempMsg(QMessageBox.Information, self.str["work_done"], self.str["work_done_detail"], "")

    def refresh(self, targetName):
        username = getpass.getuser()
        path1 = 'C:/ProgramData/Microsoft/Windows/Start Menu/'
        path2 = 'C:/Users/'+ username +'/AppData/Roaming/Microsoft/Windows/Start Menu/Programs'
        
        self.touch(path1)
        self.touch(path2)

        self.tempMsg(QMessageBox.Information, self.str["work_done"], self.str["work_done_detail"], "")

    def touch(self,path):
        fileList = os.listdir(path)
        for name in fileList:
            fullDir = os.path.join(path, name)
            if os.path.isdir(fullDir):
                try:
                    self.touch(fullDir)
                except:
                    print(fullDir, sys.exc_info()[0])
            else:
                try:
                    os.utime(fullDir, None)
                except:
                    print(fullDir,sys.exc_info()[0])
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    myWindow.setFixedSize(670,300)
    app.exec()