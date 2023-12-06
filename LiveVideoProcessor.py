# -*- coding:utf-8 -*-
from email.mime import image
from sre_parse import State
import tkinter as tk
from tkinter import filedialog
import SplitVideoScenes as svs
from PIL import Image, ImageTk

#全局变量值
tk_images = []
clips_result = []
selected_iv = []
'''存有状态值的sv列表'''
selected_cb = []
selected_clips_result = []
'''视频列表'''

imgs = []


#创建，并定义主窗口
root = tk.Tk()
root.title("LiveVideoProcessor")
root.geometry("500x300")
root.resizable(width=False,height=True)

#输入参数值
n_clusters=tk.StringVar()
n_clusters.set("2")

frame_rate=tk.StringVar()
frame_rate.set("1")
'''阈值'''

#定义视频切片选择区域
fm_cc = tk.Frame(root,bd=2,relief="sunken")
fm_cc.place(x=10,y=95,height=150,width=480)


cn_chooseClips = tk.Canvas(fm_cc)


sb_cn_cc = tk.Scrollbar(fm_cc,orient="horizontal",command=cn_chooseClips.xview)

cn_chooseClips.config(xscrollcommand=sb_cn_cc.set)

cn_chooseClips.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
sb_cn_cc.place(x=0,y=127,width=477)


#定义选取文件操作
file_path = tk.StringVar()
def SelectFile():
    #点击“选择文件按钮”
    global tk_images

    file_path.set(filedialog.askopenfilename(filetypes=[('MP4','*.mp4'),('All Files','*')]))
    if file_path.get():
        print("[Message] File Selected:"+file_path.get())
    else:
        print("[Message] No file was been selected.")

    tk_images = []





btn_chooseFile = tk.Button(root,text="选取视频文件",command=SelectFile,height=1,width=10)
ety_filePath = tk.Entry(root,textvariable=file_path,width=54)

lab_ety_n_clusters = tk.Label(root,text="目标场景数:")
ety_n_clusters = tk.Entry(root,textvariable=n_clusters,width=5)
lab_ety_frame_rate = tk.Label(root,text="每秒识别帧数:")
ety_frame_rate = tk.Entry(root,textvariable=frame_rate,width=5)


def resize_frames(frames, target_size=(100, 100)):
    """调整图像帧的尺寸"""
    resized_frames = []
    for frame in frames:
        image = Image.fromarray(frame)
        resized_image = image.resize(target_size, Image.ANTIALIAS)  # 使用抗锯齿滤波器调整尺寸
        resized_frames.append(resized_image)
    return resized_frames

def display_frames(frames):
    global cn_chooseClips,tk_images,selected_iv,selected_cb
    # 为每个帧创建一个ImageTk.PhotoImage对象并存储在这个列表中
    tk_images = [ImageTk.PhotoImage(image=frame.convert('RGB')) for frame in frames]

    if not tk_images :
        print("0 Error")

    n=0
    for tk_img in tk_images:
        cn_chooseClips.create_image(50+n*110,60,image=tk_img)
        cn_chooseClips.create_text(5+n*110,120,text=str(n))
        selected_iv.append(tk.IntVar(value=1))
        selected_cb.append(tk.Checkbutton(cn_chooseClips,variable=selected_iv[n]))
        cn_chooseClips.create_window(1+n*110,1,anchor=tk.NW,window=selected_cb[n])
        n=n+1

    cn_chooseClips.config(scrollregion=cn_chooseClips.bbox(tk.ALL))

def Save():
    global file_path,selected_clips_result,clips_result,selected_iv
    if not tk_images:
        print("Please sp first")
        return

    i=0
    for clip_result in clips_result:
        if selected_iv[i].get():
            selected_clips_result.append(clip_result)
        i=i+1

    svs.concatenate_and_save_video(file_path.get(),selected_clips_result)
    print("[Message] Video saved")


btn_save = tk.Button(root,text="保存",height=1,width=10,command=Save)


#定义运行函数
def SplitCilps():

    global clips_result,imgs,n_clusters,btn_save,root
    clips_result = svs.scene_splitter(file_path.get(),int(n_clusters.get()), float(frame_rate.get()))
    imgs = svs.get_first_frames(clips_result)
    imgs = resize_frames(imgs)
    display_frames(imgs)




btn_deleteUselessCilps = tk.Button(root,text="自动分割片段",height=1,width=10,command=SplitCilps)


#显示所有元素
btn_chooseFile.place(x=10,y=10)
btn_deleteUselessCilps.place(x=10,y=50)



btn_save.place(x=390,y=260)

ety_filePath.place(x=100,y=15)
lab_ety_n_clusters.place(x=100,y=55)
ety_n_clusters.place(x=170,y=55)
lab_ety_frame_rate.place(x=220,y=55)
ety_frame_rate.place(x=300,y=55)

root.mainloop()
