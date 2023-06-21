#!python
# check zips
# v1.0 2023 paulo.ernesto, debora.roldao
# Copyright 2023 Vale
# License: Apache 2.0

import sys, os.path, threading, zipfile, pickle, time
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtGui import QFont

class TreeWalk(QThread):
  _fp = '.'
  _tl = threading.Lock()
  _ps = dict()
  _pp = os.path.splitext(os.path.realpath(sys.argv[0]))[0] + '.pyp'
  _tf = False

  def run(self):
    self._tf = True
    for root, dirs, files in os.walk(self._fp):
      for fn in files:
        if fn == self._pp:
          print("found resume file:", fn)
          self._ps.update(pickle.load(open(os.path.join(root, fn), 'rb')))
      
      for fn in files:
        p = os.path.join(root, fn)
        self._tl.acquire()
        if p in self._ps:
          print(self._ps.get(p) == None and 'pass' or 'fail','(resumed)',p)
        elif fn.lower().endswith('zip'):
          z = zipfile.ZipFile(p)
          t = None
          try:
            t = z.testzip()
          except Exception as e:
            t = str(e)
          if t:
            print('fail ‼',p,':',t)
          else:
            print('pass',p)
          self._ps[p] = t

        self._tl.release()
    self.save()
    self._tf = False
  
  def result(self):
    return self._ps
  
  def get(self):
    return self._fp

  def set(self, fp = None):
    if fp is not None:
      self._fp = fp

  def save(self):
    p = os.path.join(self._fp, self._pp)
    pickle.dump(self._ps, open(p,'wb'))

  def toggle(self):
    if self.isRunning():
      if self._tf:
        self._tl.acquire()
        self._tf = False
        self.save()
      elif self._tl.locked():
        self._tf = True
        self._tl.release()
    else:
      self.start()

  def has_resume(self):
    return os.path.exists(os.path.join(self._fp, self._pp))

  def clear(self):
    self._ps.clear()
    p = os.path.join(self._fp, self._pp)
    if os.path.exists(p):
      os.remove(p)

class CentralWidget(QWidget):
  _s_start = '⏩ start'
  _s_stop = '⏸️ pause'
  _folder = None
  _walker = None
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setLayout(QVBoxLayout())
    self.setFont(QFont(self.font().family(), self.font().pointSize() * 2))
    w = QLabel('check zip files')
    w.setAlignment(Qt.AlignHCenter)
    self.layout().addWidget(w)
    self.layout().addSpacing(self.layout().spacing() * 2)
    self._pb_browse = QPushButton('📂 select folder')
    self._pb_browse.clicked.connect(self.browse)
    self.layout().addWidget(self._pb_browse)
    self.layout().addSpacing(self.layout().spacing() * 2)
    self._pb_resume = QPushButton('🔄 clear resume data')
    self._pb_resume.setEnabled(False)
    self._pb_resume.clicked.connect(self.clear_resume)
    self.layout().addWidget(self._pb_resume)
    self.layout().addSpacing(self.layout().spacing() * 2)
    self._pb_toggle = QPushButton(self._s_start)
    self._pb_toggle.clicked.connect(self.worker_toggle)
    self.layout().addWidget(self._pb_toggle)
    self._te_result = QTextEdit()
    self.layout().addWidget(self._te_result)
  
  def browse(self):
    fp = QFileDialog.getExistingDirectory()
    if fp:
      self.worker_setup(fp)
      self._te_result.append('select folder: ' + fp)
      self._pb_resume.setEnabled(self._walker.has_resume())

  def worker_setup(self, fp = None):
    if self._walker is None or self._walker.isFinished():
      self._te_result.clear()
      if fp is None and self._walker is not None:
        fp = self._walker.get()
      self._walker = TreeWalk()
      self._walker.set(fp)
      self._walker.finished.connect(self.worker_finished)
    
    if fp is not None:
      self._walker.set(fp)

  def clear_resume(self):
    if self._walker is not None:
      self._walker.clear()
    self._pb_resume.setEnabled(False)

  def worker_toggle(self):
    self.worker_setup()
    if self._pb_toggle.text() == self._s_start:
      self._pb_toggle.setText(self._s_stop)
      self._te_result.append(time.strftime('%H:%M:%S start'))
    else:
      self._pb_toggle.setText(self._s_start)
      self._te_result.append(time.strftime('%H:%M:%S pause'))
    
    self._pb_toggle.setEnabled(False)
    self._walker.toggle()
    self._pb_toggle.setEnabled(True)

  def worker_finished(self):
    self._pb_toggle.setText(self._s_start)
    self._pb_resume.setEnabled(True)
    r = self._walker.result()
    self._te_result.append(time.strftime('%H:%M:%S finished'))
    self._te_result.append('%d files PASS' % len([None for v in r.values() if v is None]))
    self._te_result.append('%d files FAIL' % len([None for v in r.values() if v is not None]))
    for k,v in r.items():
      if v is not None:
        self._te_result.append('%s : %s' % (k,v))
  
  def save(self):
    if self._walker is not None and self._walker.isRunning():
      self._walker.save()

class App(QApplication):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._mw = QMainWindow(size = self.desktop().availableGeometry().size() * 0.5)
    self._cw = CentralWidget()
    self._mw.setCentralWidget(self._cw)
    self.aboutToQuit.connect(self.close_event)
    self._mw.show()
    self.exec()
  
  def close_event(self):
    self._cw.save()

if __name__=="__main__":
  App(sys.argv)
