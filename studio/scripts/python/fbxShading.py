selection_node = hou.selectedNodes()[0]
path = str(selection_node.path()).replace(str(selection_node), '')

partition_node = selection_node.createOutputNode('partition')

partition_node.parm('rule').set("`@shop_materialpath`")

material = hou.node(path).createNode('matnet')
material_path = material.path()
mat = partition_node.createOutputNode('material')
mat.parm('num_materials').set(0)


groups = [g.name() for g in partition_node.geometry().primGroups()]
for i, name in enumerate(groups, 1):
    mat.parm('num_materials').insertMultiParmInstance(i-1)
    
    
    
    group = mat.parm('group%d' %i)
    shop = mat.parm('shop_materialpath%d' %i)

    group.set(name)
    shop.set('../{}/'.format(material) + name)
    
    
    rs_node = hou.node(material_path).createNode('redshift_vopnet')
    rs_node.setName(name)
