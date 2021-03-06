

from prometheus import EventATLAS
from prometheus.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel, Logger
from Gaugi import ToolSvc, ToolMgr
import argparse
mainLogger = Logger.getModuleLogger("job")
parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()


parser.add_argument('-i','--inputFiles', action='store', 
    dest='inputFiles', required = True, nargs='+',
    help = "The input files that will be used to generate the plots")

parser.add_argument('-o','--outputFile', action='store', 
    dest='outputFile', required = False, default = None,
    help = "The output store name.")

parser.add_argument('-n','--nov', action='store', 
    dest='nov', required = False, default = -1, type=int,
    help = "Number of events.")

import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()



acc = EventATLAS( "EventATLASLoop",
                  inputFiles = args.inputFiles, 
                  treePath= '*/HLT/PhysVal/Egamma/photons',
                  dataframe = DataframeEnum.Photon_v1, 
                  outputFile = args.outputFile,
                  level = LoggingLevel.INFO
                  )



from EventSelectionTool import EventSelection, SelectionType, EtCutType

evt = EventSelection('EventSelection', dataframe = DataframeEnum.Photon_v1)
# evt.setCutValue( SelectionType.SelectionOnlineWithRings )
#pidname = 'MediumLLH_DataDriven_Rel21_Run2_2018'
pidname = 'ph_tight'
evt.setCutValue( SelectionType.SelectionPID, pidname ) 
evt.setCutValue( EtCutType.L2CaloAbove , 10)


ToolSvc += evt


from TrigEgammaEmulationTool import Chain, Group, TDT

triggerList = [
                Group( TDT( "HLT_g10_etcut","HLT__TDT__g10_etcut"), 'ph_tight', 10 ),
                # Group( Chain( "HLT__TDT__g10_etcut__medium","L1_EM3","HLT_g10_medium_noringer"), 'ph_medium', 10 ),
                # Group( Chain( "HLT__TDT__g10_etcut__loose","L1_EM3","HLT_g10_loose_noringer"), 'ph_loose', 10 ),
                ]
                




from EfficiencyTools import EfficiencyTool
alg = EfficiencyTool( "Efficiency", dataframe = DataframeEnum.Photon_v1 )


for group in triggerList:
  alg.addGroup( group )

ToolSvc += alg

acc.run(args.nov)