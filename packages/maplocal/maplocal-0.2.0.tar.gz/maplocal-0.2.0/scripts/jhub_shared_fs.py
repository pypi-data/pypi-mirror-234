"""has to be ran in the browser with Javscript displayed."""

import os
from IPython.display import Javascript, display, HTML
from typing import Tuple
import pathlib
import getpass
import datetime
from maplocal import maplocal


APPLAUNCHER_EXPLORER = 'mfllp:explorer.exe?'
FDIR_APPDATA = pathlib.PureWindowsPath("J:/J4321/Apps/.maplocal")
FDIR_APPDATA_LINUX = pathlib.Path("/home/jovyan/jobs/J4321/Apps/.maplocal")
MYGENERICBATTEMPLATE = f'''
@echo off
title Running...
echo Executing the script... 
{0}
echo Done!
pause
'''

def make_open_url(fpth):
    return f"{APPLAUNCHER_EXPLORER}{fpth}"

def open_url(url):
    """uses Javascript in the browser to open a new tab with URL"""
    display(Javascript('window.open("{url}");'.format(url=url)))

def fpth_windows_to_launch(fpth):
    """not sure why but more slashes makes it work...!"""
    return '\\\\'.join(pathlib.PureWindowsPath(fpth).parts)

def javascript_open_url(url):
    """uses Javascript in the browser to open a new tab with URL
    
    Code:
        return Javascript('window.open("{url}");'.format(url=url))
    """
    return Javascript('window.open("{url}");'.format(url=url))

def get_user():
    try:
        return os.environ["JUPYTERHUB_USER"]
    except:
        return getpass.getpass()

def get_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
    
def make_filename(process_name=None):
    s = get_datetime() + "-" + get_user()
    if process_name is not None:
        s += f"-{process_name}"
    return s

def runcmd(cmd):
    FDIR_APPDATA_LINUX.mkdir(exist_ok=True)
    path = FDIR_APPDATA / (make_filename() + ".bat")
    bat_string = MYGENERICBATTEMPLATE.format(cmd)
    f = open(path, "w")
    f.write("".format(bat_string))
    f.close()
    openpath(path)
    return path

def openpath(fpth_windows: pathlib.PureWindowsPath):
    """
    opens file or folder on the users machine using their default application. heavy lifting done
    by AppLaucher. requires Javascript in the browser so if used within an App in Voila it must be 
    called with the display visible via an output widget. 
    
    Example:
        #  how to use with widgets
        from IPython.display import display, Markdown, clear_output
        from mf_file_utilities.applauncher_wrapper import open_windows_fpth
        
        def fn_open(click):
            display(Markdown('doesnt work as the Javascript doesnt get injected into the browser'))
            display(open_windows_fpth(fpth))
        def fn1_open(click):
            with out:
                clear_output()
                display(Markdown('works as the Javascript gets injected into the browser'))
                open_windows_fpth(fpth)
        fpth = r'J:\J4321\DigitalDesignTeam\MfOpenBIM\Reference Material\PAS 14191.pdf'
        button_open = widgets.Button(icon='fa-folder-open', button_style='danger')
        button_open.on_click(fn_open)
        button_open1 = widgets.Button(icon='fa-folder-open', button_style='success')
        button_open1.on_click(fn1_open)
        out = widgets.Output()
        display(Markdown('## Using Javacript and AppLauncher to open files and folders'))
        display(widgets.HBox([button_open, button_open1]))
        display(out)
    """
    if type(fpth_windows) == str:
        path_win = pathlib.PureWindowsPath(fpth_windows)
    else:
        path_win = fpth_windows
    fpth = fpth_windows_to_launch(path_win)
    url = make_open_url(fpth)
    icon="fa-folder-open"
    text = 'open'
    html = f"""
<html>
<sandbox="allow-popups allow-popups-to-escape-sandbox">
<body>
<i class="fas fa-thumbs-up"></i>
<i class="fas {icon}"></i>
<b>{text}</b>
<i class="fas fa-arrow-right"></i>
<i style="color:green;">{str(path_win)}</i>
</body>
</html>
"""
    display(HTML(html))
    display(javascript_open_url(url))