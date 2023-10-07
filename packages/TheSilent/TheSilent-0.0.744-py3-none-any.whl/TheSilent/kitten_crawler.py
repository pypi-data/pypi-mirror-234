import re
import time
import urllib.parse
import TheSilent.puppy_requests as puppy_requests

CYAN = "\033[1;36m"

def kitten_crawler(init_host,delay=0):
    host = init_host.rstrip("/")
    host_list = [host + "/"]
    try:
        sitemap_list = []
        data = puppy_requests.text(init_host + "/sitemap.xml").lower()
        data = data.replace("<","\n<")
        data = re.findall("<loc>(http\S+)",data.lower())
        for _ in data:
            _ = _.split("<")[0]
            if "sitemap" in _:
                sitemap_list.append(_)

            else:
                host_list.append(_)

    except:
        pass

    if len(sitemap_list) > 0:
        for _ in sitemap_list:
            time.sleep(delay)
            try:
                data = puppy_requests.text(_).lower()
                data = data.replace("<","\n<")
                data = re.findall("<loc>(http\S+)",data.lower())
                for __ in data:
                    host_list.append(__)

            except:
                pass

    _ = -1
    while True:
        _ += 1
        try:
            print(CYAN + host_list[_])
            time.sleep(delay)
            host_list = list(dict.fromkeys(host_list[:]))
            data = urllib.parse.unquote_plus(puppy_requests.text(host_list[_]).lower())

            contents = re.findall("content\s?=\s?[\"\'](\S+)[\"\']",data.lower())
            contents = list(set(contents[:]))
            for content in contents:
                skip = False
                for __ in content:
                    if re.search("[\"\'\<\>]",__):
                        skip = True

                if not skip:
                    if "script" not in content:
                        if content.startswith("/"):
                            content = href.rstrip('"')
                            content = href.rstrip("'")
                            host_list.append(host + content)

                        elif not content.startswith("http://") and not content.startswith("https://") and urllib.parse.urlparse(host).netloc not in content:
                            host_list.append(init_host + "/" + content)

                        elif content.startswith("http://") and content.startswith(init_host) in content or content.startswith("https://") and content.startswith(init_host):
                            host_list.append(content)

                        elif not content.startswith("http://") and not content.startswith("https://") and urllib.parse.urlparse(host).netloc in content and content.startswith("//"):
                            host_list.append(urllib.parse.urlparse(host).scheme + content)


            hrefs = re.findall("href\s?=\s?[\"\'](\S+)[\"\']",data.lower())
            hrefs = list(set(hrefs[:]))
            for href in hrefs:
                skip = False
                for __ in href:
                    if re.search("[\"\'\<\>]",__):
                        skip = True

                if not skip:
                    if "script" not in href:
                        if href.startswith("/"):
                            href = href.rstrip('"')
                            href = href.rstrip("'")
                            host_list.append(host + href)

                        elif not href.startswith("http://") and not href.startswith("https://") and urllib.parse.urlparse(host).netloc not in href:
                            host_list.append(init_host + "/" + href)

                        elif href.startswith("http://") and href.startswith(init_host) in href or href.startswith("https://") and href.startswith(init_host):
                            host_list.append(href)

                        elif not href.startswith("http://") and not href.startswith("https://") and urllib.parse.urlparse(host).netloc in href and href.startswith("//"):
                            host_list.append(urllib.parse.urlparse(host).scheme + href)

            sources = re.findall("src\s?=\s?[\"\'](\S+)[\"\']",data.lower())
            sources = list(set(sources[:]))
            for source in sources:
                skip = False
                for __ in source:
                    if re.search("[\"\'\<\>]",__):
                        skip = True

                if not skip:
                    if "script" not in source:
                        if source.startswith("/"):
                            source = source.rstrip('"')
                            source = source.rstrip("'")
                            host_list.append(init_host + source)

                        elif not source.startswith("http://") and not source.startswith("https://") and urllib.parse.urlparse(host).netloc not in source:
                            host_list.append(init_host + "/" + source)

                        elif source.startswith("http://") and source.startswith(init_host) or source.startswith("https://") and source.startswith(init_host):
                            host_list.append(source)

                        elif not source.startswith("http://") and not source.startswith("https://") and urllib.parse.urlparse(host).netloc in source and source.startswith("//"):
                            host_list.append(urllib.parse.urlparse(host).scheme + "/" + source)

        except IndexError:
            break

        except:
            continue

    host_list = list(dict.fromkeys(host_list[:]))
    return host_list
