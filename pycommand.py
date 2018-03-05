#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Wei Shuai"
__copyright__ = "Copyright 2018 Wei Shuai <cpuwolf@gmail.com>"
__version__ = "1.0"
__email__ = "cpuwolf@gmail.com"
"""
Created on March 2018
@author: Wei Shuai <cpuwolf@gmail.com>

redirect prompt command stdout,stderr to Qt GUI

"""

import os
import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import QThread, QDir
from PyQt4.QtGui import QFileDialog
import ConfigParser
import subprocess
import Queue
import threading


def resource_path(relative_path): # needed for bundling                                                                                                                            
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class MyConfig:
    def __init__(self):
        self.text_valuepath = None
        self.cmdstart = None
        self.cmdend = None
        
    def readconfig(self):
        config = ConfigParser.RawConfigParser()
        config.read(resource_path('pycommand.cfg'))
        self.text_valuepath = config.get('basic', 'inputfile')
        self.cmdstart = config.get('basic', 'commandstart')
        self.cmdend = config.get('basic', 'commandend')
        return [self.text_valuepath, self.cmdstart, self.cmdend]
    
    def writeconfig(self,ifile):
        config = ConfigParser.RawConfigParser()
        config.add_section('basic')
        config.set('basic', 'inputfile', ifile)
        config.set('basic', 'commandstart',self.cmdstart)
        config.set('basic', 'commandend',self.cmdend)
        with open('pycommand.cfg', 'wb') as configfile:
            config.write(configfile)


def read_stdout(pipe,q):
    for line in iter(pipe.readline,''):
        q.put(line)
    pipe.close()
    q.put(None)

        
def read_stderr(pipe,q):
    for line in iter(pipe.readline,''):
        q.put('<span style="color:#ff0000;">'+line+'</span>')
    pipe.close()
    q.put(None)

                
class MyThread(QThread):
    set_text = QtCore.pyqtSignal('QString')
    set_done = QtCore.pyqtSignal()
    text_valuepath = None
    cmdstart = None
    cmdend = None
    def __init__(self):
        QThread.__init__(self)

        self.textQ = Queue.Queue()
    def __del__(self):
        self.wait()
    def run(self):
        self.set_text.emit("<h1>Go</h1>")
        cmd = self.cmdstart+' '+self.text_valuepath+' '+self.cmdend
        self.set_text.emit("<h3>"+cmd+"<h3>")
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        tout = threading.Thread(target=read_stdout, args=[p.stdout,self.textQ])
        terr = threading.Thread(target=read_stderr, args=[p.stderr,self.textQ])
        for t in (tout, terr):
            t.start()
        for line in iter(self.textQ.get,None):
            line.replace('\r\n','\n')
            self.set_text.emit(line)
        
        for t in (tout, terr):
            t.join()

        p.wait()
        p.stdout.close()
        p.stderr.close()
        self.textQ.put(None)
        self.set_text.emit("<h1>End</h1>")
        self.set_done.emit()


qtCreatorFile = "main.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(resource_path(qtCreatorFile))

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButtonfix.clicked.connect(self.GoCrazy)
        self.pushButtonValue.clicked.connect(self.getfile)
        self.mycnf=MyConfig()
        a = self.mycnf.readconfig()
        self.lineEditvalue.setText(a[0])
    
    def GoCrazy(self):
        #print "start"
        a=self.mycnf.readconfig()
        self.myThread = MyThread()
        self.myThread.text_valuepath = unicode(self.lineEditvalue.text())
        self.myThread.cmdstart = a[1]
        self.myThread.cmdend = a[2]
        self.myThread.set_text.connect(self.on_set_text)
        self.myThread.set_done.connect(self.on_set_done)
        self.pushButtonfix.setEnabled(False)
        self.myThread.start()
        
    def on_set_done(self):
        self.pushButtonfix.setEnabled(True)

    def on_set_text(self, generated_str):
        self.textBrowser.append(generated_str)
    
    def upconfig(self):
        self.mycnf.writeconfig(self.lineEditvalue.text())
        
    def getfile(self):
        path=QFileDialog.getOpenFileName(self, 'Open file', self.lineEditvalue.text(),"text files (*.txt *.*)")
        self.lineEditvalue.setText(QDir.toNativeSeparators(path))
        self.upconfig()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()
print "all done!"