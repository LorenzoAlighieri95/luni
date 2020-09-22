from .luniPlugin import LuniPlugin

def classFactory(iface):
    return LuniPlugin(iface)