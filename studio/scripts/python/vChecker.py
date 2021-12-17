from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

import hou
import os
from functools import partial


class VersionChecker(QtWidgets.QWidget):

    def getHoudiniMainWindow():
        """Get the Houdini main window.

        Returns:
            PySide2.QtWidgets.QWidget: 'QWidget' Houdini main window.
        """
        return hou.qt.mainWindow()

    def __init__(self):
        super(VersionChecker, self).__init__(hou.qt.mainWindow())


        self.setWindowTitle("Version Checker")
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
        self.table_wdg = QtWidgets.QTreeWidget()
        
        ### create the widgets ###
        self.populate()
        # print('moco')

    def _actionCombo(self):

        self.version_combo = QtWidgets.QComboBox()

        return self.version_combo


    def populate(self):

        """
        Create all the widgets
        """
        self.table_wdg.clear()
        ### set the mains labels ###
        self.table_wdg.setHeaderLabels(['Files', 'Version', 'Apply', 'Path' ])
        self.table_wdg.setColumnWidth(0,100)
        self.table_wdg.setColumnWidth(1,80)
        self.table_wdg.setColumnWidth(2,80)
        self.table_wdg.setColumnWidth(3,200)

        self.combos_dict = {}
        self.names_dict = {}
        self.paths_dict = {}
        ### get all the alembic nodes ###
        self.alembicList = hou.nodeType('Sop/alembic').instances()
        for abc in self.alembicList:
            full_path = abc.parm('fileName').eval()
            node_name = abc.name()
            self.combos_dict[node_name] = QtWidgets.QComboBox()
            i_path = full_path.replace('/' + full_path.split('/')[-1], '')
            current_version = i_path.split('/')[-1]
            v_path = i_path.replace(current_version, '')
	    try:
	        versions = sorted([v for v in os.listdir(v_path)])
	        self.combos_dict.get(node_name).addItems(versions)
	        max_version = versions[-1]
	        self.combos_dict.get(node_name).setCurrentIndex(versions.index(current_version))
	    


		self.change_btn = QtWidgets.QPushButton('Change')
		project_path_itm = QtWidgets.QTreeWidgetItem(self.table_wdg, [node_name, '', '', full_path])
		self.names_dict[node_name] = QtWidgets.QLineEdit(node_name)
		self.names_dict.get(node_name).setReadOnly(True)
		self.paths_dict[node_name] = QtWidgets.QLineEdit(full_path)
		self.paths_dict.get(node_name).setReadOnly(True)
		self.table_wdg.setItemWidget(project_path_itm, 0, self.names_dict.get(node_name))
		self.table_wdg.setItemWidget(project_path_itm, 1, self.combos_dict.get(node_name))
		self.table_wdg.setItemWidget(project_path_itm, 2, self.change_btn)
		self.table_wdg.setItemWidget(project_path_itm, 3, self.paths_dict.get(node_name))
		if current_version == max_version:
		    self.names_dict.get(node_name).setStyleSheet("color: green;  background-color: black")
		else:
		    self.names_dict.get(node_name).setStyleSheet("color: red;  background-color: black")

		self.change_btn.clicked.connect(partial(self.change_version, abc, current_version, v_path))
	    except:
		pass
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        """
        Create all the layouts from the window
        """
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.table_wdg)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        """
        Create all the connections from the buttons
        """
        self.refresh_btn.clicked.connect(self.refresh_table)
        self.close_btn.clicked.connect(self.close)
        # self.table_wdg.itemClicked.connect(self.clicked_node)

    def refresh_table(self):
        """
        Execute populape module to delete and re-create all the widgets
        """
        self.populate()

    def change_version(self, abc, current_version, v_path, *args):
        new_version = self.combos_dict.get(abc.name()).currentText()
        current_path = abc.parm('fileName').eval()
        new_path = v_path + new_version
        file_path = [file for file in os.listdir(new_path) if file.endswith('.abc')][0]
        # final_path = os.path.join(new_path , file_path)
        final_path = new_path + '/'+  file_path
        abc.parm('fileName').set(final_path)
        self.populate()



_ui = None
def show():
    global _ui
    if _ui is None:
        _ui = VersionChecker()
    _ui.show()

show()
