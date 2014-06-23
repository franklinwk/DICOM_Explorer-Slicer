cmake_minimum_required(VERSION 2.8.9)

#-----------------------------------------------------------------------------
project(DicomExplorer)

#-----------------------------------------------------------------------------
set(EXTENSION_HOMEPAGE "http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Modules/DicomExplorer")
set(EXTENSION_CATEGORY "DICOM ")
set(EXTENSION_CONTRIBUTORS "Franklin King (PerkLab, Queen's University), Saskia Camps (Brigham)")
set(EXTENSION_DESCRIPTION "Leap Motion ")
set(EXTENSION_ICONURL "http://www.slicer.org/slicerWiki/images/7/71/DicomExplorerLogo.png")
set(EXTENSION_SCREENSHOTURLS "http://www.slicer.org/slicerWiki/images/c/ca/DicomExplorerScreenshot.png")
set(EXTENSION_STATUS "Experimental")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated list or 'NA' if any

#-----------------------------------------------------------------------------
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
add_subdirectory(DicomExplorer)

#-----------------------------------------------------------------------------
INCLUDE(${Slicer_EXTENSION_CPACK})
