# coding=utf-8
import shutil
import os
import sys
import time
import json
import tempfile
def extractall(self, path=None, members=None, pwd=None):
    if members is None: members = self.namelist()
    path = os.getcwd() if path is None else os.fspath(path)
    for zipinfo in members:
        try:    _zipinfo = zipinfo.encode('cp437').decode('gbk')
        except: _zipinfo = zipinfo.encode('utf-8').decode('utf-8')
        print('[*] unpack...', _zipinfo)
        if _zipinfo.endswith('/') or _zipinfo.endswith('\\'):
            myp = os.path.join(path, _zipinfo)
            if not os.path.isdir(myp):
                os.makedirs(myp)
        else:
            myp = os.path.join(path, _zipinfo)
            youp = os.path.join(path, zipinfo)
            self.extract(zipinfo, path)
            if myp != youp:
                os.rename(youp, myp)
import zipfile
zipfile.ZipFile.extractall = extractall

def creat_windows_shortcut(exe_path, name=None):
    vbsscript = '\n'.join([
        'set WshShell = WScript.CreateObject("WScript.Shell" )',
        'set oShellLink = WshShell.CreateShortcut(Wscript.Arguments.Named("shortcut") & ".lnk")',
        'oShellLink.TargetPath = Wscript.Arguments.Named("target")',
        'oShellLink.WindowStyle = 1',
        'oShellLink.Save',
    ])
    s = tempfile.mkdtemp()
    try:
        vbs = os.path.join(s, 'temp.vbs')
        with open(vbs, 'w', encoding='utf-8') as f:
            f.write(vbsscript)
        exe  = exe_path
        link = os.path.join(os.path.expanduser("~"), 'Desktop', name or os.path.split(exe_path)[1])
        if os.path.isfile(link + '.lnk'):
            os.remove(link + '.lnk')
        cmd = r'''
        {} /target:"{}" /shortcut:"{}"
        '''.format(vbs, exe, link).strip()
        print('[*] make shortcut in Desktop:', cmd)
        v = os.popen(cmd)
        v.read()
        v.close()
    finally:
        import traceback;
        if traceback.format_exc().strip() != 'NoneType: None':
            print('create shortcut failed.')
            traceback.print_exc()
        shutil.rmtree(s)

# zip_path_exe
def get_zip_path_exe(zip, path, exe):
    localpath = os.path.split(__file__)[0]
    v_tools_file = os.path.join(localpath, zip)
    if '/' in path:
        path, inner  = path.split('/')
        v_tools_target = os.path.join(os.path.split(sys.executable)[0], 'Scripts', path)
        v_tools_exec = os.path.join(v_tools_target, inner, exe)
    else:
        v_tools_target = os.path.join(os.path.split(sys.executable)[0], 'Scripts', path)
        v_tools_exec = os.path.join(v_tools_target, exe)
    return {
        'file': v_tools_file,
        'target': v_tools_target,
        'exec': v_tools_exec,
        'type': 'zip_path_exe',
        'path': path,
        'exe': exe,
    }
# zip_path_exe
def unpack_v_zip_path_exe(zeobj):
    print('[*] zip file path ===>', zeobj['file'])
    print('[*] exe file path ===>', zeobj['exec'])
    if not os.path.isdir(zeobj['target']):
        print('[*] unpack...')
        f = zipfile.ZipFile(zeobj['file'], 'r')
        f.extractall(zeobj['target'])
        f.close()
        print('[*] unpacked path ===>', zeobj['target'])
    creat_windows_shortcut(zeobj['exec'], zeobj['exe'])
# zip_path_exe
def remove_v_zip_path_exe(zeobj, kill_process=True):
    if os.path.isdir(zeobj['target']):
        if kill_process:
            os.popen('taskkill /f /im "{}" /t'.format(zeobj['exe'])).read()
        print('[*] remove...', zeobj['target'])
        time.sleep(0.2)
        for i in range(10):
            try:
                shutil.rmtree(zeobj['target'])
                break
            except:
                print('[*] wait...')
                time.sleep(0.2)
        link = os.path.join(os.path.expanduser("~"), 'Desktop', zeobj['exe'])
        if os.path.isfile(link + '.lnk'):
            os.remove(link + '.lnk')

def get_scripts_scrt_desktop(zip, path, password_tips):
    localpath = os.path.split(__file__)[0]
    v_tools_file = os.path.join(localpath, zip)
    v_tools_target = os.path.join(os.path.expanduser("~"), 'Desktop', path)
    return {
        'file': v_tools_file,
        'target': v_tools_target,
        'password_tips': password_tips,
    }
# zip_path_exe
def unpack_v_scripts_scrt_desktop(zeobj):
    if zeobj['password_tips'] == 'none':
        if not os.path.isdir(zeobj['target']):
            print('[*] unpack...')
            f = zipfile.ZipFile(zeobj['file'], 'r')
            f.extractall(zeobj['target'])
            f.close()
            print('[*] unpacked path ===>', zeobj['target'])
    else:
        print('[*] zip file path ===>', zeobj['file'])
        if not os.path.isdir(zeobj['target']):
            os.makedirs(zeobj['target'])
        shutil.copy(zeobj['file'], zeobj['target'])
        print('[*] unpacked path ===>', zeobj['target'])
        print('[*] password_tips:', zeobj['password_tips'])

# zip_path_exe
def remove_v_scripts_scrt_desktop(zeobj):
    if os.path.isdir(zeobj['target']):
        print('[*] remove...', zeobj['target'])
        time.sleep(0.2)
        for i in range(10):
            try:
                shutil.rmtree(zeobj['target'])
                break
            except:
                print('[*] wait...')
                time.sleep(0.2)

install_list = [
    {
        'name': 'sublime',
        'type': 'zip_path_exe',
        'info': ['sublime3.zip', 'sublime3', 'sublime_fix.exe']
    },
    {
        'name': 'scrcpy',
        'type': 'zip_path_exe',
        'info': ['scrcpy-win64-v2.1.1.zip', 'scrcpy/scrcpy-win64-v2.1.1', 'scrcpy.exe']
    },
    {
        'name': 'version',
        'type': 'scripts_scrt_desktop',
        'info': ['version.zip', 'version', 'none']
    },
    {
        'name': 'VC_redist.x64',
        'type': 'scripts_scrt_desktop',
        'info': ['VC_redist.x64.zip', 'VC_redist.x64', 'none']
    },
]

def install():
    for meta in install_list:
        if meta['type'] == 'zip_path_exe':
            unpack_v_zip_path_exe(get_zip_path_exe(meta['info'][0], meta['info'][1], meta['info'][2]))
        if meta['type'] == 'scripts_scrt_desktop':
            unpack_v_scripts_scrt_desktop(get_scripts_scrt_desktop(meta['info'][0], meta['info'][1], meta['info'][2]))

def remove(kill_process=True):
    for meta in install_list:
        if meta['type'] == 'zip_path_exe':
            remove_v_zip_path_exe(get_zip_path_exe(meta['info'][0], meta['info'][1], meta['info'][2]), kill_process)
        if meta['type'] == 'scripts_scrt_desktop':
            remove_v_scripts_scrt_desktop(get_scripts_scrt_desktop(meta['info'][0], meta['info'][1], meta['info'][2]))

def execute():
    argv = sys.argv
    print('v_tools :::: [ {} ]'.format(' '.join(argv)))
    if len(argv) == 1:
        print('[install]:  v_tools install')
        print('[remove]:   v_tools remove')
        return
    if len(argv) > 1:
        if argv[1] == 'install':
            install()
        if argv[1] == 'remove':
            remove()

if __name__ == '__main__':
    # execute()
    # install()
    remove()
    pass
