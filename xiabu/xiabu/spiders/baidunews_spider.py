import scrapy
from w3lib.html import remove_tags
from xiabu.items import BaiduNewsItem
import datetime

class BaiduNewsSpider(scrapy.Spider):
    name = "BaiduNews"
    print("Running...")
    # wd(Keyword) 关键词
    keyword = ["呷哺", "茶米茶"]
    # rtt = 1 是按照焦点排序，rtt = 4 是按照时间排序
    # pn(Page Number) 为页码 pn = [0,10,20,30,40,50,...]
    # rn(Record Number)：搜索结果显示条数，缺省设置rn=10，取值范围:10-100
    # cl(Class)：搜索类型，cl=3为网页搜索，cl=2为百度消息
    # ct 语言限定 0-所有语言，1-简体中文网页，2-繁体中文网页;其它不确定或者无效或。默认值为0.
    # ie(Input Encoding)：查询关键词的编码，缺省设置为简体中文
    # start_urls = [
    #     'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=4&bsst=1&rsv_dl=news_b_pn&cl=2&wd=' + wd + '&tn=news&rsv_bp=1&oq=&rsv_btype=t&f=8&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&pn=0',
    # ]
    start_urls = ['https://www.baidu.com']
    AllUrl = []
    for i in range(len(keyword)):
        con_url = 'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=4&bsst=1&rsv_dl=news_b_pn&cl=2&wd=' + keyword[i] + '&tn=news&rsv_bp=1&oq=&rsv_btype=t&f=8&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&pn=0'
        AllUrl.append(con_url)
    num = len(AllUrl)
    print("本次要爬的初始网站URL有%d条：\n" % num)
    print(AllUrl)

    def parse(self, response):
        print("进入parse函数")
        for i in range(len(self.AllUrl)):
            print("总计要爬%d个关键词，现在要爬的第%d个关键词" % (self.num, i+1))
            yield scrapy.Request(self.AllUrl[i], callback=self.spideron)

    def spideron(self, response):
        news = BaiduNewsItem()
        for id in response.css('div.result-op.c-container.xpath-log.new-pmd::attr(id)').getall():
            #itemid 解决爬取时元素为空的情况，实现爬完一个新闻所有需要元素，再爬下一个
            itemid = '//*[@id="' + str(id) + '"]'
            news['key_word'] = response.xpath('//*[@id="kw"]/@value').get()
            news['create_time'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            news['title'] = remove_tags(response.xpath(itemid).css('h3.news-title_1YtI1').get(default=None))
            news['source'] = response.xpath(itemid).css('div.news-source span.c-color-gray.c-font-normal.c-gap-right::text').get(default=None)
            news['time'] = response.xpath(itemid).css('div.news-source span.c-color-gray2.c-font-normal::text').get(default=None)
            news['url'] = response.xpath(itemid).css('h3.news-title_1YtI1 a::attr(href)').get(default=None)
            news['content'] = remove_tags(response.xpath(itemid).css('span.c-font-normal.c-color-text').get(default=None))
            yield news

        # 判断是否有下一页连接,有则递归解析下一页 2021-05-12 steve
        a = response.css('div.page-inner a.n::text').getall()
        b = response.css('div.page-inner a.n::attr(href)').getall()
        c = dict(zip(a, b))
        if '下一页 >' in c:
            next_page = response.urljoin(c['下一页 >'])
            yield scrapy.Request(next_page, callback=self.spideron)
        else:
            print("已无下一页")