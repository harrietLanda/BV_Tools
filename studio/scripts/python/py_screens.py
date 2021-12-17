import hou

def flat():
    rop_nets = hou.nodeType('Driver/ifd').instances()

    rop_nets[0].parm('execute').pressButton()

def curved():
    rop_nets = hou.nodeType('Driver/ifd').instances()

    rop_nets[1].parm('execute').pressButton()

def create_cam():
    p = hou.pwd().path()
    n = hou.node(p) 
    name = str(p).split('/')[2]
    resX = n.parm('cam_resx').eval()
    resY = n.parm('cam_resy').eval()
    posX = n.parm('cam_posx').eval()
    posY = n.parm('cam_posy').eval()
    posZ = n.parm('cam_posz').eval()
    cam_top = hou.node('/obj/').createNode('cam', 'CAM_TOP')
    cam_top.moveToGoodPosition()
    cam_top.parm('resx').set(resX)
    cam_top.parm('resy').set(resY)
    cam_top.parm('rx').set(-90)
    cam_top.parm('tx').set(posX)
    cam_top.parm('ty').set(posY)
    cam_top.parm('tz').set(posZ)
    rndr_flat = hou.node('/obj/').createNode('geo', 'RNDR_flat')
    rndr_flat.moveToGoodPosition()
    obj_flat = hou.node('/obj/RNDR_flat').createNode('object_merge', 'input_flat')
    obj_flat.parm('objpath1').set('./../../{}/{}/FLAT'.format(name, str(n)))
    rndr_curve = hou.node('/obj/').createNode('geo', 'RNDR_curve')
    rndr_curve.moveToGoodPosition()
    obj_curve = hou.node('/obj/RNDR_curve').createNode('object_merge', 'input_curve')
    obj_curve.parm('objpath1').set('/../../{}/{}/SCREEN'.format(name, str(n)))

    net = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    net.setCurrentNode(n)
    net.homeToSelection()


