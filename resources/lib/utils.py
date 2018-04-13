# -*- coding: utf-8 -*-

import errno
import os
import re
import shutil

import xbmc
import xbmcaddon
import xbmcgui

__author__ = 'Mancuniancol'


def copy_anything(src, dst):
    try:
        copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            pass


# noinspection PyBroadException
def move_anything(src, dst):
    try:
        copytree(src, dst)
        shutil.rmtree(src)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            try:
                shutil.copy(src, dst)
                os.remove(src)
            except:
                pass
        else:
            pass


def copytree(source, destination, symlinks=False, ignore=None):
    names = os.listdir(source)
    if ignore is not None:
        ignored_names = ignore(source, names)
    else:
        ignored_names = set()

    if not os.path.isdir(destination):  # This one line does the trick
        os.makedirs(destination)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        src_name = os.path.join(source, name)
        dst_name = os.path.join(destination, name)
        try:
            if symlinks and os.path.islink(src_name):
                link_to = os.readlink(src_name)
                os.symlink(link_to, dst_name)
            elif os.path.isdir(src_name):
                copytree(src_name, dst_name, symlinks, ignore)
            else:
                # Will raise a SpecialFileError for unsupported file types
                shutil.copy2(src_name, dst_name)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except shutil.Error, err:
            errors.extend(err.args[0])
        except EnvironmentError, why:
            errors.append((src_name, dst_name, str(why)))
    try:
        shutil.copystat(source, destination)
    except OSError, why:
        if WindowsError is not None and isinstance(why, WindowsError):
            # Copying file access times may fail on Windows
            pass
        else:
            errors.extend((source, destination, str(why)))
    if errors:
        raise shutil.Error, errors


# Borrowed from xbmc swift2
def get_setting(key, converter=str, choices=None):
    value = xbmcaddon.Addon().getSetting(id=key)
    if converter is str:
        return value
    elif converter is unicode:
        return value.decode('utf-8')
    elif converter is bool:
        return value == 'true'
    elif converter is int:
        return int(value)
    elif isinstance(choices, (list, tuple)):
        return choices[int(value)]
    else:
        raise TypeError('Acceptable converters are str, unicode, bool and '
                        'int. Acceptable choices are instances of list '
                        ' or tuple.')


def get_icon_path():
    addon_path = xbmcaddon.Addon().getAddonInfo("path")
    return os.path.join(addon_path, 'icon.png')


def string(id_value):
    return xbmcaddon.Addon().getLocalizedString(id_value)


class Magnet:
    def __init__(self, magnet):
        self.magnet = magnet + '&'
        # hash
        info_hash = re.search('urn:btih:(.*?)&', self.magnet)
        result = ''
        if info_hash is not None:
            result = info_hash.group(1)
        self.info_hash = result
        # name
        name = re.search('dn=(.*?)&', self.magnet)
        result = ''
        if name is not None:
            result = name.group(1).replace('+', ' ')
        self.name = result.title()
        # trackers
        self.trackers = re.findall('tr=(.*?)&', self.magnet)


def get_int(text):
    return int(get_float(text))


def get_float(text):
    value = 0
    if isinstance(text, (float, long, int)):
        value = float(text)
    elif isinstance(text, str):
        # noinspection PyBroadException
        try:
            text = clean_number(text)
            match = re.search('([0-9]*\.[0-9]+|[0-9]+)', text)
            if match:
                value = float(match.group(0))
        except:
            value = 0
    return value


# noinspection PyBroadException
def size_int(size_txt):
    try:
        return int(size_txt)
    except:
        size_txt = size_txt.upper()
        size1 = size_txt.replace('B', '').replace('I', '').replace('K', '').replace('M', '').replace('G', '')
        size = get_float(size1)
        if 'K' in size_txt:
            size *= 1000
        if 'M' in size_txt:
            size *= 1000000
        if 'G' in size_txt:
            size *= 1e9
        return size


def clean_number(text):
    comma = text.find(',')
    point = text.find('.')
    if comma > 0 and point > 0:
        if comma < point:
            text = text.replace(',', '')
        else:
            text = text.replace('.', '')
            text = text.replace(',', '.')
    return text


def notify(message, image=None):
    dialog = xbmcgui.Dialog()
    dialog.notification(xbmcaddon.Addon().getAddonInfo("name"), message, icon=image)
    del dialog


def display_message_cache():
    p_dialog = xbmcgui.DialogProgressBG()
    p_dialog.create('Magnetic Manager', string(32061))
    xbmc.sleep(250)
    p_dialog.update(25, string(32065))
    xbmc.sleep(250)
    p_dialog.update(50, string(32065))
    xbmc.sleep(250)
    p_dialog.update(75, string(32065))
    xbmc.sleep(250)
    p_dialog.close()
    del p_dialog
