from os import rename,path
import requests,config,youtube_dl


class Get_video():
    def __init__(self,keyword):
        self.keyword=keyword
    def run(self,detail_data):
        if 'bilibili' in detail_data['url']:
            return self.get_bilibili(detail_data['url'])

        elif 'youtube' in detail_data['url']:
            get_video_status=self.get_youtube(detail_data['url'])
            # if get_video_status:
            #     self.download_img(detail_data['img_src'],detail_data['source'],self.keyword)
            # return 1
        else:
            print('下载未匹配域名!')
            return None

    # 下载图片
    def download_img(self,img_src, source, keyword):
        if config.PROXY:
            proxies = config.PROXY
        else:
            proxies = None
        img_path = path.join(config.IMG_PATH, keyword, source + '.png')
        try:
            img_res = requests.get(img_src, proxies=proxies).content
            with open(img_path, 'wb+') as f:
                f.write(img_res)
            return img_path
        except Exception:
            print(f'图片下载失败:{source} {img_src}')
            return None
    def get_bilibili(self,url: str):
        """
        imgs、videos
        """
        headers = {
            "user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Referer": "https://www.bilibili.com/",
        }
        res=requests.get(url, headers=headers, timeout=10,proxies=config.PROXY)
        print(res.json())
        ##################################################################################
        # data = {}
        # av_number_pattern = r'(BV[0-9a-zA-Z]*)'
        # cover_pattern = r"readyPoster: '(.*?)',"
        # video_pattern = r"readyVideoUrl: '(.*?)',"
        # title_pattern = r'title":"(.*?)",'
        #
        # av = re.findall(av_number_pattern, url)
        # if av:
        #     av = av[0]
        # else:
        #     data["msg"] = "链接可能不正确，因为我无法匹配到av号"
        #     return data
        # url = f"https://www.bilibili.com/video/{av}"
        # with requests.get(url, headers=headers, timeout=10,proxies={"https":"http://127.0.0.1:11000"}) as rep:
        #     if rep.status_code == 200:
        #         cover_url = re.findall(cover_pattern, rep.text)
        #         if cover_url:
        #             cover_url = cover_url[0]
        #             if '@' in cover_url:
        #                 cover_url = cover_url[:cover_url.index('@')]
        #             data["imgs"] = ['https:' + cover_url]
        #
        #         video_url = re.findall(video_pattern, rep.text)
        #         title_text = re.findall(title_pattern, rep.text)
        #         if video_url:
        #             video_url = video_url[0]
        #             data["videos"] = [video_url]
        #         if title_text:
        #             data["videoName"] = title_text[0]
        #     else:
        #         data["msg"] = "获取失败"
        #     return data

    def rename_hook(self, d):
        # youtube重命名下载的视频名称的钩子
        if d['status'] == 'finished':
            file_name =path.join(config.VIDEOS_PATH,self.keyword,d['filename']+'.mp4')
            # file_name = config.VIDEOS_PATH+'/'+self.keyword+'+'+d['filename']+'.mp4'
            rename(d['filename'], file_name)

    def get_youtube(self,youtube_url):
        # 定义某些下载参数
        ydl_opts = {
            'format': 'bestaudio',
            # best：选择具有视频和音频的单个文件所代表的最佳质量格式。
            # worst：选择具有视频和音频的单个文件所代表的最差质量格式。
            # bestvideo：选择最佳质量的仅视频格式（例如DASH视频）。可能无法使用。
            # worstvideo：选择质量最差的纯视频格式。可能无法使用。
            # bestaudio：选择质量最佳的音频格式。可能无法使用。
            # worstaudio：选择质量最差的音频格式。可能无法使用。
            'progress_hooks': [self.rename_hook],
             # 格式化下载后的文件名，避免默认文件名太长无法保存
            'outtmpl':'%(id)s',
            'quiet': True,
        }
        # try:

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                result = ydl.extract_info(youtube_url, download=True)
                print(f'下载成功:{youtube_url}')
                return 1
            except FileNotFoundError:
                print(f'下载成功:{youtube_url}')
                return 1
            except youtube_dl.utils.DownloadError as e:
                print( '下载失败:{} {}'.format(youtube_url,e))
                return None
            except Exception as e:
                print('下载失败:{} {}'.format(youtube_url,e))
                return None
        #return '下载成功:{}'.format(youtube_url)

        # except Exception as e:
        #     # raise Exception('下载报错: '+youtube_url+' '+str(e))
        #     return config.VIDEOS_PATH + '/' + result['id'] + '.mp4'


# if __name__ == "__main__":
#
#      Get_video().run('https://www.youtube.com/watch?v=Y1bV2IYvjgw')
    #Get_video().get_youtube('https://api.bilibili.com/x/web-interface/search/type?context=&keyword=英文&page=1&search_type=video&changing=id&__refresh__=true&__reload__=false&highlight=1&single_column=0')

