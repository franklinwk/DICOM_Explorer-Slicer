from __main__ import math, vtk, qt, ctk, slicer
import bisect

class DicomExplorerDateBlock(qt.QDialog):
    def __init__(self, parent, Date):
        qt.QDialog.__init__(self,parent)
        self.timeList=[]
        self.listImageBlocks=[]
        self.setup(Date)
        
    def setup(self,Date):
        self.dateLayout=qt.QHBoxLayout(self)
        self.loadDate(Date)
        
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
        

