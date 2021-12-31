from threading import Thread  # 继承Thread方法，重写run方法


class Spider(Thread):

    def __init__(self, url, target) -> "初始化变量":
        super().__init__(target=target, daemon=True)  # daemon线程等待，target是运行的函数
        self.target = target

        # # 实例化redis数据库
        # import redis
        # self.redis = redis.Redis()

        # 构建ip池
        self.file = open("../content/ip.txt")  # 得到大量ip地址
        self.ipList = self.file.readlines()
        self.file.close()
        from random import choice
        self.ip = choice(self.ipList).strip()

        # # 实例化mongo数据库
        # import pymongo
        # self.mongo = pymongo.MongoClient()
        # self.clo = self.mongo["python"]["default"]  # 还要说明MongoDB使用的表名

        # 传入requests所需要的参数
        self.headers = {
            'User-Agent': "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 96.0.4664 .93 Safari / 537.36"  # UA伪装
        }
        self.url = url
        self.proxy = {
            "http": f"http://{self.ip}"  # 代理IP
        }
        self.cookies = None

    def crawl(self) -> "发送请求":
        """发送请求"""
        import requests
        try:  # 反止有人不知道设置代理ip
            if self.cookies:
                resp = requests.get(url=self.url, headers=self.headers, proxies=self.proxy, cookies=self.cookies)
            else:
                resp = requests.get(url=self.url, headers=self.headers, proxies=self.proxy)
        except Exception as e:
            print(e)
            if self.cookies:
                resp = requests.get(url=self.url, headers=self.headers, cookies=self.cookies)
            else:
                resp = requests.get(url=self.url, headers=self.headers)
        if resp.status_code == 200:
            resp.encoding = "utf-8"
            return resp
        else:
            print("Requests Error")

    # def spider(self) -> "业务处理":
    #     """业务处理"""
    #     pass
    #
    # def save(self, data=None, name=None, mode="file") -> "持久化存储":
    #     """持久化存储"""
    #     pass
    #     if mode == "mongo":  # 当选择mongo时，保存在mongo数据库中
    #         if isinstance(data, dict):
    #             self.clo.insert_one(data)
    #         else:
    #             print("Store Error")
    #     elif mode == "file":  # 保存在文件中
    #         with open(f"{self.path}", "a+", encoding="utf-8") as file:
    #             file.write(data)
    #     elif mode == "img" and name:  # 保存为图片
    #         with open(f"./{name}", "wb") as f:
    #             f.write(data)
    #     else:
    #         raise 'FileTypeError.The way can only file or mongo'
    #
    # def parse(self) -> "数据分析":
    #     """数据分析"""
    #     pass
    #
    # def run(self) -> "运行程序":
    #     """运行程序"""
    #     from loguru import logger
    #     logger.info("开始运行爬虫程序")
    #     self.spider()
