from video_speech import Video_speech
from speech_text import Speech_text
from get_video import Get_video
from get_detail_data import Get_detail_data
from utils import create_video_dir,create_text_dir
from mysql_db import Mysql_session
from multiprocessing import Pool
import config,os

def run(domain,keyword0,category,video_num:int):
    keyword=keyword0.replace(' ','+')
    mysql_session = Mysql_session()
    video_speech = Video_speech()
    speech_text = Speech_text()
    get_video = Get_video(keyword)

    #创建文件
    print(create_video_dir(keyword))
    #print(create_img_dir(keyword))
    print(create_text_dir(keyword))

    # 获取详情页
    detail_data_list = Get_detail_data().run(domain=domain, keyword=keyword, video_num=video_num)

    # 处理详情数据
    for detail_data in detail_data_list:
        if mysql_session.check_duplicate(detail_data['source']) == True:#去重
            detail_data_list.remove(detail_data)
            print('数据重复:{}'.format(detail_data["source"]))
        else:
            detail_data.update({'category': category})  # 增加分类
            print(mysql_session.save_1(detail_data))  # 第一次入库

    #下载视频
    pool = Pool(8)
    pool.map_async(get_video.run,detail_data_list)
    pool.close()
    pool.join()
    print('全部视频下载完成')

    for video_name in os.listdir(os.path.join(config.VIDEOS_PATH,keyword)):
        # 视频转语音
        video_path=os.path.join(config.VIDEOS_PATH,keyword,video_name)
        speech_path_list=video_speech.run(video_path)
        print(f'转换语音完成:{video_name},开始语音识别:{speech_path_list}')

        # 提取图片路径
        source = video_name[0:11]
        img_path = ''
        # img_path = os.path.join(config.IMG_PATH, keyword, source + '.png')
        # if not os.path.exists(img_path):
        #     img_path = config.DEFAULT_IMG_PATH

        # 语音转文字
        content = speech_text.run(speech_path_list)
        #第二次入库
        print(f'语音识别完成:{video_name},开始二次入库...')
        mysql_session.save_2(content=content,source=source,img_path=img_path)
        print(f'二次入库完成:{video_name}!!')
    mysql_session.repair_data()


if __name__ == '__main__':
    for key in ['T20 World Cup','Cricket star']:
        run(domain='youtube', keyword0=key,category='体育项目',video_num=700)
    #os.system('shutdown /s /f /t 60')