from modelexp.models.sas import SAXSModel
from fortSAS import sphere_cs_coupled

class SphereCSCoupled(SAXSModel):
  def initParameters(self):
    self.params.add('particleSize', 100)
    self.params.add('d', 20)
    self.params.add('sldCore', 40e-6)
    self.params.add('sldShell', 30e-6)
    self.params.add('sldSolvent', 10e-6)
    self.params.add('sigR', 0.05)
    self.params.add('sigD', 0)
    self.params.add('i0', 1)
    self.params.add('bg', 1e-6)


  def calcModel(self):
    self.I = self.params['i0'] * sphere_cs_coupled.formfactor(
      self.q,
      self.params['particleSize'],
      self.params['d'],
      self.params['sldCore'],
      self.params['sldShell'],
      self.params['sldSolvent'],
      self.params['sigR'],
      self.params['sigD']
    ) + self.params['bg']

    self.r, self.sld = sphere_cs_coupled.sld(
      self.params['RpD'],
      self.params['d'],
      self.params['sldCore'],
      self.params['sldShell'],
      self.params['sldSolvent']
    )
