import numpy as np
from mne.decoding import CSP
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import fif
import utils

class Classifier():
  def __init__(self):
    self.trained = False
    self.csp = None
    self.lda = None
    self.info = None

  def train(self, userid):
    data, y_train, self.info = fif.get_session(userid)

    if data is None:
      return self.info

    self.lda = LinearDiscriminantAnalysis()
    self.csp = CSP(n_components=4, reg=None, log=True, norm_trace=False)

    X_train = self.csp.fit_transform(data, y_train)

    self.lda.fit(X_train, y_train)
    self.trained = True
    return self.info

  def predict(self, record, userid=None):
    if self.trained is False or userid != self.info['userid']:
      self.train(userid)
    record = np.array([record])
    record = utils.normalize_data(record)
    X_test = self.csp.transform(record)
    return self.lda.predict(X_test)