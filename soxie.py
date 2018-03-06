#coding:utf-8
'''
Created on 2018年2月27日

@author: lmm
'''

import urllib,urllib2,bs4
import ssl
import re
from bs4 import BeautifulSoup
shop_list = []
shop = {}
shop_pd_dict = {}
shop_pd_dict_all = {}
key_a = 'sooxie.com'
url_shop_list_entry = 'https://sooxie.com/list.aspx'
pt_soxie_header = {
    'Referer':'https://www.sooxie.com/List.aspx',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }

def add2ddict(thedict, key_a, key_b, val): 
    if key_a in thedict:
        thedict[key_a].update({key_b:val})
    else:
        thedict.update({key_a:{key_b:val}})
        
def pt_build_https_opener():
    global opener
    context = ssl._create_unverified_context()
    httpshandler = urllib2.HTTPSHandler(context=context)
    opener = urllib2.build_opener(httpshandler)
    
def get_shop_list_page_cnt(url,data_dict):
    global pn
    print '---get shop list page cnt---'
    data_ecd = urllib.urlencode(data_dict)
    url = url+'?'+data_ecd
    req = urllib2.Request(url,headers=pt_soxie_header)
    res = opener.open(req)
    resr = res.read()
    #print resr
    soup = BeautifulSoup(resr,'html.parser')
    #tag_shop = 
    script_txt = soup.find_all('script')[-2].get_text()
    #print str(a)
    print type(script_txt)
    #a = a.encode('utf-8')
    if 'pnc=' in script_txt:
        pn = script_txt.split(';')[1].split('=')[1]
        print pn
        pn = int(pn)
def pt_get_shop_list_page_pn():
    url = url_shop_list_entry
    data_dict = {
        'r':'all',
        #'Page':'all',
        }
    get_shop_list_page_cnt(url,data_dict)
def pt_get_shop_list_page(url,shop_list,data_dict):
    print '---get one page shop list---'
    print '--get %s--'%url
    data_ecd = urllib.urlencode(data_dict)
    url = url+'?'+data_ecd
    req = urllib2.Request(url,headers=pt_soxie_header)
    res = opener.open(req)
    resr = res.read()
    #print resr
    soup = BeautifulSoup(resr,'html.parser')
    #tag_shop = 
    script_txt = soup.find_all('script')[-2].get_text()
    #print str(a)
    print type(script_txt)
    #a = a.encode('utf-8')
    #shop_list = soup.find(class_='sjlist').find_all('a',href=re.compile(key_a))
    shop_list = soup.find(class_='sjlist').find_all(class_ = 'message')
    shop_cnt_page = len(shop_list)
    for x in xrange(shop_cnt_page):
        shop['name'] = shop_list[x].find(class_='storename').get_text()
        shop['area'] = shop_list[x].find_all(class_='orange appr')[0].em.string
        shop['class'] = shop_list[x].find_all(class_='orange appr')[1].em.string
        shop['phone'] = shop_list[x].find_all(class_='detmsg')[0].font.string
        shop['age'] = shop_list[x].find_all(class_='detmsg')[1].font.string
        shop['qq'] = shop_list[x].find_all(class_='detmsg')[2].font.next_sibling.next_sibling.get_text().encode('utf-8').split(' ')[0]
        shop['addr'] = shop_list[x].find(class_='detaddr').string
        shop['website'] = shop_list[x].a.get('href')
        print '===shop %d======'%x
        for k,v in shop.iteritems():
            print k,v
        shop_list.append(shop)
        
def pt_get_all_shop_list():
    print '===get all shop list==='
    url = url_shop_list_entry
    for x in xrange(pn):
        data_dict = {
        'r':'all',
        'Page':'%d'%(x+1),
        }
        pt_get_shop_list_page(url, shop_list, data_dict)
        
def pt_get_shop_product(url):
    print '===get shop product==='
    n = 0
    data_dict = {}
    data_ecd = urllib.urlencode(data_dict)
    url = url
    req = urllib2.Request(url,headers=pt_soxie_header)
    res = opener.open(req)
    resr = res.read()
    #print resr
    soup = BeautifulSoup(resr,'html.parser')
    #tag_shop = 
    script_txt = soup.select('head script')[6].get_text()
    print script_txt
    if 'totalpage =' in str(script_txt):
        totalpage = int(script_txt.split('=')[1].split(';')[0])
        print 'totalpage %d'%totalpage
    pro_list = soup.select('.probox .pro')
    for x in xrange(len(pro_list)):
        pro = pro_list[x].select_one('.pname').a.get('href')
        print pro
        n+=1
    '''get more pro'''
    if totalpage > 1:
        for x in range(2,totalpage+1):
            shop_name = url.split('//')[1].split('.')[0]
            data_dict = {
                'url':shop_name,
                'page':x,
                }
            data_ecd = urllib.urlencode(data_dict)
            url = url+'page.aspx'+'?'+data_ecd
            req = urllib2.Request(url,headers=pt_soxie_header)
            res = opener.open(req)
            resr = res.read()
            soup = BeautifulSoup(resr,'html.parser')
            pro_list = soup.select('.pro')
            for y in xrange(len(pro_list)):
                pro = pro_list[y].select_one('.pname').a.get('href')
                print pro
                n+=1
    print '=== shop %s total product num %d ==='%(shop_name,n)
    
def pt_get_prod_detail(url,):
    print '=== get prod detail ==='
    shop_name = url.split('//')[1].split('.')[0]
    pd_id = url.split('/')[3].split('.')[0]
    req = urllib2.Request(url,headers=pt_soxie_header)
    res = opener.open(req)
    resr = res.read()
    soup = BeautifulSoup(resr,'html.parser')
    pd_info = soup.select('.proinfo .infobox_h .infoline')
    print len(pd_info)
    pd_name = pd_info[0].strip
    pd_num = pd_info[1].strong.get_text()
    pd_price = pd_info[2].em.get_text()
    pd_hot_index = pd_info[3].select('strong')[0].get_text()
    pd_update_time = pd_info[3].select('strong')[1].font.get_text()
    pd_size = pd_info[4].select_one('#size').select('li')
    pd_color = pd_info[5].select_one('#color').select('li')
    size_list = []
    color_list = []
    pd_dict = {}
    for x in xrange(len(pd_size)):
        size_list.append(pd_size[x].get_text())
    for x in xrange(len(pd_color)):
        color_list.append(pd_color[x].get_text())
    pd_dict['pd_name'] = pd_name
    pd_dict['pd_num'] = pd_num
    pd_dict['pd_price'] = pd_price
    pd_dict['pd_hot_index'] = pd_hot_index
    pd_dict['pd_update_time'] = pd_update_time
    pd_dict['pd_size'] = size_list
    pd_dict['pd_color'] = color_list
    for k,v in pd_dict.iteritems():
        print k,v
    add2ddict(shop_pd_dict,shop_name,pd_id,pd_dict)
def main():
    print '---main func---'
    pt_build_https_opener()
    #pt_get_shop_list_page_pn()
    #pt_get_all_shop_list()
    #url = url_shop_list_entry
    url = 'https://lingxiu.sooxie.com/'
    data_dict = {
        'r':'all',
        }
    #pt_get_shop_list_page(url, shop_list, data_dict)
    pt_get_shop_product(url)
    pt_get_prod_detail('https://hengjia.sooxie.com/288811.aspx')
    pass

if __name__ == "__main__":
    main()
    
