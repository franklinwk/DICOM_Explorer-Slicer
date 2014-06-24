from __main__ import math, vtk, qt, ctk, slicer

class DicomExplorerImageBlock(qt.QWidget):
  def __init__(self, parent):
    qt.QWidget.__init__(self, parent)
    self.imageLabel = qt.QLabel()
    self.textLabel = qt.QLabel("<font color='55ff88'>empty</font>")
    self.description = ""
    self.time = "NULL"
    self.imageNode = slicer.vtkMRMLScalarVolumeNode()
    self.imageCache = {}
    
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
      
      #Could be more efficient if reimplemented mrmlUtils.vtkImageDataToQImage to take the slice, but cache seems to be enough
      for i in range(0,imageDataWidth-widthStep-1,widthStep):
        for j in range(0,imageDataHeight-heightStep-1,heightStep):
          value = imageData.GetScalarComponentAsDouble(i,j,math.floor(imageDataDepth*offsetPortion),0)

          imageDataSlice.SetScalarComponentFromDouble(i//widthStep,j//heightStep,0,0,value/4)
          imageDataSlice.SetScalarComponentFromDouble(i//widthStep,j//heightStep,0,1,value/4)
          imageDataSlice.SetScalarComponentFromDouble(i//widthStep,j//heightStep,0,2,value/4)

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