import json
import time

import csv
import os

import requests
from lxml import etree as ET
from selenium import webdriver


class Contents:
    def __init__(self, userName, homeUrl, text, imgUrl, address, time):
        self.userName = userName
        self.homeUrl = homeUrl
        self.text = text
        self.imgUrl = imgUrl
        self.address = address
        self.time = time


def getPostingUrls(url, firstPage, lastPage):
    url = url[:url.find("pn=")]
    postingUrlLists = []
    for page in range(firstPage, lastPage + 1):
        url = url + "pn=" + str(page * 50)
        response = requests.get(url).text
        content = ET.HTML(response)
        postingUrlList = content.xpath(
            '//ul[@id="thread_list"]//div[contains(@class,"threadlist_title pull_left j_th_tit")]//a[@rel="noopener"]/@href')
        for i in range(len(postingUrlList)):
            postingUrlList[i] = "https://tieba.baidu.com" + postingUrlList[i]
        postingUrlLists.append(postingUrlList)

    return postingUrlLists


def writeCSV(filename, userNames, userUrls, contentList, imgUrlList, userAddress, contentTimes):
    newUserContents = []
    for i in range(len(userUrls)):
        userUrls[i] = "https://tieba.baidu.com" + userUrls[i]
    for i in range(len(contentList)):
        contentList[i] = contentList[i].lstrip()
        if contentList[i] != "":
            newUserContents.append(contentList[i])
    data = zip(userNames, userUrls, contentList, imgUrlList, userAddress, contentTimes)

    with open(filename, 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        if os.path.getsize(filename) == 0:
            writer.writerow(['Name', 'URL', 'Content', 'imgUrlList', 'Address', 'Time'])  # 写入标题行

        writer.writerows(data)  # 写入数据行


def getPostingReplys(url):
    chrome = webdriver.Chrome()
    chrome.get(url)
    html = chrome.page_source
    print(html)
    chrome.quit()


def getPostingInfo(postingUrlLists):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    for postingUrlList in postingUrlLists:
        for postingUrl in postingUrlList:
            response = requests.get(postingUrl, headers=headers).text
            content = ET.HTML(response)
            pageNum = content.xpath(
                '//li[@class="l_pager pager_theme_5 pb_list_pager"]//a[contains(text(),"尾页")]/@href')
            pageNum = pageNum[0][-1:]
            filename = postingUrl[postingUrl.find("/p/") + 3:]
            folder_path = "csv/" + filename
            os.makedirs(folder_path, exist_ok=True)
            filename = folder_path + "/contents.csv"
            for page in range(1):
                # for page in range(int(pageNum)):
                page += 1
                newPostingUrl = postingUrl + "?pn=" + str(page)
                response = requests.get(newPostingUrl, headers=headers).text
                content = ET.HTML(response)
                # userNames = content.xpath(
                #     '//div[@class="l_post l_post_bright j_l_post clearfix  "]//div[@class="d_author"]//ul[@class="p_author"]/li[@class="d_name"]/a/text()')
                # userUrls = content.xpath(
                #     '//div[@class="l_post l_post_bright j_l_post clearfix  "]//div[@class="d_author"]//ul[@class="p_author"]/li[@class="d_name"]/a/@href')
                # contentList = []
                # imgUrlList = []
                # userAddress = content.xpath(
                #     '//div[@class="l_post l_post_bright j_l_post clearfix  "]//div[contains(@class,"d_post_content_main")]/div[@class="core_reply j_lzl_wrapper"]//div[@class="post-tail-wrap"]/span[contains(text(),"IP")]/text()')
                # contentTimes = content.xpath(
                #     '//div[@class="l_post l_post_bright j_l_post clearfix  "]//div[contains(@class,"d_post_content_main")]/div[@class="core_reply j_lzl_wrapper"]//div[@class="post-tail-wrap"]/span[contains(text(),"-")]/text()')
                # userContents = content.xpath(
                #     '//div[@class="d_post_content j_d_post_content "]')
                # for root in userContents:
                #     imgs = root.findall("img")
                #     if imgs != None:
                #         imgList = []
                #         for img in imgs:
                #             imgList.append(img.get("src"))
                #         imgUrlList.append(imgList)
                #     else:
                #         imgUrlList.append("")
                #     contentList.append(root.text)

                # writeCSV(filename, userNames, userUrls, contentList, imgUrlList, userAddress, contentTimes)

            # time.sleep(3)
            # replys = getPostingReplys(url)

            # replyUserNames=
            # replyUrls
            # replyContents
            # replyTimes
            # for i in range(len(userContents)):
            #     print(userNames[i]+"\t"+"https://tieba.baidu.com"+userUrls[i]+"\t"+userContents[i]+"\t"+userAddress[i]+"\t"+str(contentTimes[i]))


def teibaSpider(url):
    # postingUrlLists=getPostingUrls(url,0,0)
    postingUrlLists = [["https://tieba.baidu.com/p/8739749136"]]
    getPostingInfo(postingUrlLists)


if __name__ == '__main__':
    # 某个吧的url(如足球吧)
    # url = 'https://tieba.baidu.com/f?kw=%E8%B6%B3%E7%90%83&ie=utf-8&pn=0'
    #
    # teibaSpider(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    url1="https://tieba.baidu.com/p/totalComment?tid=8739749136"
    contents = requests.get(url1, headers=headers).text
    json_obj = json.loads(contents)
    json_obj=json_obj['data']['comment_list']
    json_form = json.dumps(json_obj, indent=4)
    # print(json_form)
    for comment_id,comment_info in json_obj.items():
        comment_info_list = comment_info['comment_info']
        for comment in comment_info_list:
            # 获取评论的content值
            content = comment['content']
            print(content)


