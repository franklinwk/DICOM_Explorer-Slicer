from __main__ import math, vtk, qt, ctk, slicer
import LeapLib.Leap
from LeapLib.Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
#
# DicomExplorer
#

class DicomExplorerBrowser(qt.QDialog):
  def __init__(self, parent):
    qt.QDialog.__init__(self, parent)
    self.currentVolumeNodeList = []
    self.setup()
    
  def setup(self):
    tempLayout = qt.QFormLayout(self) #change to whatever layout is suitable, is any layout suitable? maybe not, I don't know right now
    tempLayout.addWidget(qt.QLabel("I'm a placeholder for fancier things to come!"))
    
    #Start a qTimer for the update loop that animates thumnails

    
  def vtkImageDataToQImage(self, imageData):
    #Take into account orientation at some point, or to do this quickly, just assume the greatest dimension is the axial view for now
    width = imageData.GetDimensions()[0] #take spacing into account later
    height = imageData.GetDimensions()[1]
    qtImage = qt.QImage(width, height, QImage.Format_RGB32)
    
    #access qtImage pixel data, copy in imageData pixel data for a specific slice
    #Spacing will need to be taken into account, but I want to get it working like this first
    
    
  def populateBrowser(self, volumeNodeList):
    #Take in a list of scalar volume nodes that have DICOM data
    
    #Compare with volumeNodeList here, can keep in Node format for the dicom data, but it might be less efficient
    #Add in any series that does not appear in self.currentVolmeNodeList
    pass

    
  def updateBrowser(self):
    #update browser, called with the qTimer
    
    #Go through volume node list and extract vtkImageData from them with relevant fixes (spacing, etc.)
    #Iterate (or repeat) some range of numbers representing which slice of each image should be previewed (based on percentage, so they all repeat the animation in sync)
    #use vtkImageDataToQImage to convert at the correct slice location, then display at correct position in layout
    pass

    