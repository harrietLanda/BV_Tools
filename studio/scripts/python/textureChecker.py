import json
import os

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

import hou

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

def get_textures():

    class_type = '<hou.NodeType for Vop redshift::TextureSampler>'
    mat_path = '_mat_path_'

    node_type = hou.nodeType(hou.vopNodeTypeCategory(), "redshift_vopnet")
    mats = node_type.instances()

    nodes_list = []

    for each in mats:
        list = hou.node(each.path()).allSubChildren()
        for i in list:
            if str(i.type()) == class_type:
                nodes_list.append(i)


    return nodes_list

def get_main_dict():

    class_type = '<hou.NodeType for Vop redshift::TextureSampler>'
    mat_path = '_mat_path_'

    node_type = hou.nodeType(hou.vopNodeTypeCategory(), "redshift_vopnet")
    mats = node_type.instances()

    textures_dict = {}


    for each in mats:
        info_dict = {}
        list = hou.node(each.path()).allSubChildren()
        info_dict[mat_path] = each.path()
        for i in list:
            if str(i.type()) == class_type:

                sel = hou.node(i.path()).parm('tex0').eval()
                tex_name = sel.split('/')[-1].split('.')[0]
                info_dict[tex_name] = sel
                textures_dict[str(each)] = info_dict

    return textures_dict

class TextureChecker(QtWidgets.QWidget):

    def getHoudiniMainWindow():
        """Get the Houdini main window.

        Returns:
            PySide2.QtWidgets.QWidget: 'QWidget' Houdini main window.
        """
        return hou.qt.mainWindow()

    def __init__(self):
        super(TextureChecker, self).__init__(hou.qt.mainWindow())

        self.CONFIG = _get_json_dict()

        self.setWindowTitle("BCN VISUALS CHECKER")
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.resize(1000,400)

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

    def populate(self):

        """
        Create all the widgets
        """

        self.table_wdg.clear()
        ### set the mains labels ###
        self.table_wdg.setHeaderLabels(['Materials', 'Material Path'])
        self.table_wdg.setColumnWidth(0,432)
        self.table_wdg.setColumnWidth(1,400)

        self.main_dict = get_main_dict()

        for k, v in self.main_dict.items():

            material_name = QtWidgets.QTreeWidgetItem(self.table_wdg, [k, v.get('_mat_path_')])
            #material_name.setForeground(0,QtGui.QBrush(QtGui.QColor("#00ff08")))
            for i, u in v.items():
                if '_mat_path' in i:
                    pass
                else:
                    cg = QtWidgets.QTreeWidgetItem(material_name, [i, u])
                    if u.endswith('.rstexbin'):
                        cg.setForeground(0,QtGui.QBrush(QtGui.QColor(self.CONFIG.get('supported_files').get('.rstexbin'))))
                        cg.setForeground(1,QtGui.QBrush(QtGui.QColor(self.CONFIG.get('supported_files').get('.rstexbin'))))
                    else:
                        cg.setForeground(0,QtGui.QBrush(QtGui.QColor(self.CONFIG.get('supported_files').get('BAD'))))
                        cg.setForeground(1,QtGui.QBrush(QtGui.QColor(self.CONFIG.get('supported_files').get('BAD'))))

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
        Execute populate module to delete and re-create all the widgets
        """
        self.populate()

    def clicked_node(self, it , col ):
        """
        Fit the network view on clicked item

        Args:
            it ([type]): [the item from the self.table_wdg]
            col ([type]): [the current item column]
        """
        currentItemText = it.text(col)

        self.NODES = get_textures()

        try:
            temp = []
            for i in self.NODES:
                sel = hou.node(i.path()).parm('tex0').eval()
                tex_name = sel.split('/')[-1].split('.')[0]
                if str(currentItemText) in tex_name:
                    temp.append(i.path())
            currentNode = hou.node(temp[0])
            currentNode.setSelected(1,1)
            p = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
            p.setCurrentNode(currentNode)
            p.homeToSelection()
        except IndexError, AttributeError:
            pass



_ui_tex = None
def show():
    global _ui_tex
    if _ui_tex is None:
        _ui_tex = TextureChecker()
    _ui_tex.show()

show()
