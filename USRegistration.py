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
    self.parent.title = "Fast registration"
    self.parent.categories = ["Examples"]
    #TODO: write dependencies and instruction
    self.parent.dependencies = []
    self.parent.contributors = ["Anna Zapaishchykova(TUM)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = "This is the module for 3d spatial ultrasound registration. "
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
    layoutManager = slicer.app.layoutManager()
    #views = layoutManager.layoutLogic().GetViewNodes().GetItemAsObject(1)
    layoutManager.setLayout(6)

    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Configuration Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Configuration"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    # "Run extend.bat" button
    extendButton = qt.QPushButton("1. Run extend.bat")
    extendButton.toolTip = "Run configuration file"
    parametersFormLayout.addWidget(extendButton)
    extendButton.connect('clicked(bool)', self.onExtendButtonClicked)

    # loadSequence button
    loadButton = qt.QPushButton("2. Load data")
    loadButton.toolTip = "Load file"
    parametersFormLayout.addWidget(loadButton)
    loadButton.connect('clicked(bool)', self.onLoadButtonClicked)

    # loadSequence button
    addNeedleModelButton = qt.QPushButton("3. Add needle model")
    addNeedleModelButton.toolTip = "Create Models module"
    parametersFormLayout.addWidget(addNeedleModelButton)
    addNeedleModelButton.connect('clicked(bool)', self.onAddNeedleModelClicked)

    # tranform button
    addTransformButton = qt.QPushButton("4. Change transform")
    addTransformButton.toolTip = "Change hierarchy order"
    parametersFormLayout.addWidget(addTransformButton)
    addTransformButton.connect('clicked(bool)', self.onTransformClicked)

    # configure fiducials button
    #TODO: make thois button small and place near button 5* with same subsection
    #TODO: try to avoid this 6* button and make it work after 5*
    configureFidButton = qt.QPushButton("6*. Place ProbeTo fiducial points")
    configureFidButton.toolTip = "Configue fiducials"
    parametersFormLayout.addWidget(configureFidButton)
    configureFidButton.connect('clicked(bool)', self.onconfigFiducialClicked)

    # tranform button
    addTransformImageButton = qt.QPushButton("7. Change final transform")
    addTransformImageButton.toolTip = "Change hierarchy order"
    parametersFormLayout.addWidget(addTransformImageButton)
    addTransformImageButton.connect('clicked(bool)', self.onTransformImageClicked)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.extendButton = extendButton
    self.loadButton = loadButton
    self.addNeedleModelButton = addNeedleModelButton
    self.addTransformButton = addTransformButton
    self.configureFidButton = configureFidButton


  def onExtendButtonClicked(self):
    logic = ModuleLogic()
    result = logic.process()
    qt.QMessageBox.information(slicer.util.mainWindow(), 'Slicer Python', result)

  def onLoadButtonClicked(self):
    logic = ModuleLogic()
    result = logic.loading()
    fiducialCollapsibleButton = ctk.ctkCollapsibleButton()
    fiducialCollapsibleButton.text = "5*. Set up fiducial points"
    self.layout.addWidget(fiducialCollapsibleButton)

    # Layout within the dummy collapsible button
    fiducialFormLayout = qt.QFormLayout(fiducialCollapsibleButton)

    # Buttons for placing feducials
    imageF = slicer.qSlicerMarkupsPlaceWidget()
    imageF.setMRMLScene(slicer.mrmlScene)
    markupsNodeID = slicer.modules.markups.logic().AddNewFiducialNode('ImageF')
    imageF.setCurrentNode(slicer.mrmlScene.GetNodeByID(markupsNodeID))
    imageF.placeButton().show()
    imageF.show()
    fiducialFormLayout.addWidget(imageF)

    # player buttons after it's loaded
    browser = slicer.qMRMLSequenceBrowserToolBar()
    browser.setMRMLScene(slicer.mrmlScene)
    browser.show()
    fiducialFormLayout.addWidget(browser)

    qt.QMessageBox.information(slicer.util.mainWindow(), 'Slicer Python', result)

  def onAddNeedleModelClicked(self):
    logic = ModuleLogic()
    result = logic.addNeedleModel()
    qt.QMessageBox.information(slicer.util.mainWindow(), 'Slicer Python', result)

  def onTransformClicked(self):
    logic = ModuleLogic()
    result = logic.transformation()
    qt.QMessageBox.information(slicer.util.mainWindow(), 'Slicer Python', result)

  def onconfigFiducialClicked(self):
    logic = ModuleLogic()
    result = logic.configureFid()
    qt.QMessageBox.information(slicer.util.mainWindow(), 'Slicer Python', result)

  def onTransformImageClicked(self):
    logic = ModuleLogic()
    result = logic.transformationImage()


    #f = slicer.vtkMRMLFiducialRegistrationWizardNode()
    f = slicer.util.selectModule('FiducialRegistrationWizard')
    f = slicer.util.getNode('FiducialRegistrationWizard')
    f.SetScene(slicer.mrmlScene)
    f.SetRegistrationModeToSimilarity()

    f.SetAndObserveFromFiducialListNodeId('vtkMRMLMarkupsFiducialNode1') #ImageF
    f.SetAndObserveToFiducialListNodeId('vtkMRMLMarkupsFiducialNode2')  #ProbeT
    f.RegistrationModeFromString('ImageToProbe')

    f.SetOutputTransformNodeId('vtkMRMLLinearTransformNode9')
    f.SetUpdateModeToAuto()
    f.UpdateScene(slicer.mrmlScene)

    driver = slicer.modules.volumereslicedriver.logic()
    layoutManager = slicer.app.layoutManager()
    redView = layoutManager.layoutLogic().GetViewNodes().GetItemAsObject(0)
    driver.SetMRMLScene(slicer.mrmlScene)
    driver.SetModeForSlice(6, redView)
    driver.SetDriverForSlice('vtkMRMLScalarVolumeNode1', redView)

    print("Final configuration matrix:")
    #TODO: print here final matrix
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

    w = slicer.vtkMRMLFiducialRegistrationWizardNode()
    w.SetRegistrationModeToSimilarity()
    imageToProbe = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLinearTransformNode", "ImageToProbe")
    w.SetProbeTransformToNodeId(imageToProbe.GetID())

    fidTransform = slicer.mrmlScene.GetNodeByID('vtkMRMLLinearTransformNode6')
    toFids = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "ProbeT")
    #slicer.modules.fiducialregistrationwizard.logic().AddFiducial(fidTransform, toFids)

    return "Transformation matrices configured!"

  def transformationImage(self):
    imageToProbeNode = slicer.util.getNode("ImageToProbe")
    imageModelNode = slicer.util.getNode("volume3-Image")

    imageModelNode.SetAndObserveTransformNodeID(imageToProbeNode.GetID())

    w = slicer.vtkMRMLFiducialRegistrationWizardNode()
    w.SetRegistrationModeToSimilarity()
    imageToProbe = slicer.mrmlScene.GetFirstNodeByName("ImageToProbe")
    w.SetProbeTransformToNodeId(imageToProbe.GetID())

    slicer.modules.fiducialregistrationwizard.logic().UpdateCalibration(imageToProbe)
    slicer.modules.fiducialregistrationwizard.logic().UpdateCalibration(w)

    return "Transformation matrices configured!"

  def configureFid(self):
    '''
    w = slicer.vtkMRMLFiducialRegistrationWizardNode()
    w.SetRegistrationModeToSimilarity()
    w.SetProbeTransformToNodeId(transformNode.GetID())



    fidReg = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLFiducialRegistrationWizardNode", "Fiducial")
    toFids = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "ProbeF")
    '''

    #fromFids = slicer.mrmlScene.GetNodeByID('vtkMRMLMarkupsFiducialNode1')
    # TODO: places only one to fields
    w = slicer.vtkMRMLFiducialRegistrationWizardNode()
    w.SetRegistrationModeToSimilarity()
    imageToProbe = slicer.mrmlScene.GetFirstNodeByName("ImageToProbe")
    w.SetProbeTransformToNodeId(imageToProbe.GetID())

    fidTransform = slicer.mrmlScene.GetFirstNodeByName("volume3-StylusTipToStylus")
    toFids = slicer.mrmlScene.GetFirstNodeByName("ProbeT")
    slicer.modules.fiducialregistrationwizard.logic().AddFiducial(fidTransform, toFids)
    return "Fiducial Wizard Configured!"


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
