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
swbtimes=1
filesaved=0
#changepicindi=0
#changemodeindi=0

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
    global original,imagedetected,output,rect,formatted_time,original_dir,canvaspic,newimage,aspectratio,duration,fps,changepicindi,changemodeindi,previousheight

    changepicindi=0
    changemodeindi=0

    original = Image.open(original_dir)
    if original_dir.endswith(('.gif','.GIF')):
        with imageio.get_reader(original_dir) as reader:
            duration = reader.get_meta_data()['duration']
            fps = 1000 / duration
    imagedetected = 1
    rect = None

    def create():
        if extension == ".gif" or extension == ".GIF":
            global processedimage, outputdir, processedimages
            with imageio.get_reader(original_dir) as reader:
                outputdir = f"{current_dir}\outputs\{original_name}_output_{formatted_time}{extension}"
                images = []
                processedimages = []
                for image in reader:
                    img = Image.fromarray(image).convert("RGBA")
                    images.append(img)
            del images[0]
            firstframe = Image.open(original_dir)
            images.insert(0, firstframe)
            for image in images:
                image = image.resize((int(newwidth) - 20, int(newheight) - 100))
                croppedimage = image.crop(
                    (min(clickx, releasex), min(clicky, releasey), max(clickx, releasex), max(clicky, releasey)))
                if mode == 1 or mode == 2:
                    flipped = croppedimage.transpose(Image.FLIP_LEFT_RIGHT)
                    frameoutput = Image.new('RGBA', (croppedimage.width * 2, croppedimage.height))
                elif mode == 3 or mode == 4:
                    flipped = croppedimage.transpose(Image.FLIP_TOP_BOTTOM)
                    frameoutput = Image.new('RGBA', (croppedimage.width, croppedimage.height * 2))
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
                processedimages.append(np.array(frameoutput))
        else:
            global output
            croppedimage = newimage.crop(
                (min(clickx, releasex), min(clicky, releasey), max(clickx, releasex), max(clicky, releasey)))
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

    def save():
        global formatted_time

        time = datetime.datetime.now()
        formatted_time = time.strftime("%Y%m%d%H%M%S")
        os.makedirs(f"{current_dir}\outputs", exist_ok=True)
        os.makedirs(f"{current_dir}\original_images", exist_ok=True)

        create()
        if extension == ".gif" or extension == ".GIF":
            imageio.mimsave(outputdir, processedimages, fps=fps, loop=0, disposal=2)
        else:
            output.save(f"{current_dir}\outputs\{original_name}_output_{formatted_time}{extension}")
        print(f"已将输出存储为{current_dir}\outputs\{original_name}_output_{formatted_time}{extension}")

        if os.path.exists(f"{current_dir}\original_images\{original_name}{extension}"):
            # print(formatted_time)
            egg = int("egg")
            # egg
        elif savemode == 0:
            os.rename(original_dir, f"{current_dir}\original_images\{original_name}{extension}")
        elif savemode == 1 and original_dir.replace("/",
                                                    "\\") != f"{current_dir}\original_images\{original_name}{extension}":
            shutil.copy(original_dir, f"{current_dir}\original_images\{original_name}{extension}")
        if savemode == 0:
            print(f"已将原图移动至{current_dir}\original_images")
        elif savemode == 1:
            print(f"已将原图复制至{current_dir}\original_images")

    def windowresize(event):
        global newimage,originaltk,canvaspic,last_time,newheight,newwidth,rect,releasex,releasey,previousheight
        newheight=root.winfo_height()
        newwidth=int((newheight-100)*aspectratio+20)
        if previousheight!=newheight:
            if rect:
                canvas.delete(rect)
            try:
                del releasex, releasey
            except NameError:
                pass
        current_time = time.time()
        try:
            last_time = last_time
        except NameError:
            last_time = 0
        if abs(newwidth - root.winfo_width()) > 5 and (current_time - last_time) > 0.005:
            try:
                root.geometry(f"{newwidth}x{newheight}")
                last_time = current_time
            except tkinter.TclError:
                pass
        if original_dir.endswith(('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG')):
            try:
                newimage = original.resize((int(newwidth) - 20, int(newheight) - 100))
            except ValueError:
                pass
            originaltk = ImageTk.PhotoImage(newimage)
            canvas.itemconfig(canvaspic, image=originaltk)
            canvas.config(width=newwidth - 20, height=newheight - 100)
            tutorial.config(font=("微软雅黑", int((newimage.width + 20) / 33)))
        previousheight=newheight

    def mousepress(event):
        global clickx, clicky
        clickx = event.x
        clicky = event.y

    def mousemove(event):
        global rect
        if rect:
            canvas.delete(rect)
        dispx=event.x
        dispy=event.y
        if event.x<2:
            dispx=2
        if event.y<2:
            dispy=2
        if event.x>int(newwidth)-23:
            dispx=int(newwidth)-23
        if event.y>int(newheight)-101:
            dispy=int(newheight)-101
        rect = canvas.create_rectangle(clickx, clicky, dispx, dispy, outline='red')
        #print(event.x)

    def mouserelease(event):
        global releasex, releasey, filesaved
        filesaved = 0
        releasex = event.x
        releasey = event.y
        if event.x<0:
            releasex=0
        if event.y<0:
            releasey=0
        if event.x>newwidth-20:
            releasex=newwidth-20
        if event.y>newheight-100:
            releasey=newheight-100

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

    def preview():
        global previewwidth,previewheight,previewframe,rootp,animating
        try:
            egg=clickx
            try:
                rootp.destroy()
            except (NameError, tkinter.TclError):
                pass

            def swb():
                global swbtimes,filesaved
                try:
                    save()
                    #pass
                except ValueError:
                    if swbtimes==1:
                        if savemode == 0:
                            os.rename(original_dir,
                                      f"{current_dir}\original_images\{original_name}_{formatted_time}{extension}")
                            print(f"已将原图移动至{current_dir}\original_images")
                        elif savemode == 1:
                            shutil.copy(original_dir,
                                        f"{current_dir}\original_images\{original_name}_{formatted_time}{extension}")
                            print(f"已将原图复制至{current_dir}\original_images")
                        print(
                            f"注意：由于{current_dir}\original_images文件夹中已存在同名文件，故将原图重命名为{original_name}_{formatted_time}{extension}后存储")
                if swbtimes==1:
                    swbtext=""
                else:
                    swbtext=f"({swbtimes})"
                #print(swbtimes)
                showsaved.config(text=f"保存成功!{swbtext}")
                swbtimes+=1
                filesaved=1

            create()
            rootp = tkinter.Toplevel()
            rootp.title("预览")
            screenwidth = rootp.winfo_screenwidth()
            screenheight = rootp.winfo_screenheight()
            rootp.maxsize = (screenwidth - 200, screenheight - 200)
            rootp.resizable(False, False)
            previewwidth = max(clickx, releasex) - min(clickx, releasex)
            previewheight = max(clicky, releasey) - min(clicky, releasey)
            if mode == 1 or mode == 2:
                previewwidth *= 2
            elif mode == 3 or mode == 4:
                previewheight *= 2
            aspectratio = previewwidth / previewheight
            if previewwidth > screenwidth - 200:
                previewwidth = screenwidth - 200
                previewheight = previewwidth / aspectratio
            if previewheight > screenheight - 200:
                previewheight = screenheight - 200
                previewwidth = previewheight * aspectratio
            rootp.geometry(f"{int(previewwidth) + 20}x{int(previewheight) + 90}")
            # label=tkinter.Label(rootp,text="将会保存的图像如下，可关闭窗口修改框选范围")
            # label.pack()
            savebutton=tkinter.Button(rootp,text="保存",command=swb)
            savebutton.pack()
            canvas = tkinter.Canvas(rootp, width=previewwidth, height=previewheight)
            canvas.pack(padx=10, pady=10)
            showsaved=tkinter.Label(rootp,text="",font=("微软雅黑",15))
            showsaved.pack()
            # canvas.pack(padx=10, pady=10)
            if original_dir.endswith(('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG')):
                newimage = output.resize((int(previewwidth), int(previewheight)))
                originaltk = ImageTk.PhotoImage(newimage)
                previewpic = canvas.create_image(0, 0, anchor=tkinter.NW, image=originaltk)
            elif original_dir.endswith(('.gif', '.GIF')):
                def animatepreview(animateindex):
                    global previewframe, previewtk
                    proceed = True
                    try:
                        image = previewframes[animateindex].resize((int(previewwidth), int(previewheight)))
                        previewtk = ImageTk.PhotoImage(image)
                        canvas.itemconfig(previewframe, image=previewtk)
                    except NameError:
                        canvas.itemconfig(previewframe, image=previewframestk[animateindex])
                    except tkinter.TclError:
                        proceed = False
                    if proceed == True:
                        animateindex += 1
                        if animateindex == len(frames):
                            animateindex = 0
                        root.after(duration, lambda: animatepreview(animateindex))

                def getallpreviewframes():
                    global previewframes, previewframestk
                    previewframes = []
                    previewframestk = []
                    for image in processedimages:
                        image = Image.fromarray(image)
                        previewframes.append(image)
                        imagetk = ImageTk.PhotoImage(image)
                        previewframestk.append(imagetk)

                getallpreviewframes()
                previewframe = canvas.create_image(0, 0, anchor=tkinter.NW, image=previewframestk[0])
                animatepreview(0)
            root.mainloop()
        except NameError:
            print("未框选区域")

    def reselmode():
        global mode,changemodeindi
        mode=None
        changemodeindi=1
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
    previousheight=root.winfo_height()
    tutorial = tkinter.Label(root, text="请框选希望用于镜像的区域，框选完成后关闭本窗口", font=("微软雅黑",int((newimage.width+20)/33)))
    tutorial.pack(side="top", padx=10,fill=tkinter.BOTH,expand=True)
    framegrid = tkinter.Frame(root)
    framegrid.pack()
    quitbutton=tkinter.Button(framegrid,text="重新选择图片",command=quit)
    quitbutton.grid(row=0,column=0,padx=10)
    reselmodebutton=tkinter.Button(framegrid,text="重新选择模式",command=reselmode)
    reselmodebutton.grid(row=0,column=1,padx=10)
    previewbutton=tkinter.Button(framegrid, text="预览", command=preview)
    previewbutton.grid(row=0,column=2,padx=10)
    quit4realbutton = tkinter.Button(framegrid, text="退出", command=quit4real)
    quit4realbutton.grid(row=0,column=3,padx=10)
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
            except ValueError:
                pass
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
            del frames[0]
            del framestk[0]
            firstframe=Image.open(original_dir)
            firstframetk=ImageTk.PhotoImage(firstframe)
            frames.insert(0,firstframe)
            framestk.insert(0,firstframetk)

        getallframes()
        canvaspic = canvas.create_image(0, 0, anchor=tkinter.NW, image=framestk[0])
        animate(0)

    canvas.bind("<Button-1>", mousepress)
    canvas.bind("<B1-Motion>", mousemove)
    canvas.bind("<ButtonRelease-1>", mouserelease)
    root.bind("<Configure>",windowresize)
    root.mainloop()

    if changemodeindi==1:
        egg=int(egg)

    if changepicindi==0 and doquit==0:
        print("文件处理中...")

    if filesaved==0:
        save()

def imgdrop():
    global original_dir,original_name,extension,savemode,swbtimes

    swbtimes=1

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
#print("模式：1-原图置于左侧 2-原图置于右侧 3-原图置于上方 4-原图置于下方")

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
        while mode not in [1, 2, 3, 4]:
            modeselect()
        mirror()
        input("按enter以退出...")
        break

    except NameError:
        if changemodeindi==0:
            print("未进行裁剪")
        changemodeindi=0

    except ValueError:
        if swbtimes==1:
            if savemode == 0:
                os.rename(original_dir, f"{current_dir}\original_images\{original_name}_{formatted_time}{extension}")
                print(f"已将原图移动至{current_dir}\original_images")
            elif savemode == 1:
                shutil.copy(original_dir, f"{current_dir}\original_images\{original_name}_{formatted_time}{extension}")
                print(f"已将原图复制至{current_dir}\original_images")
            print(
                f"注意：由于{current_dir}\original_images文件夹中已存在同名文件，故将原图重命名为{original_name}_{formatted_time}{extension}后存储")
        input("按enter以退出...")
        break

    except (AttributeError,OSError):
        if doquit==1:
            break
        if changepicindi==0:
            print("未找到照片")
        imgdrop()
