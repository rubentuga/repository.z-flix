import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
import shutil
import hashlib
import time
import urllib.request
import xml.etree.ElementTree as ET
from inspect import getframeinfo, stack
from urllib.parse import quote_plus, unquote_plus
from .addonvar import addon_name, addon_version, addons_path, addon_icon, addon_id, addon_profile

chk_interval = 60
translatePath = xbmcvfs.translatePath

#PB Fix Paths
fix_chk = 'PB-FIX'
fenlt = "plugin.video.fenlight"
fenlt_addon = addons_path + translatePath('plugin.video.fenlight/')
fenlt_ver = os.path.join(addon_profile,'last_version.txt')
fenlt_file = addons_path + translatePath('plugin.video.fenlight/resources/lib/modules/sources.py')

fix_url = "http://dr-venture.com/709/Wizard/fenlt_fix/fix/sources.py"
dflt_url = "http://dr-venture.com/709/Wizard/fenlt_fix/dflt/sources.py"
fenlt_dflt = os.path.join(addon_profile,'sources.py')

def add_dir(name,url,mode,icon,fanart,description, name2='', version='', kodi='', size='', addcontext=False,isFolder=True):
    u=sys.argv[0]+"?url="+quote_plus(url)+"&mode="+str(mode)+"&name="+quote_plus(name)+"&icon="+quote_plus(icon) +"&fanart="+quote_plus(fanart)+"&description="+quote_plus(description)+"&name2="+quote_plus(name2)+"&version="+quote_plus(version)+"&kodi="+quote_plus(kodi)+"&size="+quote_plus(size)
    liz=xbmcgui.ListItem(name)
    liz.setArt({'fanart':fanart,'icon':icon,'thumb':icon})
    liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "plotoutline": description})
    if addcontext:
        contextMenu = []
        liz.addContextMenuItems(contextMenu)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)

def play_video(name, url, icon, description):
    xbmcplugin.setPluginCategory(int(sys.argv[1]), name)
    url = unquote_plus(url)
    if url.endswith('.jpg') or url.endswith('.jpeg') or url.endswith('.png'):
        string = "ShowPicture(%s)" %url
        xbmc.executebuiltin(string)
        return
    liz = xbmcgui.ListItem(name)
    liz.setInfo('video', {'title': name, 'plot': description})
    liz.setArt({'thumb': icon, 'icon': icon})
    xbmc.Player().play(url, liz)

def GetParams():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

def get_mode():
    params=GetParams()
    mode = None
    try:
        mode=int(params["mode"])
    except:
        pass
    return mode

def Log(msg):
    fileinfo = getframeinfo(stack()[1][0])
    xbmc.log('*__{}__{}*{} Python file name = {} Line Number = {}'.format(addon_name,addon_version,msg,fileinfo.filename,fileinfo.lineno), level=xbmc.LOGINFO)

def log(_text, _var):
    xbmc.log(f'{_text} = {str(_var)}', xbmc.LOGINFO)

def dl_dflt_file(url, save_path):
    #Download default file
    urllib.request.urlretrieve(url, save_path)

def dl_fix_file(url, dstn_path):
    if not xbmcvfs.exists(fenlt_addon):
        return None
    # Read fix file
    with urllib.request.urlopen(url) as response:
        data = response.read()   # Read bytes from URL

    # Write fix to the destination file (overwrite)
    with open(dstn_path, "wb") as file:
        file.write(data)

def get_addon_version(addon_id):
    #Return the version of the installed addon by reading its addon.xml
    if not xbmcvfs.exists(fenlt_addon):
        return None
    try:
        addon_path = translatePath(f"special://home/addons/{addon_id}/addon.xml")
        if not xbmcvfs.exists(addon_path):
            return None

        tree = ET.parse(addon_path)
        root = tree.getroot()
        return root.attrib.get('version')
    except Exception as e:
        xbmc.log(f"[UpdateMonitor] Error reading addon version: {e}", xbmc.LOGERROR)
        return None

def load_last_version():
    #Retreive previous version
    if not xbmcvfs.exists(fenlt_ver):
        return None
    with xbmcvfs.File(fenlt_ver) as f:
        return f.read()

def save_last_version(version):
    #Save current version
    with xbmcvfs.File(fenlt_ver, 'w') as f:
        f.write(version)

def compare_files(file1, file2):
    #Compare two files
    with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
        return f1.read() == f2.read()

def pbf_chk():
    if xbmcvfs.exists(fenlt_file):
        with open(fenlt_file, encoding="utf8") as f:
            if fix_chk in f.read():
                xbmc.log("Fix already applied!", xbmc.LOGERROR)
                return True
            else:
                return False
fix_check = pbf_chk()

def compare_apply():
    #Compare files and apply fix if required
    if not xbmcvfs.exists(fenlt_addon):
        if os.path.exists(fenlt_ver):
            os.remove(fenlt_ver)
        if os.path.exists(fenlt_dflt):
            os.remove(fenlt_dflt)
        return None
    
    if xbmcvfs.exists(fenlt_file) and xbmcvfs.exists(fenlt_dflt):
        if compare_files(fenlt_file, fenlt_dflt):
            try:
                dl_fix_file(fix_url, fenlt_file)
            except Exception as e:
                xbmc.log("Error copying fix file: {e}", xbmc.LOGERROR)
            
    #If compare fails, check if file contains fix
    else:
        if fenlt_file and fix_check == True:
            pass

def pbf():
    #Fen Light External Playback Fix
    if not xbmcvfs.exists(fenlt_addon):
        if os.path.exists(fenlt_ver):
            os.remove(fenlt_ver)
        if os.path.exists(fenlt_dflt):
            os.remove(fenlt_dflt)
        return None
    
    #Create wiz data directory if it doesn't already exist
    if not os.path.exists(addon_profile):
        os.mkdir(addon_profile)
        
    #Compare files at startup and apply fix if required
    dl_dflt_file(dflt_url, fenlt_dflt)
    if xbmcvfs.exists(fenlt_file) and xbmcvfs.exists(fenlt_dflt):
        if compare_files(fenlt_file, fenlt_dflt):
            try:
                dl_fix_file(fix_url, fenlt_file)
            except Exception as e:
                xbmc.log("Error copying fix file: {e}", xbmc.LOGERROR)

    #If compare fails, check if file contains fix
    else:
        if xbmcvfs.exists(fenlt_file) and fix_check == True:
            pass

    #Check if addon updated   
    last_version = load_last_version()
    current_version = get_addon_version(fenlt)

    if current_version and last_version != current_version:
        compare_apply()
        save_last_version(current_version)
        if os.path.exists(fenlt_dflt):
            os.remove(fenlt_dflt)
    
    #Start monitoring loop to monitor for Fen Light updates (Checks every 60sec)
    xbmc.log("[UpdateMonitor] Service started", xbmc.LOGINFO)
    while not xbmc.Monitor().abortRequested():
        xbmc.sleep(chk_interval * 1000)

        #Check if addon updated
        new_version = get_addon_version(fenlt)
        last_version = load_last_version()
        if new_version and new_version != last_version:
            dl_dflt_file(dflt_url, fenlt_dflt)
            compare_apply()
            save_last_version(new_version)
            if os.path.exists(fenlt_dflt):
                os.remove(fenlt_dflt)
