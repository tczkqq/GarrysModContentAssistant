from re import findall, compile as re_compile
from urllib.parse import unquote
from bs4 import BeautifulSoup
from requests import session
from os import system, path
from zipfile import ZipFile
import winreg


def open_website(*args):
    system("start https://github.com/Tomeczekqq/GarrysModContentAssistant")


def size_format(b):
    if b < 1000:
        return '%i' % b + 'B'
    elif 1000 <= b < 1000000:
        return '%.1f' % float(b/1000) + 'KB'
    elif 1000000 <= b < 1000000000:
        return '%.1f' % float(b/1000000) + 'MB'
    elif 1000000000 <= b < 1000000000000:
        return '%.1f' % float(b/1000000000) + 'GB'
    elif 1000000000000 <= b:
        return '%.1f' % float(b/1000000000000) + 'TB'


def scrap_mediafire(url):
    '''
    I will no longer support scraping mediafire links...
    TODO: Change or delete this method
    '''
    pre_regex = r"""(?xi)
    \b
    (
      (?:
        [a-z][\w-]+:
        (?:
          /{1,3}
          |
          [a-z0-9%]

        )
        |
        www\d{0,3}[.]
        |
        [a-z0-9.\-]+[.][a-z]{2,4}/
      )
      (?:
        [^\s()<>]+
        |
        \(([^\s()<>]+|(\([^\s()<>]+\)))*\)
      )+
      (?:
        \(([^\s()<>]+|(\([^\s()<>]+\)))*\)
        |
        [^\s`!()\[\]{};:'".,<>?]
      )
    )"""
    regex = re_compile(pre_regex)
    ses = session()
    result = ses.get(url)
    soup = BeautifulSoup(result.content)
    div_tag = soup.find_all(class_="download_link")[0]
    script_tag = div_tag("script")[0]
    link = findall(regex, script_tag.contents[0])[0][0]
    print(link)
    return link


def find_steam():
    '''
    Currently working only on windows.
    TODO: Add linux, mac os support
    '''
    try:
        key = winreg.CreateKey(
            winreg.HKEY_CURRENT_USER, "Software\Valve\Steam")
        location = winreg.QueryValueEx(key, "SteamPath")[0]
        return location + '/steamapps/common/GarrysMod/garrysmod/addons/'
    except:
        return path.dirname(path.abspath(__file__)) + 'downloads/steamapps/common/GarrysMod/garrysmod/addons/'


def unzip(link, dir):
    '''
    Unziping only zip files.
    TODO: Add .rar support
    '''
    a = path.split(link)
    filename = unquote(a[1])
    print(filename)
    with ZipFile(dir + filename, "r") as zip_ref:
        zip_ref.extractall(dir)
        print("unzipped")
    print("hej")
    return [True, filename]
