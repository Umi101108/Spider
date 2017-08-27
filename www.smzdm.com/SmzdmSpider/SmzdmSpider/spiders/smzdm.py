# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor


# class SmzdmSpider(scrapy.Spider):
class SmzdmSpider(CrawlSpider):
    name = 'smzdm'
    allowed_domains = ['smzdm.com']
    start_urls = ['http://www.smzdm.com/']

    rules = (
        # Rule(LinkExtractor(allow=("fenlei/.*",)), follow=True),
        # Rule(LinkExtractor(allow=("baoliao/.*",)), follow=True),
        Rule(LinkExtractor(allow=r'www.smzdm.com/p/\d+/$'), callback='parse_article', follow=True),
        # Rule(LinkExtractor(allow=r'p/\d+/p\d+/'), callback='parse_comment', follow=True),
    )

    # def parse(self, response):
    #     pass

    # def parse_post(self, response):
    #     # yield self.parse_article(response)
    #     yield scrapy.Request(response.url, callback=self.parse_article, dont_filter=True)

    def parse_article(self, response, follow=True):
        # 获取爆料内容
        print 2333
        article_title = response.css('.article_title > em[itemprop="name"]::text').extract_first("")
        ellipsis_author = response.css('.ellipsis.author > a::text').extract_first("")
        ellipsis_author_id = response.css('.ellipsis.author > a::attr(href)').extract_first("")
        # update_time = response.css('.article_meta > span::text').extract()[-1]
        price = response.css('em[itemprop="price"]::text').extract_first("")
        price_currency = response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first("")
        buy_url = response.css('.buy a::attr(href)').extract_first("")
        content = response.css('.item-preferential').extract_first("")

        fav_num = response.css('div.leftLayer > a.fav em::text').extract_first("")
        comment_num = response.css('div.leftLayer > a.comment em::text').extract_first("")

        rating_all_num = response.css('#rating_all_num em::text').extract_first("")
        rating_worthy_num = response.css('#rating_worthy_num::text').extract_first("")
        rating_unworthy_num = response.css('#rating_unworthy_num::text').extract_first("")

        tags = response.css('span.tags div::text').extract()
        tags = [tag.strip() for tag in tags if tag.strip()]
        tags = ','.join(tags)
        print article_title, ellipsis_author, price, fav_num, comment_num
        # self.getTag(response)
        if response.css('.comment_wrap'):
            try:
                pageno = response.xpath('//div[@class="comment_wrap"]/div[@class="tab_info"]/ul[@class="pagination"]/li[not(@class)]/a/text()')[-2].extract()
                print pageno
            except:
                pageno = 1

            self.parse_comment(response)

            for p in xrange(2, int(pageno)+1):
                comment_url = response.url + 'p{}/'.format(str(p))
                print comment_url
                # self.parse_comment(response)
                yield Request(url=comment_url, dont_filter=True, callback=self.parse_comment)
                yield Request(url=comment_url, dont_filter=True, callback=self.parse_article)
        else:
            print "暂无评论"


    def parse_comment(self, response, follow=True):
        comments = response.css("div#commentTabBlockNew ul.comment_listBox li.comment_list")
        for comment in comments:
            grey = comment.css('span::text').extract_first("")
            usmzdmid = comment.css('a.a_underline::attr(usmzdmid)').extract_first("")
            author = comment.css('span[itemprop="author"]::text').extract_first("")
            rank = comment.css('div.rank::attr(title)').extract_first("")
            comment_con = comment.css('div.comment_conWrap')[-1].css('div.comment_con span::text').extract_first("")
            dingnum = comment.css('div.comment_action a.dingNum span::text').extract_first("")
            cainum = comment.css('div.comment_action a.caiNum span::text').extract_first("")

            print grey, usmzdmid, author, rank, dingnum, cainum, comment_con

    def getTag(self, response):
        tags = response.css('.meta-tags')
        for tag in tags:
            tag_url = tag.css('a::attr(href)').extract_first("")
            tag_detail = tag.css('a::text').extract_first("")
            tag_sort = tag.css('div div::text').extract_first("").split(u'：')[0] if tag.css('div div') else "暂无分类"
            print tag_sort, tag_detail, tag_url
