import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "src"))
import bioprint

# wxPython
import wx.adv
import wx

from multiprocessing import Process
import webbrowser

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

TRAY_TOOLTIP = 'Allevi Bioprint'
TRAY_ICON = resource_path('allevi.png')


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_click)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Open Bioprint', self.on_open_bioprint)
        menu.AppendSeparator()
        create_menu_item(menu, 'Quit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_click(self, event):
        pass

    def on_open_bioprint(self, event):
        webbrowser.open('http://bioprint', new=2)

    def on_exit(self, event):
        p.terminate()
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def startUI():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    #  Start Bioprint
    p = Process(target=bioprint.main)
    p.start()

    startUI()
