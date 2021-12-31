from spiderModule import Spider
from lxml import etree
import re, os
from loguru import logger


class SpiderEveryUrl(Spider):

    def __init__(self, url):
        """初始化变量"""
        Spider.__init__(self, url, target=self.run)
        self.urlAdd = "https://www.umei.cc/meinvtupian/"

    def spider(self):
        """处理业务"""
        html = etree.HTML(super().crawl().text)
        pageUrlList = html.xpath("/html/body/div[2]/div[8]/ul/li/a/@href")
        for i in pageUrlList:
            pageUrl = f"{self.urlAdd}{i.split('/meinvtupian/')[1]}"
            urListAll.append(pageUrl)

    def run(self):
        """启动程序"""
        self.spider()


class SpiderPicUrl(Spider):

    def __init__(self, url):
        Spider.__init__(self, url, target=self.run)
        self.add = "https://www.umei.cc"

    def spider(self):
        """处理业务"""
        html = etree.HTML(Spider.crawl(self).text)
        nuUrl = html.xpath("/html/body/div[2]/div[12]/a/@href")  
        try:
            if nuUrl:
                nuUrl = nuUrl[-1]
                maxIndex, headersNum, headersAlph = re.search(obj1, nuUrl).group().split("_")[1], re.search(obj2, nuUrl).group(), re.search(obj3, nuUrl).group()
                for i in range(1, int(maxIndex) + 1):
                    if i == 1:
                        eveUrl = f"{self.add}{headersAlph}{headersNum.split('_')[0]}.htm"
                    else:
                        eveUrl = f"{self.add}{headersAlph}{headersNum}{str(i)}.htm"
                    preUrl.append(eveUrl)
            else:
                unRun.append(self.url)
        except Exception as e:
            print(e)

    def run(self):
        """运行程序"""
        self.spider()


class SpiderPicSrc(Spider):

    def __init__(self, url):
        """初始化变量"""
        Spider.__init__(self, url, target=self.run)

    def spider(self):
        """处理业务"""
        html = etree.HTML(super(SpiderPicSrc, self).crawl().text)  # 调用模块中封装的方法
        src = html.xpath("//*[@id='ArticleId{dede:field.reid/}']/p/a/img/@src")
        file = open("../content/picSrc.txt", "a+")
        file.write(f"{src[0]}\n")
        file.close()
        # try:
        #     if src:
        #         if self.redis.sadd("src", src[0]):  # 使用redis去重
        #             print(f"正在保存图片src：{src[0]}")
        #             self.file.write(f"{src[0]}\n")
        #         else:
        #             logger.info(f'{src[0]}已保存')
        # except Exception as e:
        #     with open("./log.log", 'a+') as file:
        #         file.write(f"{e}\n{src}")
        #     print(e)

    def run(self):
        """运行程序"""
        self.spider()


"""线程的使用方法"""
# def Many_Thread(target, *args) -> "示范""其为使用的方式":
#     th = []
#     for i in range(25):  # 开25个线程
#         t = threading.Thread(target=target, args=args)
#         th.append(t)
#         t.setDaemon(True)  # 添加守护线程，即防止进程进度与线程进度不一样
#     for i in th:  # 循环启动25个线程
#         i.start()
#     for i in th:
#         i.join()  # 阻塞线程


if __name__ == '__main__':
    while True:
        start, end = input("请输入要下载该网站的哪部分图片如（1 3）表示下载1到3页的图片，最多有540页：").split()
        try:
            if isinstance(eval(start), int) and isinstance(eval(end), int) and int(start) <= int(end):
                print("s")
                break
            else:
                continue
        except Exception as e:
            print(e)
            print("请按要求输入！！！")
    print("hello")
    urListAll, threads, preUrl, unRun = [], [], [], []
    obj1, obj2, obj3 = re.compile(r"_\d+"), re.compile(r"\d+_"), re.compile(r"\D+")  # 在这里创建正则表达式，减少缓存的占用
    for i in range(int(start), int(end)+1):
        if i == 1:
            url = "https://www.umei.cc/meinvtupian/"
        else:
            url = f"https://www.umei.cc/meinvtupian/index_{i}.htm"
        logger.info(f"{url}")
        th = SpiderEveryUrl(url)
        threads.append(th)
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    with open("../content/EveryUrl.txt", "w") as f:  # 将提取到的url保存到EveryUrl中，防止因为意外原因，使得数据丢失
        f.write(str(urListAll))
    print(f"urListAll提取完成")
    threads.clear()

    f = open("../content/EveryUrl.txt", "r")  # 提取文件中的url
    urList = eval(f.read())
    f.close()
    for url in urListAll:
        logger.info(url)
        th = SpiderPicUrl(url)
        threads.append(th)
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    with open("../content/PicUrl.txt", "w") as f:  # 将提取到的url保存到EveryUrl中，防止因为意外原因，使得数据丢失
        f.write(str(preUrl))
    print(f"preUrl提取完成\n错误的有：{unRun}" if not unRun else "preUrl提取完成")  # 三目运算
    threads.clear()

    f = open("../content/PicUrl.txt", "r")  # 提取文件中的url
    urList = eval(f.read())
    f.close()
    for url in preUrl:
        logger.info(f"{url}_src")
        th = SpiderPicSrc(url)
        threads.append(th)
    for i in threads:
        i.start()
    for i in threads:
        i.join()

    print("all over")

