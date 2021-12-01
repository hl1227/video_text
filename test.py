from concurrent.futures import ThreadPoolExecutor
import requests,time,threading,json,re,sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'referer': 'https://www.google.com/'}
#接口请求
def Get_Keyword(keyword_start):

    url='https://www.google.com/complete/search?q={}&cp=13&client=gws-wiz&xssi=t&hl=en&authuser=0&newwindow=1&dpr=1'.format(keyword_start)
    keyword = []
    try:
        date_str=requests.get(url,headers=headers,timeout=3,proxies={"https":"http://127.0.0.1:11000","http":"http://127.0.0.1:11000"}).content.decode('raw_unicode-escape').replace(")]}'\n","")
        time.sleep(0.2)
        date_list=json.loads(date_str)
        for date in date_list[0]:
            key = date[0].replace('<b>', '').replace('</b>', '')
            if key != keyword_start:
                keyword.append(key)
    except Exception:
        keyword=[]
    return keyword

def xunhuan(keyword):
    res_list=[]
    two_res_list=Get_Keyword(keyword)
    res_list+=two_res_list
    for two_res in two_res_list:
        three_res_list=Get_Keyword(two_res)
        res_list+=three_res_list
    return res_list

def run(keyword):
    one_res_list=Get_Keyword(keyword)
    max_workers=len(one_res_list)
    with  ThreadPoolExecutor(max_workers=max_workers) as pool:
        two_res_list=[]
        res_iterator=pool.map(xunhuan,one_res_list)
        for res in res_iterator:
            two_res_list+=res
        return list(set(two_res_list))

if __name__ == '__main__':
    keyword_list=['cricket team']
    for keyword in keyword_list:
        run(keyword)