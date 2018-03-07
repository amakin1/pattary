#coding:utf-8
'''
Created on 2018年2月27日

@author: lmm
'''

import urllib,urllib2,bs4
import ssl
import re
import time
import xlwt
import copy
from bs4 import BeautifulSoup

shop_list = []
shop_info_dict = {}
shop_pd_list = []
shop_pd_dict = {}
shop = {}
shop_pd_detail_dict = {}
shop_pd_detail_dict_all = {}
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
def pt_time_init():
    global time_tag
    print '--- time init ---'
    time_now = time.time()
    time_now_for_ck = int(time_now)
    time_now_for_ck2 = time_now_for_ck+15
    setcookie_str = ''
    setcookie_str+='Hm_lvt_a402dc646b9ff3767a84eba34e4a86f8=%s;'%time_now_for_ck
    setcookie_str+='Hm_lpvt_a402dc646b9ff3767a84eba34e4a86f8=%s;'%time_now_for_ck2
    t_local = time.localtime(time_now)
    t_Y = time.strftime("%Y",t_local)
    t_m = time.strftime("%m",t_local)
    t_d = time.strftime("%d",t_local)
    t_d = str(int(t_d)+0)
    t_H = time.strftime("%H",t_local)
    t_M = time.strftime("%M",t_local)
    t_S = time.strftime("%S",t_local)
    t_w = time.strftime("%w",t_local)
    time_tag=t_Y+t_m+t_d+t_H+t_M
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
        shop['qq'] = shop['qq'].decode('utf-8')
        shop['addr'] = shop_list[x].find(class_='detaddr').string
        shop['website'] = shop_list[x].a.get('href')
        shop_name = shop['website'].split('//')[1].split('.')[0]
        print '===shop %d======'%x
        for k,v in shop.iteritems():
            print k,v
            #add2ddict(shop_info_dict,'%s'%shop_name,k,v)
        shop_info_dict['%s'%shop_name] = copy.deepcopy(shop)
        
def pt_get_all_shop_list():
    print '===get all shop list==='
    url = url_shop_list_entry
    pn = 2
    for x in xrange(pn):
        data_dict = {
        'r':'all',
        'Page':'%d'%(x+1),
        }
        pt_get_shop_list_page(url, shop_list, data_dict)
        
def pt_get_shop_product(url):
    print '--- get shop product ---'
    n = 0
    shop_name = url.split('//')[1].split('.')[0]
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
        shop_pd_list.append(pro)
        n+=1
    '''get more pro'''
    if totalpage > 1:
        for x in range(2,totalpage+1):
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
                shop_pd_list.append(pro)
                n+=1
    shop_pd_dict['%s'%shop_name] = shop_pd_list
    print '=== shop %s total product num %d ==='%(shop_name,n)
    
def pt_get_prod_detail(url,):
    print '--- get prod detail ---'
    shop_name = url.split('//')[1].split('.')[0]
    pd_id = url.split('/')[3].split('.')[0]
    req = urllib2.Request(url,headers=pt_soxie_header)
    res = opener.open(req)
    resr = res.read()
    soup = BeautifulSoup(resr,'html.parser')
    pd_info = soup.select('.proinfo .infobox_h .infoline')
    print len(pd_info)
    pd_name = pd_info[0].get_text().strip()
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
    add2ddict(shop_pd_detail_dict,shop_name,pd_id,pd_dict)
    
def pt_save_shop_pd_detail_data(data_dict):
    pt_time_init()
    pd_x =2
    pd_y =1
    '''
    with open('.\data\pt_sooxie_%s.txt'%time_tag,mode = 'a+') as f:
        for k,v in data_dict.iteritems():
            if isinstance(v,dict):
                for kk,vv in v.iteritems():
                    line = '%s:%s:%s \n'%(k,kk,vv)
                    f.writelines(line)
            else:
                print 'no pd'
    '''
    pattern = xlwt.Pattern() # Create the Pattern
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern.pattern_fore_colour = 3
    style = xlwt.XFStyle() # Create the Pattern
    style.pattern = pattern # Add Pattern to Style
    wkb = xlwt.Workbook()
    sheet_pd = wkb.add_sheet(u'商品信息')
    '''
    sheet_pd.write(1,1,u'商家',style)
    sheet_pd.write(1,2,u'商品链接',style)
    sheet_pd.write(1,3,u'价格',style)
    sheet_pd.write(1,4,u'货号',style)
    sheet_pd.write(1,5,u'颜色',style)
    sheet_pd.write(1,6,u'更新时间',style)
    sheet_pd.write(1,7,u'尺码',style)
    sheet_pd.write(1,8,u'名称',style)
    sheet_pd.write(1,9,u'热度',style)
    for k,v in data_dict.iteritems():
        if isinstance(v,dict):
            for kk,vv in v.iteritems():
                if isinstance(vv,dict):
                    sheet_pd.write(pd_x,pd_y,k)
                    pd_y+=1
                    sheet_pd.write(pd_x,pd_y,kk)
                    pd_y+=1
                    for kkk,vvv in vv.iteritems():
                        if isinstance(vvv,list):
                            tmp_v = ''
                            for x in xrange(len(vvv)):
                                tmp_v+=vvv[x]+','
                            sheet_pd.write(pd_x,pd_y,tmp_v)
                            pd_y+=1
                        else:
                            sheet_pd.write(pd_x,pd_y,vvv)
                            pd_y+=1
                pd_y= 1
                pd_x+=1
                line = '%s:%s:%s \n'%(k,kk,vv)
    '''
    sheet_shop = wkb.add_sheet(u'商家信息')
    pd_x =2
    pd_y =1
    sheet_shop.write(1,1,u'商家简称',style)
    sheet_shop.write(1,2,u'商家名称',style)
    sheet_shop.write(1,3,u'区域',style)
    sheet_shop.write(1,4,u'等级',style)
    sheet_shop.write(1,5,u'电话',style)
    sheet_shop.write(1,6,u'年份',style)
    sheet_shop.write(1,7,u'QQ',style)
    sheet_shop.write(1,8,u'地址',style)
    sheet_shop.write(1,9,u'网址',style)
    lenn = len(shop_info_dict)
    for k,v in shop_info_dict.iteritems():
        if isinstance(v,dict):
            print k,v
            sheet_shop.write(pd_x,pd_y,k)
            pd_y+=1
            for kk,vv in v.iteritems():
                sheet_shop.write(pd_x,pd_y,vv)
                pd_y+=1
            pd_y= 1
            pd_x+=1    
    wkb.save('.\data\pt_soxie_%s.xls'%time_tag)
    print '---save data done---'
    

def main():
    print '---main func---'
    pt_build_https_opener()
    #pt_get_shop_list_page_pn()
    pt_get_all_shop_list()
    #url = url_shop_list_entry
    url = 'https://lingxiu.sooxie.com/'
    data_dict = {
        'r':'all',
        }
    #pt_get_shop_list_page(url, shop_list, data_dict)
    pt_get_shop_product(url)
    '''
    for k,v in shop_pd_dict.iteritems():
        if isinstance(v,list):
            for x in xrange(len(v)):
                id = v[x]
                pt_get_prod_detail(id)
    '''
    pt_get_prod_detail('https://hengjia.sooxie.com/288811.aspx')
    pt_save_shop_pd_detail_data(shop_pd_detail_dict)
    pass

if __name__ == "__main__":
    main()
    
