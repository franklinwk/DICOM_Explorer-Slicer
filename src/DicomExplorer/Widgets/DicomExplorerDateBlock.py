from __main__ import math, vtk, qt, ctk, slicer
import bisect

class DicomExplorerDateBlock(qt.QWidget):
    def __init__(self, parent, Date):
        qt.QWidget.__init__(self,parent)
        self.timeList=[]
        self.listImageBlocks=[]
        self.setup(Date)
        
    def setup(self,Date):
        self.dateLayout=qt.QHBoxLayout(self)
        self.dateLayout.setAlignment(qt.Qt.AlignLeft)
        self.loadDate(Date)
        self.dateLayout.addStretch(1)
        #self.setLayout(self.dateLayout)
        
    def loadDate(self,Date):
        dateLabel=qt.QLabel()
        dateLabel.setText("<font color='white'>" + Date)
        self.dateLayout.addWidget(dateLabel)
        
    def loadImageBlock(self,blocktime,imageBlock):
        bisect.insort(self.timeList,blocktime)
        self.timeList.sort(reverse=True)
        
        ind=self.timeList.index(blocktime)
        self.listImageBlocks.append(imageBlock)
        self.dateLayout.insertWidget(ind+1,imageBlock)

        
        
