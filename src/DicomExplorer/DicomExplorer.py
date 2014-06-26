from __main__ import math, vtk, qt, ctk, slicer
import Widgets
import LeapLib.Leap
from LeapLib.Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
#
# DicomExplorer
#

class DicomExplorer:
  def __init__(self, parent):
    parent.title = "DICOM_Explorer"
    parent.categories = ["DICOM "]
    parent.contributors = ["Franklin King (Queen's University), Saskia Camps (Brigham)"]
    parent.helpText = """
    Add help text
    """
    parent.acknowledgementText = """
    This work was funded by Cancer Care Ontario and the Ontario Consortium for Adaptive Interventions in Radiation Oncology (OCAIRO)
""" 
    parent.icon = qt.QIcon(os.path.dirname(parent.path) + '/Resources/Icons/DicomExplorer.png')
    self.parent = parent

#
# qDicomExplorerWidget
#
class DicomExplorerWidget:
  def __init__(self, parent = None):
    self.path = os.path.dirname(slicer.modules.dicomexplorer.path)
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    self.lastCommandId = 0
    self.timeoutCounter = 0
    if not parent:
      self.setup()
      self.parent.show()

      
  def setup(self):
    # # Instantiate and connect widgets
    
    connectorCollapsibleButton = ctk.ctkCollapsibleButton()
    connectorCollapsibleButton.text = "Leap Motion Controller Connector"
    self.layout.addWidget(connectorCollapsibleButton)    
    connectorLayout = qt.QFormLayout(connectorCollapsibleButton)    

    # Start and stop listening
    self.startButton = qt.QPushButton("Start Recording")
    connectorLayout.addRow(self.startButton)
    
    self.stopButton = qt.QPushButton("Stop Recording")
    connectorLayout.addRow(self.stopButton)
    
    #Buttons, boxes
    self.schemeBrowserSelector = ctk.ctkComboBox()
    self.schemeBrowserSelector.addItem('%s. Pointer Browser' % 0)
    self.schemeBrowserSelector.addItem('%s. Spinner Browser' % 1)
    connectorLayout.addRow("Browser Type:", self.schemeBrowserSelector)
    
    self.browserButton = qt.QPushButton("Open Browser")
    connectorLayout.addRow(self.browserButton)  
    
    self.updateButton = qt.QPushButton("Update")
    connectorLayout.addRow(self.updateButton)    
    
    # Debug box
    self.textBox = qt.QTextEdit()
    self.layout.addWidget(self.textBox)
    
    
    self.layout.addStretch(1)
    
    #Connections
    self.startButton.connect('clicked(bool)', self.onStart)
    self.stopButton.connect('clicked(bool)', self.onStop)
    self.browserButton.connect('clicked(bool)', self.onOpenBrowser)

    self.updateButton.connect('clicked(bool)', self.onUpdate)   
    
    # Instantiate timer
    self.timer = qt.QTimer()
    
    # Instantiate Leap Motion device
    self.controller = LeapLib.Leap.Controller()
    self.controller.enable_gesture(LeapLib.Leap.Gesture.TYPE_CIRCLE);
    self.controller.enable_gesture(LeapLib.Leap.Gesture.TYPE_KEY_TAP);
    self.controller.enable_gesture(LeapLib.Leap.Gesture.TYPE_SCREEN_TAP);
    self.controller.enable_gesture(LeapLib.Leap.Gesture.TYPE_SWIPE);    
  
  def onStart(self):
    self.timer.timeout.connect(self.frameUpdate)
    self.timer.start(70)
  
  def onStop(self):
    self.timer.stop()

  def onOpenBrowser(self):
    type = self.schemeBrowserSelector.currentIndex
    if type == 0:
      self.browser = Widgets.DicomExplorerPointerBrowser(self.parent)
      pal = self.browser.palette
      pal.setColor(self.browser.backgroundRole(), qt.QColor(20,20,20))
      self.browser.setPalette(pal)
      #self.browser.setWindowFlags(not qt.Qt.WindowStaysOnTopHint)
      self.browser.show()
    else:
      self.browser = Widgets.DicomExplorerSpinnerBrowser(self.parent)
      pal = self.browser.palette
      pal.setColor(self.browser.backgroundRole(), qt.QColor(50,50,50))
      self.browser.setPalette(pal)
      #self.browser.setWindowFlags(not qt.Qt.WindowStaysOnTopHint)
      self.browser.show()
      
  def onUpdate(self):
    self.browser.populateBrowser()    
  
  def frameUpdate(self):
    logic = DicomExplorerLogic()
    frame = self.controller.frame()
    lastFrame = self.controller.frame(1)    
    
    debugInfo = self.browser.leapUpdate(frame, lastFrame)
    self.textBox.setPlainText(debugInfo)
    

#
# DicomExplorerLogic
#
class DicomExplorerLogic:
  def __init__(self):
    pass
 
  def extended_fingers(self, fingerList):
    extendedFingerList = []
    for finger in fingerList:
      if finger.is_extended is True:
        extendedFingerList.append(finger)

    return extendedFingerList   



