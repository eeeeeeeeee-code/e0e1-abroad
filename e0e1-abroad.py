# -*- coding: utf-8 -*-
import argparse
import time
import requests
import pandas as pd
import concurrent.futures
import re
import os
from bs4 import BeautifulSoup
from colorama import Fore
from yaml import safe_load

requests.packages.urllib3.disable_warnings()


class CONFIG:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        config = safe_load(open(config_path, "r",encoding="utf-8").read())
        self.suffix_com = ['net', 'fr', 'me', 'ch', 'at', 'de', 'co', 'pt', 'se', 'it', 'pl', 'cloud', 'es', 'eu', 'be', 'jp', 'fi', 'nl', 'io', 'lu', 'link', 'tv', 'dk', 'info', 'ca', 'team', 'hu', 'com', 'cm', 'ie', 'no']

        self.it_api = config['intigriti']['api-key']
        self.it_max_thead = 5
        self.it_file_xlsx = "./result/it.xlsx"

        self.h1_user = config['hackerone']['hacker-user']
        self.h1_key = config['hackerone']['hacker-key']
        self.h1_max_thead = 5
        self.h1_file_xlsx = "./result/h1.xlsx"

        self.bc_token = config['bugcrowd']['bug_token']
        self.bc_max_thead = 3
        self.bc_file_xlsx = "./result/bc.xlsx"

        self.ob_max_thead = 5
        self.ob_file_xlsx = "./result/ob.xlsx"

        self.im_max_thead = 5
        self.im_file_xlsx = "./result/im.xlsx"

        self.in_token = config["inspectiv"]["in_token"]
        self.in_max_thead = 5
        self.in_file_xlsx = "./result/inspectiv.xlsx"

        self.yh_token = config["yeswehack"]["yh_token"]
        self.yh_max_thead = 5
        self.yh_file_xlsx = "./result/yeswehack.xlsx"


class Common:
    class Colored(object):
        def red(self, s):
            return Fore.RED + s + Fore.RESET

        def green(self, s):
            return Fore.GREEN + s + Fore.RESET

        def yellow(self, s):
            return Fore.YELLOW + s + Fore.RESET

        def blue(self, s):
            return Fore.BLUE + s + Fore.RESET

        def magenta(self, s):
            return Fore.MAGENTA + s + Fore.RESET

    def optimize_url(self, url):
        try:
            root_list = []
            url_list = []
            error_list = []
            error_root_list = []
            if url[0].startswith('*'):
                it_list = url[0].replace("*.", "").replace("/*", "").replace("/", "").strip()
                if it_list[-1] == "*":
                    for i in CONFIG().suffix_com:
                        it_com = it_list.split(".")
                        it_com[1] = i
                        url[0] = ".".join(it_com)
                        root_list += (list(url))
                elif re.search(r"[*()\[{\]}<>]", it_list):
                    error_root_list += (["有问题自行处理的url:" + it_list, url[1]])
                elif "." in it_list:
                    url[0] = it_list
                    root_list += url
            elif "." in url[0]:
                it_url = url[0].replace("/*", "").strip()
                if re.search(r"[*()\[{\]}<>]", it_url):
                    error_list += (["有问题自行处理的url:" + it_url, url[1]])
                else:
                    url_list += ([it_url, url[1]])
            return error_list + url_list, error_root_list + root_list
        except Exception as e:
            print(Common.Colored().red("bug :{}".format(e)))
            return [["", ""]], [["", ""]]

    def split_list_root(self, sublists):
        try:
            processed_list = []

            def split_sublists(sublist):
                return [sublist[i:i + 2] for i in range(0, len(sublist), 2)]

            for item in sublists:
                if len(item) > 2:
                    processed_list.extend(split_sublists(item))
                else:
                    processed_list.append(item)

            return processed_list
        except Exception as e:
            print(Common.Colored().red("bug :{}".format(e)))
            return [["", ""]]

    def url_optimize(self, url_result2):
        try:
            if argss.Urlop_tf:
                root_result = []
                url_result = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    results = executor.map(Common().optimize_url, url_result2)
                    for i in results:
                        c, b = i
                        root_result.append(b)
                        url_result.append(c)
                return (sorted(list(filter(None, root_result)), key=Intigriti().custom_sort)), (sorted(list(filter(None, url_result)), key=Intigriti().custom_sort))
        except Exception as e:
            print(Common.Colored().red("bug :{}".format(e)))
            return [["", ""]], [["", ""]]


class Process_Print2:
    def __init__(self, file_path):
        self.file_path = file_path

    def all_xlsx_file(self, data, columns_name, sheet_name):
        df = pd.DataFrame.from_records(data)
        df.columns = columns_name
        with pd.ExcelWriter(self.file_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=sheet_name, engine='xlsxwriter', index=False)

    def add_xlsx_file(self, data, columns_name, sheet_name):
        df = pd.DataFrame.from_records(data)
        df.columns = columns_name
        with pd.ExcelWriter(self.file_path, engine="openpyxl", mode='a', if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name=sheet_name, engine='xlsxwriter', index=False)


class Intigriti:
    def __init__(self):
        self.it_api = CONFIG().it_api
        self.it_result = []
        self.it_url_result = []
        self.it_app_result = []
        self.it_auth_result = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            "accept": "application/json",
            "Authorization": "Bearer {}".format(self.it_api)
        }

    def set_it_xlsx(self):
        Process_Print2(CONFIG().it_file_xlsx).all_xlsx_file(self.it_result, ['项目值', '项目名称'], "all")
        if argss.Urlop_tf:
            root_result, url_result = Common().url_optimize(self.it_url_result)
            Process_Print2(CONFIG().it_file_xlsx).add_xlsx_file(Common().split_list_root(root_result), ['项目值', '项目名称'], "root")
            Process_Print2(CONFIG().it_file_xlsx).add_xlsx_file(url_result, ['项目值', '项目名称'], "url")
        else:
            Process_Print2(CONFIG().it_file_xlsx).add_xlsx_file(self.it_url_result, ['项目值', '项目名称'], "url")
        if argss.App_tf:
            Process_Print2(CONFIG().it_file_xlsx).add_xlsx_file(self.it_app_result, ['项目值', '项目名称'], "app")
        Process_Print2(CONFIG().it_file_xlsx).add_xlsx_file(self.it_auth_result, ['项目值', '项目名称'], "auth")

    def find_jsonkey(self, item_data, key, name):
        try:
            for item in item_data:
                if item.get("tier", {}).get("value") != "Out Of Scope":
                    type_value = item.get("type", {}).get("value")
                    if key in item:
                        self.it_result.append([item[key], name])
                    if argss.Url_tf:
                        if key in item and type_value in ["Url", "Wildcard", "IpRange"]:
                            self.it_url_result.append([item[key], name])
                    if argss.App_tf:
                        if key in item and type_value in ["iOS", "Android"]:
                            self.it_app_result.append([item[key], name])
                    if type_value in ['Device', 'Other']:
                        self.it_auth_result.append([item[key], name])
        except Exception as e:
            print(Common.Colored().red(e))

    def custom_sort(self, item):
        if item[0].startswith("有问题"):
            return 0, item[0]
        elif not item[0].startswith('.'):
            return 1, item[0]
        return 2, item[0]

    def get_it_id(self):
        try:
            id_url = "https://api.intigriti.com/external/researcher/v1/programs/?limit=500"
            itreqo = requests.get(url=id_url, headers=self.headers, timeout=3, verify=False).json()
            print(Common.Colored().magenta("intigriti_id返回完成\n"))
            return itreqo['records']
        except Exception as e:
            print(Common.Colored().red("get_it_id bugs: {}".format(e)))

    def fetch_data(self, it_id):
        pid_url = f"https://api.intigriti.com/external/researcher/v1/programs/{it_id['id']}"
        try:
            response = requests.get(pid_url, headers=self.headers, timeout=3, verify=False)
            data = response.json()
            self.find_jsonkey(data['domains']['content'], "endpoint", data["name"])
            print(Common.Colored().green(f"已处理：{data['name']}"))
        except Exception as e:
            print(Common.Colored().red(f"it-id 问题 {it_id['id']}: {e}"))

    def get_it_programs(self):
        if self.it_api not in "":
            print(Common.Colored().magenta("开始收集it-url"))
        else:
            print(Common.Colored().red("请设置it-key"))
            exit(0)

        with concurrent.futures.ThreadPoolExecutor(max_workers=CONFIG().it_max_thead) as executor:
            executor.map(self.fetch_data, self.get_it_id())

        self.set_it_xlsx()
        print(Common.Colored().yellow(f"Intigriti处理完成, 文件已保存至{CONFIG().it_file_xlsx}"))


class Hackerone:
    def __init__(self):
        self.h1_user = CONFIG().h1_user
        self.h1_key = CONFIG().h1_key
        self.h1_reulst = []
        self.h1_url = []
        self.h1_app = []
        self.h1_auth = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'application/json'
        }

    def set_it_xlsx(self):
        Process_Print2(CONFIG().h1_file_xlsx).all_xlsx_file(self.h1_reulst, ['项目值', '项目名称'], "all")
        if argss.Urlop_tf:
            root_result, url_result = Common().url_optimize(self.h1_url)
            Process_Print2(CONFIG().h1_file_xlsx).add_xlsx_file(Common().split_list_root(root_result), ['项目值', '项目名称'], "root")
            Process_Print2(CONFIG().h1_file_xlsx).add_xlsx_file(url_result, ['项目值', '项目名称'], "url")
        elif argss.Url_tf:
            Process_Print2(CONFIG().h1_file_xlsx).add_xlsx_file(self.h1_url, ['项目值', '项目名称'], "url")
        if argss.App_tf:
            Process_Print2(CONFIG().h1_file_xlsx).add_xlsx_file(self.h1_app, ['项目值', '项目名称'], "app")
        Process_Print2(CONFIG().h1_file_xlsx).add_xlsx_file(self.h1_auth, ['项目值', '项目名称'], "auth")

    def find_jsonkey(self, item_data, name):
        for item in item_data:
            if item.get('attributes').get("eligible_for_submission"):
                type_value = item.get('attributes').get("asset_type")
                self.h1_reulst.append([item["attributes"]["asset_identifier"], name])
                if argss.Url_tf:
                    if type_value in ["URL", "WILDCARD", "OTHER", "CIDR", "API"]:
                        self.h1_url.append([item["attributes"]["asset_identifier"], name])
                if argss.App_tf:
                    if type_value in ["GOOGLE_PLAY_APP_ID", "OTHER_APK", "GOOGLE_PLAY_APP_ID", "WINDOWS_APP_STORE_APP_ID", "TESTFLIGHT"]:
                        self.h1_app.append([item["attributes"]["asset_identifier"], name])
                if type_value in ["AI_MODEL", "HARDWARE", "OTHER", "DOWNLOADABLE_EXECUTABLES0", "SMART_CONTRACT", "SOURCE_CODE"]:
                    self.h1_auth.append([item["attributes"]["asset_identifier"], name])

    def get_h1_id(self):
        number = 1
        prams = []
        while True:
            api_url = f"https://api.hackerone.com/v1/hackers/programs?page[size]=100&page[number]={number}"
            try:
                response = requests.get(api_url, auth=(self.h1_user, self.h1_key))
                if response.status_code != 200:
                    print(Common.Colored().red("回显不为200，重新配置h1 user和key"))
                    exit(0)
                h1_req = response.json().get("data")
                if not h1_req:
                    return prams
                prams += h1_req
            except requests.exceptions.RequestException as e:
                print(Common.Colored().red("user或者key错误"))
                break
            number += 1
        print(Common.Colored().magenta("获取id完成~~~~~"))
        return prams

    def get_h1_url(self, id_params):
        try:
            h1_name = id_params["attributes"]["handle"]
            api_url = "https://api.hackerone.com/v1/hackers/programs/{}/structured_scopes?page[number]=1&page[size]=100".format(h1_name)
            h1_req = requests.get(api_url, auth=(self.h1_user, self.h1_key)).json()
            h1_data = h1_req['data']
            self.find_jsonkey(h1_data, h1_name)
            print(Common.Colored().green(f"已处理：{h1_name}"))
        except Exception as e:
            print(Common.Colored().red("bugs {}".format(e)))

    def get_h1_programs(self):
        try:
            if self.h1_user != "" and self.h1_key != "":
                print(Common.Colored().magenta("h1已配置"))
            else:
                print(Common.Colored().red("h1 user和key未配置"))
                exit(0)

            id_params = Hackerone().get_h1_id()
            with concurrent.futures.ThreadPoolExecutor(max_workers=CONFIG().h1_max_thead) as executor:
                executor.map(self.get_h1_url, id_params)

            self.set_it_xlsx()
            print(Common.Colored().yellow(f"Hackerone 处理完成，结果保存至{CONFIG().h1_file_xlsx}"))
        except Exception as e:
            print(Common.Colored().red("bugs {}".format(e)))


class Bugcrowd:
    def __init__(self):
        self.bc_result = []
        self.bc_url = []
        self.bc_app = []
        self.bc_auth = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Cookies': f'_bugcrowd_session={CONFIG().bc_token}',
            'Accept': '*/*'
        }

    def set_it_xlsx(self):
        Process_Print2(CONFIG().bc_file_xlsx).all_xlsx_file(self.bc_result, ['项目值', '项目名称'], "all")
        if argss.Urlop_tf:
            root_result, url_result = Common().url_optimize(self.bc_url)
            Process_Print2(CONFIG().bc_file_xlsx).add_xlsx_file(Common().split_list_root(root_result), ['项目值', '项目名称'], "root")
            Process_Print2(CONFIG().bc_file_xlsx).add_xlsx_file(url_result, ['项目值', '项目名称'], "url")
        else:
            Process_Print2(CONFIG().bc_file_xlsx).add_xlsx_file(self.bc_url, ['项目值', '项目名称'], "url")
        if argss.App_tf:
            Process_Print2(CONFIG().bc_file_xlsx).add_xlsx_file(self.bc_app, ['项目值', '项目名称'], "app")
        Process_Print2(CONFIG().bc_file_xlsx).add_xlsx_file(self.bc_auth, ['项目值', '项目名称'], "auth")

    def find_jsonkey(self, item_data, name):
        for item in item_data:
            type_value = item.get('category')
            self.bc_result.append([item["name"], name])
            if type_value in ["other", "hardware"]:
                self.bc_auth.append([item["name"], name])
            if argss.Url_tf:
                if type_value in ["website", "api"]:
                    self.bc_url.append([item["name"], name])
            if argss.App_tf:
                if type_value in ["android", "ios"]:
                    self.bc_app.append([item["name"], name])

    def get_handle(self):
        try:
            jurl = "https://bugcrowd.com/engagements.json?category=bug_bounty&sort_by=promoted&sort_direction=desc&page="
            page = 1
            br_list = []
            while True:
                repose = requests.get(f"{jurl}{page}", headers=self.headers, timeout=5, verify=False).json()
                print(repose)
                if not repose['engagements']:
                    break
                br_list += [eng['briefUrl'] for eng in repose['engagements']]
                page += 1
                time.sleep(0.3)
            print(Common.Colored().magenta("获取handle完成"))
            return br_list
        except Exception as e:
            print(Common.Colored().red(e))

    def get_handle_url(self, handle):
        try:
            bc_url = f"https://bugcrowd.com"
            repose_url = requests.get(f'{bc_url}{handle}/target_groups', headers=self.headers, timeout=5, verify=False).json()
            targets_list = [tars["targets_url"] for tars in repose_url['groups'] if tars["in_scope"]]
            for tar in targets_list:
                repose_tars = requests.get(f'{bc_url}/{tar}', headers=self.headers, timeout=5, verify=False)
                self.find_jsonkey(repose_tars.json()["targets"], handle)
            print(Common.Colored().green(f"已处理：{handle}"))
        except Exception as e:
            print(Common.Colored().red(e))

    def get_bc_programs(self):
        try:
            if CONFIG().bc_token == "":
                print(Common.Colored().red("bc_token未设置"))
                exit(0)
            else:
                print(Common.Colored().magenta("bc_token已经设置"))

            handle_list = self.get_handle()
            with concurrent.futures.ThreadPoolExecutor(max_workers=CONFIG().bc_max_thead) as executor:
                executor.map(self.get_handle_url, handle_list)

            self.set_it_xlsx()
            print(Common.Colored().yellow(f"Bugcrowd 已处理完成，结果保存至{CONFIG().bc_file_xlsx}"))
        except Exception as e:
            print(Common.Colored().red(e))


class Openbugbounty:
    def __init__(self):
        self.ob_result = []
        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.headers2 = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

    def set_it_xlsx(self):
        Process_Print2(CONFIG().ob_file_xlsx).all_xlsx_file(self.ob_result, ['项目值', '项目名称'], "all")
        if argss.Urlop_tf:
            root_result, url_result = Common().url_optimize(self.ob_result)
            Process_Print2(CONFIG().ob_file_xlsx).add_xlsx_file(Common().split_list_root(root_result), ['项目值', '项目名称'], "root")
            Process_Print2(CONFIG().ob_file_xlsx).add_xlsx_file(url_result, ['项目值', '项目名称'], "url")

    def get_ob_handle(self):
        try:
            page_int = 49
            a_tag_list = []
            while True:
                data = {
                    'draw': '40',
                    'columns[0][data]': '0',
                    'columns[0][name]': '',
                    'columns[0][searchable]': 'true',
                    'columns[0][orderable]': 'false',
                    'columns[0][search][value]': '',
                    'columns[0][search][regex]': 'false',
                    'columns[1][data]': '1',
                    'columns[1][name]': '',
                    'columns[1][searchable]': 'true',
                    'columns[1][orderable]': 'false',
                    'columns[1][search][value]': '',
                    'columns[1][search][regex]': 'false',
                    'columns[2][data]': '2',
                    'columns[2][name]': '',
                    'columns[2][searchable]': 'true',
                    'columns[2][orderable]': 'false',
                    'columns[2][search][value]': '',
                    'columns[2][search][regex]': 'false',
                    'start': page_int,
                    'length': '50',
                    'search[value]': '',
                    'search[regex]': 'false',
                }

                response = requests.post('https://www.openbugbounty.org/bugbounty-list/ajax.php', headers=self.headers, data=data, timeout=5, verify=False)

                if "/images/404.jpg" in response.text:
                    break
                for a_tag in response.json()["data"]:
                    soup = BeautifulSoup(a_tag[0], "html.parser")
                    a_tag_list.append(soup.a["href"])
                page_int += 50
            print(Common.Colored().magenta("获取handle完成~~\n"))
            return a_tag_list
        except Exception as e:
            print(Common.Colored().red(e))

    def get_ob_handleurl(self, handle):
        try:
            response = requests.get(f'https://www.openbugbounty.org{handle}', headers=self.headers2, timeout=5, verify=False)
            soup = BeautifulSoup(response.content, "html.parser")
            tables = soup.find_all('table', class_="wishlist open-bounty")[0]
            self.ob_result += [[td_tar.text, handle] for td_tar in tables.find_all("td")]
            print(Common.Colored().green(f"已处理：{handle}"))
        except Exception as e:
            print(Common.Colored().red(e))

    def get_ob_parms(self):
        try:
            print(Common.Colored().magenta("Openbugbounty 已准备完成"))
            handle_list = self.get_ob_handle()

            with concurrent.futures.ThreadPoolExecutor(max_workers=CONFIG().ob_max_thead) as executor:
                executor.map(self.get_ob_handleurl, handle_list)

            self.set_it_xlsx()
            print(Common.Colored().yellow(f"Openbugbounty 处理完成，结果保存至{CONFIG().ob_file_xlsx}"))
        except Exception as e:
            print(Common.Colored().red(e))


class immunefi:
    def __init__(self):
        self.im_result = []
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

    def set_it_xlsx(self):
        Process_Print2(CONFIG().im_file_xlsx).all_xlsx_file(self.im_result, ['项目值', '项目名称'], "all")
        if argss.Urlop_tf:
            root_result, url_result = Common().url_optimize(self.im_result)
            Process_Print2(CONFIG().im_file_xlsx).add_xlsx_file(Common().split_list_root(root_result), ['项目值', '项目名称'], "root")
            Process_Print2(CONFIG().im_file_xlsx).add_xlsx_file(url_result, ['项目值', '项目名称'], "url")

    def get_im_handle(self):
        try:
            repose = requests.get("https://immunefi.com/_next/data/MyPLbGoqDLuTD2N74EBK7/bug-bounty.json", headers=self.headers).json()
            name_list = [tar["id"] for tar in repose["pageProps"]["bounties"]]
            print(Common.Colored().magenta("name 获取完成~~~~"))
            return name_list
        except Exception as e:
            print(Common.Colored().red(e))

    def get_im_handle_url(self, handle):
        try:
            repose = requests.get(f"https://immunefi.com/bounty/{handle}/", headers=self.headers)
            soup = BeautifulSoup(repose.text, "html.parser")
            section = soup.find_all('section', class_='mb-12')
            for section in section:
                h3_tag = section.find('h3')
                if h3_tag is not None and h3_tag.text == 'Assets in scope':
                    a_tags = section.find_all('a')
                    for a_tag in a_tags:
                        try:
                            self.im_result.append([a_tag['title'], handle])
                        except:
                            pass
            print(Common.Colored().green(f"已处理：{handle}"))
        except Exception as e:
            print(Common.Colored().red(e))

    def get_im_parms(self):
        try:
            print(Common.Colored().magenta("im 开始~~~~~"))

            name_list = self.get_im_handle()

            with concurrent.futures.ThreadPoolExecutor(max_workers=CONFIG().im_max_thead) as executor:
                executor.map(self.get_im_handle_url, name_list)

            self.set_it_xlsx()
            print(Common.Colored().yellow(f"immunefi 已处理完成，结果保存至{CONFIG().im_file_xlsx}"))
        except Exception as e:
            print(Common.Colored().red(e))


class inspectiv:
    def __init__(self):
        self.in_result = []
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': f'Token {CONFIG().in_token}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

    def set_it_xlsx(self):
        Process_Print2(CONFIG().in_file_xlsx).all_xlsx_file(self.in_result, ['项目值', '项目名称'], "all")
        if argss.Urlop_tf:
            root_result, url_result = Common().url_optimize(self.in_result)
            Process_Print2(CONFIG().in_file_xlsx).add_xlsx_file(Common().split_list_root(root_result), ['项目值', '项目名称'], "root")
            Process_Print2(CONFIG().in_file_xlsx).add_xlsx_file(url_result, ['项目值', '项目名称'], "url")

    def get_in_handle(self):
        try:
            parg_int = 1
            uuid_list = []
            while True:
                params = {
                    'page': parg_int,
                    'search': '',
                    'all': 'true',
                    'private': 'false',
                    'favorites': 'false',

                }

                response = requests.get('https://api.bounty.inspectiv.com/api/programs/short-list/', params=params, headers=self.headers).json()
                try:
                    if str(response["status_code"]) == "404":
                        break
                except:
                    pass
                uuid_list += [tars["uuid"] for tars in response["results"]]
                parg_int += 1
            print(Common.Colored().magenta("uuid收集完成"))
            return uuid_list
        except Exception as e:
            print(Common.Colored().red(e))

    def get_in_handleurl(self, handle):
        try:
            repose = requests.get(f"https://api.bounty.inspectiv.com/api/programs/{handle}/", headers=self.headers)
            url_name = repose.json()["company_name"]
            url_list = re.findall(r"(?:Tier [123])\s*\|\s*(.*?)\s*(?=\|)", repose.text)
            self.in_result += [[tar, url_name] for tar in url_list]
            print(Common.Colored().green(f"已处理：{url_name}"))
        except Exception as e:
            print(Common.Colored().red(e))

    def get_in_parms(self):
        try:
            if CONFIG().in_token == "":
                print(Common.Colored().red("请配置in_token"))
                exit(0)
            else:
                print(Common.Colored().magenta("已配置in_token"))

            uuid_list = self.get_in_handle()
            with concurrent.futures.ThreadPoolExecutor(max_workers=CONFIG().in_max_thead) as executor:
                executor.map(self.get_in_handleurl, uuid_list)

            self.set_it_xlsx()
            print(Common.Colored().yellow(f"inspectiv 处理完成，结果已保存至{CONFIG().in_file_xlsx}"))
        except Exception as e:
            print(Common.Colored().red(e))


class Yeswehack:
    def __init__(self):
        self.yh_result = []
        self.yh_url = []
        self.yh_app = []
        self.yh_auth = []
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Authorization': f"Bearer {CONFIG().yh_token}"
        }

    def set_it_xlsx(self):
        Process_Print2(CONFIG().yh_file_xlsx).all_xlsx_file(self.yh_result, ['项目值', '项目名称'], "all")
        if argss.Urlop_tf:
            root_result, url_result = Common().url_optimize(self.yh_url)
            Process_Print2(CONFIG().yh_file_xlsx).add_xlsx_file(Common().split_list_root(root_result), ['项目值', '项目名称'], "root")
            Process_Print2(CONFIG().yh_file_xlsx).add_xlsx_file(url_result, ['项目值', '项目名称'], "url")
        elif argss.Url_tf:
            Process_Print2(CONFIG().yh_file_xlsx).add_xlsx_file(self.yh_url, ['项目值', '项目名称'], "url")
        if argss.App_tf:
            Process_Print2(CONFIG().yh_file_xlsx).add_xlsx_file(self.yh_app, ['项目值', '项目名称'], "app")
        Process_Print2(CONFIG().yh_file_xlsx).add_xlsx_file(self.yh_auth, ['项目值', '项目名称'], "auth")
    def find_jsonkey(self, item_data, name):
        for item in item_data:
            type_value = item.get('scope_type')
            self.yh_result.append([item["scope"], name])
            if argss.Url_tf:
                if type_value in ["web-application", "api", "ip-address"]:
                    self.yh_url.append([item["scope"], name])
            if argss.App_tf:
                if type_value in ["mobile-application-android", "mobile-application-ios", "mobile-application"]:
                    self.yh_app.append([item["scope"], name])
            if type_value in ["other", "application"]:
                self.yh_auth.append([item["scope"], name])

    def get_yh_handle(self):
        try:
            page_int = 1
            handle_list = []
            while True:
                repose = requests.get(f"https://api.yeswehack.com/programs?page={page_int}&resultsPerPage=50", headers=self.headers, timeout=5, verify=False).json()
                if not repose["items"]:
                    break
                for i in repose["items"]:
                    handle_list.append(i["slug"])
                page_int += 1
            print(Common.Colored().magenta("ye slug列表获取完成"))
            return handle_list
        except Exception as e:
            print(Common.Colored().red(e))

    def get_yh_handle_url(self, handle):
        try:
            repose = requests.get(f"https://api.yeswehack.com/programs/{handle}", headers=self.headers, timeout=5, verify=False).json()
            scope_list = repose["scopes"]
            self.find_jsonkey(scope_list, handle)
            print(Common.Colored().green(f"已处理：{handle}"))
        except Exception as e:
            print(Common.Colored().red(e))

    def get_yh_parms(self):
        try:
            if CONFIG().yh_token == "":
                print(Common.Colored().red("yeswehack 没有配置token"))
                exit(0)
            else:
                print(Common.Colored().magenta("yeswehack token已配置"))

            handle_list = self.get_yh_handle()
            with concurrent.futures.ThreadPoolExecutor(max_workers=CONFIG().yh_max_thead) as executor:
                executor.map(self.get_yh_handle_url, handle_list)

            self.set_it_xlsx()
            print(Common.Colored().yellow(f"Yeswehack 已处理完成，结果保存至{CONFIG().yh_file_xlsx}"))
        except Exception as e:
            print(Common.Colored().red(e))


def args_port():
    try:
        parser = argparse.ArgumentParser(description='Abroad input')
        parser.add_argument('--it', dest='Intigriti_tf', action='store_true', help='获取Intigriti程序内容')
        parser.add_argument('--h1', dest='Hackerone_tf', action='store_true', help='获取hackeron程序内容')
        parser.add_argument('--bc', dest='Bugcrowd_tf', action='store_true', help='获取bugcrowd程序内容')
        parser.add_argument('--ob', dest='Openbugbounty_tf', action='store_true', help='获取Openbugbounty程序内容')
        parser.add_argument('--im', dest='Immunefi_tf', action='store_true', help='获取immunefi程序内容')
        parser.add_argument('--in', dest='Inspectiv_tf', action='store_true', help='获取Inspectiv程序内容')
        parser.add_argument('--yh', dest='Yeswehack_tf', action='store_true', help='获取Yeswehack程序内容')
        parser.add_argument('--url', dest='Url_tf', action='store_true', help='额外获取url内容')
        parser.add_argument('--app', dest='App_tf', action='store_true', help='额外获取app内容')
        parser.add_argument('--url-op', dest='Urlop_tf', action='store_true', help='选择是否优化url内容')
        args = parser.parse_args()
        return args
    except Exception as e:
        print("args_port bugs: {}".format(e))


def run():
    try:
        e0e1_abroad = Common.Colored().green('''
 -------------------------------------------------------------
|        ___       _             _                         _  |
|   ___ / _ \  ___/ |       __ _| |__  _ __ ___   __ _  __| | |
|  / _ \ | | |/ _ \ |_____ / _` | '_ \| '__/ _ \ / _` |/ _` | |
| |  __/ |_| |  __/ |_____| (_| | |_) | | | (_) | (_| | (_| | |
|  \___|\___/ \___|_|      \__,_|_.__/|_|  \___/ \__,_|\__,_| |
|                  -- by: eeeeee --                           |         
|           -- 该工具仅用于学习参考，均与作者无关 --          |              
 --------------------------------------------------------------
       ''')

        if argss.Intigriti_tf:
            print(e0e1_abroad)
            Intigriti().get_it_programs()

        if argss.Hackerone_tf:
            print(e0e1_abroad)
            Hackerone().get_h1_programs()

        if argss.Bugcrowd_tf:
            print(e0e1_abroad)
            Bugcrowd().get_bc_programs()

        if argss.Openbugbounty_tf:
            print(e0e1_abroad)
            Openbugbounty().get_ob_parms()

        if argss.Immunefi_tf:
            print(e0e1_abroad)
            immunefi().get_im_parms()

        if argss.Inspectiv_tf:
            print(e0e1_abroad)
            inspectiv().get_in_parms()

        if argss.Yeswehack_tf:
            print(e0e1_abroad)
            Yeswehack().get_yh_parms()
    except Exception as e:
        print("__run bugs: {}".format(e))


if __name__ == "__main__":
    global argss
    argss = args_port()
    run()
