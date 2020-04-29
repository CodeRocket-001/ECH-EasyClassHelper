import sys,functools,random,time,os,json

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from modules.UI import *
from modules.ech import *

classes={}
saver=echSaver("./savings/save.json")
settings={"FONT":"宋体","LANG":"translations/zh_cn","BTN_COLOR":(220,220,220),"BG_COLOR":(240,240,240)}
_tr=QCoreApplication.translate


class EditHtml(QDialog,Html_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.see.clicked.connect(self.show_text)
        self.save.clicked.connect(self.save_html)
        self.open.clicked.connect(self.open_html)
        self.textEdit.textChanged.connect(self.change_text)
        self.s=""
        self.save.setIcon(QIcon(QPixmap("./images/save.png")))
        self.save.setIconSize(QSize(40,40))
        self.open.setIcon(QIcon(QPixmap("./images/open.png")))
        self.open.setIconSize(QSize(40,40))

    def change_text(self):
        if self.see.text()==_tr("htmlDialog","预览文本内容"):
            self.s=self.textEdit.toPlainText()

    def show_text(self):
        self.see.setText(_tr("htmlDialog","返回编辑界面"))
        self.textEdit.setHtml(self.s)
        self.textEdit.setReadOnly(True)
        self.see.clicked.disconnect(self.show_text)
        self.see.clicked.connect(self.show_html)

    def show_html(self):
        self.see.setText(_tr("htmlDialog","预览文本内容"))
        self.textEdit.setReadOnly(False)
        self.textEdit.setPlainText(self.s)
        try:
            self.see.clicked.disconnect(self.show_html)
        except TypeError:
            pass
        self.see.clicked.connect(self.show_text)

    def save_html(self):
        self.show_html()
        if self.lineEdit.text():
            with open("./savings/html/"+self.lineEdit.text()+".html","w") as f:
                f.write(self.textEdit.toPlainText())
                QMessageBox.information(self,_tr("htmlDialog","提示"),self.lineEdit.text()+".html "+_tr("htmlDialog","保存成功！"))

    def open_html(self):
        f_name,ok=QFileDialog.getOpenFileName(self,_tr("htmlDialog","选择要打开的html文件"),".","HTML Files (*.html)")
        if ok:
            with open(f_name,"r") as f:
                f_name=f_name.split('/')
                f_name=f_name[len(f_name)-1]
                self.lineEdit.setText(f_name[:len(f_name)-5])
                self.show_html()
                self.textEdit.setPlainText(f.read())


class EditCode(QDialog,Code_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.save.setIcon(QIcon(QPixmap("./images/save.png")))
        self.save.setIconSize(QSize(40,40))
        self.save.clicked.connect(self.run_code)
        self.open.setIcon(QIcon(QPixmap("./images/open.png")))
        self.open.clicked.connect(self.open_code)
        self.open.setIconSize(QSize(40,40))

    def run_code(self):
        with open("./savings/code/"+self.lineEdit.text()+".py","w") as f:
            f.write(self.plainTextEdit.toPlainText())
            QMessageBox.information(self,_tr("codeDialog","提示"),self.lineEdit.text()+".py "+_tr("codeDialog","保存成功并在控制台窗口运行！"))
        os.system("cls")
        print("="*20+"RESTART CODE '"+self.lineEdit.text()+".py'"+"="*20)
        exec(self.plainTextEdit.toPlainText())
        print("="*20+"TASK '"+self.lineEdit.text()+".py' ENDED!"+"="*20)

    def open_code(self):
        f_name,ok=QFileDialog.getOpenFileName(self,_tr("codeDialog","选择要打开的python文件"),".","Python Files (*.py)")
        if ok:
            with open(f_name,"r") as f:
                f_name=f_name.split('/')
                f_name=f_name[len(f_name)-1]
                self.lineEdit.setText(f_name[:len(f_name)-3])
                self.plainTextEdit.setPlainText(f.read())
        

class EditColor(QDialog,Color_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.res=()
        self.red.valueChanged.connect(self.update_color)
        self.green.valueChanged.connect(self.update_color)
        self.blue.valueChanged.connect(self.update_color)
        self.choose_color.currentTextChanged.connect(self.use_color)
        self.update_color()

    def get_color(self):
        self.res=(self.red.value(),self.green.value(),self.blue.value())
        return self.res

    def update_color(self):
        self.show_color.setStyleSheet("background-color:rgb"+str(self.get_color())+";")

    def use_color(self):
        colors={_tr("colorDialog","淡灰色"):(220,220,220),\
                _tr("colorDialog","淡黄色"):(250,250,0),\
                _tr("colorDialog","浅红色"):(255,100,100),\
                _tr("colorDialog","淡蓝色"):(110,190,240),\
                _tr("colorDialog","浅绿色"):(100,255,100),\
                _tr("colorDialog","亮白色"):(255,255,255)}
        cl=colors[self.choose_color.currentText()]
        self.red.setValue(cl[0])
        self.green.setValue(cl[1])
        self.blue.setValue(cl[2])
        self.update_color()


class MyWindow(QMainWindow,Ui_MainWindow):
    
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon("./images/logo.png"))
        self.choosed_t=0
        self.info_btns=[]
        self.del_btns=[]
        self.labels=[]
        self.setupUi(self)
        self.setFixedSize(1300,800)
        self.add_class.setIcon(QIcon(QPixmap("./images/add.png")))
        self.add_class.setIconSize(QSize(35,35))
        self.del_class.setIcon(QIcon(QPixmap("./images/del.png")))
        self.del_class.setIconSize(QSize(35,35))
        self.info.setIcon(QIcon(QPixmap("./images/stu_info.png")))
        self.info.setIconSize(QSize(35,35))
        self.set_lang.setIcon(QIcon(QPixmap("./images/earth.png")))
        self.set_lang.setIconSize(QSize(35,35))
        self.add_test.setEnabled(False)
        self.add_stu.setEnabled(False)
        self.add_stu.hide()
        self.sort_btn.hide()
        self.score.hide()
        self.add_class.clicked.connect(self.new_class)
        self.del_class.clicked.connect(self.remove_class)
        self.add_test.clicked.connect(self.new_test)
        self.add_stu.clicked.connect(self.new_stu)
        self.sort_btn.clicked.connect(self.sort_marks)
        self.main.clicked.connect(self.main_menu)
        self.set_lang.clicked.connect(self.change_lang)
        self.rand_stu.triggered.connect(self.choose_stu)
        self.write_html.triggered.connect(self.edit_html)
        self.write_Python.triggered.connect(self.edit_code)
        self.set_font.triggered.connect(self.reset_font)
        self.set_btn.triggered.connect(self.reset_btn)
        self.set_bg.triggered.connect(self.reset_bg)
        self.choose_class.currentIndexChanged.connect(self.show_tests)
        for key in classes.keys():
            self.choose_class.addItem(key)
        self.setStyleSheet("QPushButton{background-color:rgb"+str(settings["BTN_COLOR"])+";}")
        self.choose_class.setStyleSheet("background-color:rgb"+str(settings["BTN_COLOR"])+";")
        self.plainTextEdit.setStyleSheet("background-color:rgb"+str(settings["BTN_COLOR"])+";")
        plt=QPalette();c=settings["BG_COLOR"]
        plt.setColor(self.backgroundRole(),QColor(c[0],c[1],c[2]))
        self.setPalette(plt)
        font=QFont();font.setFamily(settings["FONT"]);font.setPointSize(15)
        self.main.setFont(font)
        self.choose_class.setFont(font)
        self.add_stu.setFont(font)
        self.add_test.setFont(font)
        self.sort_btn.setFont(font)
        self.label.setFont(font)
        self.label_2.setFont(font)
        self.trans=QTranslator()
        self.trans.load(settings["LANG"])
        _app=QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)

    def new_class(self):
        class_name,ok=QInputDialog.getText(self,_tr("MainWindow","添加班级"),_tr("MainWindow","请输入班级名："))
        if ok:
            clas=echClass(class_name)
            classes[class_name]=clas
            self.choose_class.addItem(class_name)
            QMessageBox.information(self,_tr("MainWindow","提示"),_tr("MainWindow","班级添加成功！"),QMessageBox.Ok,QMessageBox.Ok)

    def remove_class(self):
        ok=QMessageBox.question(self,_tr("MainWindow","删除班级"),_tr("MainWindow","您确定要删除该班级吗？"),QMessageBox.Yes|QMessageBox.No)
        if ok==QMessageBox.Yes:
            classes.pop(self.choose_class.currentText())
            self.choose_class.removeItem(self.choose_class.currentIndex())
            QMessageBox.information(self,_tr("MainWindow","提示"),_tr("MainWindow","班级删除成功！"),QMessageBox.Ok,QMessageBox.Ok)

    def new_test(self):
        test_name,ok=QInputDialog.getText(self,_tr("MainWindow","添加测试"),_tr("MainWindow","请输入测试名："))
        if ok:
            classes[self.choose_class.currentText()].add_test(test_name)
            self.show_tests()

    def remove_test(self,s):
        ok=QMessageBox.question(self,_tr("MainWindow","删除测试"),_tr("MainWindow","您确定要删除该测试吗？"),QMessageBox.Yes|QMessageBox.No)
        if ok==QMessageBox.Yes:
            classes[self.choose_class.currentText()].del_test(s)
            self.show_tests()

    def new_stu(self):
        s,ok1=QInputDialog.getText(self,_tr("MainWindow","添加学生"),_tr("MainWindow","请输入学生名："))
        if ok1:
            n,ok2=QInputDialog.getInt(self,_tr("MainWindow","添加学生"),_tr("MainWindow","请输入学生学号："))
            if ok2:
                classes[self.choose_class.currentText()].add_stu(s,int(n))
                self.show_stus()

    def remove_stu(self,s):
        ok=QMessageBox.question(self,_tr("MainWindow","删除学生"),_tr("MainWindow","您确定要删除学生%s吗？")%s,QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if ok==QMessageBox.Yes:
            classes[self.choose_class.currentText()].del_stu(s)
            self.show_stus()

    def change_mark(self,t,s):
        clas=classes[self.choose_class.currentText()]
        m,ok=QInputDialog.getInt(self,_tr("MainWindow","更改成绩"),_tr("MainWindow","请输入%s的成绩：")%(s.name))
        if ok:
            clas.tests[t].change(s.name,m)
            self.show_marks(t)

    def show_tests(self):
        if self.choose_class.currentText()=="":
            return
        self.info.setEnabled(True)
        self.add_class.setEnabled(True)
        self.del_class.setEnabled(True)
        self.info.setIcon(QIcon(QPixmap("./images/stu_info.png")))
        try:
            self.info.clicked.disconnect(self.show_tests)
        except TypeError:
            pass
        self.info.clicked.connect(self.show_stus)
        self.info.setToolTip(_tr("MainWindow","显示学生信息"))
        clas=classes[self.choose_class.currentText()]
        self.add_test.setEnabled(True)
        for i_btn in self.info_btns:
            i_btn.deleteLater()
        for d_btn in self.del_btns:
            d_btn.deleteLater()
        for l in self.labels:
            l.deleteLater()
        self.add_stu.hide()
        self.info_btns.clear()
        self.del_btns.clear()
        self.labels.clear()
        i=0
        self.scrollAreaWidgetContents.resize(990,(len(clas.tests)+1)*60+10)
        while i<len(clas.tests):
            self.info_btns.append(QPushButton(self.scrollAreaWidgetContents))
            self.del_btns.append(QPushButton(self.scrollAreaWidgetContents))
            self.labels.append(QPushButton(self.scrollAreaWidgetContents))
            self.info_btns[i].setGeometry(870,10+i*60,50,50)
            self.info_btns[i].setIcon(QIcon(QPixmap("./images/info.png")))
            self.info_btns[i].setIconSize(QSize(45,45))
            self.info_btns[i].setToolTip(_tr("MainWindow","测试详细信息"))
            self.del_btns[i].clicked.connect(functools.partial(self.remove_test,i))
            self.del_btns[i].setGeometry(930,10+i*60,50,50)
            self.del_btns[i].setIcon(QIcon(QPixmap("./images/del2.png")))
            self.del_btns[i].setIconSize(QSize(45,45))
            self.del_btns[i].setToolTip(_tr("MainWindow","删除测试"))
            self.labels[i].setStyleSheet("text-align:left")
            self.labels[i].setText("· "+clas.tests[i].name)
            font=QFont();font.setFamily(settings["FONT"]);font.setPointSize(15)
            self.labels[i].setFont(font)
            self.labels[i].setGeometry(10,10+i*60,850,50)
            self.labels[i].clicked.connect(functools.partial(self.show_marks,i))
            self.info_btns[i].show()
            self.del_btns[i].show()
            self.labels[i].show()
            i+=1
        self.add_test.move(10,10+i*60)
        self.add_test.show()

    def show_stus(self):
        self.info.setIcon(QIcon(QPixmap("./images/test_info.png")))
        try:
            self.info.clicked.disconnect(self.show_stus)
        except TypeError:
            pass
        self.info.clicked.connect(self.show_tests)
        self.info.setToolTip(_tr("MainWindow","显示测试信息"))
        clas=classes[self.choose_class.currentText()]
        self.add_stu.setEnabled(True)
        for i_btn in self.info_btns:
            i_btn.deleteLater()
        for d_btn in self.del_btns:
            d_btn.deleteLater()
        for l in self.labels:
            l.deleteLater()
        self.add_test.hide()
        self.info_btns.clear()
        self.del_btns.clear()
        self.labels.clear()
        self.scrollAreaWidgetContents.resize(990,(len(clas.stus)+1)*60+10)
        i=0
        while i<len(clas.stus):
            self.info_btns.append(QPushButton(self.scrollAreaWidgetContents))
            self.del_btns.append(QPushButton(self.scrollAreaWidgetContents))
            self.labels.append(QPushButton(self.scrollAreaWidgetContents))
            self.info_btns[i].setGeometry(870,10+i*60,50,50)
            self.info_btns[i].setIcon(QIcon(QPixmap("./images/info.png")))
            self.info_btns[i].setIconSize(QSize(45,45))
            self.info_btns[i].setToolTip(_tr("MainWindow","学生详细信息"))
            stu=clas.stus[i]
            self.del_btns[i].clicked.connect(functools.partial(self.remove_stu,stu.name))
            self.del_btns[i].setGeometry(930,10+i*60,50,50)
            self.del_btns[i].setIcon(QIcon(QPixmap("./images/del2.png")))
            self.del_btns[i].setIconSize(QSize(45,45))
            self.del_btns[i].setToolTip(_tr("MainWindow","删除学生"))
            self.labels[i].setText(_tr("MainWindow","· %d号 -- %s")%(stu.no,clas.stus[i].name))
            self.labels[i].setStyleSheet("text-align:left")
            font=QFont();font.setFamily(settings["FONT"]);font.setPointSize(15)
            self.labels[i].setFont(font)
            self.labels[i].setGeometry(10,10+i*60,850,50)
            self.info_btns[i].show()
            self.del_btns[i].show()
            self.labels[i].show()
            i+=1
        self.add_stu.move(10,10+i*60)
        self.add_stu.show()

    def show_marks(self,x):
        self.info.setEnabled(False)
        self.add_class.setEnabled(False)
        self.del_class.setEnabled(False)
        clas=classes[self.choose_class.currentText()]
        test=clas.tests[x]
        self.choosed_t=x
        for btn in self.info_btns:
            btn.deleteLater()
        for btn in self.del_btns:
            btn.deleteLater()
        for l in self.labels:
            l.deleteLater()
        self.add_test.hide()
        self.info_btns.clear()
        self.del_btns.clear()
        self.labels.clear()
        self.scrollAreaWidgetContents.resize(990,(len(clas.stus)+2)*60+10)
        i=0
        avg=0
        test.stus.sort()
        while i<len(test.stus):
            self.info_btns.append(QPushButton(self.scrollAreaWidgetContents))
            self.info_btns[i].setText(_tr("MainWindow","%d号%s -- %d分")%(test.stus[i].no,test.stus[i].name,test.stus[i].mark))
            avg+=test.stus[i].mark
            self.info_btns[i].clicked.connect(functools.partial(self.change_mark,x,test.stus[i]))
            font=QFont();font.setFamily(settings["FONT"]);font.setPointSize(15)
            self.info_btns[i].setFont(font)
            self.info_btns[i].setGeometry(10,10+(i+1)*60,970,50)
            self.info_btns[i].show()
            i+=1
        try:
            avg/=len(test.stus)
            avg=float("%.2f"%avg)
        except ZeroDivisionError:
            avg=None
        self.sort_btn.show()
        self.score.setText(_tr("MainWindow","平均分：%.2f分")%avg)
        self.score.move(10,10+(i+1)*60)
        self.score.show()
        
    def sort_marks(self):
        t=classes[self.choose_class.currentText()].tests[self.choosed_t]
        if self.sort_btn.text()==_tr("MainWindow","按成绩排序"):
            t.sort(1)
            self.sort_btn.setText(_tr("MainWindow","按学号排序"))
        else:
            t.sort(2)
            self.sort_btn.setText(_tr("MainWindow","按成绩排序"))
        self.show_marks(self.choosed_t)

    def main_menu(self):
        self.sort_btn.hide()
        for btn in self.info_btns:
            btn.deleteLater()
        self.info_btns.clear()
        self.show_tests()
        self.score.hide()

    def choose_stu(self):
        t=self.choose_class.currentText()
        if t!="" and len(clsses[t].stus)>0:
            s=random.choice(classes[self.choose_class.currentText()].stus)
            QMessageBox.information(self,_tr("MainWindow","随机点名"),_tr("MainWindow","%d号%s被点中了！")%(s.no,s.name))
            return
        QMessageBox.critical(self,_tr("MainWindow","出错了"),_tr("MainWindow","程序不知道怎么点名QwQ"))

    def edit_html(self):
        d=EditHtml()
        d.exec_()

    def edit_code(self):
        d=EditCode()
        d.exec_()

    def reset_font(self):
        f,ok=QFontDialog.getFont()
        if ok:
            f.setPointSize(15)
            settings["FONT"]=f.family()
            self.main.setFont(f)
            self.choose_class.setFont(f)
            self.add_stu.setFont(f)
            self.add_test.setFont(f)
            self.sort_btn.setFont(f)
            self.label.setFont(f)
            self.label_2.setFont(f)
            self.show_tests()

    def reset_btn(self):
        d=EditColor()
        ok=d.exec_()
        if ok:
            s="rgb"+str(d.res)
            settings["BTN_COLOR"]=d.res
            self.setStyleSheet("QPushButton{background-color:"+s+";}")
            self.choose_class.setStyleSheet("background-color:"+s+";")
            self.plainTextEdit.setStyleSheet("background-color:"+s+";")
            c=settings["BG_COLOR"];plt=QPalette()
            plt.setColor(QPalette.Background,QColor(c[0],c[1],c[2]))
            self.setPalette(plt)

    def reset_bg(self,event):
        d=EditColor()
        ok=d.exec_()
        if ok:
            settings["BG_COLOR"]=d.res
            plt=QPalette()
            plt.setColor(QPalette.Background,QColor(d.res[0],d.res[1],d.res[2]))
            self.setPalette(plt)

    def change_lang(self):
        items=["简体中文","English"]
        langs={"简体中文":"translations/zh_cn","English":"translations/en"}
        l,ok=QInputDialog.getItem(self,"Language","Select a language:",items,0,False)
        if ok:
            _app=QApplication.instance()
            settings["LANG"]=langs[l]
            self.trans.load(langs[l])
            _app.installTranslator(self.trans)
            self.retranslateUi(self)
            self.show_tests()

    def closeEvent(self,QCloseEvent):
        reply=QMessageBox.warning(self,_tr("MainWindow","退出程序"),_tr("MainWindow","退出前需要保存您所做的更改吗？"),QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
        if reply==QMessageBox.Yes:
            saver.save(classes)
            QCloseEvent.accept()
            f_obj=open("./savings/AppSetting.json","w")
            json.dump(settings,f_obj,indent=4)
        elif reply==QMessageBox.No:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


print("     --*| Opening ECH... |*--     ")
print("==================================")
time.sleep(1)
pyqtRemoveInputHook()
app=QApplication(sys.argv)
splash=QSplashScreen(QPixmap("./images/loading.png"))
splash.showMessage("Loading savings...")
splash.show()
try:
    classes=saver.load()
except FileNotFoundError:
    pass
try:
    f_obj=open("./savings/AppSetting.json","r")
    settings=json.load(f_obj)
    settings["BTN_COLOR"]=tuple(settings["BTN_COLOR"])
    settings["BG_COLOR"]=tuple(settings["BG_COLOR"])
except FileNotFoundError:
    pass
time.sleep(1)
splash.showMessage("Initializing...")
window=MyWindow()
time.sleep(1)
splash.showMessage("Finished!")
time.sleep(1)
window.show()
splash.finish(window)
sys.exit(app.exec_())