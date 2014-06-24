from __main__ import math, vtk, qt, ctk, slicer
import LeapLib.Leap
from LeapLib.Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
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
    

    for node in self.totalListSorted:
      image = self.vtkImageDataToQImage(node[2].GetImageData())
      node[3].setPixmap(qt.QPixmap.fromImage(image))
    
    
    #Go through volume node list and extract vtkImageData from them with relevant fixes (spacing, etc.)
    #Iterate (or repeat) some range of numbers representing which slice of each image should be previewed (based on percentage, so they all repeat the animation in sync)
    #use vtkImageDataToQImage to convert at the correct slice location, then display at correct position in layout
  
  def setup(self):
    self.browserLayout = qt.QVBoxLayout(self) #change to whatever layout is suitable, is any layout suitable? maybe not, I don't know right now    
    self.scrollArea = qt.QScrollArea(self)
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setHorizontalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)
    self.scrollArea.setVerticalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)
    
    self.viewport = qt.QWidget(self)
    self.scrollArea.setWidget(self.viewport)
    
    self.scrollLayout = qt.QGridLayout(self.viewport)
    self.viewport.setLayout(self.scrollLayout)
    
    self.tempLabel2 = qt.QLabel("testing")
    self.scrollLayout.addWidget(self.tempLabel2)    
    
    self.browserLayout.addWidget(self.scrollArea)
    
    #self.currentVolumeNodeList.append(slicer.mrmlScene.GetNodeByID("vtkMRMLScalarVolumeNode1"))
    #self.tempLabel2.setText("<font color='white'>" + slicer.mrmlScene.GetNodeByID("vtkMRMLScalarVolumeNode1").GetAttribute("DICOM.patient") + "\n" + slicer.mrmlScene.GetNodeByID("vtkMRMLScalarVolumeNode1").GetAttribute("DICOM.date"))
    
    #For the conversion function
    self.mrmlUtils = slicer.qMRMLUtils()
    
    #Should be called elsewhere
    self.populateBrowser()
    
    self.timer = qt.QTimer()
    self.timer.timeout.connect(self.updateBrowser)
    self.timer.start(750)
    #Start a qTimer for the update loop that animates thumnails

    
  def vtkImageDataToQImage(self, imageData):
    #Take into account orientation at some point, or to do this quickly, just assume the greatest dimension is the axial view for now
    imageDataWidth = imageData.GetDimensions()[0] #take spacing into account later
    imageDataHeight = imageData.GetDimensions()[1]
    imageDataDepth = imageData.GetDimensions()[2]
    
    width = 50
    height = 50
    if imageDataWidth < 50:
      width = imageDataWidth
    if imageDataHeight < 50:
      height = imageDataHeight
    qtImage = qt.QImage(width, height)
    
    heightStep = imageDataHeight//height
    widthStep = imageDataWidth//width
    
    imageDataSlice = vtk.vtkImageData()
    imageDataSlice.SetDimensions(50,50,1)
    imageDataSlice.SetScalarTypeToUnsignedChar()
    imageDataSlice.SetNumberOfScalarComponents(3)
    imageDataSlice.SetSpacing(1,1,1)
    imageDataSlice.SetOrigin(0,0,0)
    imageDataSlice.AllocateScalars()
    
    #Inefficient, should reimplement mrmlUtils.vtkImageDataToQImage to take the slice or have a cache
    for i in range(0,imageDataWidth-widthStep-1,widthStep):
      for j in range(0,imageDataHeight-heightStep-1,heightStep):
        value = imageData.GetScalarComponentAsDouble(i,j,math.floor(imageDataDepth*self.offsetPortion),0)

        imageDataSlice.SetScalarComponentFromDouble(i//widthStep,j//heightStep,0,0,value/4)
        imageDataSlice.SetScalarComponentFromDouble(i//widthStep,j//heightStep,0,1,value/4)
        imageDataSlice.SetScalarComponentFromDouble(i//widthStep,j//heightStep,0,2,value/4)

    self.mrmlUtils.vtkImageDataToQImage(imageDataSlice, qtImage)
    
    return qtImage
    
    #access qtImage pixel data, copy in imageData pixel data for a specific slice
    #Spacing will need to be taken into account, but I want to get it working like this first
    
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
        imageLabel = qt.QLabel()
        #self.scrollLayout.addWidget(imageLabel)      
        totalList.append([date,time,scalarVolumeNode,imageLabel,description])
        self.GenerateBlock([date,time,scalarVolumeNode,imageLabel,description])
      self.totalListSorted=sorted(totalList,key = lambda x: (x[1], x[2]),reverse=True)

    #Compare with volumeNodeList here, can keep in Node format for the dicom data, but it might be less efficient
    #Add in any series that does not appear in self.currentVolmeNodeList

  def GenerateBlock(self,newNodeData):
    #Method1

    Block=qt.QGroupBox(newNodeData[4])
    vbox=qt.QVBoxLayout()
    vbox.addWidget(newNodeData[3])
    Block.setLayout(vbox)
    self.scrollLayout.addWidget(Block,0,0) ### Position still needs to be set!!!

##    #Method2
##    for i in len(totalListSorted):
##        Block=qt.QWidget()
##        textLabel=qt.QLabel(totalListSorted[i][4])
##        imageLabel=qt.QLabel()
##        vbox = qt.QVBoxLayout()
##        vbox.addWidget(textLabel)
##        vbox.addWidget(imageLabel)
##        Block.setLayout(vbox)
##        self.scrollLayout.addWidget(Block, 2, 0)###Position still needs to be set
      
    

  def updateNodeList(self, volumeNodeList):

    pass
    
    
  def scrollBrowser(self, value):
    current = self.scrollArea.verticalScrollBar().value
    self.scrollArea.verticalScrollBar().setValue(current + value)

