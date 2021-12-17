from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

import json
import hou

import os

try:
    currentPath = os.path.abspath(__file__)
except:
    currentPath = r'H:/BCN_Visuals/studio/scripts/python'
    # currentPath = r'/mnt/studio/config/houdini/hda/studio/scripts/python'

JSON = "{}/config/config.json".format(currentPath)

def _get_json_dict():
    with open(JSON) as json_file:
        data = json.load(json_file)
        return(data)

class FileChecker(QtWidgets.QWidget):

    def getHoudiniMainWindow():
        """Get the Houdini main window.

        Returns:
            PySide2.QtWidgets.QWidget: 'QWidget' Houdini main window.
        """
        return hou.qt.mainWindow()

    def __init__(self):
        super(FileChecker, self).__init__(hou.qt.mainWindow())

        self.CONFIG = _get_json_dict()

        self.setWindowTitle("BCN VISUALS CHECKER")
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.resize(700,250)

        stylesheet = hou.qt.styleSheet()
        self.setStyleSheet(stylesheet)

        self.create_widgets()
        self.create_layout()
        self.create_connections()



    def get_firts_path(self, name, dict):
        """
        Get the values from a dic

        Args:
            name ([type]): [set the name to search in the dict]
            dict ([type]): [use this dictionary to search the name and returns the value]

        Returns:
            [type]: [the value from the name in the dict]
        """
        returnList = []
        for k , v in dict.items():
            if v == name:
                returnList.append(k)
        return returnList

    def create_widgets(self):
        """
        Create all the widgets to use in the window
        """
        self.table_wdg = QtWidgets.QTreeWidget()
        ### create the widgets ###
        self.populate()
        # print('moco')
    def populate(self):

        """
        Create all the widgets
        """
        self.table_wdg.clear()
        ### set the mains labels ###
        self.table_wdg.setHeaderLabels(['Files', 'Relative Path', 'Full Path' ])
        self.table_wdg.setColumnWidth(0,200)
        self.table_wdg.setColumnWidth(1,200)
        self.table_wdg.setColumnWidth(2,200)

        ### get all the filecahces and file nodes ###
        self.cacheList = hou.nodeType('Sop/filecache').instances()
        self.fileList = hou.nodeType('Sop/file').instances()
        self.nodesList = self.cacheList + self.fileList

        self.filesDict = {}
        self.projectsPaths = []
        self.simpleDict = {}
        self.simplePaths = []
        for each in self.nodesList:
            filePath = each.parm('file').rawValue()
            if len(filePath.split('/')) >= 2:
                firtsName = filePath.split('/')[0]
                if "`chs" in firtsName:
                    self.projectsPaths.append("`chs")
                    self.filesDict[each] = "`chs"
                else:
                    self.projectsPaths.append(firtsName)
                    self.filesDict[each] = firtsName
            else:
                self.simplePaths.append(each)
                self.simpleDict[each] = each

        ### iterate all the items from the nodesList list with all thew nodes ###
        simpleNames_itm = QtWidgets.QTreeWidgetItem(self.table_wdg, ['Simple Paths'])
        simpleNames_itm.setForeground(0,QtGui.QBrush(QtGui.QColor("#FFB600")))

        #ref_path_itm = QtWidgets.QTreeWidgetItem(self.table_wdg, ['Referenced Paths'])
        #ref_path_itm.setForeground(0,QtGui.QBrush(QtGui.QColor("#FFB600")))

        for each in set(self.projectsPaths):

            if each in self.CONFIG.get('supported_types').keys():
                project_path_itm = QtWidgets.QTreeWidgetItem(self.table_wdg, [each])
                project_path_itm.setForeground(0,QtGui.QBrush(QtGui.QColor(self.CONFIG.get('supported_types').get(each))))
                moono = self.get_firts_path(name=each, dict=self.filesDict)

                for node in moono:
                    nodeFilePath = node.parm('file').rawValue()
                    nodeFileRealPath = node.parm('file').eval()
                    cg = QtWidgets.QTreeWidgetItem(project_path_itm, [str(node.name()), str(nodeFilePath), str(nodeFileRealPath)])
                    cg.setForeground(0,QtGui.QBrush(QtGui.QColor(self.CONFIG.get('supported_types').get(each))))

            else:
                project_path_itm = QtWidgets.QTreeWidgetItem(self.table_wdg, [each])
                project_path_itm.setForeground(0,QtGui.QBrush(QtGui.QColor(self.CONFIG.get('supported_types').get('BAD'))))
                moo = self.get_firts_path(name=each, dict=self.filesDict)

                for node in moo:
                    nodeFilePath = node.parm('file').rawValue()
                    nodeFileRealPath = node.parm('file').eval()
                    cg = QtWidgets.QTreeWidgetItem(project_path_itm, [str(node.name()), str(nodeFilePath), str(nodeFileRealPath)])
                    cg.setForeground(0,QtGui.QBrush(QtGui.QColor(self.CONFIG.get('supported_types').get('BAD'))))


        for each in set(self.simplePaths):

            monkey = self.get_firts_path(name=each, dict=self.simpleDict)
            for node in monkey:
                nodeFilePath = node.parm('file').rawValue()
                nodeFileRealPath = node.parm('file').eval()
                cg = QtWidgets.QTreeWidgetItem(simpleNames_itm, [str(node.name()), str(nodeFilePath), str(nodeFileRealPath)])
                cg.setForeground(0,QtGui.QBrush(QtGui.QColor("#FFB600")))

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
        self.table_wdg.itemClicked.connect(self.clicked_node)
        self.refresh_btn.clicked.connect(self.refresh_table)
        self.close_btn.clicked.connect(self.close)

    def refresh_table(self):
        """
        Execute populape module to delete and re-create all the widgets
        """
        self.populate()

    def rename_node(self, item,  *args):
        """
        Rename the selected node

        Args:
            item ([type]): [pyside item must be passed]
        """
        selected_nodes = hou.selectedNodes()[0]
        newName = item.text()
        selected_nodes.setName(newName)
        print('Name changed from {} to {}'.format(item.text(), newName))


    def clicked_node(self, it , col ):
        """
        Fit the network view on clicked item

        Args:
            it ([type]): [the item from the self.table_wdg]
            col ([type]): [the current item column]
        """
        currentItemText = it.text(col)
        try:
            node_path = [node.path() for node in self.nodesList if currentItemText in str(node)][0]
            currentNode = hou.node(node_path)
            currentNode.setSelected(1,1)
            p = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
            p.setCurrentNode(currentNode)
            p.homeToSelection()
        except IndexError:
            pass


_ui = None
def show():
    global _ui
    if _ui is None:
        _ui = FileChecker()
    _ui.show()

show()
