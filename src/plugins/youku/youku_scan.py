#!/usr/bin/env python
#!coding:utf-8


from BeautifulSoup import BeautifulSoup
import urllib2
import urllib

def keyword_to_gb2312(keyword):
    #key = keyword.decode("utf-8").encode("gb2312")
    key = keyword
    return urllib.quote(key)

def scan_page(page_index=1, keyword="linuxdeepin"):
    url_base = "http://www.soku.com/search_video/q_%s_orderby_1_page_%s"
    url = url_base % (keyword_to_gb2312(keyword), page_index)
    print url
    data = urllib2.urlopen(url).read()
    sounp = BeautifulSoup(data)
    '''
    print sounp.title
    print sounp.name
    print sounp.string
    print sounp.title.parent.name
    print sounp.a
    print sounp.a['href']
    print "sum:", sounp.findAll('div', {'class':'stat'})
    '''
    for link in sounp.findAll('a'):
        title = link.get('title')
        if title:
            print "---------------------------"
            print "标题是:", title
            print "播放地址:", link.get("href")
            print "---------------------------"



if __name__ == "__main__":
    for i in range(1, 2) :
        scan_page(i, "编译原理")
