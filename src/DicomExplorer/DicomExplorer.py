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
    
    self.browserButton = qt.QPushButton("Open Browser")
    connectorLayout.addRow(self.browserButton)
    
    self.tempButton = qt.QPushButton("Temp")
    connectorLayout.addRow(self.tempButton)    
    
    # Debug box
    self.textBox = qt.QTextEdit()
    self.layout.addWidget(self.textBox)
    
    
    self.layout.addStretch(1)
    
    #Connections
    self.startButton.connect('clicked(bool)', self.onStart)
    self.stopButton.connect('clicked(bool)', self.onStop)
    self.browserButton.connect('clicked(bool)', self.onOpenBrowser)
    self.tempButton.connect('clicked(bool)', self.onTemp)   
    
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
    self.browser = Widgets.DicomExplorerBrowser(self.parent)
    pal = self.browser.palette
    pal.setColor(self.browser.backgroundRole(), qt.QColor(20,20,20))
    self.browser.setPalette(pal)
    #self.browser.setWindowFlags(qt.Qt.FramelessWindowHint)
    self.browser.show()
    
  def onTemp(self):
    self.browser.populateBrowser()    
  
  def extended_fingers(self, fingerList):
    extendedFingerList = []
    for finger in fingerList:
      if finger.is_extended is True:
        extendedFingerList.append(finger)
    return extendedFingerList
  
  def countKeyTaps(self, frame, previousFrameWindow):
    gestureList = frame.gestures(previousFrameWindow)
    count = 0
    for gesture in gestureList:
      if gesture.type == gesture.TYPE_KEY_TAP:
        count = count + 1
    return count
    
  def frameUpdate(self):
    logic = DicomExplorerLogic()
    frame = self.controller.frame()
    lastFrame = self.controller.frame(1)
    fingerList = self.extended_fingers(frame.fingers)
    self.textBox.setPlainText("Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (frame.id, frame.timestamp, len(frame.hands), len(fingerList), len(frame.tools), len(frame.gestures())))
    
    extendedFrameLeftFingers = self.extended_fingers(frame.hands.leftmost.fingers)
    lastFrameLeftFingers = self.extended_fingers(lastFrame.hands.leftmost.fingers)
  
    if (len(frame.hands) == 1 and len(extendedFrameLeftFingers) <= 2 and len(extendedFrameLeftFingers) > 0 and len(lastFrameLeftFingers) <= 2 and frame.hands.leftmost.confidence >= 0.2):
      self.browser.scrollBrowser(frame.hands.leftmost.fingers.frontmost.tip_position.y - lastFrame.hands.leftmost.fingers.frontmost.tip_position.y)

    

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



