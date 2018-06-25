from ._fit import Fit
import lmfit, datetime, pkg_resources

class LevenbergMarquardt(Fit):
  def fit(self):
    self.ptrGui.updateParamsVaryFromCheckbox()
    self.startedFit = datetime.datetime.now()
    self.fit_result = lmfit.minimize(
      self.ptrExperiment.residuum, self.ptrModel.params, method='leastsq'
    )
    self.endFit = datetime.datetime.now()
    print(lmfit.fit_report(self.fit_result))

    # Update the parameters of model
    self.ptrModel.params = self.fit_result.params
    return self.fit_result

  def exportResult(self, filename):
    with open(filename, 'w') as f:
      f.write(
        '#File generated by ModelExp v' +
        pkg_resources.require('modelexp')[0].version + '\n'
      )
      if (self.fit_result is not None):
        f.write('#Started Fit at ' + str(self.startedFit) + '\n')
        f.write('#Finished Fit at ' + str(self.endFit) + '\n')
        f.write('#'+lmfit.fit_report(self.fit_result).replace('\n','\n#')+'\n')

      self.ptrExperiment.saveModelDataToFile(f)