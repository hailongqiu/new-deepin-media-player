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
    if data.find("最新资讯") != -1: # 防止出现最新资讯，最新...的垃圾信息.
        data = data.decode("utf-8")
        data = data[55000:]
    elif data.find("热门作品") != -1:
        data = data.decode("utf-8")
        data = data[40000:]
    sounp = BeautifulSoup(data)

    # 获取图片.
    image_list = []
    for image in sounp.findAll("img"):
        if image.get("onerror"):
            image_addr = image.get("src")
            image_list.append(image_addr)
    length_list = []
    # 获取播放长度.
    for length in sounp.findAll("span", {"class":"num"}):
        length_str = length.string
        if length_str:
            if length_str.find(":") != -1:
                length_list.append(length_str)
                #print length_str
    temp_dict = {} # 过于过滤多于的地址.
    save_info_list = []
    index = 0
    for link in sounp.findAll('a'):
        title = link.get('title')
        if title and link.get("_log_vid"):
            addr = link.get("href")
            if not temp_dict.has_key(addr):
                # 过滤带有这些字眼的垃圾信息.
                if (addr.startswith("/search") or 
                    addr.startswith("/detail") or
                    not addr.startswith("http://v.youku.com/") or
                    addr.find("?s=") != -1
                    ):
                    continue;
                image_addr      = image_list[index]
                length          = length_list[index]
                '''
                print "---------------------------"
                print "标题是:",   title
                print "播放地址:", addr
                print "图片地址:", image_addr
                print "播放长度:", length
                '''
                info = (title, addr, image_addr, length)
                temp_dict[addr] = info
                save_info_list.append(info)
                index += 1
    
    # 获取视频一页的总数.
    page_num = len(temp_dict)
    sum      = 0
    if page_index == 1:
        # 获取视频的总数.
        sum_str = sounp.findAll('div', {'class':'stat'})[0].string
        sum = int(sum_str.replace("\n", "").strip().split(" ")[1])
        '''
        print "length num:", len(length_list)
        print "image num:", len(image_list)
        print "page_num:", page_num
        print "sum:", sum
        '''
    return save_info_list, page_num, sum




if __name__ == "__main__":
    import sys
    from youku_to_flvcd import YouToFlvcd
    scan_info = scan_page(1, sys.argv[1])
    info_list = scan_info[0]
    page_num  = scan_info[1]
    sum       = scan_info[2]
    flvcd     = YouToFlvcd()
    for info in info_list: 
        print "----------------------"
        print "标题:",     info[0]
        print "播放地址:", info[1]
        print "图片地址:", info[2]
        print "播放长度:", info[3]
        print "----------------------"
        flvcd.parse(info[1])

    print "sum:", sum
    print "总页数:", sum/page_num




