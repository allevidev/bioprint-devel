import sys, os
import mimetypes

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "src"))
import bioprint

from bioprint.util.singleton import SingleInstance, SingleInstanceException
from multiprocessing import Process, freeze_support
import webbrowser

# Bioprint worker process handle
global p

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = os.path.abspath(sys._MEIPASS)
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

TRAY_TOOLTIP = 'Allevi Bioprint'
TRAY_ICON = resource_path('allevi.png')

# Function to start the UI. Must be run after importing wx
#
# It's kinda gross to put classes inside functions but this is the only way it
# runs without errors on older versions of OS X
def startUI():
    # Import wxPython
    import wx.adv
    import wx

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

            # Open browser after 1 second
            wx.CallLater(1000, self.on_open_bioprint, None)

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
            #  Open browser to Bioprint page if server is running
            if p.is_alive():
                webbrowser.open('http://localhost:9999', new=2)
            else:
                print 'Server is not running. Exiting!'
                sys.exit()

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

    # Start UI
    app = App(False)
    app.MainLoop()

#  Starts Bioprint server in a new process
def startBioprint():
    p = Process(target=bioprint.main, args=(True, None, None, 'localhost', 9999))
    p.start()
    return p

if __name__ == '__main__':
    # On Windows calling this function is necessary.
    # On Linux/OSX it does nothing.
    freeze_support()

    # Use local mime.types to avoid call to /etc on OS X
    mimetypes.init(files=['./mime.types'])

    try:
        bioprintInstance = SingleInstance()
    except SingleInstanceException:
        sys.exit()

    p = startBioprint()

    startUI()
