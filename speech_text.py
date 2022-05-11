from aip import AipSpeech
import config
from concurrent.futures import ThreadPoolExecutor

class Speech_text():
    def __init__(self):
        APP_ID = '25306101'
        API_KEY = 'hdNLX9RLwIdgUob2L1G7lXAW'
        SECRET_KEY = 'FmSNi7RlVI5uGt3zra9BcMBCN8GEYGC8'
        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        if config.PROXY:
            self.client.setProxies(config.PROXY)
    def read_speech(self,file_path):
        with open(file_path, 'rb') as fp:
            return fp.read()
    def asr(self,file_path):
        res = ''
        try:
            rb_speech=self.read_speech(file_path)
            api_res=self.client.asr(speech=rb_speech,format='pcm',rate=16000,options= {'dev_pid': 1737,}) #英文:1737(标点加强)  中文:1537
            if api_res['err_no']==0:
                res+=api_res['result'][0]
            else:
                print(f'语音识别错误:{file_path},response:{api_res}')
        except Exception as e:
            print(f'语音识别错误:{e}')
        return res

    def run(self,file_path_list):
        content=''
        with ThreadPoolExecutor(max_workers=4) as pool:
            res_iterator=pool.map(self.asr,file_path_list)
            for res in res_iterator:
                content+=res
            pool.shutdown()
            return content

if __name__ == '__main__':

    speech_text=Speech_text()
    # for file in ['./videos/Mv3dkRmCnOA_1.pcm', './videos/Mv3dkRmCnOA_2.pcm', './videos/Mv3dkRmCnOA_3.pcm', './videos/Mv3dkRmCnOA_4.pcm', './videos/Mv3dkRmCnOA_5.pcm']:
    content=speech_text.run(['./videos/.default/-uevumiLg8I_1.pcm', './videos/.default/-uevumiLg8I_2.pcm', './videos/.default/-uevumiLg8I_3.pcm'])
    print(content)

        # res=pool.map(speech_text.run,)
        # for a in res:
        #     print(a)

