#!/usr/bin/python3
# -*- coding: utf8 -*-

__all__=["读简单配置","获取组成员","未完成退出","异常退出","sw配置文件"]

import time,base64,sys,json,urllib.request,ssl,os,datetime
import libsw3 as sw3
sw3.__all__=sw3.__all__ + __all__

def 读简单配置(文件名,项目):  #读简单配置文件，一行一条数据，第一列是项目，返回项目后的内容
    dh,_=os.path.splitdrive(os.getcwd())
    fn=os.path.join(dh,"/etc",文件名)
    if os.path.isfile(fn):
        f=open(fn,"r")
    else:
        sw3.swexit(-1,"无法打开连接串配置文件%s" %(fn))
    wjnr=f.readlines()
    f.close()
    for i in wjnr:
        s=i.split()
        if len(s)<2:
            continue
        if s[0]==项目:
            return " ".join(s[1:])
    return ""

def 获取组成员(组id):
    pass

def 未完成退出(信息,*参数):
    if len(参数)>0:
        信息=信息 %(参数)
    sw3.swexit(1,信息)

def 异常退出(信息,*参数):
    if len(参数)>0:
        信息=信息 %(参数)
    sw3.swexit(-1,信息)

def sw配置文件(文件名):    #根据文件名，返回带目录的配置文件名
    dh,_=os.path.splitdrive(os.getcwd())
    return os.path.join(dh,"/etc",文件名)
