# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Helper Module containing various sites direct links generators. This module is copied and modified as per need
from https://github.com/AvinashReddy3108/PaperplaneExtended . I hereby take no credit of the following code other
than the modifications. See https://github.com/AvinashReddy3108/PaperplaneExtended/commits/master/userbot/modules/direct_links.py
for original authorship. """

from bot import UPTOBOX_TOKEN
import logging
import json
import math
import re
import urllib.parse
from os import popen
from random import choice
from urllib.parse import urlparse

import lk21
import requests
from bs4 import BeautifulSoup
from js2py import EvalJs
from lk21.extractors.bypasser import Bypass
from base64 import standard_b64encode

from bot.helper.ext_utils.exceptions import DirectDownloadLinkException


def direct_link_generator(link: str):
    """ direct links generator """
    if not link:
        raise DirectDownloadLinkException("`No links found!`")
    elif 'zippyshare.com' in link:
        return zippy_share(link)
    elif 'yadi.sk' in link:
        return yandex_disk(link)
    elif 'cloud.mail.ru' in link:
        return cm_ru(link)
    elif 'mediafire.com' in link:
        return mediafire(link)
    elif 'uptobox.com' in link:
        return uptobox(link)
    elif 'osdn.net' in link:
        return osdn(link)
    elif 'github.com' in link:
        return github(link)
    elif 'racaty.net' in link:
        return racaty(link)
    elif 'hxfile.co' in link:
        return hxfile(link)
    elif 'anonfiles.com' in link:
        return anon(link)
    elif 'femax20.com' in link:
        return femax20(link)
    elif 'layarkacaxxi.icu' in link:
        return layarkacaxxi(link)
    elif '1drv.ms' in link:
        return onedrive(link)
    elif 'streamtape.com' in link:
        return streamtape(link)
    elif '1fichier.com' in link:
        return fichier(link)
    else:
        raise DirectDownloadLinkException(f'No Direct link function found for {link}')


def zippy_share(url: str) -> str:
    link = re.findall("https:/.(.*?).zippyshare", url)[0]
    response_content = (requests.get(url)).content
    bs_obj = BeautifulSoup(response_content, "lxml")

    try:
        js_script = bs_obj.find("div", {"class": "center",}).find_all(
            "script"
        )[1]
    except:
        js_script = bs_obj.find("div", {"class": "right",}).find_all(
            "script"
        )[0]

    js_content = re.findall(r'\.href.=."/(.*?)";', str(js_script))
    js_content = 'var x = "/' + js_content[0] + '"'

    evaljs = EvalJs()
    setattr(evaljs, "x", None)
    evaljs.execute(js_content)
    js_content = getattr(evaljs, "x")

    return f"https://{link}.zippyshare.com{js_content}"


def yandex_disk(url: str) -> str:
    """ Yandex.Disk direct links generator
    Based on https://github.com/wldhx/yadisk-direct """
    try:
        link = re.findall(r'\bhttps?://.*yadi\.sk\S+', url)[0]
    except IndexError:
        reply = "`No Yandex.Disk links found`\n"
        return reply
    api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
    try:
        dl_url = requests.get(api.format(link)).json()['href']
        return dl_url
    except KeyError:
        raise DirectDownloadLinkException("`Error: File not found/Download limit reached`\n")


def cm_ru(url: str) -> str:
    """ cloud.mail.ru direct links generator
    Using https://github.com/JrMasterModelBuilder/cmrudl.py """
    reply = ''
    try:
        link = re.findall(r'\bhttps?://.*cloud\.mail\.ru\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No cloud.mail.ru links found`\n")
    command = f'vendor/cmrudl.py/cmrudl -s {link}'
    result = popen(command).read()
    result = result.splitlines()[-1]
    try:
        data = json.loads(result)
    except json.decoder.JSONDecodeError:
        raise DirectDownloadLinkException("`Error: Can't extract the link`\n")
    dl_url = data['download']
    return dl_url


def uptobox(url: str) -> str:
    """ Uptobox direct links generator
    based on https://github.com/jovanzers/WinTenCermin """
    try:
        link = re.findall(r'\bhttps?://.*uptobox\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Uptobox links found`\n")
    if UPTOBOX_TOKEN is None:
        logging.error('UPTOBOX_TOKEN not provided!')
        dl_url = url
    else:
        try:
            link = re.findall(r'\bhttp?://.*uptobox\.com/dl\S+', url)[0]
            logging.info('Uptobox direct link')
            dl_url = url
        except:
            file_id = re.findall(r'\bhttps?://.*uptobox\.com/(\w+)', url)[0]
            file_link = 'https://uptobox.com/api/link?token=%s&file_code=%s' % (UPTOBOX_TOKEN, file_id)
            req = requests.get(file_link)
            result = req.json()
            dl_url = result['data']['dlLink']
    return dl_url


def mediafire(url: str) -> str:
    """ MediaFire direct links generator """
    try:
        link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No MediaFire links found`\n")
    page = BeautifulSoup(requests.get(link).content, 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    dl_url = info.get('href')
    return dl_url


def osdn(url: str) -> str:
    """ OSDN direct links generator """
    osdn_link = 'https://osdn.net'
    try:
        link = re.findall(r'\bhttps?://.*osdn\.net\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No OSDN links found`\n")
    page = BeautifulSoup(
        requests.get(link, allow_redirects=True).content, 'lxml')
    info = page.find('a', {'class': 'mirror_link'})
    link = urllib.parse.unquote(osdn_link + info['href'])
    mirrors = page.find('form', {'id': 'mirror-select-form'}).findAll('tr')
    urls = []
    for data in mirrors[1:]:
        mirror = data.find('input')['value']
        urls.append(re.sub(r'm=(.*)&f', f'm={mirror}&f', link))
    return urls[0]


def github(url: str) -> str:
    """ GitHub direct links generator """
    try:
        re.findall(r'\bhttps?://.*github\.com.*releases\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No GitHub Releases links found`\n")
    download = requests.get(url, stream=True, allow_redirects=False)
    try:
        dl_url = download.headers["location"]
        return dl_url
    except KeyError:
        raise DirectDownloadLinkException("`Error: Can't extract the link`\n")


def racaty(url: str) -> str:
    """ Racaty direct links generator
    based on https://github.com/breakdowns/slam-mirrorbot """
    dl_url = ''
    try:
        link = re.findall(r'\bhttps?://.*racaty\.net\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Racaty links found`\n")
    reqs=requests.get(link)
    bss=BeautifulSoup(reqs.text,'html.parser')
    op=bss.find('input',{'name':'op'})['value']
    id=bss.find('input',{'name':'id'})['value']
    rep=requests.post(link,data={'op':op,'id':id})
    bss2=BeautifulSoup(rep.text,'html.parser')
    dl_url=bss2.find('a',{'id':'uniqueExpirylink'})['href']
    return dl_url


def hxfile(url: str) -> str:
    """ Hxfile direct links generator
    based on https://github.com/breakdowns/slam-mirrorbot """
    dl_url = ''
    try:
        link = re.findall(r'\bhttps?://.*hxfile\.co\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Hxfile links found`\n")
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_url(link)
    return dl_url


def anon(url: str) -> str:
    """ Anonfiles direct links generator
    based on https://github.com/breakdowns/slam-mirrorbot """
    dl_url = ''
    try:
        link = re.findall(r'\bhttps?://.*anonfiles\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Anonfiles links found`\n")
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_url(link)
    return dl_url


def femax20(url: str) -> str:
    """ Fembed direct links generator
    based on https://github.com/breakdowns/slam-mirrorbot """
    dl_url = ''
    try:
        link = re.findall(r'\bhttps?://.*femax20\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Fembed links found`\n")
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_fembed(link)
    lst_link = []
    count = len(dl_url)
    for i in dl_url:
        lst_link.append(dl_url[i])
    return lst_link[count-1]


def layarkacaxxi(url: str) -> str:
    """ Fembed direct links generator
    based on https://github.com/breakdowns/slam-mirrorbot """
    dl_url = ''
    try:
        link = re.findall(r'\bhttps?://.*layarkacaxxi\.icu\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No Fembed links found\n")
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_fembed(link)
    lst_link = []
    count = len(dl_url)
    for i in dl_url:
        lst_link.append(dl_url[i])
    return lst_link[count-1]


def onedrive(link: str) -> str:
    """ Onedrive direct link generator
    Based on https://github.com/UsergeTeam/Userge """
    link_without_query = urlparse(link)._replace(query=None).geturl()
    direct_link_encoded = str(standard_b64encode(bytes(link_without_query, "utf-8")), "utf-8")
    direct_link1 = f"https://api.onedrive.com/v1.0/shares/u!{direct_link_encoded}/root/content"
    resp = requests.head(direct_link1)
    if resp.status_code != 302:
        return "`Error: Unauthorized link, the link may be private`"
    dl_link = resp.next.url
    file_name = dl_link.rsplit("/", 1)[1]
    resp2 = requests.head(dl_link)
    return dl_link

def streamtape(url: str) -> str:
    """ Streamtape direct link generator
    Based on https://github.com/breakdowns/slam-mirrorbot """
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_streamtape(url)
    return dl_url


def fichier(link: str) -> str:
    """ 1Fichier direct links generator
    Based on https://github.com/Maujar/updateref-16-7-21
             https://github.com/breakdowns/slam-mirrorbot """
    regex = r"^([http:\/\/|https:\/\/]+)?.*1fichier\.com\/\?.+"
    gan = re.match(regex, link)
    if not gan:
      raise DirectDownloadLinkException("ERROR: The link you entered is wrong!")
    if "::" in link:
      pswd = link.split("::")[-1]
      url = link.split("::")[-2]
    else:
      pswd = None
      url = link
    try:
      if pswd is None:
        req = requests.post(url)
      else:
        pw = {"pass": pswd}
        req = requests.post(url, data=pe)
    except:
      raise DirectDownloadLinkException("ERROR: Unable to reach 1fichier server!")
    if req.status_code == 404:
      raise DirectDownloadLinkException("ERROR: File not found / The link you entered is wrong!")
    soup = BeautifulSoup(req.content, 'lxml')
    if soup.find("a", {"class": "ok btn-general btn-orange"}) is not None:
      dl_url = soup.find("a", {"class": "ok btn-general btn-orange"})["href"]
      if dl_url is None:
        raise DirectDownloadLinkException("ERROR: Unable to generate Direct Link 1fichier!")
      else:
        return dl_url
    else:
      if len(soup.find_all("div", {"class": "ct_warn"})) == 2:
        str_2 = soup.find_all("div", {"class": "ct_warn"})[-1]
        if "you must wait" in str(str_2).lower():
          numbers = [int(word) for word in str(str_2).split() if word.isdigit()]
          if len(numbers) == 0:
            raise DirectDownloadLinkException("ERROR: 1fichier is on a limit. Please wait a few minutes/hour.")
          else:
            raise DirectDownloadLinkException(f"ERROR: 1fichier is on a limit. Please wait {numbers[0]} minute.")
        elif "protect access" in str(str_2).lower():
          raise DirectDownloadLinkException("ERROR: This link requires a password!\n\n<b>This link requires a password!</b>\n- Insert sign <b>::</b> after the link and write the password after the sign.\n\n<b>Example:</b>\n<code>/mirror https://1fichier.com/?smmtd8twfpm66awbqz04::love you</code>\n\n* No spaces between the signs <b>::</b>\n* For the password, you can use a space!")
        else:
          raise DirectDownloadLinkException("ERROR: Error trying to generate Direct Link from 1fichier!")
      elif len(soup.find_all("div", {"class": "ct_warn"})) == 3:
        str_1 = soup.find_all("div", {"class": "ct_warn"})[-2]
        str_3 = soup.find_all("div", {"class": "ct_warn"})[-1]
        if "you must wait" in str(str_1).lower():
          numbers = [int(word) for word in str(str_1).split() if word.isdigit()]
          if len(numbers) == 0:
            raise DirectDownloadLinkException("ERROR: 1fichier is on a limit. Please wait a few minutes/hour.")
          else:
            raise DirectDownloadLinkException(f"ERROR: 1fichier is on a limit. Please wait {numbers[0]} minute.")
        elif "bad password" in str(str_3).lower():
          raise DirectDownloadLinkException("ERROR: The password you entered is wrong!")
        else:
          raise DirectDownloadLinkException("ERROR: Error trying to generate Direct Link from 1fichier!")
      else:
        raise DirectDownloadLinkException("ERROR: Error trying to generate Direct Link from 1fichier!")



def useragent():
    """
    useragent random setter
    """
    useragents = BeautifulSoup(
        requests.get(
            'https://developers.whatismybrowser.com/'
            'useragents/explore/operating_system_name/android/').content,
        'lxml').findAll('td', {'class': 'useragent'})
    user_agent = choice(useragents)
    return user_agent.text
