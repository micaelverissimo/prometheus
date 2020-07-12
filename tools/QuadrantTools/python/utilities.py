
from Gaugi.monet.PlotFunctions import *
from Gaugi.monet.TAxisFunctions import *
from copy import copy


def AddTopLabels(can,legend, legOpt = 'p', quantity_text = '', etlist = None
                     , etalist = None, etidx = None, etaidx = None, legTextSize=10
                     , runLabel = '', extraText1 = None, legendY1=.68, legendY2=.93
                     , maxLegLength = 19, logger=None):
    text_lines = []
    text_lines += [GetAtlasInternalText()]
    text_lines.append( GetSqrtsText(13) )
    _etlist = copy(etlist)
    _etalist = copy(etalist)
    if runLabel: text_lines.append( runLabel )
    if extraText1: text_lines.append( extraText1 )
    DrawText(can,text_lines,.40,.68,.70,.93,totalentries=4)
    if legend:
        MakeLegend( can,.73,legendY1,.89,legendY2,textsize=legTextSize
                  , names=legend, option = legOpt, squarebox=False
                  , totalentries=0, maxlength=maxLegLength )
    try:
        extraText = []
        if _etlist and etidx is not None:
            # add infinity in case of last et value too large
            if _etlist[-1]>9999:  _etlist[-1]='#infty'
            binEt = (str(_etlist[etidx]) + ' < E_{T} [GeV] < ' + str(_etlist[etidx+1]) if etidx+1 < len(_etlist) else
                                     'E_{T} > ' + str(_etlist[etidx]) + ' GeV')
            extraText.append(binEt)
        if quantity_text: 
            if not isinstance(quantity_text,(tuple,list)): quantity_text = [quantity_text]
            extraText += quantity_text
        if _etalist and etaidx is not None:
            binEta = (str(_etalist[etaidx]) + ' < #eta < ' + str(_etalist[etaidx+1]) if etaidx+1 < len(_etalist) else
                                        str(_etalist[etaidx]) + ' < #eta < 2.47')
            extraText.append(binEta)
        DrawText(can,extraText,.14,.68,.35,.93,totalentries=4)
    except NameError as e:
        if logger:
          logger.warning("Couldn't print test due to error: %s", e)
        pass


class QuadrantConfig(object):
  def __init__(self, name_a, expression_a, name_b, expression_b):
    self._name_a=name_a; self._name_b=name_b
    self._expression_a=expression_a; self._expression_b=expression_b
  
  def name_a(self):
    return self._name_a

  def expression_a(self):
    return self._expression_a

  def name_b(self):
    return self._name_b

  def expression_b(self):
    return self._expression_b





