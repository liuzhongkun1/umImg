from spiderModule import Spider
from loguru import logger
import os


class SpiderDown(Spider):

    def __init__(self, url):
        super().__init__(url, target=self.run)

    def spider(self):
        """处理业务"""
        data = Spider.crawl(self).content
        name = self.url.split("/")[-1]
        logger.info(f"正在下载{name}")
        with open(f"../img/{name}", "wb") as f:
            f.write(data)
        # if self.redis.sadd("imgName", name):  # redis去重
        #     logger.info(f"正在下载{name}")
        #     Spider.save(self, data=data, name=name, mode="img")
        # else:
        #     logger.info(f"{name}已经下载")

    def run(self):
        """运行程序"""
        self.spider()


if __name__ == '__main__':
    threads = []
    with open("../content/picSrc.txt", "r") as file:
        urls = file.readlines()
    for url in urls:
        th = SpiderDown(url.strip())
        threads.append(th)
        th.setDaemon(False)
    for i in threads:
        i.start()
    
    os.remove("../content/PicSrc.txt")



























