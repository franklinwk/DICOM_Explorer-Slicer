from __main__ import math, vtk, qt, ctk, slicer
import bisect
import Widgets
#
# DicomExplorer
#

class DicomExplorerPointerBrowser(qt.QDialog):
  def __init__(self, parent):
    qt.QDialog.__init__(self, parent)
    self.dateList = []
    self.currentVolumeIDList = []
    self.offsetPortion = 0.1
    self.dateBlockDict = {}
    self.selectedDate = 0
    self.setup()
  
  def updateBrowser(self):
    #update browser, called with the qTimer
    if self.offsetPortion >= 0.8:
      self.offsetPortion = 0.1
    else:
      self.offsetPortion = self.offsetPortion + 0.2
    
    for date in self.dateBlockDict:
      for imageBlock in self.dateBlockDict[date].listImageBlocks:
        imageBlock.updateImageLabel(self.offsetPortion)
    
    #Go through volume node list and extract vtkImageData from them with relevant fixes (spacing, etc.)
    #Iterate (or repeat) some range of numbers representing which slice of each image should be previewed (based on percentage, so they all repeat the animation in sync)
    #use vtkImageDataToQImage to convert at the correct slice location, then display at correct position in layout
  
  def setup(self):
    self.browserLayout = qt.QVBoxLayout(self) #change to whatever layout is suitable, is any layout suitable? maybe not, I don't know right now    
    
    self.fullscreenButton = qt.QPushButton("Fullscreen")
    self.browserLayout.addWidget(self.fullscreenButton)
    self.fullscreenButton.connect('clicked(bool)', self.onFullscreen)
    
    self.scrollArea = qt.QScrollArea(self)
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setHorizontalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)
    self.scrollArea.setVerticalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)
    
    self.viewport = qt.QWidget(self)
    self.scrollArea.setWidget(self.viewport)
    
    self.scrollLayout = qt.QVBoxLayout(self.viewport)
    self.viewport.setLayout(self.scrollLayout)
    
    self.tempLabel2 = qt.QLabel("<font color='white'> This is a widget added to this layout!")
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
      IDFirstSlice=scalarVolumeNode.GetAttribute("DICOM.instanceUIDs").split()
      IDFirstSlice=IDFirstSlice[0]
      if IDFirstSlice not in self.currentVolumeIDList:
        self.currentVolumeIDList.append(IDFirstSlice)
        date=scalarVolumeNode.GetAttribute("DICOM.date")
        time=scalarVolumeNode.GetAttribute("DICOM.time")
        time = str(int(float(time)))
        description=scalarVolumeNode.GetAttribute("DICOM.modality")+"-"+scalarVolumeNode.GetAttribute("DICOM.seriesDescription")
        
        if date not in  self.dateBlockDict:
          dateBlock = Widgets.DicomExplorerDateBlock(self, date)
          
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
    
    
  def scrollBrowser(self, value):
    current = self.scrollArea.verticalScrollBar().value
    self.scrollArea.verticalScrollBar().setValue(current + value)

