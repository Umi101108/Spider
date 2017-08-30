# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor
from scrapy.loader import ItemLoader
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from SmzdmSpider.items import SmzdmspiderItemLoader, SmzdmArticleItem, ArticleTagItem, CommentItem


class SmzdmSpider(CrawlSpider):
    name = 'smzdm'
    allowed_domains = ['smzdm.com']
    start_urls = ['http://www.smzdm.com/']

    rules = (
        # Rule(LinkExtractor(allow=("fenlei/.*",)), follow=True),
        # Rule(LinkExtractor(allow=("baoliao/.*",)), follow=True),
        Rule(LinkExtractor(allow=r'www.smzdm.com/p/\d+/$'), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow=r'www.smzdm.com/p/\d+/p\d+/'), callback='parse_comment', follow=True),
    )



    def parse_article(self, response, follow=True):
        # 获取爆料内容
        match_obj = re.match(".*?www.smzdm.com/p/(\d+)/.*?", response.url)
        if match_obj:
            article_id = int(match_obj.group(1))
        # article_title = response.css('.article_title > em[itemprop="name"]::text').extract_first("")
        # ellipsis_author = response.css('.ellipsis.author > a::text').extract_first("商家自荐")
        # ellipsis_author_id = response.css('.ellipsis.author > a::attr(href)').extract_first("商家自荐")
        # update_time = response.css('.article_meta > span::text').extract()[-1]
        # price = response.css('em[itemprop="price"]::text').extract_first("")
        # price_currency = response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first("")
        # buy_url = response.css('.buy a::attr(href)').extract_first("")
        # content = response.css('.item-preferential').extract_first("")
        #
        # fav_num = response.css('div.leftLayer > a.fav em::text').extract_first("")
        # comment_num = response.css('div.leftLayer > a.comment em::text').extract_first("")
        #
        # rating_all_num = response.css('#rating_all_num em::text').extract_first("")
        # rating_worthy_num = response.css('#rating_worthy_num::text').extract_first("")
        # rating_unworthy_num = response.css('#rating_unworthy_num::text').extract_first("")

        item_loader = SmzdmspiderItemLoader(item=SmzdmArticleItem(), response=response)
        item_loader.add_value("article_id", article_id)
        item_loader.add_css("article_title", '.article_title > em[itemprop="name"]::text')
        item_loader.add_value("article_url", response.url)
        # item_loader.get_css('span[class="ellipsis author"] > a::text', 'ellipsis_author', '')
        ellipsis_author = response.css('span[class="ellipsis author"] > a::text').extract_first("商家自荐")
        ellipsis_author_id = response.css('.ellipsis.author > a::attr(href)').extract_first("商家自荐")
        item_loader.add_value("ellipsis_author", ellipsis_author)
        item_loader.add_value("ellipsis_author_id", ellipsis_author_id)
        item_loader.add_css("update_time", '.article_meta > span:last-child::text')
        price = response.css('em[itemprop="price"]::text').extract_first("0")
        item_loader.add_value("price", price)
        item_loader.add_css("price_currency", 'meta[itemprop="priceCurrency"]::attr(content)')
        item_loader.add_css("price_detail", 'em[itemprop="offers"] span.red::text')
        item_loader.add_css("buy_url", '.buy a::attr(href)')
        item_loader.add_css("content", '.item-preferential')
        item_loader.add_css("fav_num", 'div.leftLayer > a.fav em::text')
        item_loader.add_css("comment_num", 'div.leftLayer > a.comment em::text')
        item_loader.add_css("rating_all_num", '#rating_all_num em::text')
        item_loader.add_css("rating_worthy_num", '#rating_worthy_num::text')
        item_loader.add_css("rating_unworthy_num", '#rating_unworthy_num::text')

        article_item = item_loader.load_item()
        # article_item = SmzdmArticleItem()
        # article_item["article_id"] = article_id
        # article_item["article_url"] = response.url
        # article_item["article_title"] = article_title
        # article_item["ellipsis_author"] = ellipsis_author
        # article_item["ellipsis_author_id"] = ellipsis_author_id
        # article_item["update_time"] = update_time
        # article_item["price"] = price
        # article_item["price_currency"] = price_currency
        # article_item["buy_url"] = buy_url
        # article_item["content"] = content
        # article_item["fav_num"] = fav_num
        # article_item["comment_num"] = comment_num
        # article_item["rating_all_num"] = rating_all_num
        # article_item["rating_worthy_num"] = rating_worthy_num
        # article_item["rating_unworthy_num"] = rating_unworthy_num
        yield article_item

        # tags = response.css('span.tags div::text').extract()
        # tags = [tag.strip() for tag in tags if tag.strip()]
        # tags = ','.join(tags)

        tags = response.css('.meta-tags')
        for tag in tags:
            tag_item = ArticleTagItem()
            tag_url = tag.css('a::attr(href)').extract_first("")
            tag_detail = tag.css('a::text').extract_first("")
            tag_sort = tag.css('div div::text').extract_first("").split(u'：')[0] if tag.css('div div') else "暂无分类"
            print tag_sort, tag_detail, tag_url

            tag_item["article_id"] = article_id
            tag_item["article_url"] = response.url
            tag_item["tag_sort"] = tag_sort
            tag_item["tag_detail"] = tag_detail
            yield tag_item

        if response.css('.comment_wrap'):
            try:
                pageno = response.xpath('//div[@class="comment_wrap"]/div[@class="tab_info"]/ul[@class="pagination"]/li[not(@class)]/a/text()')[-2].extract()
            except:
                pageno = 1

            # self.parse_comment(response)
            comments = response.css("div#commentTabBlockNew ul.comment_listBox li.comment_list")
            for comment in comments:
                grey = comment.css('span::text').extract_first("")
                usmzdmid = comment.css('a.a_underline::attr(usmzdmid)').extract_first("")
                author = comment.css('span[itemprop="author"]::text').extract_first("")
                rank = comment.css('div.rank::attr(title)').extract_first("")
                comment_con = comment.css('div.comment_conWrap')[-1].css('div.comment_con span::text').extract_first("")
                dingnum = comment.css('div.comment_action a.dingNum span::text').extract_first("")
                cainum = comment.css('div.comment_action a.caiNum span::text').extract_first("")

                # print grey, usmzdmid, author, rank, dingnum, cainum, comment_con
                item_loader = SmzdmspiderItemLoader(item=CommentItem(), response=response)
                item_loader.add_value("article_id", article_id)
                item_loader.add_value("article_url", response.url)
                item_loader.add_value("grey", grey)
                item_loader.add_value("usmzdmid", usmzdmid)
                item_loader.add_value("author", author)
                item_loader.add_value("rank", rank)
                item_loader.add_value("comment_con", comment_con)
                item_loader.add_value("dingnum", dingnum)
                item_loader.add_value("cainum", cainum)

                comment_item = item_loader.load_item()
                yield comment_item

            for p in xrange(2, int(pageno)+1):
                comment_url = response.url + 'p{}/'.format(str(p))
                print comment_url
                yield Request(url=comment_url, dont_filter=True, callback=self.parse_comment, meta={"article_id": article_id})
        else:
            print "暂无评论"

    def getTag(self, response, article_id):
        print 2333
        tags = response.css('.meta-tags')
        for tag in tags:
            tag_item = ArticleTagItem()
            tag_url = tag.css('a::attr(href)').extract_first("")
            tag_detail = tag.css('a::text').extract_first("")
            tag_sort = tag.css('div div::text').extract_first("").split(u'：')[0] if tag.css('div div') else "暂无分类"
            print tag_sort, tag_detail, tag_url

            tag_item["article_id"] = article_id
            tag_item["article_url"] = response.url
            tag_item["tag_sort"] = tag_sort
            tag_item["tag_detail"] = tag_detail
            yield tag_item

    def parse_comment(self, response, follow=True):
        # print 233
        comments = response.css("div#commentTabBlockNew ul.comment_listBox li.comment_list")
        match_obj = re.match(".*?www.smzdm.com/p/(\d+)/.*?", response.url)
        if match_obj:
            article_id = int(match_obj.group(1))
        for comment in comments:
            grey = comment.css('span::text').extract_first("")
            usmzdmid = comment.css('a.a_underline::attr(usmzdmid)').extract_first("")
            author = comment.css('span[itemprop="author"]::text').extract_first("")
            rank = comment.css('div.rank::attr(title)').extract_first("")
            comment_con = comment.css('div.comment_conWrap')[-1].css('div.comment_con span::text').extract_first("")
            dingnum = comment.css('div.comment_action a.dingNum span::text').extract_first("")
            cainum = comment.css('div.comment_action a.caiNum span::text').extract_first("")

            # print grey, usmzdmid, author, rank, dingnum, cainum, comment_con
            item_loader = SmzdmspiderItemLoader(item=CommentItem(), response=response)
            item_loader.add_value("article_id", article_id)
            item_loader.add_value("article_url", response.url)
            item_loader.add_value("grey", grey)
            item_loader.add_value("usmzdmid", usmzdmid)
            item_loader.add_value("author", author)
            item_loader.add_value("rank", rank)
            item_loader.add_value("comment_con", comment_con)
            item_loader.add_value("dingnum", dingnum)
            item_loader.add_value("cainum", cainum)

            comment_item = item_loader.load_item()
            yield comment_item

