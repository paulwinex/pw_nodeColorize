'''menuData
act={name:Colorize Nodes,action:show_houdini()}
'''



def show_houdini():
    import nc_houdini
    reload(nc_houdini)
    nc_houdini.show()

def show_nuke():
    pass
