import bisect

class DateBlock(qt.QDialog,Date,imageBlock):
    def __init__(self, parent):
        qt.QDialog.__init__(self,parent)
        self.timeList=[]
        self.listImageBlocks=[]
        self.setup()
        
    def setup(self,Date):
        self.dateLayout=qt.HBoxLayout(self)
        self.loadDate(Date)
        
    def loadDate(self,Date):
        dateLabel=qt.QLabel()
        dateLabel.setText(Date)
        self.dateLayout.addWidget(dateLabel)
        
    def loadImageBlock(self,blocktime,imageBlock):
        bisect.insort(self.timeList,blocktime)
        ind=self.timeList.index(blocktime)
        self.listImageBlocks.append(imageBlock)
        self.dateLayout.insertWidget(ind,blocktime)
        

