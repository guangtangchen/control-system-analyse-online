# 控制系统性能在线分析
一款能够根据输入的传递函数进行控制系统基本性能分析的微信小程序
### 简介
本项目灵感来源于19年末对《自动控制原理》课程的复习。通常我们分析控制系统是用matlab，然鹅出去复习偶尔没带电脑，以及matlab过于强大以至于体积实在太大了，杀鸡焉用牛刀，想者要是能在手机上用就好了，因此写了一个实现这个功能的小程序。
### 功能
根据用户输入的传递函数，输出5张图片，分别是step response, impulse response, bode图, nyquist图，root locus图。
### 实现
后台主要是调用了python control库的相关函数，服务器单次计算时间大约在4S左右。
### 体验
![图片未能正确显示，可以到微信里搜索小程序：根轨迹](http://www.guangtang.xyz/resource/genguiji_small.JPG)
