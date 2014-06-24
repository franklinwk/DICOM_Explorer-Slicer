from __main__ import math, vtk, qt, ctk, slicer
import Widgets
#
# DicomExplorer
#

class DicomExplorerBrowser(qt.QDialog):
  def __init__(self, parent):
    qt.QDialog.__init__(self, parent)
    self.totalListSorted = []
    self.currentVolumeIDList = []
    self.offsetPortion = 0.1
    self.setup()
  
  def updateBrowser(self):
    #update browser, called with the qTimer
    if self.offsetPortion >= 0.8:
      self.offsetPortion = 0.1
    else:
      self.offsetPortion = self.offsetPortion + 0.2
    

    for imageBlock in self.totalListSorted:
      imageBlock.updateImageLabel(self.offsetPortion)
    
    
    #Go through volume node list and extract vtkImageData from them with relevant fixes (spacing, etc.)
    #Iterate (or repeat) some range of numbers representing which slice of each image should be previewed (based on percentage, so they all repeat the animation in sync)
    #use vtkImageDataToQImage to convert at the correct slice location, then display at correct position in layout
  
  def setup(self):
    self.browserLayout = qt.QVBoxLayout(self) #change to whatever layout is suitable, is any layout suitable? maybe not, I don't know right now    
    self.scrollArea = qt.QScrollArea(self)
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setHorizontalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)
    self.scrollArea.setVerticalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)
    
    print " this happened first"
    
    self.viewport = qt.QWidget(self)
    self.scrollArea.setWidget(self.viewport)
    
    self.scrollLayout = qt.QGridLayout(self.viewport)
    self.viewport.setLayout(self.scrollLayout)
    
    self.tempLabel2 = qt.QLabel("testing")
    self.scrollLayout.addWidget(self.tempLabel2)
    
    self.browserLayout.addWidget(self.scrollArea)
    
    #self.currentVolumeNodeList.append(slicer.mrmlScene.GetNodeByID("vtkMRMLScalarVolumeNode1"))
    #self.tempLabel2.setText("<font color='white'>" + slicer.mrmlScene.GetNodeByID("vtkMRMLScalarVolumeNode1").GetAttribute("DICOM.patient") + "\n" + slicer.mrmlScene.GetNodeByID("vtkMRMLScalarVolumeNode1").GetAttribute("DICOM.date"))
    
    self.timer = qt.QTimer()
    self.timer.timeout.connect(self.updateBrowser)
    self.timer.start(750)
    #Start a qTimer for the update loop that animates thumbnails

    

    
  def populateBrowser(self):
    #Take in a list of scalar volume nodes that have DICOM data
    collection=slicer.mrmlScene.GetNodesByClass('vtkMRMLScalarVolumeNode')
    numberItems=collection.GetNumberOfItems()
    currentVolumeIDList=[]
    totalList=[]
    for i in range(numberItems):
      scalarVolumeNode=collection.GetItemAsObject(i)
      nodeID=scalarVolumeNode.GetID()
      IDFirstSlice=scalarVolumeNode.GetAttribute("DICOM.instanceUIDs").split()
      IDFirstSlice=IDFirstSlice[0]
      if IDFirstSlice not in currentVolumeIDList:
        currentVolumeIDList.append(IDFirstSlice)
        date=scalarVolumeNode.GetAttribute("DICOM.date")
        time=scalarVolumeNode.GetAttribute("DICOM.time")
        description=scalarVolumeNode.GetAttribute("DICOM.modality")+"-"+scalarVolumeNode.GetAttribute("DICOM.seriesDescription")
        
        #for dateBlock in dateBlockList:
        #  if dateBlock.date 
        
        #dateBlock = Widgets.DicomExplorerDateBlock(self)
        
        imageBlock = Widgets.DicomExplorerImageBlock(self)
        imageBlock.setVolumeNode(scalarVolumeNode)
        imageBlock.updateImageLabel(self.offsetPortion)
        imageBlock.setTime(time)
        imageBlock.setDescription(description)
        
        #dateBlock.addImageBlock(imageBlock)
        
        
        self.scrollLayout.addWidget(imageBlock)
        
        #self.scrollLayout.addWidget(imageLabel)      
        self.totalListSorted.append(imageBlock) # Temporary
        #totalList.append([date,time,scalarVolumeNode,imageLabel,description])
        #self.GenerateBlock([date,time,scalarVolumeNode,imageLabel,description])
      #self.totalListSorted=sorted(totalList,key = lambda x: (x[1], x[2]),reverse=True)
      
    #Compare with volumeNodeList here, can keep in Node format for the dicom data, but it might be less efficient
    #Add in any series that does not appear in self.currentVolmeNodeList
      
    

  def updateNodeList(self, volumeNodeList):
    pass
    
    
  def scrollBrowser(self, value):
    current = self.scrollArea.verticalScrollBar().value
    self.scrollArea.verticalScrollBar().setValue(current + value)

