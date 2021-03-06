

__all__ = ["RetrieveBinningIdx"]


def RetrieveBinningIdx(et,eta,etbins,etabins, logger=None):
  # Fix eta value if > 2.5
  if eta > etabins[-1]:  eta = etabins[-1]
  if et > etbins[-1]:  et = etbins[-1]
  ### Loop over binnings
  for etBinIdx in range(len(etbins)-1):
    if et >= etbins[etBinIdx] and  et < etbins[etBinIdx+1]:
      for etaBinIdx in range(len(etabins)-1):
        if eta >= etabins[etaBinIdx] and eta < etabins[etaBinIdx+1]:
          return etBinIdx, etaBinIdx
  return -1, -1#


from . import EventSelection
__all__.extend(EventSelection.__all__)
from .EventSelection import *




