from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy import create_engine
from utils import delete_img


class Mysql_session():
    def __init__(self):
        engine = create_engine(
                #url=f'mysql+pymysql://root:66884747@127.0.0.1:3306/fastapi_blog?charset=utf8',
                url=f'mysql+pymysql://root:itfkgsbxf3nyw6s1@154.212.112.247:13006/video_txt?charset=utf8',
                max_overflow=3,  # 超过连接池大小外最多创建的连接
                pool_size=3,  # 连接池大小
                pool_pre_ping=True,
                #pool_timeout=100,  # 池中没有线程最多等待的时间，否则报错
                pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
            )
        SessionFactory = sessionmaker(bind=engine)
        self.session = scoped_session(SessionFactory)

    def save_1(self,detail_data):
        detail_data['keyword']=detail_data['keyword'].replace('+',' ')
        try:
            cur=self.session.execute("insert into data(title,keyword,source,url,category,img_src) values(:title,:keyword,:source,:url,:category,:img_src)",detail_data)
            self.session.commit()
            self.session.remove()
            return '第一次入库成功 id:{}'.format(cur.lastrowid)
        except Exception as e:
            return '第一次入库失败:{}'.format(e)

    def save_2(self,content,source,img_path):
        try:
            self.session.execute("update data set content=:content,img_path=:img_path,status=1 where source = :source",{'content':content,'source':source,'img_path':img_path})
            self.session.commit()
            self.session.remove()
            return f'第二次入库成功:{source}.mp4'
        except Exception as e:
            self.session.remove()
            return '第二次入库失败:{}'.format(e)
    def check_duplicate(self,source):
        try:
            cur=self.session.execute("select source from data where source = :source",{'source':source})
            self.session.remove()
            if cur.fetchone():
                return True
            else:
                return False
        except Exception as e:
            self.session.remove()
            print(f'检查重复失败:{e}')
            return False
    #删除数据库异常数据及本地封面图
    def repair_data(self):
        res_list=self.session.execute("select * from data where status = 1 and (length(content)<=150 or content is null)").fetchall()
        for res in res_list:
            self.session.execute("update data set status = 0,img_path='' where id ={}".format(res[0]))
            self.session.commit()
            print(f'数据库状态修改成功:id:{res[0]},titile:{res[1]}')
            #delete_img(res[4])
        self.session.remove()

    def li_mysql_to_txt(self,keyword):
        sqldata_list=self.session.execute(f"select id,title,content,source,img_src from data where status = 1 and keyword = '{keyword.replace('+',' ')}'").fetchall()
        for sqldata in sqldata_list:
            try:
                text=sqldata[1]+'\n'+'<img src= "'+sqldata[4]+'" >'+'\n'+sqldata[1]+' '+sqldata[2].replace('"','-')
                with open(f'text/{keyword.replace(" ","+")}/{sqldata[3]}.txt','w+',encoding='utf-8') as f:
                    f.write(text)
                    f.close()
            except Exception as e:
                print(f"err:id{sqldata[0]},msg:{e}")
        self.session.remove()
            # '''
            # 标题
            # <img src= "图片链接" >
            # 标题 正文.replace('"','-')
            # '''
    def lc_mysql_to_txt(self,keyword):
        sqldata_list = self.session.execute(f"select title,content,img_src from data where status = 1 and keyword = '{keyword.replace('+', ' ')}'").fetchall()
        self.session.remove()
        f=open('11-29_content.txt','a+',encoding='utf-8')
        for sqldata in sqldata_list:
            f.write(sqldata[1]+'\n')
        f.close()

    def hl_xiufu(self):
        import random
        b=[]
        aa=self.session.execute(f"select img_src from data where img_src not like 'no-rj'")
        a=list(aa)
        for bb in a:
            if 'ffff-no-rj' not in bb[0]:
                b.append(bb[0])
        l=self.session.execute(f"select id,img_src from data where img_src is NULL ").fetchall()
        for res in l:
            print(res)
            self.session.execute(f"update data set img_src='{random.choice(b)}' where id = {res[0]}")
        self.session.commit()
        self.session.remove()
if __name__ == '__main__':

    mysql_session=Mysql_session()
    # mysql_session.hl_xiufu()
    for key in ['CRICKET MATCH','Cricket News','Cricket Live','IPL','Cricket Score']:
        mysql_session.li_mysql_to_txt(keyword=key)
