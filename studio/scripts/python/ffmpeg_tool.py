from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

import json
import hou

import re
import os


class MovieMaker(QtWidgets.QWidget):

    def getHoudiniMainWindow():
        """Get the Houdini main window.

        Returns:
            PySide2.QtWidgets.QWidget: 'QWidget' Houdini main window.
        """
        return hou.qt.mainWindow()

    def __init__(self):
        super(MovieMaker, self).__init__(hou.qt.mainWindow())

        

        self.setWindowTitle("ffmpeg converter")
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.resize(700,250)

        stylesheet = hou.qt.styleSheet()
        self.setStyleSheet(stylesheet)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """
        Create all the widgets to use in the window
        """
    
        ### create the widgets ###
        self.populate()
        
    def populate(self):

        """
        Create all the widgets
        """
	self.main_lbl = QtWidgets.QLabel("Convert Sequence to mp4")
	self.main_lbl.setAlignment(QtCore.Qt.AlignCenter)
	self.input_lbl = QtWidgets.QLabel("Input")
	self.input_path = QtWidgets.QLineEdit()
	self.input_brw = QtWidgets.QPushButton("...")

	self.name_lbl = QtWidgets.QLabel("Movie Name")
	self.name_text = QtWidgets.QLineEdit()

	self.output_lbl = QtWidgets.QLabel("Output")
	self.output_path = QtWidgets.QLineEdit()
	self.output_brw = QtWidgets.QPushButton("...")
	
	self.apply_btn = QtWidgets.QPushButton("Apply")
        
	self.terminal = QtWidgets.QTextEdit(readOnly=True)
	self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        """
        Create all the layouts from the window
        """
	master_layout = QtWidgets.QHBoxLayout(self)
        button_layout = QtWidgets.QHBoxLayout()

        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.close_btn)
	
	input_layout = QtWidgets.QHBoxLayout()
	input_layout.addWidget(self.input_lbl)
	input_layout.addWidget(self.input_path)
	input_layout.addWidget(self.input_brw)
	
	name_layout = QtWidgets.QHBoxLayout()	
	name_layout.addWidget(self.name_lbl)
	name_layout.addWidget(self.name_text)

	output_layout = QtWidgets.QHBoxLayout()
	output_layout.addWidget(self.output_lbl)
	output_layout.addWidget(self.output_path)
	output_layout.addWidget(self.output_brw)


        main_layout = QtWidgets.QVBoxLayout()
 
	
        main_layout.addWidget(self.main_lbl)
	main_layout.addLayout(input_layout)
	main_layout.addLayout(name_layout)
        main_layout.addLayout(output_layout)
	main_layout.addWidget(self.apply_btn)

	master_layout.addLayout(main_layout)
	#master_layout.addWidget(self.terminal)

    def create_connections(self):
        """
        Create all the connections from the buttons
        """
        self.refresh_btn.clicked.connect(self.refresh_table)
        self.close_btn.clicked.connect(self.close)
	self.input_brw.clicked.connect(self.input_action)
	self.output_brw.clicked.connect(self.output_action)
	self.apply_btn.clicked.connect(self.ffmpeg_action)


    def refresh_table(self):
        """
        Execute populape module to delete and re-create all the widgets
        """
        self.populate()

    def input_action(self):
	path_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Load Sequence"), self.tr(str(hou.hipFile.path())))
	txt = path_file.split('.')[-2].split('/')[-1]
	e = re.findall(r'\d+', txt)
	new_path = path_file.replace(str(e[0]), '%04d')
	self.input_path.setText(new_path)



    def output_action(self):
	path_file = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Set Ouput Folder"), self.tr(str(hou.hipFile.path())))
	
	self.output_path.setText(path_file + '/' + self.name_text.text() + '.mp4')
        
    def ffmpeg_action(self):
       	input = self.input_path.text()
	output = self.output_path.text()
	command = 'ffmpeg -start_number 1001 -r 60 -i {} -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" {} 2> /mnt/production/user/harriet.landa/temp/{}.txt '.format(input, output, self.name_text.text())
	
	
        output = os.system(command)
	self.terminal.append(output)

_ui = None
def show():
    global _ui
    if _ui is None:
        _ui = MovieMaker()
    _ui.show()

show()
