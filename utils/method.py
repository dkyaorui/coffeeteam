from PIL import Image
from  blog import models
import os
import re
import random
from django.core.mail import send_mail
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class PageHalper:
    def __init__(self,total_count,current_page,base_url,per_page=10):
        self.total_count = total_count
        self.current_page = current_page
        self.base_url = base_url
        self.per_page = per_page

    @property
    def db_start(self):
        return (self.current_page-1)*self.per_page

    @property
    def db_end(self):
        return self.current_page*self.per_page

    def total_page(self):
        #获取分页页数
        v,a = divmod(self.total_count,self.per_page)
        if a!=0:
            v+=1
        return v

    def pager_str(self):
        v = self.total_page()

        pager_list = []
        pager_list.append('<a class="first" href="%s?p=1">首页</a>'%(self.base_url))
        if self.current_page == 1:
            pager_list.append('<a class="pre" href="javascript:void(0)">上一页</a>')
        else:
            pager_list.append('<a href="%s?p=%s">上一页</a>'%(self.base_url,self.current_page-1))
        pager_list.append('<span class="num">')

        if v <= 5:
            pager_range_start = 1
            pager_range_end = v
        else:
            if self.current_page < 4:
                pager_range_start = 1
                pager_range_end = 5+1
            else:
                pager_range_start = self.current_page - 2
                pager_range_end = self.current_page + 2 + 1
                print(self.current_page,pager_range_start,pager_range_end)
                if pager_range_end > v:
                    pager_range_start = v - 5
                    pager_range_end = v + 1

        for i in range(pager_range_start, pager_range_end):
            if i == self.current_page:
                pager_list.append('<a class="current" href="%s?p=%s">%s</a>' % (self.base_url, i, i,))
            else:
                pager_list.append('<a href="%s?p=%s">%s</a>' % (self.base_url, i, i,))

        if self.current_page == v:
            pager_list.append('<a href="javascript:void(0);">下一页</a>')
        else:
            pager_list.append('<a class="next" href="%s?p=%s">下一页</a>' % (self.base_url, self.current_page + 1,))
        pager_list.append('</span>')
        pager_list.append('<a class="last" href="%s?p=%s">尾页</a>' % (self.base_url,v))
        pager = "".join(pager_list)
        return pager


def listHelper_small(data):
    list=[]
    for item in data:
        id = item.id
        path ='<li class="list_small"><div class="news_small"><a href="/blog/article_detial/?id=%s" title="%s">%s</a></div></li><hr>' % (id, item.title, item.title)
        list.append(path)
    pathlist="".join(list)
    return pathlist

def listHelper_big(data):
    list=[]
    for item in data:
        id = item.id
        time =re.search(r"(\d{4}-\d{2}-\d{2})",str(item.ctime))
        print(time.group(0))
        path ='<li class="list"><div class="news"><a href="/blog/article_detial/?id=%s" title="%s">%s</a></div><div class="time"><a>%s</a></div></li><hr>' % (id, item.title, item.title, time.group(0))
        list.append(path)
    pathlist="".join(list)
    return pathlist



#对path进行处理
def mkdir(path):
    # 去除左右两边的空格
    path=path.strip()
    # 去除尾部 \符号
    path=path.rstrip("\\")

    if not os.path.exists(path):
        os.makedirs(path)
    return path
def resize_by_width(cls):
    """按照宽度进行所需比例缩放"""
    im = Image.open(cls)
    (x, y) = im.size
    if x>400:
        x_s = 400
        y_s = int(y*(400/x))
        im.resize((x_s, y_s), Image.ANTIALIAS).save(cls)
#保存相关的文件
def save_file(path, file_name, data):
    if data == None:
        return

    mkdir(path)
    if(not path.endswith("/")):
        path=path+"/"
    file=open(path+file_name, "wb")
    file.write(data)
    file.flush()
    file.close()
    resize_by_width(os.path.join(BASE_DIR,path+file_name))


def comment_list_helper(comments,user_id):
    list1=[]
    list2=[]
    tempdict={}
    for item in comments:
        list1.append(item.id)
        tempdict.update({"id":item.id})
        tempdict.update({"user":item.user})
        tempdict.update({"content":item.content})
        tempdict.update({"ctime":item.ctime})
        tempdict.update({"parent_comment":item.parent_comment})
        tempdict.update({"favor_count":item.favor_count})
        is_favor = item.favor.filter(id=user_id)
        if is_favor:
            a = 1
        else:
            a = 0
        tempdict.update({"is_favor": a})

        list2.append(tempdict)
        tempdict={}
    comments = dict(zip(list1,list2))
    for item in comments:
        comments[item].update({"children":[]})

    report = []
    for item in comments:
        parentRow = comments[item]['parent_comment']

        if parentRow:
            id = re.search(r"(\d+)", str(parentRow)).group(0)
            id=int(id)
            comments[id]['children'].append(comments[item])
        else:
            report.append(comments[item])
    return report

def random_codeStr(codelength=16):
    char  = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(char) - 1
    str = ''
    for x in range(codelength):
        str += char[random.randint(0,length)]
    return str

