
__all__ = ['EventSelection', 'EtCutType', 'SelectionType']


from Gaugi import Algorithm
from Gaugi import StatusCode, NotSet
from Gaugi import StatusCode, NotSet
from prometheus import Dataframe as DataframeEnum
from Gaugi.messenger.macros import *
from Gaugi.constants import GeV
from Gaugi.enumerations import StatusWTD
from Gaugi import EnumStringification
import numpy as np

class EtCutType(EnumStringification):
  OfflineAbove =  5
  OfflineBelow = -5
  L1CaloAbove  =  1
  L1CaloBelow  = -1
  L2CaloAbove  =  2
  L2CaloBelow  = -2
  EFCaloAbove  =  3
  EFCaloBelow  = -3
  HLTAbove     =  4
  HLTBelow     = -4


class SelectionType(EnumStringification):
  # @brief: selection from Data taken events
  SelectionData = 0
  # @brief: selection only Z candidates (Monte Carlo)
  SelectionZ = 1
  # @brief: selection only W candidates (Monte Carlo)
  SelectionW = 2
  # @brief: selection only Fakes candidates
  SelectionFakes = 3
  # @brief: Select only events between a lb range
  SelectionLumiblockRange = 4
  # @brief: Select only events by run number
  SelectionRunNumber = 5
  # @brief: Select only events with online ringer calo rings
  SelectionOnlineWithRings = 6
  # @brief: Select only events with  offline ringer calo rings
  SelectionOfflineWithRings = 7
  # @brief: Select by PID
  SelectionPID = 8




class EventSelection( Algorithm ):

  def __init__(self, name):
    Algorithm.__init__(self, name)
    self._selectionType =SelectionType.SelectionZ
    self._pidname = None
    self._cutValues = {}


  def initialize(self):
    return StatusCode.SUCCESS

  def setCutValue(self, cutType, value=NotSet):
    self._cutValues[cutType] = value


  def execute(self, context):

    elCont    = context.getHandler( "ElectronContainer" )
    fc        = context.getHandler( "HLT__FastCaloContainer" )
    mc        = context.getHandler( "MonteCarloContainer")
    eventInfo = context.getHandler( "EventInfoContainer" )

    # Apply all et cut values setted in the dict
    for key, value in self._cutValues.items():

      self._logger.debug('Apply Selection cut for %s',EtCutType.tostring(key))
      self._logger.debug('Apply Selection cut for %s',SelectionType.tostring(key))
      el=elCont
      if key is EtCutType.OfflineAbove and el.et()/GeV < value:
        self.wtd = StatusWTD.ENABLE
        self._logger.debug('Reproved by Et cut value. Et = %1.3f < EtCut = %1.3f',el.et()/GeV,value)
        return StatusCode.SUCCESS

      if key is EtCutType.OfflineBelow and el.et()/GeV >= value:
        self.wtd = StatusWTD.ENABLE
        self._logger.debug('Reproved by Et cut value. Et = %1.3f >= EtCut = %1.3f',el.et()/GeV,value)
        return StatusCode.SUCCESS

      elif key is EtCutType.L2CaloAbove and fc.et()/GeV < value:
        self.wtd = StatusWTD.ENABLE
        self._logger.debug('Reproved by Et cut value. Et = %1.3f < EtCut = %1.3f',el.et()/GeV,value)
        return StatusCode.SUCCESS

      elif key is EtCutType.L2CaloBelow and fc.et()/GeV >= value:
        self.wtd = StatusWTD.ENABLE
        self._logger.debug('Reproved by Et cut > value. Et = %1.3f >= EtCut = %1.3f',el.et()/GeV,value)
        return StatusCode.SUCCESS


      elif key is EtCutType.HLTAbove or key is EtCutType.HLTBelow:
        passed = False
        for eg in elCont:
          # Et cut value for each electron object
          if key is EtCutType.HLTAbove and eg.et()/GeV >= value:  passed=True; break
          if key is EtCutType.HLTBelow and eg.et()/GeV < value:  passed=True; break

        # Loop over electrons from HLT
        if not passed:
          self.wtd = StatusWTD.ENABLE
          self._logger.debug('Reproved by Et cut value. Et = %1.3f and EtCut = %1.3f',el.et()/GeV,value)
          return StatusCode.SUCCESS


      # Is good ringer
      elif key is SelectionType.SelectionOnlineWithRings and not fc.isGoodRinger():
        self.wtd = StatusWTD.ENABLE
        self._logger.debug('Event dont contain the online ringer rings values. skip...')
        return StatusCode.SUCCESS

      # Is good ringer
      elif key is SelectionType.SelectionOfflineWithRings and not el.isGoodRinger():
        self.wtd = StatusWTD.ENABLE
        self._logger.debug('Event dont contain the offline ringer rings values. skip...')
        return StatusCode.SUCCESS

      # Monte Carlo event selection truth cuts
      elif key is SelectionType.SelectionFakes and mc.isMC() and mc.isEfromZ():
        self.wtd = StatusWTD.ENABLE
        self._logger.debug('Fakes: is Z! reject')
        return StatusCode.SUCCESS

      # Monte Carlo event selection truth cuts
      elif key is SelectionType.SelectionZ and mc.isMC() and not mc.isEfromZ():
        self.wtd = StatusWTD.ENABLE
        self._logger.debug('Z: is not Z! reject')
        return StatusCode.SUCCESS

      #elif key is SelectionType.SelectionRunNumber and (eventInfo.RunNumber != value):
      #  self.wtd = StatusWTD.ENABLE
      #  self._logger.debug('Reject event by RunNumber. skip...')
      #  return StatusCode.SUCCESS

      # Offline recostruction cut by PID selectors
      elif key is SelectionType.SelectionPID:
        pidname = value
        self._logger.debug('Apply PID selection...')
        # is this a veto criteria?
        isVeto = True if '!' in pidname else False
        # remove the not (!) charactere in the pidname
        pidname = pidname.replace('!','') if isVeto else pidname
        # Get the bool accept from some pidname branch or decoration inside of the electron object

        passed=False
        for eg in elCont:
          passed = eg.accept(pidname)
          if passed: break

        # Apply veto event selection
        self._logger.debug('PID (%s) is %d',pidname,passed)
        if isVeto and passed:
          self.wtd = StatusWTD.ENABLE
          return StatusCode.SUCCESS
        if not isVeto and not passed:
          self.wtd = StatusWTD.ENABLE
          return StatusCode.SUCCESS
      else:
        self._logger.debug('Selection cut (%s) approved.',key)


    self.wtd = StatusWTD.DISABLE
    return StatusCode.SUCCESS


  def finalize(self):
    return StatusCode.SUCCESS









