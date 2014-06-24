cmake_minimum_required(VERSION 2.8.9)

#-----------------------------------------------------------------------------
set(MODULE_NAME DicomExplorer)

#-----------------------------------------------------------------------------
#Change this once it is packaged as an extension
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
  ${MODULE_NAME}.py
  ${MODULE_NAME}Browser
  )

set(MODULE_PYTHON_RESOURCES
  #Resources/qSlicer${MODULE_NAME}Module.qrc
  Resources/Icons/DicomExplorer.png
  #Resources/Icons/MenuSwitchNone.png
  #Resources/Icons/MenuSwitchOffset.png
  #Resources/Icons/MenuSwitchBrightness.png
  #Resources/Icons/MenuSwitchFiducial.png
  LeapLib/__init__.py
  LeapLib/LeapPython.pyd
  LeapLib/Leap.py
  LeapLib/Leap.dll
  LeapLib/Leap.lib
  LeapLib/LeapJava.dll
  LeapLib/msvcp120.dll
  LeapLib/msvcr120.dll
  )

#-----------------------------------------------------------------------------
slicerMacroBuildScriptedModule(
  NAME ${MODULE_NAME}
  SCRIPTS ${MODULE_PYTHON_SCRIPTS}
  RESOURCES ${MODULE_PYTHON_RESOURCES}
  WITH_GENERIC_TESTS
  )

#-----------------------------------------------------------------------------
if(BUILD_TESTING)

  # Register the unittest subclass in the main script as a ctest.
  # Note that the test will also be available at runtime.
  slicer_add_python_unittest(SCRIPT ${MODULE_NAME}.py)

  # Additional build-time testing
  add_subdirectory(Testing)
endif()