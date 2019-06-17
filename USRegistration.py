# coding: utf-8
import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import subprocess

#
# USRegistration
#


class USRegistration(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Fast registration" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["Anna Zapaishchykova(TUM)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = "This is the module for 3d spatial ultrasound registration"
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = "PMSD course"

#
# USRegistrationWidget
#


class USRegistrationWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    # "Run extend.bat" button
    extendButton = qt.QPushButton("Run extend.bat")
    extendButton.toolTip = "Run configuration file"
    parametersFormLayout.addWidget(extendButton)
    extendButton.connect('clicked(bool)', self.onExtendButtonClicked)

    # loadSequence button
    loadButton = qt.QPushButton("Load data")
    loadButton.toolTip = "Load file"
    parametersFormLayout.addWidget(loadButton)
    loadButton.connect('clicked(bool)', self.onLoadButtonClicked)

    # loadSequence button
    addNeedleModelButton = qt.QPushButton("Add needle model")
    addNeedleModelButton.toolTip = "Create Models module"
    parametersFormLayout.addWidget(addNeedleModelButton)
    addNeedleModelButton.connect('clicked(bool)', self.onAddNeedleModelClicked)

    # tranform button
    addTransformButton = qt.QPushButton("Change transform")
    addTransformButton.toolTip = "Change hierarchy order"
    parametersFormLayout.addWidget(addTransformButton)
    addTransformButton.connect('clicked(bool)', self.onTransformClicked)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.extendButton = extendButton
    self.loadButton = loadButton
    self.addNeedleModelButton = addNeedleModelButton


  def onExtendButtonClicked(self):
    logic = ModuleLogic()
    result = logic.process()
    qt.QMessageBox.information(slicer.util.mainWindow(), 'Slicer Python', result)

  def onLoadButtonClicked(self):
    logic = ModuleLogic()
    result = logic.loading()
    qt.QMessageBox.information(slicer.util.mainWindow(), 'Slicer Python', result)

  def onAddNeedleModelClicked(self):
    logic = ModuleLogic()
    result = logic.addNeedleModel()
    qt.QMessageBox.information(slicer.util.mainWindow(), 'Slicer Python', result)

  def onTransformClicked(self):
    logic = ModuleLogic()
    result = logic.transformation()
    qt.QMessageBox.information(slicer.util.mainWindow(), 'Slicer Python', result)
#
# ModuleLogic
#


class ModuleLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def process(self):
    subprocess.call([r'D:\calibration_20190520\extend.bat'])
    return "Settings configured!"

  def loading(self):
    # sequence = slicer.mrmlScene.AddNode(slicer.vtkMRMLSequenceNode())
    # sequencebrowser = slicer.mrmlScene.AddNode(slicer.vtkMRMLSequenceBrowserNode())
    # model0 = slicer.util.loadModel(r“D:\calibration_20190520\volume3.mha”, True)[1]
    io = slicer.app.ioManager()
    params = {}
    io.openDialog("Sequence Metafile", slicer.qSlicerFileDialog.Read, params)
    return "File loaded!"

  def addNeedleModel(self):
    scene = slicer.mrmlScene
    e = vtk.vtkImageEllipsoidSource()

    # Create model node
    logic = slicer.modules.createmodels.logic()
    model = logic.CreateNeedle(80, 1, 2.5, True)
    model.SetScene(scene)
    model.SetName(scene.GenerateUniqueName("NeedleModel"))

    # Add to scene
    model.GetDisplayNode().SetSliceIntersectionVisibility(True)
    model.GetDisplayNode().SetSliceIntersectionThickness(3)
    model.GetDisplayNode().SetColor(1, 1, 0)

    return "Needle Model created!"

  def transformation(self):
    trackerToProbeNode = slicer.util.getNode("volume3-TrackerToProbe")
    stylusToTrackerNode = slicer.util.getNode("volume3-StylusToTracker")
    stylusTipToStylusNode = slicer.util.getNode("volume3-StylusTipToStylus")
    needleModelNode = slicer.util.getNode("NeedleModel_1")

    needleModelNode.SetAndObserveTransformNodeID(stylusTipToStylusNode.GetID())
    stylusTipToStylusNode.SetAndObserveTransformNodeID(stylusToTrackerNode.GetID())
    stylusToTrackerNode.SetAndObserveTransformNodeID(trackerToProbeNode.GetID())

    return "Transformation matrices configured!"


'''
fiduciaReg = slicer.modules.fiducialregistration
'''

class ModuleTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_Module1()

  def test_Module1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    logic = ModuleLogic()
    result = logic.process()
    self.assertIsNotNone(result)
    self.delayDisplay('Test passed!')
