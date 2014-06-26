from __main__ import math, vtk, qt, ctk, slicer
import bisect

class DicomExplorerSpinnerDateBlock(qt.QWidget):
    def __init__(self, parent, Date):
        qt.QWidget.__init__(self,parent)
        self.timeList=[]
        self.rightImageBlocks=[]
        self.leftImageBlocks=[]
        self.selectedImageBlock = None
        self.selectedTimeIndex = 0
        self.selectedPreviousTime = 0
        self.setup(Date)
        
    def setup(self,Date):
        self.dateLayout=qt.QHBoxLayout(self)
        self.dateLayout.setAlignment(qt.Qt.AlignLeft)
        self.loadDate(Date)
        
        #self.dateLayout.addStretch(1)
        
        self.leftImagesWidget = qt.QWidget(self)
        self.dateLayout.addWidget(self.leftImagesWidget)
        self.leftImagesLayout = qt.QHBoxLayout(self.leftImagesWidget)
        self.leftImagesLayout.setAlignment(qt.Qt.AlignRight)
        self.leftImagesWidget.setFixedSize(qt.QSize(300, 120))

        self.selectedImageWidget = qt.QWidget(self)
        self.dateLayout.addWidget(self.selectedImageWidget)
        self.selectedImageLayout = qt.QHBoxLayout(self.selectedImageWidget)
        self.selectedImageLayout.setAlignment(qt.Qt.AlignHCenter)        
        
        self.rightImagesWidget = qt.QWidget(self)
        self.dateLayout.addWidget(self.rightImagesWidget)
        self.rightImagesLayout = qt.QHBoxLayout(self.rightImagesWidget)
        self.rightImagesLayout.setAlignment(qt.Qt.AlignLeft)
        self.leftImagesWidget.setFixedSize(qt.QSize(300, 120))
        
        self.dateLayout.addStretch(1)
        
        
    def loadDate(self,Date):
        dateLabel=qt.QLabel()
        dateLabel.setText("<font color='green'>" + Date)
        self.dateLayout.addWidget(dateLabel)
        
    def loadImageBlock(self,blocktime,imageBlock):
        bisect.insort(self.timeList,blocktime)
        self.timeList.sort(reverse=True)
        
        ind=self.timeList.index(blocktime)
        
        if len(self.timeList) is 1:
          self.selectedImageBlock = imageBlock
          self.selectedImageLayout.addWidget(imageBlock)
          self.selectedTimeIndex = ind
          self.selectedImageBlock.setFrameShape(qt.QFrame.Panel)
          self.selectedPreviousTime = blocktime
        elif blocktime > self.selectedPreviousTime:
          self.leftImageBlocks.insert(ind, imageBlock)
          self.leftImagesLayout.insertWidget(ind, imageBlock)
          self.selectedTimeIndex = self.selectedTimeIndex + 1
        else:
          self.rightImageBlocks.insert(ind-self.selectedTimeIndex, imageBlock)
          self.rightImagesLayout.insertWidget(ind-self.selectedTimeIndex, imageBlock)

    
    def moveSelectionRight(self):
      if len(self.rightImageBlocks) > 0:
        oldSelectedImageBlock = self.selectedImageBlock
        self.selectedPreviousTime = self.selectedImageBlock.time
        self.leftImageBlocks.append(oldSelectedImageBlock)
        self.leftImagesLayout.addWidget(oldSelectedImageBlock)
        #self.selectedImageLayout.removeItem(self.selectedImageLayout.itemAt(0))
        
        self.selectedTimeIndex = self.selectedTimeIndex + 1
        
        self.selectedImageBlock.setFrameShape(qt.QFrame.NoFrame)
        self.selectedImageBlock = self.rightImageBlocks[0]
        self.selectedImageBlock.setFrameShape(qt.QFrame.Panel)
        self.selectedImageLayout.addWidget(self.selectedImageBlock)
        self.rightImageBlocks.pop(0)
        #self.rightImagesLayout.removeItem(self.rightImagesLayout.itemAt(0))

    def moveSelectionLeft(self):
      if len(self.leftImageBlocks) > 0:
        oldSelectedImageBlock = self.selectedImageBlock
        self.selectedPreviousTime = self.selectedImageBlock.time
        self.rightImageBlocks.insert(0,oldSelectedImageBlock)
        self.rightImagesLayout.addWidget(oldSelectedImageBlock)
        #self.selectedImageLayout.removeItem(self.selectedImageLayout.itemAt(0))
        
        self.selectedTimeIndex = self.selectedTimeIndex - 1
        
        self.selectedImageBlock.setFrameShape(qt.QFrame.NoFrame)
        self.selectedImageBlock = self.leftImageBlocks[self.selectedTimeIndex]
        self.selectedImageBlock.setFrameShape(qt.QFrame.Panel)
        self.selectedImageLayout.addWidget(self.selectedImageBlock)
        self.leftImageBlocks.pop()
        #self.leftImagesLayout.removeItem(self.leftImagesLayout.itemAt(self.selectedTimeIndex))


