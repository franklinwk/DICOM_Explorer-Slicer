from __main__ import math, vtk, qt, ctk, slicer

class DicomExplorerImageBlock(qt.QFrame):
  def __init__(self, parent):
    qt.QFrame.__init__(self, parent)
    self.setFrameShape(qt.QFrame.NoFrame)
    self.setFixedSize(qt.QSize(100, 120))
    
    self.imageLabel = qt.QLabel()
    self.textLabel = qt.QLabel("<font color='55ff88'>empty</font>")
    self.description = ""
    self.time = "NULL"
    self.imageNode = slicer.vtkMRMLScalarVolumeNode()
    self.imageCache = {}
    self.thumbnailWidth = 100
    self.thumbnailHeight = 100
    
    #For the conversion function
    self.mrmlUtils = slicer.qMRMLUtils()    
    
    layout = qt.QVBoxLayout(self)
    
    layout.addWidget(self.textLabel)
    layout.addWidget(self.imageLabel)

  
  def vtkImageDataToQImage(self, imageData, offsetPortion):
  
    if offsetPortion in self.imageCache:
      return self.imageCache[offsetPortion]
    else:
      #Take into account orientation at some point, or to do this quickly, just assume the greatest dimension is the axial view for now
      imageDataDimensions = [0,0,0]
      imageDataDimensions[0] = imageData.GetDimensions()[0] #take spacing into account later
      imageDataDimensions[1] = imageData.GetDimensions()[1]
      imageDataDimensions[2] = imageData.GetDimensions()[2]
      
      imageDataDepth = min(imageDataDimensions)
      imageDataWidth = max(imageDataDimensions)
      widthIndex = imageDataDimensions.index(imageDataWidth)
      imageDataDimensions[widthIndex] = -1
      imageDataHeight = max(imageDataDimensions)
      heightIndex = imageDataDimensions.index(imageDataHeight)
      
      width = self.thumbnailWidth
      height = self.thumbnailHeight
      if imageDataWidth < self.thumbnailWidth:
        width = imageDataWidth
      if imageDataHeight < self.thumbnailHeight:
        height = imageDataHeight
      qtImage = qt.QImage(width, height)
      
      depth = math.floor(imageDataDepth*offsetPortion)
      
      widthStep = int(math.ceil(imageDataWidth/width))
      heightStep = int(math.ceil(imageDataHeight/height))
      
      imageDataSlice = vtk.vtkImageData()
      imageDataSlice.SetDimensions(width,height,1)
      imageDataSlice.SetScalarTypeToUnsignedChar()
      imageDataSlice.SetNumberOfScalarComponents(3)
      imageDataSlice.SetSpacing(1,1,1)
      imageDataSlice.SetOrigin(0,0,0)
      imageDataSlice.AllocateScalars()
      
      #Could be more efficient if reimplemented mrmlUtils.vtkImageDataToQImage to take the slice, but cache seems to be enough
      for i in range(0,width):
        for j in range(0,height):
          #just using the largest two as length and width, spacing is not taken into account
          if (widthIndex is 0 and heightIndex is 1):
            value = imageData.GetScalarComponentAsDouble(i*widthStep,j*heightStep,depth,0)
          elif (widthIndex is 1 and heightIndex is 0):
            value = imageData.GetScalarComponentAsDouble(j*heightStep,i*widthStep,depth,0)
          elif (widthIndex is 1 and heightIndex is 2):
            value = imageData.GetScalarComponentAsDouble(depth,i*widthStep,j*heightStep,0)
          elif (widthIndex is 2 and heightIndex is 1):
            value = imageData.GetScalarComponentAsDouble(depth,j*heightStep,i*widthStep,0)
          elif (widthIndex is 0 and heightIndex is 2):
            value = imageData.GetScalarComponentAsDouble(i*widthStep,depth,j*heightStep,0)
          else:
            value = imageData.GetScalarComponentAsDouble(j*heightStep,depth,i*widthStep,0)
          
          imageDataSlice.SetScalarComponentFromDouble(i,j,0,0,value/3)
          imageDataSlice.SetScalarComponentFromDouble(i,j,0,1,value/3)
          imageDataSlice.SetScalarComponentFromDouble(i,j,0,2,value/3)

      self.mrmlUtils.vtkImageDataToQImage(imageDataSlice, qtImage)
      
      self.imageCache[offsetPortion] = qtImage
      return qtImage
    
    #access qtImage pixel data, copy in imageData pixel data for a specific slice
    #Spacing will need to be taken into account, but I want to get it working like this first
  
  def setVolumeNode(self, node):
    self.imageNode = node
    
  def updateTextLabel(self):
    self.textLabel.setText("<font color='green'>" + self.time + "    " + self.description + "</font>")
    
  def setTime(self, newTime):
    self.time = newTime

  def setDescription(self, newDescription):
    self.description = newDescription
    self.updateTextLabel()

  def updateImageLabel(self, offsetPortion):
    image = self.vtkImageDataToQImage(self.imageNode.GetImageData(), offsetPortion)
    self.imageLabel.setPixmap(qt.QPixmap.fromImage(image))


# #Method1

    # Block=qt.QGroupBox(newNodeData[4])
    # vbox=qt.QVBoxLayout()
    # vbox.addWidget(newNodeData[3])
    # Block.setLayout(vbox)
    # self.scrollLayout.addWidget(Block,0,0) ### Position still needs to be set!!!

# ##    #Method2
# ##    for i in len(totalListSorted):
# ##        Block=qt.QWidget()
# ##        textLabel=qt.QLabel(totalListSorted[i][4])
# ##        imageLabel=qt.QLabel()
# ##        vbox = qt.QVBoxLayout()
# ##        vbox.addWidget(textLabel)
# ##        vbox.addWidget(imageLabel)
# ##        Block.setLayout(vbox)
# ##        self.scrollLayout.addWidget(Block, 2, 0)###Position still needs to be set