import os
import tkinter
import datetime
import shutil
from PIL import Image,ImageTk
from tkinterdnd2 import *

imagedetected=0
original_dir=None
formatted_time=None
savemode=0

def mirror():
    global original,imagedetected,output,rect,formatted_time
    original = Image.open(original_dir)
    imagedetected = 1
    rect = None

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

    root = tkinter.Tk()
    root.title("裁剪照片")
    tutorial = tkinter.Label(root, text="请框选希望用于镜像的区域，框选完成后关闭本窗口", font=("微软雅黑", 25))
    tutorial.pack(side="top", padx=10)
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    root.maxsize = (screenwidth - 200, screenheight - 200)
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
    root.geometry(f"{newimage.width + 20}x{newimage.height + 80}")
    canvas = tkinter.Canvas(root, width=newimage.width, height=newimage.height)
    canvas.pack(side="bottom", padx=10, pady=10)
    originaltk = ImageTk.PhotoImage(newimage)
    canvas.create_image(0, 0, anchor=tkinter.NW, image=originaltk)
    canvas.bind("<Button-1>", mousepress)
    canvas.bind("<B1-Motion>", mousemove)
    canvas.bind("<ButtonRelease-1>", mouserelease)
    root.mainloop()

    croppedimage = newimage.crop((clickx, clicky, releasex, releasey))

    print("文件处理中...")
    flipped = croppedimage.transpose(Image.FLIP_LEFT_RIGHT)
    output = Image.new('RGB', (croppedimage.width * 2, croppedimage.height))
    if mode == 1:
        output.paste(croppedimage, (0, 0))
        output.paste(flipped, (croppedimage.width, 0))
    elif mode == 2:
        output.paste(flipped, (0, 0))
        output.paste(croppedimage, (croppedimage.width, 0))
    time = datetime.datetime.now()
    formatted_time = time.strftime("%Y%m%d%H%M%S")
    os.makedirs(f"{current_dir}\outputs", exist_ok=True)
    output.save(f"{current_dir}\outputs\{original_name}_output_{formatted_time}{extension}")
    os.makedirs(f"{current_dir}\original_images", exist_ok=True)
    if savemode==0:
        os.rename(original_dir, f"{current_dir}\original_images\{original_name}{extension}")
    elif savemode==1:
        shutil.copy(original_dir,f"{current_dir}\original_images\{original_name}{extension}")
    print(f"已将输出存储为{current_dir}\outputs\{original_name}_output_{formatted_time}{extension}")
    if savemode==0:
        print(f"已将原图移动至{current_dir}\original_images")
    elif savemode==1:
        print(f"已将原图复制至{current_dir}\original_images")

def imgdrop():
    global original,original_dir,original_name,extension,savemode

    def dragenter(event):
        event.widget.config(cursor="hand2")

    def dragleave(event):
        event.widget.config(cursor="")

    def drop(event):
        global original_dir,original_name,extension,savemode
        original_dir=list(event.widget.tk.splitlist(event.data))[0]
        if original_dir.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            original_name,extension=os.path.splitext(os.path.basename(original_dir))
            savemode=1
        else:
            print("不支持的文件类型")
            original_dir=None
        root.destroy()
    root=TkinterDnD.Tk()
    root.title("选择照片")
    tutorial=tkinter.Label(root,text="请拖拽/粘贴照片到本窗口或直接选择照片", font=("微软雅黑", 15))
    tutorial.pack(side="top",padx=10)
    photoselect=tkinter.Label(root,height=10)
    photoselect.pack(side="bottom")
    root.drop_target_register(DND_FILES)
    root.dnd_bind("<<DropEnter>>", dragenter)
    root.dnd_bind("<<DropLeave>>", dragleave)
    root.dnd_bind("<<Drop>>", drop)
    root.mainloop()

input("使用方法:按enter先选择模式并在新弹出的窗口中选择希望用于镜像的照片，或先将希望用于镜像的照片置于本文件同级目录，完成后按enter")
print("模式：1-原图置于左侧 2-原图置于右侧")
while True:
    try:
        output=None
        mode=int(input("请选择模式:"))
        if mode==1 or mode==2:
            break
        else:
            egg=int("egg")
    except ValueError:
        print("输入有误")
current_dir=os.path.dirname(os.path.abspath(__file__))
for root, dirs, files in os.walk(current_dir):
    if root == current_dir:
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
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

    except FileExistsError:
        if savemode == 0:
            os.rename(original_dir, f"{current_dir}\original_images\{original_name}{extension}")
        elif savemode == 1:
            shutil.copy(original_dir, f"{current_dir}\original_images\{original_name}_{formatted_time}{extension}")
        print(f"已将输出存储为{current_dir}\outputs\{original_name}_output_{formatted_time}{extension}")
        if savemode == 0:
            print(f"已将原图移动至{current_dir}\original_images")
        elif savemode == 1:
            print(f"已将原图复制至{current_dir}\original_images")
        print(f"注意：由于{current_dir}\original_images文件夹中已存在同名文件，故将原图重命名为{original_name}_{formatted_time}{extension}后存储")
        input("按enter以退出...")
        break

    except PermissionError:
        if savemode == 0:
            os.rename(original_dir, f"{current_dir}\original_images\{original_name}{extension}")
        elif savemode == 1:
            shutil.copy(original_dir, f"{current_dir}\original_images\{original_name}_{formatted_time}{extension}")
        print(f"已将输出存储为{current_dir}\outputs\{original_name}_output_{formatted_time}{extension}")
        if savemode == 0:
            print(f"已将原图移动至{current_dir}\original_images")
        elif savemode == 1:
            print(f"已将原图复制至{current_dir}\original_images")
        print(f"注意：由于{current_dir}\original_images文件夹中已存在同名文件，故将原图重命名为{original_name}_{formatted_time}{extension}后存储")
        input("按enter以退出...")
        break

    except AttributeError:
        print("未找到照片")
        imgdrop()