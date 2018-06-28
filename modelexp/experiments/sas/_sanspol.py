from .._experiment import Experiment
import numpy as np
from ...gui.plotWidgetInset import PlotWidgetInset

class Sanspol(Experiment):
  def __init__(self):
    super().__init__()
    self.plotWidgetClass = PlotWidgetInset

    self.nDatasets = 4
    self.datasetSpecificParams = {
      'dTheta': ['sa', 'la'],
      'polarization': ['p', 'm']
      }

  def connectGui(self, gui):
    self.ptrGui = gui
    self.fig = self.ptrGui.plotWidget.getFig()
    self.ax, self.axInset = self.ptrGui.plotWidget.getAllAx()

  def setAxProps(self):
    self.ax.set_xlabel(r'$\mathit{q} \, / \, \AA^{-1}$')
    self.ax.set_ylabel(r'$\mathit{I} \, / \, cm^{-1}$')
    self.ax.set_xscale('log')
    self.ax.set_yscale('log')

    self.axInset.set_xlabel(r"$\mathit{x} \, / \, \AA$")
    self.axInset.set_ylabel(r"$SLD$")

    self.ptrGui.plotWidget.draw_idle()# .tight_layout()

  def setParameters(self):
    self.model.params['polarization_p'].value = 1
    self.model.params['polarization_m'].value = -1

  def getResiForDataset(self, i):
    data = self.data.getDataset(i)
    model = self.model.getModelset(i)
    I_data = data.getValues()
    I_error = data.getErrors()
    I_model = model.getValues()
    return (np.log(I_data) - np.log(I_model)) * I_data / I_error

  def residuum(self, p):
    self.model.params = p
    self.model.updateModel()
    resi0 = self.getResiForDataset(0)
    resi1 = self.getResiForDataset(1)
    resi2 = self.getResiForDataset(2)
    resi3 = self.getResiForDataset(3)

    return (np.concatenate([resi0, resi1, resi2, resi3]))

  def getMinMaxDomainData(self):
    data0 = self.data.getDataset(0)
    data1 = self.data.getDataset(1)
    data2 = self.data.getDataset(2)
    data3 = self.data.getDataset(3)
    q_data0 = data0.getDomain()
    q_data1 = data1.getDomain()
    q_data2 = data2.getDomain()
    q_data3 = data3.getDomain()
    return min(min(q_data0), min(q_data1), min(q_data2), min(q_data3)), \
      max(max(q_data0), max(q_data1), max(q_data2), max(q_data3))

  def getMinMaxValueData(self):
    data0 = self.data.getDataset(0)
    data1 = self.data.getDataset(1)
    data2 = self.data.getDataset(2)
    data3 = self.data.getDataset(3)
    I_data0 = data0.getValues()
    I_data1 = data1.getValues()
    I_data2 = data2.getValues()
    I_data3 = data3.getValues()
    return min(min(I_data0), min(I_data1), min(I_data2), min(I_data3)),\
           max(max(I_data0), max(I_data1), max(I_data2), max(I_data3))

  def getMinMaxDomainModel(self):
    model0 = self.model.getModelset(0)
    model1 = self.model.getModelset(1)
    model2 = self.model.getModelset(2)
    model3 = self.model.getModelset(3)
    q_model0 = model0.getDomain()
    q_model1 = model1.getDomain()
    q_model2 = model2.getDomain()
    q_model3 = model3.getDomain()
    return min(min(q_model0), min(q_model1), min(q_model2), min(q_model3)), \
      max(max(q_model0), max(q_model1), max(q_model2), max(q_model3))

  def getMinMaxValueModel(self):
    model0 = self.model.getModelset(0)
    model1 = self.model.getModelset(1)
    model2 = self.model.getModelset(2)
    model3 = self.model.getModelset(3)
    I_model0 = model0.getValues()
    I_model1 = model1.getValues()
    I_model2 = model2.getValues()
    I_model3 = model3.getValues()
    return min(min(I_model0), min(I_model1), min(I_model2), min(I_model3)),\
           max(max(I_model0), max(I_model1), max(I_model2), max(I_model3))

  def adjustAxToAddedData(self):
    qMin, qMax = self.getMinMaxDomainData()
    IMin, IMax = self.getMinMaxValueData()
    self.ax.set_xlim(qMin, qMax)
    self.ax.set_ylim(IMin*0.8, IMax*1.2)

  def adjustAxToAddedModel(self):
    qModelMin, qModelMax = self.getMinMaxDomainModel()
    IModelMin, IModelMax = self.getMinMaxValueModel()
    if hasattr(self, 'data'):
      qDataMin, qDataMax = self.getMinMaxDomainData()
      IDataMin, IDataMax = self.getMinMaxValueData()
    else:
      qDataMin, qDataMax = np.inf, -np.inf
      IDataMin, IDataMax = np.inf, -np.inf
    self.ax.set_xlim(
      min(qModelMin, qDataMin),
      max(qModelMax, qDataMax)
    )
    self.ax.set_ylim(
      min(IModelMin, IDataMin)*0.8,
      max(IModelMax, IDataMax)*1.2
    )

    model0 = self.model.getModelset(0)
    r_model = model0.r
    sld_model = model0.sld
    self.axInset.set_xlim(min(r_model)/10, max(r_model)/10)
    self.axInset.set_ylim(0, max(sld_model)/1e-6*1.2)

  def saveModelDataToFile(self, f):
    if hasattr(self, 'data') and hasattr(self, 'model'):
      data0 = self.data.getDataset(0)
      data1 = self.data.getDataset(1)
      model0 = self.model.getModelset(0)
      model1 = self.model.getModelset(1)
      q_data0 = data0.getDomain()
      I_data0 = data0.getValues()
      sI_data0 = data0.getErrors()
      q_model0 = model0.getDomain()
      I_model0 = model0.getValues()

      q_data1 = data1.getDomain()
      I_data1 = data1.getValues()
      sI_data1 = data1.getErrors()
      q_model1 = model1.getDomain()
      I_model1 = model1.getValues()

      assert(len(q_data0) == len(q_model0), 'Data and Model do not have the same length.')
      f.write('#{data0.suffix}\n')
      f.write('#q / A-1\tI / cm-1\tsI / cm-1\tImodel / cm-1\n')
      for i in range(len(q_data0)):
        assert(np.isclose(q_data0[i], q_model0[i]), 'Data and Model arrays are not defined on same domain' )
        f.write(f'{q_data0[i]}\t{I_data0[i]}\t{sI_data0[i]}\t{I_model0[i]}\n')
      f.write('\n#{data1.suffix}\n')
      f.write('#q / A-1\tI / cm-1\tsI / cm-1\tImodel / cm-1\n')
      for i in range(len(q_data1)):
        assert(np.isclose(q_data1[i], q_model1[i]), 'Data and Model arrays are not defined on same domain' )
        f.write(f'{q_data1[i]}\t{I_data1[i]}\t{sI_data1[i]}\t{I_model1[i]}\n')
    elif hasattr(self, 'data'):
      data0 = self.data.getDataset(0)
      data1 = self.data.getDataset(1)
      q_data0 = data0.getDomain()
      I_data0 = data0.getValues()
      sI_data0 = data0.getErrors()
      q_data1 = data1.getDomain()
      I_data1 = data1.getValues()
      sI_data1 = data1.getErrors()

      f.write('#{data0.suffix}\n')
      f.write('#q / A-1\tI / cm-1\tsI / cm-1\n')
      for i in range(len(q_data0)):
        f.write(f'{q_data0[i]}\t{I_data0[i]}\t{sI_data0[i]}\n')
      f.write('\n#{data1.suffix}\n')
      f.write('#q / A-1\tI / cm-1\tsI / cm-1\n')
      for i in range(len(q_data1)):
        f.write(f'{q_data1[i]}\t{I_data1[i]}\t{sI_data1[i]}\n')
    elif hasattr(self, 'model'):
      model0 = self.model.getModelset(0)
      model1 = self.model.getModelset(1)
      q_model0 = model0.getDomain()
      I_model0 = model0.getValues()
      q_model1 = model1.getDomain()
      I_model1 = model1.getValues()

      f.write('#{model0.suffix}\n')
      f.write('#q / A-1\tImodel / cm-1\n')
      for i in range(len(q_model0)):
        f.write(f'{q_model0[i]}\t{I_model0[i]}\n')

      f.write('\n#{model1.suffix}\n')
      f.write('#q / A-1\tImodel / cm-1\n')
      for i in range(len(q_model1)):
        f.write(f'{q_model1[i]}\t{I_model1[i]}\n')