#!/bin/python
# coding=UTF-8
import urllib2
from BeautifulSoup import *
from urlparse import urljoin
import MySQLdb as mdb
from time import sleep
from scrapy.selector import HtmlXPathSelector
import md5
import threading


# UPDATE `movie`.`douban_url` SET `is_saved` = '0' WHERE `douban_url`.`id` = 1;
# delete from douban_url where id != 1;


class Page:
    id = 0
    url = ''
    url_md5 = ''
    html = ''
    weight = 1
    is_saved = 0
    is_movie = 0
 

def write_sql(sql):
    out_file = open("data.sql", 'a+')
    out_file.write("%s ;\n" %sql)
    out_file.close()

def get_md5(url):
    m = md5.new()
    m.update(url)
    url_md5 = m.hexdigest()
    return url_md5 

def url_is_exist(cur, url):    
    url_md5 = get_md5(url)
    sql = "select id from douban_url where url_md5 = %s"
    cur.execute(sql, (url_md5))
    rows = cur.fetchall()
    if len(rows) > 0:
        #print "url exist: ", url_md5, url
        return True
    else:
        return False

def load_like_url_from_db(cur, like_url):
    sql = "select id, url, weight, is_saved, is_movie from douban_url where is_saved = '0' and url like %s limit 1"
    cur.execute(sql, (like_url + "%"))
    rows = cur.fetchall()
    pages = []
    for row in rows:
        page = Page()
        page.id = row[0]
        page.url = row[1]
        page.weight = row[2]
        page.is_saved = row[3]
        page.is_movie = row[4]
        pages.append(page)

    return pages

def load_url_from_db(cur):
    rs = load_like_url_from_db(cur, "http://movie.douban.com/tag")
    if len(rs) > 0:
        return rs

    rs = load_like_url_from_db(cur, "http://movie.douban.com/subject")
    if len(rs) > 0:
        return rs

    rs = load_like_url_from_db(cur, "http://movie.douban.com/people")
    if len(rs) > 0:
        return rs

    sql = "select id, url, weight, is_saved, is_movie from douban_url where is_saved = '0' limit 1"
    cur.execute(sql)
    rows = cur.fetchall()
    pages = []
    for row in rows:
        page = Page()
        page.id = row[0]
        page.url = row[1]
        page.weight = row[2]
        page.is_saved = row[3]
        page.is_movie = row[4]
        pages.append(page)

    return pages

def update_page_state(conn, cur, page, saved = 0):
    sql = u"update douban_url set is_saved = %s where id = %s "

    cur.execute(sql,  (str(saved), str(page.id)))
    conn.commit()
        
def save_page(conn, cur, page, saved = 1):
    sql = u"update douban_url set html = %s, weight=%s, is_saved = %s, is_movie = %s where id = %s "

    cur.execute(sql,  (page.html, str(page.weight), str(page.is_saved), str(page.is_movie), str(page.id)))
    conn.commit()

def insert_page(conn, cur, page):
    url_md5 = get_md5(page.url)
    if re.search(r'^http://movie.douban.com/subject/(\d+)/$', page.url):
        page.is_movie = 1
    else:
        page.is_movie = 0
    sql = u"insert douban_url(url, url_md5, html, weight, is_saved, is_movie) values(%s, %s, %s, %s, %s, %s )"
    cur.execute(sql, (page.url.decode('utf-8'), url_md5,  page.html.encode('utf-8'), str(page.weight), str(page.is_saved), str(page.is_movie) ))
    conn.commit()

def create_request(url):
    request = urllib2.Request(url)
    request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request.add_header('Accept-Charset', 'GBK,utf-8;q=0.7,*;q=0.3')
    request.add_header('Accept-Language', 'zh-CN,zh;q=0.8')
    request.add_header('Cache-Control', 'max-age=0')
    request.add_header('Connection', 'keep-alive')
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.107 Safari/534.13')
    return request

def crawl(conn, cur, depth=10):
    while(True):
        pages = load_url_from_db(cur)
        if len(pages) <= 0:
            print "get 0 pages, exit"
            break;
        
        for crawl_page in pages:
            update_page_state(conn, cur, crawl_page, 1)
            newurls={}
            page_url = crawl_page.url
            try:
                # c=urllib2.urlopen(page_url)
                print "crawl url: ", page_url
                request = create_request(page_url)
                response = urllib2.urlopen(request,  timeout=30)

            except:
                continue     

            try:
                #解析元数据和url
                html = response.read()
                
                hxs = HtmlXPathSelector(text=html)

                links = hxs.select('//a/@href').extract()
                #解析电影页面
                if re.search(r'^http://movie.douban.com/subject/(\d+)/$', page_url):
                    crawl_page.html = html
                else:
                    crawl_page.html = ''

              
                for link in links:      
                    url = link
                 
                    if re.search(r'^http://movie.douban.com', url):
                        newurls[url]= crawl_page.weight +1 #连接有效。存入字典中
                        # try:
                        #     print 'add url : %s' % url 
                        # except:
                        #     pass        
            except Exception.args:
                try:
                    print "Could not parse : %s" % args
                except:
                    pass
            #newurls存入数据库 is_save=False weight=i
            crawl_page.is_saved = 2
            save_page(conn, cur, crawl_page)
            #休眠2.5秒
            save_url(conn, cur, newurls)  
            sleep(2.5)
                    
#保存url，放到数据库里
def save_url(conn, cur, newurls):
    for (url,weight) in newurls.items():
        if url_is_exist(cur, url):
                continue
        page = Page()
        page.url = url
        page.weight = weight
        page.html = ''
        insert_page(conn, cur, page)
        print "url added: ", url
        # try:
            
        # except:
        #     try:
        #         print 'url not unique: ', url
        #     except:                
        #         pass
    return True

def read_html(soup):   
    #解析出标题   
    html_title = soup.html.head.title.string   
    title = html_title[:len(html_title)-5]   
    #解析出电影介绍   
    try:   
        intro = soup.find('span',attrs={'class':'all hidden'}).text   
    except:   
        try:   
            node = soup.find('div',attrs={'class':'blank20'}).previousSibling   
            intro = node.contents[0]+node.contents[2]   
        except:   
            try:   
                contents = soup.find('div',attrs={'class':'blank20'}).previousSibling.previousSibling.text   
                intro = contents[:len(contents)-22]   
            except:   
                intro = u'暂无'   
       
    #取得图片   
    html_image = soup('a',href=re.compile('douban.com/lpic'))[0]['href']   
    data = urllib2.urlopen(html_image).read()   
    image = '201003/'+html_image[html_image.rfind('/')+1:]   
    f = file(image_path+image,'wb')   
    f.write(data)   
    f.close()   
       
           
    #解析出地区   
    try:   
        soupsoup_obmo = soup.find('div',attrs={'class':'obmo'}).findAll('span')   
        html_area = soup_obmo[0].nextSibling.split('/')   
        area = html_area[0].lstrip()   
    except:   
        area = ''   
       
    #time = soup_obmo[1].nextSibling.split(' ')[1]   
    #timetime = time.strptime(html_time,'%Y-%m-%d')   
       
    #生成电影对象   
    new_movie = Movie(titletitle=title,introintro=intro,areaarea=area,version='暂无',upload_user=user,imageimage=image)   
    new_movie.save()   
    try:   
        actors = soup.find('div',attrs={'id':'info'}).findAll('span')[5].nextSibling.nextSibling.string.split(' ')[0]   
        actors_list = Actor.objects.filter(name = actors)   
        if len(actors_list) == 1:   
            actor = actors_list[0]   
            new_movie.actors.add(actor)   
        else:   
            actor = Actor(name=actors)   
            actor.save()       
            new_movie.actors.add(actor)   
    except:   
        pass   
       
    #tag   
    tags = soup.find('div',attrs={'class':'blank20'}).findAll('a')   
    for tag_html in tags:   
        tag_str = tag_html.string   
        if len(tag_str) > 4:   
            continue   
        tag_list = Tag.objects.filter(name = tag_str)   
        if len(tag_list) == 1:   
            tag = tag_list[0]   
               
            new_movie.tags.add(tag)   
        else:   
            tag = Tag(name=tag_str)   
            tag.save()     
            new_movie.tags.add(tag)   
    #try:   
           
    #except Exception.args:   
    #   print "Could not download : %s" % args   
    print r'download success'   

def update_is_movie(conn, cur):
    sql = "select id, url from douban_url "
    cur.execute(sql)
    rows = cur.fetchall()
    pages = []
    for row in rows:
        uid = row[0]
        url = row[1]

        if re.search(r'^http://movie.douban.com/subject/(\d+)/$', url):
            # print url
            sql = u"update douban_url set is_movie = 1 where id = %s " 
            cur.execute(sql,  ( str(uid) ))
            conn.commit()


def run_crawl():
    conn = None
    try:
        conn = mdb.connect('localhost', 'root', 'azhenglive80', 'movie');
        conn.set_character_set('utf8')
        cur = conn.cursor()
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARSET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        crawl(conn, cur)
        # update_is_movie(conn, cur)
        
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    finally:    
            
        if conn:    
            conn.close()

if __name__ == "__main__":

    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    print sys.getdefaultencoding()
    
    for i in range(1, 5):        
        t = threading.Thread(target=run_crawl, args=())
        t.start()
        t.join()

