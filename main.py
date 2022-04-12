# encoding: utf-8
import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "Lib\site-packages\PyQt5\Qt5\plugins"
import sys
from PyQt5 import QtMultimedia
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
# 导入QT,其中包含一些常量，例如颜色等
from PyQt5.QtCore import Qt
# 导入常用组件
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel
# 使用调色板等
from PyQt5.QtGui import QIcon, QMovie
import os
import random
import pygame


class DemoWin(QMainWindow):
    def __init__(self):
        super(DemoWin, self).__init__()
        self.initUI()
        # 初始化，不规则窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()
        # 是否跟随鼠标
        self.is_follow_mouse = False
        self.move(1650,700)

        # 设置托盘选项
        iconpath="red.ico"
        #右键菜单
        quit_action = QAction(u'退出', self, triggered=self.quit)
        quit_action.setIcon(QIcon(iconpath))
        showwin = QAction(u'显示', self, triggered=self.showwin)
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(showwin)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(iconpath))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

        #窗口透明程度
        self.setWindowOpacity(1)

        if not self.is_follow_mouse:
            # 每隔一段时间做个动作
            self.timer = QTimer()
            self.timer.timeout.connect(self.randomAct)
            self.timer.start(7000)
        
        self.condition = 0
        self.wav_condition = 1
        self.music_condition = 1

        self.wav_files_zh = []
        for key in os.listdir("resources/Red/wav/zh"):
            if key == "红_干员报到.wav":
                file = QUrl.fromLocalFile('./resources/Red/wav/jp/红_干员报到.wav') # 音频文件路径
                content = QtMultimedia.QMediaContent(file)
                self.player = QtMultimedia.QMediaPlayer()
                self.player.setMedia(content)
                self.player.play()
                continue
            self.wav_files_zh.append("./resources/Red/wav/zh/" + key)

        self.wav_files_jp = []
        for key in os.listdir("resources/Red/wav/jp"):
            if key == "红_干员报到.wav":
                continue
            self.wav_files_jp.append("./resources/Red/wav/jp/" + key)

        self.current_wav = 1

        # 每隔一段时间做个动作
        self.timer1 = QTimer()
        self.timer1.start(20000)
        self.timer1.timeout.connect(self.talk)

        self.pet1 = []
        for i in os.listdir("resources/Red/gif_0"):
            if i == 'Default.gif':
                continue
            self.pet1.append("resources/Red/gif_0/" + i)

        self.pet2 = []
        for i in os.listdir("resources/Red/gif_1"):
            if i == 'Default.gif':
                continue
            self.pet2.append("resources/Red/gif_1/" + i)

        self.pet = 1

        self.bgm = []
        self.bgm_default = ("resources/bgm/Default.mp3")
        for i in os.listdir("resources/bgm"):
            if i == 'Default.mp3':
                continue
            self.bgm.append("resources/bgm/" + i)
        
        pygame.mixer.music.set_volume(0.6)
        self.track = pygame.mixer.music.load(self.bgm_default)
        pygame.mixer.music.play()
    
    def initUI(self):
        self.resize(400, 400)
        self.label1 = QLabel("", self)
        self.label1.setStyleSheet("font:15pt '楷体';border-width: 1px;color:red;")  # 设置边框
        # 使用label来显示动画
        self.label = QLabel("", self)
        # label大小设置为动画大小
        self.label.setFixedSize(200, 200)

        # 设置动画路径
        self.movie = QMovie("./resources/Red/gif_0/Default.gif")
        #宠物大小
        self.movie.setScaledSize(QSize(200, 200))
        # 将动画添加到label中
        self.label.setMovie(self.movie)
        # 开始播放动画
        self.movie.start()

        #透明窗口
        self.setWindowOpacity(1)

        # 添加窗口标题
        self.setWindowTitle("GIFDemo")

    '''鼠标左键按下时, 宠物将和鼠标位置绑定'''
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
    
    '''鼠标移动, 则宠物也移动'''
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            if self.pet == 1:
                self.movie = QMovie('.resources/Red/gif_0/Default.gif')
            else:
                self.movie = QMovie('.resources/Red/gif_1/Default.gif')
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    '''鼠标释放时, 取消绑定'''
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.randomAct()

    def enterEvent(self, event):  # 鼠标移进时调用
        #print('鼠标移入')
        self.setCursor(Qt.ClosedHandCursor)  # 设置鼠标形状。需要from PyQt5.QtGui import QCursor,from PyQt5.QtCore import Qt
        '''
        Qt.PointingHandCursor   指向手            Qt.WaitCursor  旋转的圆圈
        ArrowCursor   正常箭头                 Qt.ForbiddenCursor 红色禁止圈
        Qt.BusyCursor      箭头+旋转的圈      Qt.WhatsThisCursor   箭头+问号
        Qt.CrossCursor      十字              Qt.SizeAllCursor    箭头十字
        Qt.UpArrowCursor 向上的箭头            Qt.SizeBDiagCursor  斜向上双箭头
        Qt.IBeamCursor   I形状                 Qt.SizeFDiagCursor  斜向下双箭头
        Qt.SizeHorCursor  水平双向箭头          Qt.SizeVerCursor  竖直双向箭头
        Qt.SplitHCursor                        Qt.SplitVCursor  
        Qt.ClosedHandCursor   非指向手          Qt.OpenHandCursor  展开手
        '''
        # self.unsetCursor()   #取消设置的鼠标形状

    # 当按右键的时候，这个event会被触发
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        default_music = menu.addAction("切换默认音乐")
        if self.music_condition == 1:
            music_mes = "暂停音乐"
        else:
            music_mes = "播放音乐"
        play_music = menu.addAction(music_mes)
        devoice = menu.addAction("减小音乐音量")
        hevoice = menu.addAction("增加音乐音量")
        if self.wav_condition == 1:
            sound_mes = "关闭干员语音"
        else:
            sound_mes = "开启干员语音"
        clothes = menu.addAction("换皮肤")
        reset_lau = menu.addAction("中日文干员语音切换")
        sound = menu.addAction(sound_mes)
        hide = menu.addAction("隐藏")
        quitAction = menu.addAction("退出")
        
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            qApp.quit()
        if action == hide:
            self.setWindowOpacity(0)
        if action == default_music:
            self.track = pygame.mixer.music.load(self.bgm_default)
            pygame.mixer.music.play()
        if action == play_music:
            if self.music_condition == 1:
                pygame.mixer.music.stop()
                self.music_condition = 0
            else:
                smusic = random.choice(self.bgm)
                print(smusic)
                self.track = pygame.mixer.music.load(smusic)
                pygame.mixer.music.play()
                self.music_condition = 1
        if action == clothes:
            self.pet = 1 if self.pet == 2 else 2
            self.randomAct()
        if action == sound:
            self.wav_condition = 0 if self.wav_condition == 1 else 1
        if action == reset_lau:
            self.current_wav = 1 if self.current_wav == 2 else 2
        if action == devoice and pygame.mixer.music.get_volume() > 0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.2)
            print("当前音量为：" + str(pygame.mixer.music.get_volume()))
        if action == hevoice and pygame.mixer.music.get_volume() < 1:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.2)
            print("当前音量为：" + str(pygame.mixer.music.get_volume()))

    '''退出程序'''
    def quit(self):
        self.close()
        sys.exit()
    
    '''显示'''
    def showwin(self):
        self.setWindowOpacity(1)
    
    '''随机做一个动作'''
    def randomAct(self):
        if not pygame.mixer.music.get_busy() and self.music_condition == 1:
            smusic = random.choice(self.bgm)
            print(smusic)
            self.track = pygame.mixer.music.load(smusic)
            pygame.mixer.music.play()
        if not self.is_follow_mouse:
            print("状态变更")
            if self.pet == 1:
                sstr = random.choice(self.pet1)
            else:
                sstr = random.choice(self.pet2)
            print(sstr)
            self.movie = QMovie(sstr)
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.label.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.condition=1

    def talk(self):
        if self.wav_condition:
            self.player.stop()
            if self.current_wav == 1:
                path = random.choice(list(self.wav_files_jp))
            else:
                path = random.choice(list(self.wav_files_zh))
            print(path)
            file = QUrl.fromLocalFile(path) # 音频文件路径
            content = QtMultimedia.QMediaContent(file)
            self.player = QtMultimedia.QMediaPlayer()
            self.player.setMedia(content)
            self.player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("red.ico"))
    pygame.init()
    # 创建一个主窗口
    mainWin = DemoWin()
    # 显示
    mainWin.show()
    # 主循环
    sys.exit(app.exec_())