from abc import ABCMeta, abstractmethod
try:
  from ..experiments import Experiment
except ImportError:
  pass

class Data(metaclass=ABCMeta):
  '''
  Abstract class to describe a model.
  Specific models are defined by classes that have to implemented the defined functions here.
  '''
  def __init__(self, experiment):
    self.ptrExperiment: Experiment = experiment

  def connectGui(self, gui):
    self.ptrGui = gui
    self.fig = self.ptrGui.plotWidget.getFig()
    self.ax = self.ptrGui.plotWidget.getDataAx()

  @abstractmethod
  def setData(self):
    '''
    How to set data
    '''
    pass

  @abstractmethod
  def loadFromFile(self):
    '''
    How to load data from file
    '''
    pass

  @abstractmethod
  def plotData(self, ptrGui):
    '''
    How to plot data
    '''

  @abstractmethod
  def getDomain(self):
    pass

  @abstractmethod
  def getValues(self):
    pass

  @abstractmethod
  def getErrors(self):
    pass

  def draw(self):
    self.ptrGui.update()