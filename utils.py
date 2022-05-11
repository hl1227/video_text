import config,os

#创建视频文件价
def create_video_dir(keyword):
    video_path = os.path.join(config.VIDEOS_PATH, keyword)
    if not os.path.exists(video_path):
        os.mkdir(video_path)
    return f'视频文件夹创建成功:{video_path}'

# #创建封面文件夹
# def create_img_dir(keyword):
#     img_path = os.path.join(config.IMG_PATH, keyword)
#     if not os.path.exists(img_path):
#         os.mkdir(img_path)
#     return f'封面文件夹创建成功:{img_path}'

#创建文本文件夹
def create_text_dir(keyword):
    text_path = os.path.join(config.TEXT_PATH, keyword)
    if not os.path.exists(text_path):
        os.mkdir(text_path)
    return f'封面文件夹创建成功:{text_path}'

#删除视频文件夹
def delete_video_dir(keyword):
    video_path=os.path.join(config.VIDEOS_PATH,keyword)
    if os.path.exists(video_path):
        # os.rmdir(video_path)
        # print(f'文件夹删除成功:{video_path}')
        for video_name in os.listdir(video_path):
            if video_name[-3:] in ['pcm','wav','mp4']:#删除pcm和wav文件,保留MP4
                os.remove(os.path.join(video_path,video_name))

#删除封面文件
def delete_img(img_path):
    if img_path is None:
        return
    if os.path.exists(img_path):
        os.remove(img_path)
        print(f'封面图片删除成功:{img_path}')
    elif 'png' not in img_path:
        print(f'删除封面参数不对:{img_path}')

if __name__ == '__main__':
    delete_video_dir('CRICKET+MATCH')