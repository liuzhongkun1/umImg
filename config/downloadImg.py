from spiderModule import Spider
from loguru import logger
import os, sys
from threading import BoundedSemaphore


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
        with pool_sema:  # 使用这个方法，限制线程数
            self.spider()


if __name__ == '__main__':
    max_connections = 100  # 定义最大线程数
    pool_sema = BoundedSemaphore(max_connections) # 或使用Semaphore方法，在主函数中使用with pool_sema可以限制线程的数量
    if not os.path.exists("../img"):
        os.mkdir("../img")
    threads = []
    with open("../content/PicSrc.txt", "r") as file:
        urls = file.readlines()
    for url in urls:
        th = SpiderDown(url.strip())
        threads.append(th)
        th.setDaemon(False)
    for i in threads:
        i.start()
    
    os.remove("../content/PicSrc.txt")



























