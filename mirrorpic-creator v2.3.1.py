import sys
import os
import tkinter
import datetime
import shutil
import numpy as np
from PIL import Image,ImageTk
import imageio
from tkinterdnd2 import *

imagedetected=0
original_dir=None
formatted_time=None
mode=None
savemode=0
doquit=0
changepicindi=0

def modeselect():
    global mode

    def sel(num):
        global mode
        mode=num
        root.destroy()

    root=tkinter.Tk()
    framepack=tkinter.Frame(root)
    framepack.pack()
    framegrid=tkinter.Frame(root)
    framegrid.pack()
    label=tkinter.Label(framepack,text="请选择模式")
    label.pack()
    button1 = tkinter.Button(framegrid, text="原图置于左侧", command=lambda: sel(1))
    button1.grid(row=0, column=0, padx=10, pady=10)
    button2 = tkinter.Button(framegrid, text="原图置于右侧", command=lambda: sel(2))
    button2.grid(row=0, column=1, padx=10, pady=10)
    button3 = tkinter.Button(framegrid, text="原图置于上方", command=lambda: sel(3))
    button3.grid(row=1, column=0, padx=10, pady=10)
    button4 = tkinter.Button(framegrid, text="原图置于下方", command=lambda: sel(4))
    button4.grid(row=1, column=1, padx=10, pady=10)
    root.mainloop()

def mirror():
    import time

    changepicindi=0

    global original,imagedetected,output,rect,formatted_time,original_dir,canvaspic,newimage,aspectratio,duration,fps
    original = Image.open(original_dir)
    if original_dir.endswith(('.gif','.GIF')):
        with imageio.get_reader(original_dir) as reader:
            duration = reader.get_meta_data()['duration']
            fps = 1000 / duration
    imagedetected = 1
    rect = None

    def windowresize(event):
        global newimage,originaltk,canvaspic,last_time,newheight,newwidth
        newheight=root.winfo_height()
        newwidth=int((newheight-100)*aspectratio+20)
        current_time = time.time()
        try:
            last_time = last_time
        except NameError:
            last_time = 0
        if abs(newwidth - root.winfo_width()) > 5 and (current_time - last_time) > 0.005:
            root.geometry(f"{newwidth}x{newheight}")
            last_time = current_time
        if original_dir.endswith(('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG')):
            newimage = original.resize((int(newwidth) - 20, int(newheight) - 100))
            originaltk = ImageTk.PhotoImage(newimage)
            canvas.itemconfig(canvaspic, image=originaltk)
            canvas.config(width=newwidth - 20, height=newheight - 100)
            tutorial.config(font=("微软雅黑", int((newimage.width + 20) / 33)))

    def mousepress(event):
        global clickx, clicky
        clickx = event.x
        clicky = event.y

    def mousemove(event):
        global rect
        if rect:
            canvas.delete(rect)
        rect = canvas.create_rectangle(clickx, clicky, event.x, event.y, outline='red')

    def mouserelease(event):
        global releasex, releasey
        releasex = event.x
        releasey = event.y

    def quit():
        global original_dir,newimage,changepicindi
        original_dir=None
        newimage=None
        changepicindi=1
        root.destroy()

    def quit4real():
        global doquit,original_dir,newimage
        original_dir=None
        newimage=None
        doquit=1
        root.destroy()

    root = tkinter.Tk()
    root.title("裁剪照片")
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    root.maxsize = (screenwidth - 200, screenheight - 200)
    root.resizable(False, True)
    aspectratio = original.width / original.height
    width = original.width
    height = original.height
    if width > screenwidth - 200:
        width = screenwidth - 200
        height = width / aspectratio
    if height > screenheight - 200:
        height = screenheight - 200
        width = height * aspectratio
    newimage = original.resize((int(width), int(height)))
    root.geometry(f"{newimage.width + 20}x{newimage.height+100}")
    tutorial = tkinter.Label(root, text="请框选希望用于镜像的区域，框选完成后关闭本窗口", font=("微软雅黑",int((newimage.width+20)/33)))
    tutorial.pack(side="top", padx=10,fill=tkinter.BOTH,expand=True)
    framegrid = tkinter.Frame(root)
    framegrid.pack()
    quitbutton=tkinter.Button(framegrid,text="重新选择图片",command=quit)
    quitbutton.grid(row=0,column=0,padx=10)
    quit4realbutton = tkinter.Button(framegrid, text="退出", command=quit4real)
    quit4realbutton.grid(row=0,column=1,padx=10)
    canvas = tkinter.Canvas(root, width=newimage.width, height=newimage.height)
    canvas.pack(side="bottom",padx=10,pady=10)
    #canvas.pack(padx=10, pady=10)
    if original_dir.endswith(('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG')):
        originaltk = ImageTk.PhotoImage(newimage)
        canvaspic=canvas.create_image(0, 0, anchor=tkinter.NW, image=originaltk)
    elif original_dir.endswith(('.gif','.GIF')):
        def animate(animateindex):
            global canvaspic,originaltk
            try:
                image = frames[animateindex].resize((int(newwidth) - 20, int(newheight) - 100))
                originaltk = ImageTk.PhotoImage(image)
                canvas.itemconfig(canvaspic, image=originaltk)
                canvas.config(width=newwidth - 20, height=newheight - 100)
                tutorial.config(font=("微软雅黑", int((image.width + 20) / 33)))
            except NameError:
                canvas.itemconfig(canvaspic, image=framestk[animateindex])
            animateindex+=1
            if animateindex==len(frames):
                animateindex=0
            root.after(duration,lambda:animate(animateindex))

        def getallframes():
            global frames,framestk
            with imageio.get_reader(original_dir) as reader:
                frames=[]
                framestk=[]
                for image in reader:
                    image=Image.fromarray(image)
                    frames.append(image)
                    imagetk=ImageTk.PhotoImage(image)
                    framestk.append(imagetk)

        getallframes()
        canvaspic = canvas.create_image(0, 0, anchor=tkinter.NW, image=framestk[0])
        animate(0)

    canvas.bind("<Button-1>", mousepress)
    canvas.bind("<B1-Motion>", mousemove)
    canvas.bind("<ButtonRelease-1>", mouserelease)
    root.bind("<Configure>",windowresize)
    root.mainloop()

    if changepicindi==0 and doquit==0:
        print("文件处理中...")
        time = datetime.datetime.now()
        formatted_time = time.strftime("%Y%m%d%H%M%S")
        os.makedirs(f"{current_dir}\outputs", exist_ok=True)
        os.makedirs(f"{current_dir}\original_images", exist_ok=True)
    if extension==".gif" or extension==".GIF":
        with imageio.get_reader(original_dir) as reader:
            outputdir=f"{current_dir}\outputs\{original_name}_output_{formatted_time}{extension}"
            images=[]
            for image in reader:
                img=Image.fromarray(image)
                img=img.resize((int(newwidth) - 20, int(newheight) - 100))
                croppedimage=img.crop((clickx, clicky, releasex, releasey))
                if mode == 1 or mode == 2:
                    flipped=croppedimage.transpose(Image.FLIP_LEFT_RIGHT)
                    frameoutput = Image.new('RGB', (croppedimage.width * 2, croppedimage.height))
                elif mode == 3 or mode == 4:
                    flipped=croppedimage.transpose(Image.FLIP_TOP_BOTTOM)
                    frameoutput = Image.new('RGB', (croppedimage.width, croppedimage.height * 2))
                if mode == 1:
                    frameoutput.paste(croppedimage, (0, 0))
                    frameoutput.paste(flipped, (croppedimage.width, 0))
                elif mode == 2:
                    frameoutput.paste(flipped, (0, 0))
                    frameoutput.paste(croppedimage, (croppedimage.width, 0))
                elif mode == 3:
                    frameoutput.paste(croppedimage, (0, 0))
                    frameoutput.paste(flipped, (0, croppedimage.height))
                elif mode == 4:
                    frameoutput.paste(flipped, (0, 0))
                    frameoutput.paste(croppedimage, (0, croppedimage.height))
                images.append(np.array(frameoutput))
        imageio.mimsave(outputdir,images,fps=fps,loop=0)
    else:
        croppedimage = newimage.crop((clickx, clicky, releasex, releasey))
        if mode == 1 or mode == 2:
            flipped = croppedimage.transpose(Image.FLIP_LEFT_RIGHT)
            if extension == ".png" or extension == ".PNG":
                output = Image.new('RGBA', (croppedimage.width * 2, croppedimage.height), (0, 0, 0, 0))
            else:
                output = Image.new('RGB', (croppedimage.width * 2, croppedimage.height))
        elif mode == 3 or mode == 4:
            flipped = croppedimage.transpose(Image.FLIP_TOP_BOTTOM)
            if extension == ".png" or extension == ".PNG":
                output = Image.new('RGBA', (croppedimage.width, croppedimage.height * 2), (0, 0, 0, 0))
            else:
                output = Image.new('RGB', (croppedimage.width, croppedimage.height * 2))
        if mode == 1:
            output.paste(croppedimage, (0, 0))
            output.paste(flipped, (croppedimage.width, 0))
        elif mode == 2:
            output.paste(flipped, (0, 0))
            output.paste(croppedimage, (croppedimage.width, 0))
        elif mode == 3:
            output.paste(croppedimage, (0, 0))
            output.paste(flipped, (0, croppedimage.height))
        elif mode == 4:
            output.paste(flipped, (0, 0))
            output.paste(croppedimage, (0, croppedimage.height))
        output.save(f"{current_dir}\outputs\{original_name}_output_{formatted_time}{extension}")
    print(f"已将输出存储为{current_dir}\outputs\{original_name}_output_{formatted_time}{extension}")

    if os.path.exists(f"{current_dir}\original_images\{original_name}{extension}"):
        #print(formatted_time)
        egg=int("egg")
        #egg
    elif savemode==0:
        os.rename(original_dir, f"{current_dir}\original_images\{original_name}{extension}")
    elif savemode==1 and original_dir.replace("/","\\")!=f"{current_dir}\original_images\{original_name}{extension}":
        shutil.copy(original_dir,f"{current_dir}\original_images\{original_name}{extension}")
    if savemode==0:
        print(f"已将原图移动至{current_dir}\original_images")
    elif savemode==1:
        print(f"已将原图复制至{current_dir}\original_images")

def imgdrop():
    global original,original_dir,original_name,extension,savemode

    def dragenter(event):
        event.widget.config(cursor="hand2")
        event.widget.config(bg="grey")
        photoselect.config(bg="grey")

    def dragleave(event):
        event.widget.config(cursor="")
        event.widget.config(bg="grey94")
        photoselect.config(bg="grey94")

    def drop(event):
        global original_dir,original_name,extension,savemode
        original_dir=list(event.widget.tk.splitlist(event.data))[0]
        if original_dir.endswith(('.png', '.jpg', '.jpeg', '.gif', '.PNG', '.JPG', '.JPEG', '.GIF')):
            original_name,extension=os.path.splitext(os.path.basename(original_dir))
            savemode=1
        else:
            print("不支持的文件类型")
            original_dir=None
        root.destroy()

    def quit():
        global doquit
        doquit=1
        root.destroy()

    root=TkinterDnD.Tk()
    root.title("选择照片")
    tutorial=tkinter.Label(root,text="请拖拽/粘贴照片到本窗口或直接选择照片", font=("微软雅黑", 15))
    tutorial.pack(side="top",padx=10)
    photoselect=tkinter.Label(root,height=10)
    photoselect.pack(side="bottom")
    quitbutton = tkinter.Button(root, text="退出", command=quit)
    quitbutton.pack()
    root.drop_target_register(DND_FILES)
    root.dnd_bind("<<DropEnter>>", dragenter)
    root.dnd_bind("<<DropLeave>>", dragleave)
    root.dnd_bind("<<Drop>>", drop)
    root.mainloop()

input("使用方法:按enter先选择模式并在新弹出的窗口中选择希望用于镜像的照片，或先将希望用于镜像的照片置于本文件同级目录，完成后按enter")
print("模式：1-原图置于左侧 2-原图置于右侧 3-原图置于上方 4-原图置于下方")
while mode not in [1,2,3,4]:
    modeselect()

if getattr(sys,'frozen',False):
    current_dir=os.path.dirname(sys.executable)
else:
    current_dir=os.path.dirname(os.path.abspath(__file__))
for root, dirs, files in os.walk(current_dir):
    if root == current_dir:
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.PNG', '.JPG', '.JPEG', '.GIF')):
                original_name,extension=os.path.splitext(file)
                original_dir = os.path.join(root, file)
                break

while True:
    try:
        mirror()
        input("按enter以退出...")
        break

    except NameError:
        print("未进行裁剪")

    except ValueError:
        if savemode == 0:
            os.rename(original_dir, f"{current_dir}\original_images\{original_name}_{formatted_time}{extension}")
            print(f"已将原图移动至{current_dir}\original_images")
        elif savemode == 1:
            shutil.copy(original_dir, f"{current_dir}\original_images\{original_name}_{formatted_time}{extension}")
            print(f"已将原图复制至{current_dir}\original_images")
        print(f"注意：由于{current_dir}\original_images文件夹中已存在同名文件，故将原图重命名为{original_name}_{formatted_time}{extension}后存储")
        input("按enter以退出...")
        break

    except (AttributeError,OSError):
        if doquit==1:
            break
        if changepicindi==0:
            print("未找到照片")
        imgdrop()
