import os
import tkinter
from PIL import Image,ImageTk

input("使用方法:将希望用于镜像的照片置于本文件同级目录，完成后按enter")
print("模式：1-原图置于左侧 2-原图置于右侧")
while True:
    try:
        mode=int(input("请选择模式:"))
        if mode==1 or mode==2:
            break
        else:
            egg=int("egg")
    except ValueError:
        print("输入有误")
current_dir=os.path.dirname(os.path.abspath(__file__))
#print(current_dir)
for root, dirs, files in os.walk(current_dir):
    if root == current_dir:
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                original_name,extension=os.path.splitext(file)
                original_dir = os.path.join(root, file)
                break

try:
    original = Image.open(original_dir)
    rect = None
    def mousepress(event):
        global clickx,clicky
        clickx=event.x
        clicky=event.y
    def mousemove(event):
        global rect
        if rect:
            canvas.delete(rect)
        rect=canvas.create_rectangle(clickx, clicky, event.x, event.y, outline='red')
    def mouserelease(event):
        global releasex,releasey
        releasex=event.x
        releasey=event.y

    root = tkinter.Tk()
    root.title("裁剪照片")
    tutorial=tkinter.Label(root,text="请框选希望用于镜像的区域，框选完成后关闭本窗口",font=("微软雅黑",25))
    tutorial.pack(side="top",padx=10)
    screenwidth=root.winfo_screenwidth()
    screenheight=root.winfo_screenheight()
    root.maxsize=(screenwidth-200,screenheight-200)
    aspectratio=original.width/original.height
    width=original.width
    height=original.height
    if width>screenwidth-200:
        width=screenwidth-200
        height=width/aspectratio
    if height>screenheight-200:
        height=screenheight-200
        width=height*aspectratio
    newimage=original.resize((int(width),int(height)))
    root.geometry(f"{newimage.width+20}x{newimage.height+30}")
    canvas=tkinter.Canvas(root,width=newimage.width,height=newimage.height)
    canvas.pack(side="bottom",padx=10,pady=10)
    originaltk=ImageTk.PhotoImage(newimage)
    canvas.create_image(0,0,anchor=tkinter.NW,image=originaltk)
    canvas.bind("<Button-1>",mousepress)
    canvas.bind("<B1-Motion>",mousemove)
    canvas.bind("<ButtonRelease-1>",mouserelease)
    root.mainloop()

    croppedimage=newimage.crop((clickx,clicky,releasex,releasey))
    #croppedimage.show()

    #print(original_dir)
    print("文件处理中...")
    flipped=croppedimage.transpose(Image.FLIP_LEFT_RIGHT)
    output=Image.new('RGB',(croppedimage.width*2,croppedimage.height))
    if mode==1:
        output.paste(croppedimage,(0,0))
        output.paste(flipped,(croppedimage.width,0))
    elif mode==2:
        output.paste(flipped,(0, 0))
        output.paste(croppedimage,(croppedimage.width, 0))
    os.makedirs(f"{current_dir}\outputs",exist_ok=True)
    output.save(f"{current_dir}\outputs\{original_name}_output{extension}")
    os.makedirs(f"{current_dir}\original_images", exist_ok=True)
    os.rename(original_dir,f"{current_dir}\original_images\{original_name}{extension}")
    print(f"已将输出存储为{current_dir}\outputs\{original_name}_output{extension}")
    print(f"已将原图移动至{current_dir}\original_images")
except NameError:
    print("未找到照片或未进行裁剪")
input("按enter以退出...")
