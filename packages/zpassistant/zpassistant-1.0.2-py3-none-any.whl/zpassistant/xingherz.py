# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from zpassistant import SsoLoginUtil
import argparse
import json

class Xingherz():
    def __init__(self) -> None:
        self.session = SsoLoginUtil("https://zpsso.zhaopin.com/login").ssologinByBrowser( "https://xinghe.zhaopin.com/user/info",self.checkSsoLogin,type="xinghe")

    def checkSsoLogin(self,browser):
        if browser.title == '我的信息':
            print("login success ,closing browser")
            return True
        return False
    def listUploadFiles(self,page = 1,size = 20):
        # 查询已上传的文件列表
        print("fileId\t\t\t\t\t\tfileName")
        print("------------------------------------------------------------")
        response =  self.session.get("https://xinghe.zhaopin.com/user/folder".format(page,size))
        if response.status_code == 200:
            result = response.text
            # 得到的是html,解析其中的scipt,获取名叫DATA的字段
            result = result.split("DATA = ")[1].split(";\n")[0]
            # 读取并机械fileName
            result = json.loads(response.text)
            if "items" in json:
                for item in result["items"]:
                    print(item["id"],"\t\t\t\t\t\t",item["filename"])
        return None
    def uploadFile(self,filePath):
        url = 'https://xinghe.zhaopin.com/user/upload/file'
        data = {
            'pid': '0',
            'secret_type': '',
            'secret_size': '0',
            'secret_code': '0',
            'remark': '',
        }
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Origin': 'https://xinghe.zhaopin.com',
            'Referer': 'https://xinghe.zhaopin.com/user/folder',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.17',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        # 读取文件名
        fileName = os.path.basename(filePath)
        files = {'file': (fileName, open(filePath, 'rb'))}
        response = self.session.post(url, headers=headers, data=data, files=files)
        if response.status_code == 200:
            try:
                result = json.loads(response.text)
                if str(result["code"]) == "200":
                    # 打印绿色
                    print("\033[32m upload file success,fileId: "+ str(result["data"]["id"]) + " ,fileName: " + str(result["data"]["filename"]))
                else:
                    # 打印红色
                    print("\033[31m upload file failed : " + response.text)
            except Exception as e:
                print("\033[31m upload file failed " + response.text + ",exception: "+ str(e))

    def downloadFile(self,fileName):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Referer": "https://xinghe.zhaopin.com/user/folder/{}".format(fileName),
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.17",
            "sec-ch-ua": '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows"
        }
        url = "https://xinghe.zhaopin.com/user/folder/{}?action=download".format(fileName)
        # 下载文件
        response = self.session.get(url,headers=headers)
        if response.status_code == 200:
            print("\033[35m download file success,fileName: " + fileName)
            # 写入文件
            with open(fileName, 'wb') as f:
                f.write(response.content)

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description='''
example
    xingherz --delete \$(xingherz -ls) # delete 20 uploaded files
    xingherz tmp.json  # upload file
    xingherz -d "16af6563-a022-4c4f-89a4-88efd3ce7adb" -n fileName # download file by id
                                       
    ''', add_help=True, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--file', type=str, help="upload file path")
    parser.add_argument('-d', '--download', type=str, help="download file name")
    parser.add_argument('-n', '--name', type=str, help="download file name")
    parser.add_argument('-l', '--list', nargs='*', type=int, help="list uploaded files")
    args = parser.parse_args(["-d",'PyPI-Recovery-Codes-mzt12450-2023-09-13T11_13_11.642644.txt'])
    if args.list is not None:
        # 如果参数长度<2则忽略
        if len(args.list) < 2:
            args.list = [1, 20]
        Xingherz().listUploadFiles(args.list[0], args.list[1])
    
    if args.file is not None:
        Xingherz().uploadFile(args.file)
    
    if args.download is not None:
        Xingherz().downloadFile(args.download)
    
    
    
