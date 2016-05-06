import hou
import nodeColorize
reload(nodeColorize)

def selectionToCode():
    sel = hou.selectedNodes()
    if sel:
        code = []
        for s in sel:
            code.append(s.asCode())
        if len(code) == 1:
            return code[0]
        else:
            return '( %s )' % ', '.join(code)


def show():
    import hqt
    hqt.showWidget(nodeColorize.nodeColorizeClass, tool=1)
