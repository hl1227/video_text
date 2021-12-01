from moviepy.editor import AudioFileClip
import os

class Video_speech():
    def __init__(self,cut_time=40):
        self.cut_time=cut_time
    def get_video_img(self):
        pass
    def run(self,video_path):
        speech_list = []
        video_duration=AudioFileClip(video_path).duration#获取视频时长
        for cut_count,video_cut in enumerate(range(0,int(video_duration)+1,self.cut_time)):
            speech_path = video_path.replace('.mp4', '_{}.wav').format(cut_count + 1)
            my_audio_clip = AudioFileClip(video_path,fps=33000)
            try:my_audio_clip.subclip(video_cut,video_cut+self.cut_time).write_audiofile(filename=speech_path,bitrate='16K',verbose=False)
            except Exception as e:
                if "Accessing time" in str(e):
                    pass
                else:
                    print('video分割转换失败:{}'.format(e))
            ffmpeg_video_name=speech_path.replace('.wav','.pcm')
            cmd="ffmpeg -loglevel warning -y  -i {}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {}".format(speech_path,ffmpeg_video_name)
            os.system(cmd)
            speech_list.append(ffmpeg_video_name)
            my_audio_clip.close()
        return  speech_list
