# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 07:32:46 2018

@author: zhenwei.shi
"""

"""
###############################
@author: zhenwei.shi, Maastro##
###############################
"""
#from __future__ import print_function

import PyrexReader
import PyrexWithParams
import PyrexOutput
import yaml
from PyrexXNAT import ParseStructure, xnat_collection
import logging
import os
import pandas
import radiomics
import re
from rdflib import Graph
import time
'''
Usage for individual case: python HelloPyrexBatchProcessing.py 

Read parameter file of Pyrex:

# - path:
#    - myWorkingDirectory is the root directory where DICOM files are saved.
#    - exportDir is the directory where results are exported.
# - collectionURL: specify the URL of cloud repository, like 'XNAT'.
# - myProject: specify the name of dataset on cloud reposity, like 'stwstrategyrdr'
# - export_format: specify the format of output, such as rdf or csv.
# - export_name: specify the name of result file.
######################################
'''
  #----------------------------For all ROI-----------------
  
def executeORAWbatch_all(ptid,roi,myStructUID,exportDir,export_format,export_name,Img_path,RT_path,excludeStructRegex):
  outPath = r''
  progress_filename = os.path.join(outPath, 'O-RAW_log.txt')
  # Configure logging
  rLogger = logging.getLogger('radiomics')

  # Set logging level
  # rLogger.setLevel(logging.INFO)  # Not needed, default log level of logger is INFO
  handler = logging.FileHandler(filename=progress_filename, mode='w')   # Create handler for writing to log file
  handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s: %(message)s'))
  rLogger.addHandler(handler)  
  logger = rLogger.getChild('batch') # Initialize logging for batch log messages

  # Set verbosity level for output to stderr (default level = WARNING)
  #radiomics.setVerbosity(logging.INFO)

  logger.info('pyradiomics version: %s', radiomics.__version__)
  logger.info('Reading Params file for pyradiomics')
  # Reading Params file for pyradiomics
  try:
    paramsFile = os.path.join(os.getcwd(),'ParamsSettings','Pyradiomics_Params.yaml')
  except Exception:
    logger.error('Could not find params file of Pyradiomics!', exc_info=True)
    exit(-1)
#  logger.info('Reading Params file of Pyrex')
  patient = ptid
  logger.info('Parsing DICOM files and RTSTRUCT in working directory')
  logger.info('DICOM and RTSTRUCT Parsing Done')

  flists = pandas.DataFrame(data= {'patient':patient}).T # create a pandas data frame for data
  logger.info('Starting Pyrex')

  # define export output format
  if export_format == 'csv':
    RESULT = pandas.DataFrame()
  else:
    RESULT = Graph()

  for entry in flists:
      #results = pandas.DataFrame()
#      logger.info('processing patient: %s', patient[entry])
      mask_vol=PyrexReader.Read_RTSTRUCT(RT_path[entry])
      logger.info('Loading RTSTRUCT: %s', RT_path[entry])
      M=mask_vol[0]
      target = []
      for j in range(0,len(M.StructureSetROISequence)):
          target.append(M.StructureSetROISequence[j].ROIName)
      logger.info('ROI: %s', target)
      for k in range(0,len(target)):
          if re.search(excludeStructRegex,target[k]):
              print('skip ROI: %s' % target[k])
              continue
          try:
              featureVector = flists[entry]
              Image,Mask = PyrexReader.Img_Bimask(Img_path[entry],RT_path[entry],target[k])
              logger.info('Processing Radiomics on %s of Patient (%s)',target[k],patient[entry])
              if export_format == 'csv': # save results in csv
                  try:
                      result = pandas.Series(PyrexWithParams.CalculationRun(Image,Mask,paramsFile))
                      contour = pandas.Series({'contour':target[k]})
                      structUID = pandas.Series({'structUID':myStructUID})
                      featureVector = featureVector.append(contour)
                      featureVector = featureVector.append(structUID)
                      featureVector = featureVector.append(result)
                      featureVector.name = k
                      results = pandas.DataFrame()
                      results = results.join(featureVector, how='outer')
                      Image = []
                      Mask= []
                      result=[]
                      RESULT = pandas.concat([RESULT,results],axis=1)
                  except Exception:
                    logger.error('FEATURE EXTRACTION FAILED for CSV output:', exc_info=True)
              else:# save results in triple store
                  try:
                    featureVector = PyrexWithParams.CalculationRun(Image,Mask,paramsFile) #compute radiomics
                    featureVector.update({'patient':patient[entry],'contour':target[k],'RTid':myStructUID}) #add patient ID and contour                
                    graph_roi = PyrexOutput.RadiomicsRDF(featureVector,exportDir,patient[entry],myStructUID,target[k],export_format,export_name) #store radiomics locally with a specific format 
                    RESULT = RESULT + graph_roi
                    #print
                    logger.info('Extraction complete, writing rdf')
                  except Exception:
                    logger.error('FEATURE EXTRACTION FAILED for RDF output:', exc_info=True)
          except Exception:
              logger.info('FEATURE EXTRACTION FAILED:')
          logger.info('-------------------------------------------')
          print(patient[entry],target[k])
  # return RESULT
      if export_format == 'csv':
          logger.info('Extraction complete, writing CSV')          
          outputFilepath = os.path.join(exportDir,export_name+patient[entry]+ myStructUID+'.csv')     
          RESULT.T.to_csv(outputFilepath, index=False, na_rep='NaN')
          logger.info('CSV writing complete')
          logger.info('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
      else:
        RESULT.serialize(exportDir + os.sep + patient[entry]+ '_' + myStructUID +".ttl", format='turtle')

  #----------------------------For a Specific ROI-----------------

def executeORAWbatch_roi(ptid,roi,myStructUID,exportDir,export_format,export_name,Img_path,RT_path,excludeStructRegex):
  outPath = r''
  progress_filename = os.path.join(outPath, 'O-RAW_log.txt')
  # Configure logging
  rLogger = logging.getLogger('radiomics')

  # Set logging level
  # rLogger.setLevel(logging.INFO)  # Not needed, default log level of logger is INFO
  handler = logging.FileHandler(filename=progress_filename, mode='w')   # Create handler for writing to log file
  handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s: %(message)s'))
  rLogger.addHandler(handler)  
  logger = rLogger.getChild('batch') # Initialize logging for batch log messages

  # Set verbosity level for output to stderr (default level = WARNING)
  #radiomics.setVerbosity(logging.INFO)

  logger.info('pyradiomics version: %s', radiomics.__version__)
  logger.info('Reading Params file for pyradiomics')
  # Reading Params file for pyradiomics
  try:
    paramsFile = os.path.join(os.getcwd(),'ParamsSettings','Pyradiomics_Params.yaml')
  except Exception:
    logger.error('Could not find params file of Pyradiomics!', exc_info=True)
    exit(-1)
#  logger.info('Reading Params file of Pyrex')
  patient = ptid
  logger.info('Parsing DICOM files and RTSTRUCT in working directory')
  logger.info('DICOM and RTSTRUCT Parsing Done')

  flists = pandas.DataFrame(data= {'patient':patient}).T # create a pandas data frame for data
  logger.info('Starting Pyrex')

  # define export output format
  if export_format == 'csv':
    RESULT = pandas.DataFrame()
  else:
    RESULT = Graph()

  for entry in flists:
      #results = pandas.DataFrame()
#      logger.info('processing patient: %s', patient[entry])
      mask_vol=PyrexReader.Read_RTSTRUCT(RT_path[entry])
      logger.info('Loading RTSTRUCT: %s', RT_path[entry])
      M=mask_vol[0]
      target = []
      for j in range(0,len(M.StructureSetROISequence)):
          target.append(M.StructureSetROISequence[j].ROIName)
      logger.info('ROI: %s', target)
      for k in range(0,len(target)):
          if not re.search(roi,target[k]):
              print('skip ROI: %s' % target[k])
              continue
          try:
              featureVector = flists[entry]
              Image,Mask = PyrexReader.Img_Bimask(Img_path[entry],RT_path[entry],target[k])
              logger.info('Processing Radiomics on %s of Patient (%s)',target[k],patient[entry])
              if export_format == 'csv': # save results in csv
                  try:
                      result = pandas.Series(PyrexWithParams.CalculationRun(Image,Mask,paramsFile))
                      contour = pandas.Series({'contour':target[k]})
                      structUID = pandas.Series({'structUID':myStructUID})
                      featureVector = featureVector.append(contour)
                      featureVector = featureVector.append(structUID)
                      featureVector = featureVector.append(result)
                      featureVector.name = k
                      results = pandas.DataFrame()
                      results = results.join(featureVector, how='outer')
                      Image = []
                      Mask= []
                      result=[]
                      RESULT = pandas.concat([RESULT,results],axis=1)
                  except Exception:
                    logger.error('FEATURE EXTRACTION FAILED for CSV output:', exc_info=True)
              else:# save results in triple store
                  try:
                    featureVector = PyrexWithParams.CalculationRun(Image,Mask,paramsFile) #compute radiomics
                    featureVector.update({'patient':patient[entry],'contour':target[k],'RTid':myStructUID}) #add patient ID and contour                
                    graph_roi = PyrexOutput.RadiomicsRDF(featureVector,exportDir,patient[entry],myStructUID,target[k],export_format,export_name) #store radiomics locally with a specific format 
                    RESULT = RESULT + graph_roi
                    logger.info('Extraction complete, writing rdf')
                  except Exception:
                    logger.error('FEATURE EXTRACTION FAILED for RDF output:', exc_info=True)
          except Exception:
              logger.info('FEATURE EXTRACTION FAILED:')
          logger.info('-------------------------------------------')
          print(patient[entry],target[k])
  # return RESULT
      if export_format == 'csv':
          logger.info('Extraction complete, writing CSV')          
          outputFilepath = os.path.join(exportDir,export_name+patient[entry]+ myStructUID+'.csv')     
          RESULT.T.to_csv(outputFilepath, index=False, na_rep='NaN')
          logger.info('CSV writing complete')
          logger.info('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
      else:
        RESULT.serialize(exportDir + os.sep + patient[entry]+ '_' + myStructUID +".ttl", format='turtle')
