import scrapy
from w3lib.html import remove_tags

class BaiduNewsSpider(scrapy.Spider):
    name = "BaiduNews"
    # wd(Keyword) 关键词
    wd = "呷哺"
    # rtt = 1 是按照焦点排序，rtt = 4 是按照时间排序
    # rtt = (1,4)
    # pn(Page Number) 为页码
    # pn = [0,10,20,30,40,50,60]
    # rn(Record Number)：搜索结果显示条数，缺省设置rn=10，取值范围:10-100
    # cl(Class)：搜索类型，cl=3为网页搜索，cl=2为百度消息
    # ct 语言限定 0-所有语言，1-简体中文网页，2-繁体中文网页;其它不确定或者无效或。默认值为0.
    # ie(Input Encoding)：查询关键词的编码，缺省设置为简体中文
    start_urls = [
        'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=4&bsst=1&rsv_dl=news_b_pn&cl=2&wd=' + wd + '&tn=news&rsv_bp=1&oq=&rsv_btype=t&f=8&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&pn=0',
    ]

    def parse(self, response):
        for i in range(len(response.css('h3.news-title_1YtI1').getall())):
            yield {
                "title": remove_tags(response.css('h3.news-title_1YtI1').getall()[i]),
                "Source": response.css('div.news-source span.c-color-gray.c-font-normal.c-gap-right::text').getall()[i],
                "Time": response.css('div.news-source span.c-color-gray2.c-font-normal::text').getall()[i],
                "Url": response.css('h3.news-title_1YtI1 a::attr(href)').getall()[i],
                "CONT": remove_tags(response.css('span.c-font-normal.c-color-text').getall()[i]),
            }

        next_page = response.css('div.page-inner a.n::attr(href)').getall()[len(response.css('div.page-inner a.n::attr(href)').getall())-1]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)