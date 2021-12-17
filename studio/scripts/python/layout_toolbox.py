#!/usr/bin/env python
# -*- coding: utf-8 -*-

from io import TextIOBase
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

import hou
import os
import re
import json


class LayoutTool(QtWidgets.QWidget):

    def _get_json_dict(self):

        screens_json = '/mnt/production/user/harriet.landa/tools/screens_json/screens.json'
        with open(screens_json) as json_file:
            data = json.load(json_file)
            return(data)


    def getHoudiniMainWindow():
        """Get the Houdini main window.

        Returns:
            PySide2.QtWidgets.QWidget: 'QWidget' Houdini main window.
        """
        return hou.qt.mainWindow()

    def __init__(self):
        super(LayoutTool, self).__init__(hou.qt.mainWindow())


        self.setWindowTitle("LAYOUT TOOL")
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.resize(600,100)

        stylesheet = hou.qt.styleSheet()
        self.setStyleSheet(stylesheet)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """
        Create all the widgets to use in the window
        """
        self.logo = QtWidgets.QLabel()
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap('/mnt/studio/config/houdini/hda/studio/layout_lib/src/bcn_visuals_logo.png')
        pix = pixmap.scaled(200, 80)
        self.logo.setPixmap(pix)

        self.layout_lbl = QtWidgets.QLabel('LAYOUT TOOL')
        self.layout_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.populate()
        ### create the widgets ###

        self.apply_btn = QtWidgets.QPushButton("Apply")

        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.close_btn = QtWidgets.QPushButton("Close")

    def populate(self):

        """
        Create all the widgets
        """
        self.fps_lbl = QtWidgets.QLabel('FPS')
        self.fps_lbl.setAlignment(QtCore.Qt.AlignCenter)

        fps_validator = QtGui.QIntValidator(1, 120, self)
        self.fps_data = QtWidgets.QLineEdit()
        self.fps_data.setText('60')
        self.fps_data.setValidator(fps_validator)


        self.duration_lbl = QtWidgets.QLabel('Duration-frames')
        self.duration_lbl.setAlignment(QtCore.Qt.AlignCenter)

        duration_validator = QtGui.QIntValidator(2, 2000, self)
        self.duration_data = QtWidgets.QLineEdit()
        self.duration_data.setText('600')
        self.duration_data.setValidator(duration_validator)

        self.container_lbl = QtWidgets.QLabel('Containers +  Camera')
        self.container_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.C_PATH = r'/mnt/studio/config/houdini/hda/studio/layout_lib/containers'
        c_files = os.listdir(self.C_PATH)
        data = self._get_json_dict()
        self.container_list = data.get('screens')
        # self.container_list = [c.split('_')[1] for c in c_files]
        self.container_items = [QtWidgets.QCheckBox(container) for container in self.container_list]

        self.export_maya_check = QtWidgets.QCheckBox('Export to Maya')

        self.export_ma_lbl = QtWidgets.QLabel('Export layout \n to maya scene')
        self.export_ma_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.export_ma_data = QtWidgets.QLineEdit()
        self.export_ma_data.setText(str(hou.hipFile.path()))

        self.export_ma_btn = QtWidgets.QPushButton('...')

        self.export_ma_data.setDisabled(True)
        self.export_ma_lbl.setDisabled(True)
        self.export_ma_btn.setDisabled(True)

        #self.populate_variable_table()

    # def populate_variable_table(self):
    #     self.variables_table = QtWidgets.QTableWidget()
    #     self.variables_table.horizontalHeader().hide()
    #     self.variables_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
    #     self.variables_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    #     self.variables_table.verticalHeader().hide()
    #     self.variables_table.setColumnCount(2)
    #     col_width = 150
    #     row_height = 10
    #     self.variables_table.setColumnWidth(0,col_width)
    #     self.variables_table.setColumnWidth(1,col_width)
    #     self.variables_table.setRowHeight(0,row_height)
    #     self.variables_table.setRowHeight(1,row_height)
    #
    #
    #     row = 0
    #
    #
	# self.variables_dict = {}
	# all_variables = hou.hscript("setenv -s")
	# for variable in all_variables:
	#     test = variable.replace("set -g ", "").replace("'", "")
	#     main_variables = test.split("\n")
	#     for each in main_variables:
	# 	var = each.split('=')[0]
	# 	try:
	# 	    val = each.split('=')[1]
	# 	    self.variables_dict[var] = val
	# 	except:
	# 	    pass
    #
    #
    #     self.variables_table.setRowCount(len(self.variables_dict.keys()))
    #
    #     for var , val in self.variables_dict.items():
    #         # print(var, val)
    #         self.variables_table.setItem(row, 0, QtWidgets.QTableWidgetItem(var))
    #         self.variables_table.setItem(row, 1, QtWidgets.QTableWidgetItem(val))
    #         row=row+1
    #
    #     self.add_variable_btn = QtWidgets.QPushButton("+")


    def create_layout(self):
        """
        Create all the layouts from the window
        """
        master_layout = QtWidgets.QVBoxLayout(self)

        intro_layout = QtWidgets.QVBoxLayout()

        fps_layout = QtWidgets.QHBoxLayout()
        fps_layout.addWidget(self.fps_lbl)
        fps_layout.addWidget(self.fps_data)

        duration_layout = QtWidgets.QHBoxLayout()
        duration_layout.addWidget(self.duration_lbl)
        duration_layout.addWidget(self.duration_data)

        containers_layout = QtWidgets.QHBoxLayout()
        container_items_layout = QtWidgets.QVBoxLayout()
        containers_layout.addWidget(self.container_lbl)
        for item in self.container_items:
            container_items_layout.addWidget(item)
        containers_layout.addLayout(container_items_layout)

        export_ma_layout = QtWidgets.QHBoxLayout()
        export_ma_layout.addWidget(self.export_maya_check)
        export_ma_layout.addWidget(self.export_ma_lbl)
        export_ma_layout.addWidget(self.export_ma_data)
        export_ma_layout.addWidget(self.export_ma_btn)

        # variables_layout = QtWidgets.QVBoxLayout()
        #variables_layout.addWidget(self.variables_table)

        #add_del_variable_layout = QtWidgets.QHBoxLayout()
        # add_del_variable_layout.addWidget(self.add_variable_btn)
        # variables_layout.addLayout(add_del_variable_layout)

        intro_layout.addWidget(self.logo)
        intro_layout.addWidget(self.layout_lbl)

        min_layout = QtWidgets.QHBoxLayout()
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addLayout(fps_layout)
        main_layout.addLayout(duration_layout)
        main_layout.addLayout(containers_layout)
        main_layout.addLayout(export_ma_layout)

        min_layout.addLayout(main_layout)
        # min_layout.addLayout(variables_layout)

        master_layout.addLayout(intro_layout)
        master_layout.addLayout(min_layout)
        master_layout.addWidget(self.apply_btn)



    def create_connections(self):
        """
        Create all the connections from the buttons
        """
        self.apply_btn.clicked.connect(self.execute)
        # self.add_variable_btn.clicked.connect(self.add_variables)
        self.export_maya_check.clicked.connect(self.enable_export)



    def execute(self):
        self.apply_fps()
        self.apply_framerange()
        self.import_containers()
        if self.export_maya_check.isChecked():
            self.export_to_maya()
        else:
            pass
        # self.apply_variables()


    # def apply_variables(self):
    #
    #     rows = self.variables_table.rowCount()
    #     items = []
    #     for row in range(rows):
    #         items.append(self.variables_table.item(row, 0).text())
    #
    #     list_difference = []
    #     for item in items:
    #         if item not in self.variables_dict.keys():
    #             list_difference.append(item)
    #
    #
    #     paths = []
    #     for row in range(rows):
    #         paths.append(self.variables_table.item(row, 1).text())
    #
    #     list_difference_paths = []
    #     for path in paths:
    #         if path not in self.variables_dict.values():
    #             list_difference_paths.append(path)
    #
    #     for x in range(len(list_difference)):
    #         hou.hscript("set -g {}={}".format(list_difference[x], list_difference_paths[x]))



    def import_containers(self):
        current_containers = []
        for each in self.container_items:
            if each.isChecked():
                print(each.text())
                current_containers.append(each)
        if len(current_containers)<=0:
            print('No container selected')

	hou.hipFile.merge('/mnt/studio/config/houdini/hda/studio/layout_lib/main_layout.hip')

        for container in current_containers:
            print('Importing {} Layout'.format(container.text()))
            container_file = os.path.join(self.C_PATH , 'master_{}_layout.hip'.format(container.text()))
            hou.hipFile.merge(container_file)
            print('Imported {} Layout'.format(container.text()))

    def export_to_maya(self):

        print('WIP')
        # print('Exporting to alembic...')
        # print('Done')

    def enable_export(self):
        if self.export_maya_check.isChecked():
            self.export_ma_data.setDisabled(False)
            self.export_ma_lbl.setDisabled(False)
            self.export_ma_btn.setDisabled(False)
        else:
            self.export_ma_data.setDisabled(True)
            self.export_ma_lbl.setDisabled(True)
            self.export_ma_btn.setDisabled(True)

    def apply_fps(self):
        fps = self.fps_data.text()
        hou.setFps(float(fps))

    def apply_framerange(self):
        frames = float(self.duration_data.text())

        start_frame = float(1001)
        if frames > 1000:
            end_frame = frames
        else:
            end_frame = start_frame + frames
        setGobalFrangeExpr = "tset `({0}-1)/$FPS` `{1}/$FPS`".format(start_frame,end_frame)

        hou.hscript(setGobalFrangeExpr)

        hou.playbar.setFrameRange(start_frame, end_frame)

    # def add_variables(self):
    #
    #     self.variables_table.insertRow(self.variables_table.rowCount())
    #     self.variables_table.setItem( self.variables_table.rowCount()-1, 1, QtWidgets.QTableWidgetItem('newVariable'))
    #     self.variables_table.setItem( self.variables_table.rowCount()-1, 0, QtWidgets.QTableWidgetItem('newPath'))
    #     self.variables_table.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers )

_ui = None
def show():
    global _ui
    if _ui is None:
        _ui = LayoutTool()
    _ui.show()

show()
