
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtMultimedia import  QMediaPlayer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ui.window_login import Ui_MainWindow as login_window
from ui.main import Ui_MainWindow as main_window
from ui.setup import Ui_MainWindow as setup_window

from LinearEquation import LE
from LinearEquation import LE_D

import sys
import os
from opencv_engine import opencv_engine
from PIL import Image
import pandas as pd
import cv2
import numpy as np
import time
import threading
from playsound import playsound

from firebase import Firebase
from yolo_Yee import YOLO
from yolo_Yee_num import YOLO as YOLO_num
# from yolo_Yee_num import YOLO
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path

timestr=time.strftime("%Y%m%d-%H%M%S")
class PollTimeThread(QtCore.QThread):
    """
    This thread works as a timer.
    """
    update = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(PollTimeThread, self).__init__(parent)

    def run(self):
        while True:
            time.sleep(1)
            if self.isRunning():
                # emit signal
                self.update.emit()
            else:
                return
#Login
class LoginWindow_controller(QtWidgets.QMainWindow):
    windowlist1=[]
    windowlist2=[]
    windowlist3=[]

    def __init__(self):
        super().__init__() 
        self.ui =login_window()
        self.mail_login=""
        self.ui.setupUi(self)
        self.setup_control()
        self.ui.pushButton_1.clicked.connect(self.goMain)
        self.ui.pushButton_1.setShortcut('enter')  #绑定快捷键
        
        self.ui.pushButton_2.clicked.connect(QCoreApplication.instance().quit)
        self.ui.radioButton_setup.clicked.connect(self.goregister)
        self.ui.radioButton_login.setChecked(True)
        

    def goMain  (self):
        self.firebase=Firebase()
        app=self.firebase.app 
        self.mail_name=self.firebase.df["信箱"]
        self.password_name=self.firebase.df["密碼"] 
        self.combinebox=pd.concat([self.mail_name,self.password_name],axis=1)
        self.mail_login=self.ui.lineEdit_2.text()
        self.password=self.ui.lineEdit.text()
        self.mail_login_append=[]
        self.password_append=[]
        self.count=0
        global global_login_mail
        
        try:
            self.count=0
            self.mail_login_append=[]
            self.password_append=[]
            for i in self.combinebox["信箱"]:
                
                a=(i==self.mail_login)
                self.mail_login_append.append(a)
                if a==False:
                    self.count+=1
                print(self.count)    
            if self.count!=len(self.mail_login_append):
                for j in self.combinebox["密碼"]:
                    b=(j==self.password)
                    self.password_append.append(b)
                    
            if self.mail_login_append==self.password_append:
                print("登入成功")
                global_login_mail=self.ui.lineEdit_2.text()
                
                self.window2=MainWindow_controller()
                self.windowlist2.append(self.window2)
                self.close()
                self.window2.setWindowIcon(QtGui.QIcon(r"pictures\barrier.png"))
                self.window2.setWindowTitle("智慧型海上箱網防盜系統")
                self.window2.show()
                
            else:
                self.ui.label1_2.setFont(QFont('Arial',18))
                self.ui.label1_2.setAlignment(QtCore.Qt.AlignCenter)
                self.ui.label1_2.setText("請再試一次")
                print("請再試一次")
            return self.mail_login
        except:
            firebase_admin.delete_app(app)
            self.ui.label1_2.setFont(QFont('Arial',18))
            self.ui.label1_2.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.label1_2.setText("請再試一次")
        
        
    def goregister (self):
        
        self.window3=Setup_controller()
        self.windowlist3.append(self.window3)
        self.close()
        self.window3.setWindowIcon(QtGui.QIcon(r"pictures\barrier.png"))
        self.window3.setWindowTitle("智慧型海上箱網防盜系統")
        self.window3.show()   

    def setup_control(self):
        # TODO
        self.img_path = r'pictures\UI_logo.png'
        self.display_img()

    def display_img(self):
        self.img = cv2.imread(self.img_path)
        height, width, channel = self.img.shape
        bytesPerline = 3 * width
        self.qimg = QImage(self.img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.ui.label1.setPixmap(QPixmap.fromImage(self.qimg))


    
    
#Register
class Setup_controller(QtWidgets.QMainWindow):
    windowlist1=[]
    windowlist2=[]
    

    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = setup_window()
        self.ui.setupUi(self)
        self.setup_control()
        self.ui.pushButton.clicked.connect(self.register)
        self.ui.pushButton_2.clicked.connect(QCoreApplication.instance().quit)
        self.ui.radioButton_login.clicked.connect(self.gologin)
        self.ui.radioButton_setup.setChecked(True)
        self.windowlist4=[]
        
    def gologin(self):
        self.window4=LoginWindow_controller()
        self.windowlist4.append(self.window4)
        self.window4.setWindowIcon(QtGui.QIcon(r"pictures\barrier.png"))
        self.window4.setWindowTitle("智慧型海上箱網防盜系統")
        self.close()
        self.window4.show()


    def register(self):
        self.cred = credentials.Certificate(r'firebase\userbase-a8b89-firebase-adminsdk-m7weo-80d894d357.json')
        self.app=firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        
        
        self.str_name= self.ui.lineEdit_2.text()
        
        self.str_user= self.ui.lineEdit_4.text()
        if( self.str_user.find("@") == -1 or not self.str_user.endswith('.com')):
            print("Wrong Email")
        self.str_phone= self.ui.lineEdit_3.text()
        self.str_password= self.ui.lineEdit.text()
        flag=False

            

        if  (not self.str_name==None) and (not self.str_password==None) and (not self.str_phone==None) and (not self.str_user==None) :
            flag=True
            self.doc = {
            '姓名': self.str_name,
            '信箱': self.str_user,
            '電話':self.str_phone,
            '密碼':self.str_password
            }
            self.db = firestore.client()
            self.doc_ref = self.db.collection("User_name").document(self.str_name)
            # doc_ref提供一個set的方法，input必須是dictionary
            self.doc_ref.set(self.doc)

        if flag==True:
            
            self.window1=LoginWindow_controller()
            self.windowlist1.append(self.window1)
            self.window1.setWindowIcon(QtGui.QIcon(r"pictures\barrier.png"))
            self.window1.setWindowTitle("智慧型海上箱網防盜系統")
            self.close()
            self.window1.show()
            firebase_admin.delete_app(self.app)


    def goMain  (self):
        self.window2=MainWindow_controller()
        self.windowlist2.append(self.window2)
        self.window2.setWindowIcon(QtGui.QIcon(r"pictures\barrier.png"))
        self.window2.setWindowTitle("智慧型海上箱網防盜系統")
        self.close()
        self.window2.show()



    def setup_control(self):
        # TODO
        self.img_path = r'pictures\UI_logo.png'
        self.display_img()

    def display_img(self):
        self.img = cv2.imread(self.img_path)
        height, width, channel = self.img.shape
        bytesPerline = 3 * width
        self.qimg = QImage(self.img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.ui.label1.setPixmap(QPixmap.fromImage(self.qimg))


def cvImgtoQtImg(cvImg):  # 定义opencv图像转PyQt图像的函数
    QtImgBuf = cv2.cvtColor(cvImg, cv2.COLOR_BGR2BGRA)
    QtImg = QtGui.QImage(QtImgBuf.data, QtImgBuf.shape[1], QtImgBuf.shape[0], QtGui.QImage.Format_RGB32)
    return QtImg

#Main
class MainWindow_controller(QtWidgets.QMainWindow):
    videoplayer_state_dict={"stop":0,"play":1,"pause":2}

    windowlist1=[]
    windowlist2=[]
    def __init__(self):
        super().__init__() 
        self.num=1
        self.current_frame_no=0
        self.fileName=""
        self.mode=""
        self.ui = main_window()
        self.ui.setupUi(self) #初始UI
        self.setup_control()
        self.video_save_path=""
        self.video_fps=6
        self.gate=False
        self.bClose=False
        self.fencegate=False
        #設定按鈕 
        
        self.ui.pushButton_scan.clicked.connect(self.open_file) 
        self.ui.pushButton_logout.clicked.connect(self.gologin)
        self.ui.pushButton_leave.clicked.connect(QCoreApplication.instance().quit)        
        self.ui.pushButton_start.clicked.connect(self.onClick)
        

        self.btn_realtime_mode=self.ui.radioButton_2
        self.btn_video_mode=self.ui.radioButton
        self.btn_openfence=self.ui.radioButton_3
        
        self.btn_realtime_mode.toggled.connect(lambda :self.btnstate(self.btn_realtime_mode))
        self.btn_video_mode.toggled.connect(lambda :self.btnstate(self.btn_video_mode))
        self.btn_openfence.toggled.connect(lambda:self.btnstate(self.btn_openfence))

        self.btn_realtime_mode.clicked.connect(self.realtime)
        self.ui.pushButton_drawfence.setEnabled(False)
        self.ui.pushButton_scan.setEnabled(False)
        self.ui.pushButton_drawfence.clicked.connect(self.doroi)
        self.ui.pushButton_camera.clicked.connect(self.check)
        self.ui.label_2.setFont(QFont('Arial',20))
        self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.label_2.setText("請選擇模式")

        self.flag=[1]
        self.flagg=[1]
        self.Cordon_color = (255,255,0)
        self.mail_gate1=True
        self.mail_gate2=True
        self.mail_gate3=True
        
        
        #影片
        self.cap=None
        # self.cap=cv2.VideoCapture(r"pictures\0624_4_prof.avi")
        self.ui.label_video.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.label_video.setFont(QFont('Arial',15))
        self.ui.label_video.setText("Waiting for video")
        self.videoplayer_state = "stop"
        self.init_video_info()
        self.set_video_player()
        self.timer_camera=QTimer(self)

    def realtime(self,btn):
        import pyrealsense2 as rs
        self.catch = False

        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        #下面的需要修改一下，變成自己的型號
        # self.config.enable_device('918512073998')

        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # decimation 抽取
        self.decimation = rs.decimation_filter()
        # decimation.set_option(rs.option.filter_magnitude,4)

        # Start streaming
        self.pipeline.start(self.config)

        # loop variable 迴圈參數

        self.frames = []
        self.i = 0
        self.weight = 0
        self.big_gate=True
        try:
            while True:
                # print(~(self.catch), not self.catch, self.catch)
                self.start = time.time()
                self.frames_ = self.pipeline.wait_for_frames()
                self.color_frame = self.frames_.get_color_frame()
                self.color_image = np.asanyarray(self.color_frame.get_data())
                self.depth_frame = self.frames_.get_depth_frame()
                self.depth_image = np.asanyarray(self.depth_frame.get_data())

                height, width, channel = self.color_image.shape
                bytesPerline = 3 * width
                self.qimg = QImage(self.color_image, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
                self.ui.label_video.setPixmap(QPixmap.fromImage(self.qimg))
                print("in")
                cv2.waitKey(1)
                if self.big_gate==False:
                    self.pipeline.stop()
                    break
        except:
            self.pipeline.stop()
            print("123")

    def btnstate(self,btn):
    #输出按钮1与按钮2的状态，选中还是没选中
        if btn.text()=='即時影像':
            if btn.isChecked()==True:
                self.mode="realtime"
                print("已選擇"+btn.text()+"模式")
                self.ui.label_2.setText("正在開啟攝影機")
                self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
                self.ui.label_2.setFont(QFont('Arial',15))
                self.ui.pushButton_scan.setEnabled(False)

        if btn.text()=="輸入影像":
            if btn.isChecked() == True:
                self.mode="video"
                print("已選擇"+btn.text()+"模式")
                self.ui.label_2.setText("請選擇影片")
                self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
                self.ui.label_2.setFont(QFont('Arial',20))
                self.ui.pushButton_scan.setEnabled(True)
                print(global_login_mail)

        if btn.text()=='啟用圍籬':
            if btn.isChecked()==True:
                self.ui.label_2.setText("可使用圍籬")
                self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
                self.ui.label_2.setFont(QFont('Arial',20))
                self.fencegate=True
                self.ui.pushButton_drawfence.setEnabled(True)
                self.flag=[1]
                self.flagg=[1]
            elif btn.isChecked()==False:
                self.ui.pushButton_drawfence.setEnabled(False)
                self.flag=[0]
                self.flagg=[0]


    def doroi(self):
        import firebase_admin
        from firebase_admin import credentials
        from firebase_admin import firestore
        cred = credentials.Certificate(r'firebase\alarm-history-firebase-adminsdk-9jpfg-79d60a92c4.json')
        self.app2=firebase_admin.initialize_app(cred)
        self.yolo=YOLO()
        self.yolo_num=YOLO_num()
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.image import MIMEImage
        from pathlib import Path

        ############################################
        if self.mode=="realtime":
            import pyrealsense2 as rs
            self.timestr=time.strftime("%Y%m%d-%H%M%S")
            ctx = rs.context() 
            devices = ctx.query_devices()
            for dev in devices:
                dev.hardware_reset()
            #即時影像模式
            self.pipeline = rs.pipeline()
            config = rs.config()
            #下面的需要修改一下，變成自己的型號
            # config.enable_device('918512073998')
            # config.enable_record_to_file('test.bag')
            config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
            save_path=r"D:\Github\Pythonwork\GUI\Records/"
            # # Start streaming
            self.pipeline.start(config)
            tracking = False             # 設定 False 表示尚未開始追蹤
            fps = 0.0
            a = 0
            e1=cv2.getTickCount()
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(save_path+timestr+'.mp4',fourcc, 10.0, (640,480))
            tracker_list = []
            height = 200  # 圍籬高度
            outlinex = -50  # 警戒線外圍
            outliney = -20  # 警戒線外圍
            flag_range = 18000      ##VIDEO_7500  L515_12000OK
            frame_freq=1
            out_flag = True
            resize_flag = False  # 是否resize    
            colors = [(0, 0, 255), (0, 0, 255),
                    (0, 0, 255), (0, 0, 255)]  # 設定四個外框顏色

            LE_MAT1=[]
            LE_MAT2=[]
            LE_MAT3=[]
            LE_MAT4=[]
            LE_MAT5=[]
            LE_MAT6=[] 
            for self.i in range(len(colors)):
                tracker = cv2.TrackerCSRT_create()        # 創建四組追蹤器
                tracker_list.append(tracker)
            try:
                while (True):
                    t1=time.time()
                    
                    frames=self.pipeline.wait_for_frames()
                    color_frame = frames.get_color_frame()
                    frame = np.asanyarray(color_frame.get_data())
                    keyName = cv2.waitKey(1)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # 轉變成Image
                    frame = Image.fromarray(np.uint8(frame))
                    c=0
                    
                    frame, out_boxes = self.yolo.detect_image(frame)
                    
                    # RGBtoBGR滿足opencv顯示格式
                    frame = np.array(frame)
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    key = cv2.waitKey(1)
                    keyName=cv2.waitKey(90)
                    if key & 0xFF == ord('q') or key == 27:
                        self.big_gate=False
                        cv2.destroyAllWindows()
                        break
                    if a % frame_freq == 0:
                        print('in')
                        print(tracking)
                        if keyName == ord('q'):
                            break
                        if tracking == False :#and keyName & 0xFF == ord('r'):
                            print('in1')
                            # 如果尚未開始追蹤，就開始標記追蹤物件的外框
                            for i in tracker_list:
                                area = cv2.selectROI('Select_ROI', frame, showCrosshair=False, fromCenter=False)
                                i.init(frame, area)    # 初始化追蹤器
                            tracking = True            # 設定可以開始追蹤
                        # 畫線
                        if tracking:
                            print('in2')
                            for i in range(len(tracker_list)):
                                success, point = tracker_list[i].update(frame)
                                if i != 0:
                                    p_rec_x = rec_x
                                    p_rec_y = rec_y

                                    if out_flag:
                                        # p_out_rec_x = rec_x+outlinex
                                        # p_out_rec_y = rec_y+outliney
                                        p_out_rec_x = rec_x
                                        p_out_rec_y = rec_y
                                # 追蹤成功後，不斷回傳左上和右下的座標
                                if success:
                                    
                                    p1 = [int(point[0]), int(point[1])]
                                    p2 = [int(point[0] + point[2]),
                                        int(point[1] + point[3])]
                                    # cv2.rectangle(frame, p1, p2, colors[i], 1)   # 根據座標，繪製四邊形，框住要追蹤的物件
                                    rec_x = (p1[0]+p2[0])//2
                                    rec_y = (p1[1]+p2[1])//2
                                    cv2.circle(frame, (rec_x, rec_y), 3, colors[i], -1)
                                    cv2.circle(frame, (rec_x, rec_y-height),
                                            3, colors[i], -1)  # 圍籬頂點
                                    cv2.line(frame, (rec_x, rec_y), (rec_x,
                                            rec_y-height), colors[i], 1)  # 頂底連線
                                    if i != 0:
                                        cv2.line(frame, (p_rec_x, p_rec_y),
                                                (rec_x, rec_y), colors[i], 1)  # 頂底連線
                                        cv2.line(frame, (p_rec_x, p_rec_y-height),
                                                (rec_x, rec_y-height), colors[i], 1)  # 頂底連線

                                    if out_flag:    # 是否要警戒線

                                        if i == 0:
                                            cv2.circle(
                                                frame, (rec_x+(outlinex*1), rec_y+(outliney)*0), 3, (255, 0, 0), -1)
                                            cv2.circle(
                                                frame, (rec_x+(outlinex*3), rec_y+(outliney)*0), 3, (255, 100, 0), -1)
                                            cv2.circle(
                                                frame, (rec_x+(outlinex*5), rec_y+(outliney)*0), 3, (255, 255, 0), -1)
                                        if i == 1:
                                            cv2.circle(
                                                frame, (rec_x+(outlinex*1), rec_y+(outliney)*0), 3, (255, 0, 0), -1)
                                            cv2.circle(
                                                frame, (rec_x+(outlinex*3), rec_y+(outliney)*0), 3, (255, 100, 0), -1)
                                            cv2.circle(
                                                frame, (rec_x+(outlinex*5), rec_y+(outliney)*0), 3, (255, 255, 0), -1)
                                            
                                            if i != 0:
                                                cv2.line(frame, (p_out_rec_x+(outlinex*1), p_out_rec_y),
                                                        (rec_x+(outlinex*1), rec_y+(outliney)*0), (255, 0, 0), 1)  # 連線
                                                cv2.line(frame, (p_out_rec_x+outlinex*3, p_out_rec_y+(outliney)*0),
                                                        (rec_x+(outlinex*3), rec_y+(outliney)*0), (255, 100, 0), 1)  # 連線
                                                cv2.line(frame, (p_out_rec_x+outlinex*5, p_out_rec_y+(outliney)*0),
                                                        (rec_x+(outlinex*5), rec_y+(outliney)*0), (255, 255, 0), 1)  # 連線
                                                LE_MAT1 = LE_D(p_out_rec_x+(outlinex*1), p_out_rec_y, rec_x+(outlinex*1), rec_y+(outliney)*0, 0)
                                                LE_MAT2 = LE_D(p_out_rec_x+outlinex*3, p_out_rec_y, rec_x+(outlinex*3), rec_y+(outliney)*0, 0)
                                                LE_MAT3 = LE_D(p_out_rec_x+outlinex*5, p_out_rec_y, rec_x+(outlinex*5), rec_y+(outliney)*0, 0)  
                                    
                                        if i == 2:
                                            cv2.circle(
                                                frame, (rec_x-(outlinex*0), rec_y+(outliney*1)), 3, (255, 0, 0), -1)
                                            cv2.circle(
                                                frame, (rec_x-(outlinex*0), rec_y+(outliney*3)), 3, (255, 50, 0), -1)
                                            cv2.circle(
                                                frame, (rec_x-(outlinex*0), rec_y+(outliney*5)), 3, (255, 100, 0), -1)
                                            
                                            cv2.line(frame, (p_out_rec_x+(outlinex*1), p_out_rec_y+(outliney*0)),
                                                        (rec_x-(outlinex*0), rec_y+(outliney*1)), (255, 0, 0), 1)  # 連線
                                            cv2.line(frame, (p_out_rec_x+(outlinex*3), p_out_rec_y+(outliney*0)),
                                                        (rec_x-(outlinex*0), rec_y+(outliney*3)), (255,100, 0), 1)  # 連線
                                            cv2.line(frame, (p_out_rec_x+(outlinex*5), p_out_rec_y+(outliney*0)),
                                                        (rec_x-(outlinex*0), rec_y+(outliney*5)), (255, 255, 0), 1)  # 連線
                                            flag_x = rec_x
                                            LE_MAT4 = LE_D(p_out_rec_x+(outlinex*1), p_out_rec_y+(outliney*0), rec_x+(outlinex*0), rec_y+(outliney*1), 1)
                                            LE_MAT5 = LE_D(p_out_rec_x+(outlinex*3), p_out_rec_y+(outliney*0), rec_x+(outlinex*0), rec_y+(outliney*3), 3)
                                            LE_MAT6 = LE_D(p_out_rec_x+(outlinex*5), p_out_rec_y+(outliney*0), rec_x+(outlinex*0), rec_y+(outliney*5), 5)


                                            font = cv2.FONT_HERSHEY_COMPLEX
                                            # cv2.putText(frame, 'Virtual Fence', (20, 40),
                                            #             font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                                            if out_flag:
                                                cv2.putText(frame, 'Cordon', (20, 80),
                                                            font, 1, (255, 255, 0), 2, cv2.LINE_AA)
                        a = a+1
                        # -------------------------------------------------
                        # 格式轉變，BGRtoRGB
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        # 轉變成Image
                        frame = Image.fromarray(np.uint8(frame))

                        if(self.flagg[0]==1):
                            for box in out_boxes:                  
                                top, left, bottom, right = box
                                top = max(0, np.floor(top).astype('int32'))
                                left = max(0, np.floor(left).astype('int32'))
                                bottom = min(frame.size[1], np.floor(bottom).astype('int32'))
                                right = min(frame.size[0], np.floor(right).astype('int32'))
                                row=[bottom, top,]
                                col=[left, right,]
                                print("111")
                                for row1 in range(2):  # Y值
                                    print("112") 
                                    for col1 in range(2):  # X值
                                        print("113")
                                        # print(LE_MAT4[0]*col[col1]+LE_MAT4[1]*row[row1]+LE_MAT4[2])
                                        thread_1=threading.Thread(target=self.ssound1, args=(self.flag,self.flagg))
                                        if (self.flag[0]==1 and ( (flag_range>=LE_MAT1[0]*col[col1]+LE_MAT1[1]*row[row1]+LE_MAT1[2]>=0)or(0>=LE_MAT4[0]*col[col1]+LE_MAT4[1]*row[row1]+LE_MAT4[2]>=(flag_range*-1)))) :
                                            cv2.putText(frame, 'Alarm', (600, 10),
                                                        font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                                            self.flag[0]=0
                                            self.flagg[0]=0
                                            thread_1.start()  #執行sound
                                            self.ui.label_2.setText("!!!!!!")
                                            self.ui.label_2.setFont(QFont('Arial',27))
                                            self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
                                            self.ui.label_2.setStyleSheet ("background-color: rgb(255,0,0)")
                                            print("14x")
                                            break
                        if(self.flagg[0]==1):             
                            for box in out_boxes:
                                top, left, bottom, right = box
                                top = max(0, np.floor(top).astype('int32'))
                                left = max(0, np.floor(left).astype('int32'))
                                bottom = min(frame.size[1], np.floor(bottom).astype('int32'))
                                right = min(frame.size[0], np.floor(right).astype('int32'))
                                row=[bottom, top]
                                col=[left, right]
                                print("121")
                                for row1 in range(2):  # Y值
                                    print("122") 
                                    for col1 in range(2):  # X值
                                        print("123")
                                        # print(LE_MAT5[0]*col[col1]+LE_MAT5[1]*row[row1]+LE_MAT5[2])
                                        thread_2=threading.Thread(target=self.ssound2, args=(self.flag,self.flagg))
                                        if (self.flag[0]==1 and ( (flag_range>=LE_MAT2[0]*col[col1]+LE_MAT2[1]*row[row1]+LE_MAT2[2]>=0)or(0>=LE_MAT5[0]*col[col1]+LE_MAT5[1]*row[row1]+LE_MAT5[2]>=(flag_range*-1)))) :
                                            cv2.putText(frame, 'Very near', (600, 10),
                                                        font, 1, (0, 255, 0), 2, cv2.LINE_AA)
                                            self.flag[0]=0
                                            self.flagg[0]=0
                                            thread_2.start()  #執行sound
                                            self.ui.label_2.setStyleSheet ("background-color: rgb(255,255,0)")
                                            # self.ui.label_2.setStyleSheet("color:black")
                                            self.ui.label_2.setText("人很靠近")
                                            self.ui.label_2.setFont(QFont('Arial',37))
                                            self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)                                            
                                            
                                            print("25x")
                        if(self.flagg[0]==1):
                            for box in out_boxes:
                                top, left, bottom, right = box
                                top = max(0, np.floor(top).astype('int32'))
                                left = max(0, np.floor(left).astype('int32'))
                                bottom = min(frame.size[1], np.floor(bottom).astype('int32'))
                                right = min(frame.size[0], np.floor(right).astype('int32'))
                                row=[bottom, top]
                                col=[left, right]
                                print("131")
                                for row1 in range(2):  # Y值
                                    print("132") 
                                    for col1 in range(2):  # X值
                                        print("133")
                                        print(LE_MAT6[0]*col[col1]+LE_MAT6[1]*row[row1]+LE_MAT6[2])
                                        thread_3=threading.Thread(target=self.ssound3, args=(self.flag,self.flagg))
                                        if (self.flag[0]==1 and ( (flag_range>=LE_MAT3[0]*col[col1]+LE_MAT3[1]*row[row1]+LE_MAT3[2]>=0)or(0>=LE_MAT6[0]*col[col1]+LE_MAT6[1]*row[row1]+LE_MAT6[2]>=(flag_range*-1)))) :
                                            cv2.putText(frame, 'Near', (600, 10),
                                                        font, 1, (255, 0, 0), 2, cv2.LINE_AA)
                                            self.flag[0]=0

                                            self.flagg[0]=0
                                            thread_3.start()  #執行sound
                                            self.ui.label_2.setStyleSheet ("background-color: lightgreen")
                                            # self.ui.label_2.setStyleSheet("color:black")
                                            self.ui.label_2.setText("有人入侵")
                                            self.ui.label_2.setFont(QFont('Arial',37))
                                            self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
                                            
                                            print("36x")
                        if(self.flagg[0]==1):
                            self.ui.label_2.setText("")
                            self.ui.label_2.setStyleSheet ("background-color: none")
                    
                    # RGBtoBGR滿足opencv顯示格式
                    frame = np.array(frame)
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    

                    fps  = ( fps + (1./(time.time()-t1)) ) / 2
                    print("fps= %.2f"%(fps))
                    # frame = cv2.putText(frame, "fps= %.2f"%(fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    cv2.imshow("video", frame)

                    c = cv2.waitKey(1) & 0xff
                    
                    # Press esc or 'q' to close the image window
                    if key & 0xFF == ord('q') or key == 27:
                        self.ui.label_2.setStyleSheet ("background-color: none")
                        self.ui.label_2.setText("偵測結束")
                        self.ui.label_2.setFont(QFont('Arial',30))
                        self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
                        cv2.destroyAllWindows()
                         
                        break
            finally:
                
                firebase_admin.delete_app(self.app2)
                cv2.destroyAllWindows()
        
        #輸入影片模式
        if self.mode=="video":
            import os
            path1=r"record\\First.png"
            path2=r"record\\Second.png"
            path3=r"record\\Third.png"
            
            try:
                os.remove(path1)
            except OSError as e:
                print(e)
            else:
                pass
            try:
                os.remove(path2)
            except OSError as e:
                print(e)
            else:
                pass
            try:
                os.remove(path3)
            except OSError as e:
                print(e)
            else:
                pass
            
            self.vidoe_save_path=""
            height = 100  # 圍籬高度
            outlinex = -27  # 警戒線外圍
            outliney = -17 # 警戒線外圍
            flag_range = 7500
            video_path=self.fileName
            video_save_path=r"Test_out/"+timestr+'.mp4'
            video_fps=10
            out_flag = True
            resize_flag = True  # 是否resize
            frame_freq = 1  # frame_freq 幀取一幀執行程式
            capture = cv2.VideoCapture(video_path)
            if video_save_path != "":
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                out = cv2.VideoWriter(video_save_path, fourcc, video_fps, size)

            ref, frame = capture.read()
            if not ref:
                raise ValueError("未能正確讀取攝影機")
            # 主程式-------------------------------------------------------
            tracker_list = []
            # colors = [(0,0,255)]  # 設定三個外框顏色
            colors = [(0, 0, 255), (0, 0, 255),
                    (0, 0, 255),(0,0,255)]  # 設定三個外框顏色
            for i in range(len(colors)):
                tracker = cv2.TrackerCSRT_create()        # 創建三組追蹤器
                tracker_list.append(tracker)

            tracking = False             # 設定 False 表示尚未開始追蹤
            # -------------------------------------------------------------
            fps = 0.0
            a = 0       
            while(True):
                t1 = time.time()
                # 讀取某一幀
                ref, frame = capture.read()
                if not ref:
                    break

                if resize_flag:
                    frame = cv2.resize(frame, size)       # 縮小尺寸，加快速度

                keyName = cv2.waitKey(1)
                # #--------------------------------------------------

                # 格式轉變，BGRtoRGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # 轉變成Image
                frame = Image.fromarray(np.uint8(frame))
                # 進行檢測
                
                # print(np.array(yolo.detect_image(frame)))
                frame, out_boxes, num = self.yolo_num.detect_image(frame)
                self.target1=str(num[0]).ljust(7)
                self.num_1=str(num[1]).ljust(3)
                self.target2=str(num[2]).ljust(7)
                self.num_2=str(num[3]).ljust(3)
                print(num)
                
                
                
                self.inform1="有".ljust(3)+ self.target1+self.num_1+"個單位"+"\n"
                self.inform2="有".ljust(3)+ self.target2+self.num_2+"個單位"+"\n"
                
                
                
                print(type(num))
                # RGBtoBGR滿足opencv顯示格式
                frame = np.array(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                if a % frame_freq == 0:
                    if keyName == ord('q'):
                        break
                    if tracking == False:
                        # 如果尚未開始追蹤，就開始標記追蹤物件的外框
                        for i in tracker_list:
                            area = cv2.selectROI(
                                'Select_ROI', frame, showCrosshair=False, fromCenter=False)
                            i.init(frame, area)    # 初始化追蹤器
                        tracking = True            # 設定可以開始追蹤
                    if tracking:
                        for i in range(len(tracker_list)):
                            success, point = tracker_list[i].update(frame)
                            if i != 0:
                                p_rec_x = rec_x
                                p_rec_y = rec_y

                                if out_flag:
                                    # p_out_rec_x = rec_x+outlinex
                                    # p_out_rec_y = rec_y+outliney
                                    p_out_rec_x = rec_x
                                    p_out_rec_y = rec_y

                            # 追蹤成功後，不斷回傳左上和右下的座標
                            if success:
                                
                                p1 = [int(point[0]), int(point[1])]
                                p2 = [int(point[0] + point[2]),
                                    int(point[1] + point[3])]
                                # cv2.rectangle(frame, p1, p2, colors[i], 1)   # 根據座標，繪製四邊形，框住要追蹤的物件
                                rec_x = (p1[0]+p2[0])//2
                                rec_y = (p1[1]+p2[1])//2
                                cv2.circle(frame, (rec_x, rec_y), 3, colors[i], -1)
                                cv2.circle(frame, (rec_x, rec_y-height),
                                        3, colors[i], -1)  # 圍籬頂點
                                cv2.line(frame, (rec_x, rec_y), (rec_x,
                                        rec_y-height), colors[i], 1)  # 頂底連線
                                if i != 0:
                                    cv2.line(frame, (p_rec_x, p_rec_y),
                                            (rec_x, rec_y), colors[i], 1)  # 頂底連線
                                    cv2.line(frame, (p_rec_x, p_rec_y-height),
                                            (rec_x, rec_y-height), colors[i], 1)  # 頂底連線

                                if out_flag:    # 是否要警戒線
                                    section1=1
                                    section2=3
                                    section3=5
                                    x1=rec_x+((outlinex)*section1)
                                    x2=rec_x+((outlinex)*section2)
                                    x3=rec_x+((outlinex)*section3)
                                    y1=rec_y+((outliney))*0
                                    y2=rec_y+((outliney))*0
                                    y3=rec_y+((outliney))*0

                                    # if tracker_list[i] != tracker_list[1] :   #前後圍籬
                                    if i == 0:
                                        
                                        cv2.circle(
                                            frame, (x1, y1), 3, (255, 0, 0), -1)
                                        cv2.circle(
                                            frame, (x2, y2), 3, (255, 100, 0), -1)
                                        cv2.circle(
                                            frame, (x3, y3), 3, (255, 255, 0), -1)
                                    section4=1
                                    section5=3
                                    section6=5
                                    x1=rec_x+((outlinex)*section4)
                                    x2=rec_x+((outlinex)*section5)
                                    x3=rec_x+((outlinex)*section6)
                                    y1=rec_y+((outliney))*0
                                    y2=rec_y+((outliney))*0
                                    y3=rec_y+((outliney))*0
                                    if i == 1:
                                        
                                        cv2.circle(
                                            frame, (x1, y1), 3, (255, 0, 0), -1)
                                        cv2.circle(
                                            frame, (x2, y2), 3, (255, 100, 0), -1)
                                        cv2.circle(
                                            frame, (x3, y3), 3, (255, 255, 0), -1)
                                        if i != 0:
                                            cv2.line(frame, (p_out_rec_x+(outlinex*section1), p_out_rec_y),
                                                    (x1, y1), (255, 0, 0), 1)  # 連線
                                            cv2.line(frame, (p_out_rec_x+outlinex*section2, p_out_rec_y+(outliney)*0),
                                                    (x2,y2), (255, 100, 0), 1)  # 連線
                                            cv2.line(frame, (p_out_rec_x+outlinex*section3, p_out_rec_y+(outliney)*0),
                                                    (x3, y3), (255, 255, 0), 1)  # 連線
                                            LE_MAT1 = LE_D(p_out_rec_x+(outlinex*1), p_out_rec_y, rec_x+(outlinex*1), rec_y+(outliney)*0, 0)
                                            LE_MAT2 = LE_D(p_out_rec_x+(outlinex*3), p_out_rec_y, rec_x+(outlinex*3), rec_y+(outliney)*0, 0)
                                            LE_MAT3 = LE_D(p_out_rec_x+(outlinex*5), p_out_rec_y, rec_x+(outlinex*5), rec_y+(outliney)*0, 0)

                                    section4=2
                                    section5=4
                                    section6=6
                                    
                                    if i == 2:
                                        cv2.circle(
                                            frame, (rec_x-(outlinex*section4), rec_y+(outliney)*0), 3, (255, 0, 0), -1)
                                        cv2.circle(
                                            frame, (rec_x-(outlinex*section5), rec_y+(outliney)*0), 3, (255, 100, 0), -1)
                                        cv2.circle(
                                            frame, (rec_x-(outlinex*section6), rec_y+(outliney)*0), 3, (255, 255, 0), -1)
                                        center_point = ((rec_x-(outlinex*section4)+x1)//2)
                                    if i == 3:
                                        cv2.circle(
                                            frame, (rec_x-(outlinex*section4), rec_y+(outliney)*0), 3, (255, 0, 0), -1)
                                        cv2.circle(
                                            frame, (rec_x-(outlinex*section5), rec_y+(outliney)*0), 3, (255, 100, 0), -1)
                                        cv2.circle(
                                            frame, (rec_x-(outlinex*section6), rec_y+(outliney)*0), 3, (255, 255, 0), -1)
                                        cv2.line(frame, (p_out_rec_x-(outlinex*section4), p_out_rec_y),
                                                (rec_x-(outlinex*section4), rec_y+(outliney)*0), (255, 0, 0), 1)  # 連線
                                        cv2.line(frame, (p_out_rec_x-outlinex*section5, p_out_rec_y+(outliney)*0),
                                                (rec_x-(outlinex*section5), rec_y+(outliney)*0), (255, 100, 0), 1)  # 連線
                                        cv2.line(frame, (p_out_rec_x-outlinex*section6, p_out_rec_y+(outliney)*0),
                                                (rec_x-(outlinex*section6), rec_y+(outliney)*0), (255,  255, 0), 1)  # 連線
                                        LE_MAT4 = LE_D(p_out_rec_x-(outlinex*section4), p_out_rec_y, rec_x-(outlinex*section4), rec_y+(outliney)*0, 0)
                                        LE_MAT5 = LE_D(p_out_rec_x-(outlinex*section5), p_out_rec_y, rec_x-(outlinex*section5), rec_y+(outliney)*0, 0)
                                        LE_MAT6 = LE_D(p_out_rec_x-(outlinex*section6), p_out_rec_y, rec_x-(outlinex*section6), rec_y+(outliney)*0, 0)
    
                                        font = cv2.FONT_HERSHEY_COMPLEX
                                        # cv2.putText(frame, 'Virtual Fence', (20, 40),
                                        #             font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                                        if out_flag:
                                            cv2.putText(frame, 'Cordon', (20, 80),
                                                        font, 1,  self.Cordon_color, 2, cv2.LINE_AA)
                                        
                    a = a+1
                    # -------------------------------------------------
                    # 格式轉變，BGRtoRGB
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # 轉變成Image
                    frame = Image.fromarray(np.uint8(frame))
                    # if self.flagg[0]==0:
                    #     self.ui.label_2.setText("")
                   
                    if(self.flagg[0]==1):
                        self.Cordon_color=(255,255,0)

                        for box in out_boxes:                 
                            top, left, bottom, right = box
                            top = max(0, np.floor(top).astype('int32'))
                            left = max(0, np.floor(left).astype('int32'))
                            bottom = min(frame.size[1], np.floor(bottom).astype('int32'))
                            right = min(frame.size[0], np.floor(right).astype('int32'))
                            row=[bottom, top,]
                            col=[left, right,]                            
                            for row1 in range(2):  # Y值                                 
                                for col1 in range(2):  # X值                                    
                                    # print(LE_MAT4[0]*col[col1]+LE_MAT4[1]*row[row1]+LE_MAT4[2])
                                    thread_1=threading.Thread(target=self.ssound1, args=())
                                    thread_mail1=threading.Thread(target=self.mail1,args=())
                                    frame1 = np.array(frame)
                                    frame1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR)
                                    if(row[row1]>p_out_rec_y):                                   
                                        if (self.flag[0]==1 and ( (flag_range>=LE_MAT1[0]*col[col1]+LE_MAT1[1]*row[row1]+LE_MAT1[2]>=0)) ):
                                            self.Cordon_color=(0,0,255)
                                            self.flag[0]=0
                                            self.flagg[0]=0
                                            thread_1.start()  #執行sound
                                            # thread_mail1.start()
                                            self.ui.label_2.setText("!!!!!!")
                                            self.ui.label_2.setFont(QFont('Arial',27))
                                            self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
                                            self.ui.label_2.setStyleSheet ("background-color: rgb(255,0,0)")
                                            cv2.imwrite(r"record\First.png", frame1)
                                            print("14x")
                                        

                        if(self.flagg[0]==1):             
                            for box in out_boxes:
                                top, left, bottom, right = box
                                top = max(0, np.floor(top).astype('int32'))
                                left = max(0, np.floor(left).astype('int32'))
                                bottom = min(frame.size[1], np.floor(bottom).astype('int32'))
                                right = min(frame.size[0], np.floor(right).astype('int32'))
                                row=[bottom, top]
                                col=[left, right]
                                for row1 in range(2):  # Y值                                    
                                    for col1 in range(2):  # X值                                        
                                        # print(LE_MAT5[0]*col[col1]+LE_MAT5[1]*row[row1]+LE_MAT5[2])
                                        thread_2=threading.Thread(target=self.ssound2, args=())
                                        thread_mail2=threading.Thread(target=self.mail2,args=()) 
                                        frame1 = np.array(frame)
                                        frame1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR)
                                        if(row[row1]>p_out_rec_y):  
                                            if (self.flag[0]==1 and ( (flag_range>=LE_MAT2[0]*col[col1]+LE_MAT2[1]*row[row1]+LE_MAT2[2]>=0)) ):
                                                self.Cordon_color=(255,0,0)
                                                self.flag[0]=0
                                                self.flagg[0]=0
                                                thread_2.start()  #執行sound
                                                # thread_mail2.start()
                                                self.ui.label_2.setStyleSheet ("background-color: rgb(255,255,0)")
                                                # self.ui.label_2.setStyleSheet("color:black")
                                                self.ui.label_2.setText("船很靠近")
                                                self.ui.label_2.setFont(QFont('Arial',37))
                                                self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
                                                cv2.imwrite(r'record/Second.png', frame1)
                                                print("25x")                                       
                                            
                        if(self.flagg[0]==1):
                            for box in out_boxes:
                                top, left, bottom, right = box
                                top = max(0, np.floor(top).astype('int32'))
                                left = max(0, np.floor(left).astype('int32'))
                                bottom = min(frame.size[1], np.floor(bottom).astype('int32'))
                                right = min(frame.size[0], np.floor(right).astype('int32'))
                                row=[bottom, top]
                                col=[left, right]
                                for row1 in range(2):  # Y值
                                    for col1 in range(2):  # X值
                                        thread_3=threading.Thread(target=self.ssound3, args=())
                                        thread_mail3=threading.Thread(target=self.mail3,args=())
                                        frame1 = np.array(frame)
                                        frame1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR)
                                        if(row[row1]>p_out_rec_y):
                                            if (self.flag[0]==1 and ( (flag_range>=LE_MAT3[0]*col[col1]+LE_MAT3[1]*row[row1]+LE_MAT3[2]>=0)) ):
                                                self.Cordon_color=(0,255,0)
                                                self.flag[0]=0
                                                self.flagg[0]=0
                                                # thread_mail3.start()
                                                thread_3.start()  #執行sound
                                                self.ui.label_2.setStyleSheet ("background-color: lightgreen")
                                                # self.ui.label_2.setStyleSheet("color:black")
                                                self.ui.label_2.setText("有船入侵")
                                                self.ui.label_2.setFont(QFont('Arial',37))
                                                self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
                                                cv2.imwrite(r'record/Third.png', frame1)
                                            
                        if(self.flagg[0]==1):
                            self.ui.label_2.setText("")
                            self.ui.label_2.setStyleSheet ("background-color: none")
                   
                    # RGBtoBGR滿足opencv顯示格式
                    frame = np.array(frame)
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                    fps  = ( fps + (1./(time.time()-t1)) ) / 2
                    print("fps= %.2f"%(fps))
                    # frame = cv2.putText(frame, "fps= %.2f"%(fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    font = cv2.FONT_HERSHEY_COMPLEX
                    self.timestr=time.strftime("%Y%m%d-%H%M%S")
                    # frame=cv2.putText(frame,self.timestr,(320,50),font, 1, (0, 0,0), 2)
                    cv2.imshow("video", frame)
                    c = cv2.waitKey(1) & 0xff
                    if video_save_path != "":
                        out.write(frame)

                    if c == 27:
                        capture.release()
                        break
            print("Video Detection Done!")
            firebase_admin.delete_app(self.app2)
            if os.path.exists(path1)==True:
                print("mail1gogogogo")
                self.mail1()
            if os.path.exists(path2)==True:
                print("mail2gogogogo")
                self.mail2()
            if os.path.exists(path3)==True:
                print("mail3gogogogo")
                self.mail3()
            
            capture.release()
            if video_save_path != "":
                print("Save processed video to the path :" + video_save_path)
                out.release()
            cv2.destroyAllWindows() 
    def mail3(self):
        import smtplib
        print(global_login_mail)
        if self.mail_gate3:
            # self.mail_gate3=False
            content = MIMEMultipart()  #建立MIMEMultipart物件
            content["subject"] = "虛擬圍籬警報通知"  #Mail Title
            content["from"] ="tony0912045596@gmail.com"  #Sender
            content["to"] =global_login_mail #Reciever
            content.attach(MIMEText("有船入侵\n"))  #content
            content.attach(MIMEText(self.inform1))
            content.attach(MIMEText(self.inform2))
            content.attach(MIMEImage(Path(r"record\First.png").read_bytes()))
            with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # Set SMTP Server
                try:
                    smtp.ehlo()  # 驗證SMTP伺服器
                    smtp.starttls()  # 建立加密傳輸
                    print("sending to",global_login_mail)
                    smtp.login(
                        "tony0912045596@gmail.com", "mbnmygvsmpcorkhv")  # 登入寄件者gmail
                    smtp.send_message(content)  # 寄送郵件
                    print("Complete!")
                except Exception as e: 
                    print("Error message: ", e)  
            time.sleep(60)
            self.mail_gate3=True

    def mail2(self):
        import smtplib
        if self.mail_gate2:
            # self.mail_gate2=False
            content = MIMEMultipart()  #建立MIMEMultipart物件
            content["subject"] ="虛擬圍籬警報通知"  #郵件標題
            content["from"] ="tony0912045596@gmail.com"  #寄件者
            content["to"] =global_login_mail #收件者
            content.attach(MIMEText("船很靠近\n"))  #郵件內容
            content.attach(MIMEText(self.inform1))
            content.attach(MIMEText(self.inform2))
            content.attach(MIMEImage(Path(r"record/Second.png").read_bytes()))
            with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
                try:
                    print("sending to ",global_login_mail)
                    smtp.ehlo()  # 驗證SMTP伺服器
                    smtp.starttls()  # 建立加密傳輸
                    smtp.login(
                        "tony0912045596@gmail.com", "mbnmygvsmpcorkhv")  # 登入寄件者gmail
                    smtp.send_message(content)  # 寄送郵件
                    print("Complete!")
                except Exception as e: 
                    print("Error message: ", e)  
            time.sleep(60)
            self.mail_gate2=True
             
    def mail1(self):
        import smtplib
        print(global_login_mail)
        print(self.mail_gate1)
        if self.mail_gate1:
            # self.mail_gate1=False
            content = MIMEMultipart()  #建立MIMEMultipart物件
            content["subject"] ="虛擬圍籬警報通知"  #郵件標題
            content["from"] ="tony0912045596@gmail.com"  #寄件者
            content["to"] =global_login_mail #收件者
            content.attach(MIMEText("非常靠近\n"))  #郵件內容
            content.attach(MIMEText(self.inform1))
            content.attach(MIMEText(self.inform2))
            content.attach(MIMEImage(Path(r"record/Third.png").read_bytes()))
            print("sending to ",global_login_mail)
            with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
                try:
                    
                    smtp.ehlo()  # 驗證SMTP伺服器
                    smtp.starttls()  # 建立加密傳輸
                    
                    smtp.login(
                        "tony0912045596@gmail.com", "mbnmygvsmpcorkhv")  # 登入寄件者gmail
                    smtp.send_message(content)  # 寄送郵件
                    print("Complete!")
                except Exception as e: 
                    print("Error message: ", e)  
            time.sleep(60)
            self.mail_gate1=True

#不正常的sound
    def ssound3(self):
        #有船入侵
        playsound(r'D:\\Github\0820GUI\sound\\ship1.mp3')
        print("_________________________________________________________")
        time.sleep(0.1)
        self.flag[0]=1
        self.flagg[0]=1
        return self.flag,self.flagg

    def ssound2(self):
        #人很靠近
        playsound(r'D:\\Github\\0820GUI\\sound\\ship2.mp3')
        print("_________________________________________________________============================")
        time.sleep(0.1)
        self.flag[0]=1
        self.flagg[0]=1
        return self.flag,self.flagg

    def ssound1(self):
        #警鈴聲
        playsound(r'D:\\Github\\0820GUI\\sound\\alarm.mp3')
        print("_________________________________________________________.................................")
        time.sleep(0.1)
        self.flag[0]=1
        self.flagg[0]=1
        return self.flag,self.flagg

    def onClick(self): #初始化点击事件
        self.big_gate=False
        cap = cv2.VideoCapture(self.fileName)  #获取视频对象
        fps = cap.get(cv2.CAP_PROP_FPS) 
        try:
            if not cap.isOpened():
                print("Cannot open Video File")
               
            while not self.bClose:
                ret, self.frame = cap.read()  # 逐帧读取影片
                
                if not ret:
                    if self.frame is None:
                        print("The video has end.")
                    else:
                        print("Read video error!")
                    break

                QtImg = cvImgtoQtImg(self.frame)  # 将帧数据转换为PyQt图像格式
                self.ui.label_video.setPixmap(QtGui.QPixmap.fromImage(QtImg))  # 在ImgDisp显示图像
                size = QtImg.size()
                self.ui.label_video.resize(size)  # 根据帧大小调整标签大小

                self.ui.label_video.show()        # 刷新界面
                cv2.waitKey(int(500 / fps))  # 休眠一会，确保每秒播放fps帧

            # 完成所有操作后，释放捕获器
            cap.release()
        except:
            print("未正常開啟影片")
           

    def init_video_info(self):
        videoinfo = opencv_engine.getvideoinfo(self.fileName)
        self.vc = videoinfo["vc"] 
        self.video_fps = videoinfo["fps"] 
        self.video_total_frame_count = videoinfo["frame_count"] 
        self.video_width = videoinfo["width"]
        self.video_height = videoinfo["height"] 

    def set_video_player(self):
        self.timer=QTimer() # init QTimer
        self.timer.timeout.connect(self.timer_timeout_job) # when timeout, do run one
        # self.timer.start(1000//self.video_fps) # start Timer, here we set '1000ms//Nfps' while timeout one time
        self.timer.start(20) # but if CPU can not decode as fast as fps, we set 1 (need decode time)

    def timer_timeout_job(self):
        frame = self.__get_frame_from_frame_no(self.current_frame_no)
        # self.__update_label_frame(frame)

        if (self.videoplayer_state == "play"):
            self.current_frame_no += 1

        if (self.videoplayer_state == "stop"):
            self.current_frame_no = 0

        if (self.videoplayer_state == "pause"):
            self.current_frame_no = self.current_frame_no


    def __get_frame_from_frame_no(self, frame_no):
        self.vc.set(1, frame_no)
        ret, frame = self.vc.read()
        
        return frame

    def setup_control(self):
        self.img = r'pictures\UI_logo.png'
        self.display_img()

    def open_file(self):
        self.big_gate=False
        # if frame is read correctly ret is True
        try:
            if self.gate==False:
                
                self.fileName, _ = QFileDialog.getOpenFileName(self, "Selecciona los mediose",".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)")
                self.ui.textEdit.setText(self.fileName)
                self.video_path = self.fileName

                print(self.fileName)
                # self.pipline.stop()
                cap = cv2.VideoCapture(self.fileName)
                ret, frame = cap.read()
                img3=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
                img3=QImage(img3.data,img3.shape[1],img3.shape[0],QImage.Format_RGB888)
                self.ui.label_video.setPixmap(QPixmap.fromImage(img3))
    
            elif self.gate==True:
                cap = cv2.VideoCapture(self.fileName)
                while cap.isOpened():
                    ret, frame = cap.read()
                    # if frame is read correctly ret is True
                    if not ret:
                        print("Can't receive frame (stream end?). Exiting ...")
                        break
                    
                    img3=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
                    img3=QImage(img3.data,img3.shape[1],img3.shape[0],QImage.Format_RGB888)
                    self.ui.label_video.setPixmap(QPixmap.fromImage(img3))
        except:
            self.ui.label_2.setText("請再試一次")
        
            
    def check(self):
        cwd="record"
        # if frame is read correctly ret is True
        try:
            if self.gate==False:
                self.fileName, _ = QFileDialog.getOpenFileName(self, "Selecciona los mediose",cwd,".", "Video Files (*.MOV *.mp4 *.flv *.ts *.mts *.avi)")
                self.ui.textEdit.setText(self.fileName)
                self.video_path = self.fileName

                print(self.fileName)

                cap = cv2.VideoCapture(self.fileName)
                ret, frame = cap.read()
                img3=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
                img3=QImage(img3.data,img3.shape[1],img3.shape[0],QImage.Format_RGB888)
                self.ui.label_video.setPixmap(QPixmap.fromImage(img3))
                
            elif self.gate==True:
                cap = cv2.VideoCapture(self.fileName)
                while cap.isOpened():
                    ret, frame = cap.read()
                    # if frame is read correctly ret is True
                    if not ret:
                        print("Can't receive frame (stream end?). Exiting ...")
                        break
                    
                    img3=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
                    img3=QImage(img3.data,img3.shape[1],img3.shape[0],QImage.Format_RGB888)
                    self.ui.label_video.setPixmap(QPixmap.fromImage(img3))
        except:
            self.ui.label_2.setText("請再試一次")

    def start(self):
        self.gate=True
        self.open_file()

    def display_img(self):
        self.img = cv2.imread(self.img)
        height, width, channel = self.img.shape
        bytesPerline = 3 * width
        self.qimg = QImage(self.img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.ui.label.setPixmap(QPixmap.fromImage(self.qimg))

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.pushButton_start.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.ui.pushButton_start.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def handleError(self):
        self.playButton.setEnabled(False)
        self.statusBar.showMessage("Error: " + self.mediaPlayer.errorString())


    def gologin(self):
        self.window1=LoginWindow_controller()
        self.windowlist1.append(self.window1)
        self.window1.setWindowIcon(QtGui.QIcon(r"pictures\barrier.png"))
        self.window1.setWindowTitle("智慧型海上箱網防盜系統")
        self.close()
        self.window1.show()




if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window1 = LoginWindow_controller()
    window1.setWindowIcon(QtGui.QIcon(r"pictures\barrier.png"))
    window1.setWindowTitle("智慧型海上箱網防盜系統")

    window1.show()

    sys.exit(app.exec_())  