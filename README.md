# 镜像图片制作器

## 介绍

顾名思义，就是个快速自动制作那种你可能经常在QQ群里见到的难绷镜像图片的小工具

之前自己想做那种图的时候感觉好像没见过类似的工具，自己手动做又嫌有点麻烦，于是一拍脑袋写了这个

是我在制作这些图片.jpg

刚开始自学python孩子不懂事乱写的，能跑就行（

需要[Pillow](https://pillow.readthedocs.io/en/stable/)库，使用
```
pip install Pillow
```
安装即可

v2.0版本额外需要[tkinterdnd2](https://github.com/Eliav2/tkinterdnd2)库，使用
```
pip install tkinterdnd2
```
安装

v2.3版本起需要[numpy](https://numpy.org/)和[imageio](https://imageio.readthedocs.io/en/stable/)库，分别使用
```
pip install numpy
```
和
```
pip install imageio
```
安装

**支持的扩展名：.jpg .jpeg .png .gif（对.gif的支持尚不完善，需使用不带有透明部分的.gif图片以达到最好效果）**

**输出会保留原扩展名**

## 使用方法

随便新建个空文件夹，把mirrorpic-creator.py扔进去然后运行就行，剩下的步骤程序里有说

注意只支持程序的同级文件夹中包含一张图片（文件夹的子文件夹里多少张都行反正不会读取的），大于一张的话会从这几张图片里随机选出来一张处理

输出会自动放进新建的outputs文件夹，原图会自动放进original_images文件夹
