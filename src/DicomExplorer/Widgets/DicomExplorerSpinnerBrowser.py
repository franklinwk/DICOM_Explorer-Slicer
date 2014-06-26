from __main__ import math, vtk, qt, ctk, slicer
import bisect
import Widgets
import LeapLib.Leap
from LeapLib.Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
#
# DicomExplorer
#

class DicomExplorerSpinnerBrowser(qt.QDialog):
  def __init__(self, parent):
    qt.QDialog.__init__(self, parent)
    self.dateList = []
    self.currentVolumeIDList = []
    self.offsetPortion = 0.1
    self.dateBlockDict = {}
    self.selectedDate = 0
    self.gestureRepetitions = 1
    self.setup()
  
  def updateBrowser(self):
    #update browser, called with the qTimer
    if self.offsetPortion >= 0.8:
      self.offsetPortion = 0.1
    else:
      self.offsetPortion = self.offsetPortion + 0.2
    
    for date in self.dateBlockDict:
      if self.dateBlockDict[date].selectedImageBlock is not None:
        self.dateBlockDict[date].selectedImageBlock.updateImageLabel(self.offsetPortion)
      for imageBlock in self.dateBlockDict[date].rightImageBlocks:
        imageBlock.updateImageLabel(self.offsetPortion)
      for imageBlock in self.dateBlockDict[date].leftImageBlocks:
        imageBlock.updateImageLabel(self.offsetPortion)        
    
    #Go through volume node list and extract vtkImageData from them with relevant fixes (spacing, etc.)
    #Iterate (or repeat) some range of numbers representing which slice of each image should be previewed (based on percentage, so they all repeat the animation in sync)
    #use vtkImageDataToQImage to convert at the correct slice location, then display at correct position in layout
  
  def setup(self):
    self.browserLayout = qt.QVBoxLayout(self) #change to whatever layout is suitable, is any layout suitable? maybe not, I don't know right now    
    
    self.fullscreenButton = qt.QPushButton("Fullscreen")
    self.browserLayout.addWidget(self.fullscreenButton)
    self.fullscreenButton.connect('clicked(bool)', self.onFullscreen)
    
    self.left = qt.QPushButton("Left")
    self.browserLayout.addWidget(self.left)
    self.left.connect('clicked(bool)', self.onLeft)

    self.right = qt.QPushButton("Right")
    self.browserLayout.addWidget(self.right)
    self.right.connect('clicked(bool)', self.onRight)
    
    self.scrollArea = qt.QScrollArea(self)
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setHorizontalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)
    self.scrollArea.setVerticalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)
    
    self.viewport = qt.QWidget(self)
    self.scrollArea.setWidget(self.viewport)
    
    self.scrollLayout = qt.QVBoxLayout(self.viewport)
    self.viewport.setLayout(self.scrollLayout)
    
    self.tempLabel2 = qt.QLabel("<font color='white'> This is a widget added to this layout! Spinner Browser!")
    self.scrollLayout.addWidget(self.tempLabel2)
    
    self.scrollLayout.addStretch(1)
    
    self.browserLayout.addWidget(self.scrollArea)
    
    self.timer = qt.QTimer()
    self.timer.timeout.connect(self.updateBrowser)
    self.timer.start(750)
    #Start a qTimer for the update loop that animates thumbnails

  def onFullscreen(self):
    self.showFullScreen()
    
  def populateBrowser(self):
    #Take in a list of scalar volume nodes that have DICOM data
    collection=slicer.mrmlScene.GetNodesByClass('vtkMRMLScalarVolumeNode')
    numberItems=collection.GetNumberOfItems()
    totalList=[]
    for i in range(numberItems):
      scalarVolumeNode=collection.GetItemAsObject(i)
      nodeID=scalarVolumeNode.GetID()
      instanceUID = scalarVolumeNode.GetAttribute("DICOM.instanceUIDs")
      if instanceUID is not None:
        IDFirstSlice=instanceUID.split()
        IDFirstSlice=IDFirstSlice[0]
        if IDFirstSlice not in self.currentVolumeIDList:
          self.currentVolumeIDList.append(IDFirstSlice)
          date=scalarVolumeNode.GetAttribute("DICOM.date")
          time=scalarVolumeNode.GetAttribute("DICOM.time")
          time = str(int(float(time)))
          description=scalarVolumeNode.GetAttribute("DICOM.modality")+"-"+scalarVolumeNode.GetAttribute("DICOM.seriesDescription")
          
          if date not in  self.dateBlockDict:
            dateBlock = Widgets.DicomExplorerSpinnerDateBlock(self, date)
            
            bisect.insort(self.dateList,date)
            self.dateList.sort(reverse=True)
            
            ind=self.dateList.index(date)
            
            self.dateBlockDict[date] = dateBlock
            self.scrollLayout.insertWidget(ind+1,dateBlock)
          else:
            dateBlock = self.dateBlockDict[date]
          
          imageBlock = Widgets.DicomExplorerImageBlock(self)
          imageBlock.setVolumeNode(scalarVolumeNode)
          imageBlock.updateImageLabel(self.offsetPortion)
          imageBlock.setTime(time)
          imageBlock.setDescription(description)
          
          dateBlock.loadImageBlock(time, imageBlock)
      
    #Compare with volumeNodeList here, can keep in Node format for the dicom data, but it might be less efficient
    #Add in any series that does not appear in self.currentVolmeNodeList

    
  def updateNodeList(self, volumeNodeList):
    pass
    
  def onLeft(self):
    for date in self.dateBlockDict:
      self.dateBlockDict[date].moveSelectionLeft()

  def onRight(self):
    for date in self.dateBlockDict:
      self.dateBlockDict[date].moveSelectionRight()    
 
  def scrollBrowser(self, value):
    current = self.scrollArea.verticalScrollBar().value
    self.scrollArea.verticalScrollBar().setValue(current + value)

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
    
  def leapUpdate(self, frame, lastFrame):
    fingerList = self.extended_fingers(frame.fingers)
    
    extendedFrameLeftFingers = self.extended_fingers(frame.hands.leftmost.fingers)
    lastFrameLeftFingers = self.extended_fingers(lastFrame.hands.leftmost.fingers)
  
    if (len(frame.hands) == 1 and len(extendedFrameLeftFingers) <= 2 and len(extendedFrameLeftFingers) > 0 and len(lastFrameLeftFingers) <= 2 and frame.hands.leftmost.confidence >= 0.2):
      self.scrollBrowser(2*(frame.hands.leftmost.fingers.frontmost.tip_position.y - lastFrame.hands.leftmost.fingers.frontmost.tip_position.y))
    
    circleFound = False
    gestureList = frame.gestures() 
    for gesture in gestureList:
      if gesture.type == gesture.TYPE_CIRCLE:
        circleFound = True
        circleGesture = LeapLib.Leap.CircleGesture(gesture)
        if circleGesture.progress > self.gestureRepetitions:
          self.gestureRepetitions = self.gestureRepetitions + 1
          
          if circleGesture.normal.z >= 0.8:
            for date in self.dateBlockDict:
              self.dateBlockDict[date].moveSelectionLeft()
          elif circleGesture.normal.z <= -0.8:
            for date in self.dateBlockDict:
              self.dateBlockDict[date].moveSelectionRight()
        break
    
    if circleFound is False:
      self.gestureRepetitions = 1
    
    return ("Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (frame.id, frame.timestamp, len(frame.hands), len(fingerList), len(frame.tools), len(frame.gestures())))
