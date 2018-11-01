"""
###############################
@author: zhenwei.shi, Maastro##
###############################
"""
from __future__ import print_function

import time
import os,yaml
import ORAW
import glob
import shutil
import pandas as pd
from DicomDatabase import DicomDatabase

'''
Usage for a given case: python HelloORAW.py 

Read parameters:

roi = 'all' (calculate radiomics on all ROIs)
roi = '[Gg][Tt][Vv]' (calculate radiomics on a specific ROI or a type of ROI)
export_format = 'csv'/'rdf'
export_name = 'ORAW_rtest'
walk_dir = './data/PET' (directory of your data)
######################################
'''
start_time = time.clock()


#-------------------------USER-------------------------------
#----------------O-RAW initial parameters -------------------
# roi = 'all'
roi = '[Gg][Tt][Vv]'
# export_format = 'csv'
export_format = 'rdf'
export_name = 'ORAW_'
# walk_dir = "./data/PET"
walk_dir = './data/CT'
#-----------------create tmp CT/STRUCT directories-----------
CTWorkingDir = "./CTFolder"
STRUCTWorkingDir = "./StructFolder"

if not os.path.exists(CTWorkingDir):
  os.makedirs(CTWorkingDir)
if not os.path.exists(STRUCTWorkingDir):
  os.makedirs(STRUCTWorkingDir)

# -----------------------------------------------------------
# initialize dicom DB
dicomDb = DicomDatabase()
# walk over all files in folder, and index in the database
dicomDb.parseFolder(walk_dir)

# -----------------------------------------------------------
# Export data to RDF endpoint
# import json
# import requests
# import urllib
# import os
# import subprocess
# from time import sleep

# # Set default URL of RDF4J DB
# baseUrl = "http://172.17.0.3:7200"
# if os.environ.get("RDF4J_URL") is not None:
#     baseUrl = os.environ.get("RDF4J_URL")

# # Set default repo
# repo = "data"
# if os.environ.get("DBNAME") is not None:
#     repo = os.environ.get("DBNAME")

# # Set default named graph
# localGraphName = "radiomics.local"
# if os.environ.get("NAMED_GRAPH") is not None:
#     localGraphName = os.environ.get("NAMED_GRAPH")

# # Set interval between executions
# sleepTime = 60
# if os.environ.get("INTERVAL") is not None:
#     sleepTime = int(os.environ.get("INTERVAL"))

excludeStructRegex = "(Patient.*|BODY.*|Body.*|NS.*|Couch.*)"
if os.environ.get("EXCLUDE_STRUCTURE_REGEX") is not None:
    excludeStructRegex = os.environ.get("EXCLUDE_STRUCTURE_REGEX")
# ----------------------------------------------------
if export_format == 'rdf':
    exportDir = './RFstore/Turtle_output' # export format is RDF
else:
    exportDir = './RFstore/CSV_output' # export format is CSV
# loop over patients
for ptid in dicomDb.getPatientIds():
    print("staring with Patient %s" % (ptid))
    # get patient by ID
    myPatient = dicomDb.getPatient(ptid)
    # loop over RTStructs of this patient
    for myStructUID in myPatient.getRTStructs():
        print("Starting with RTStruct %s" % myStructUID)
        # Get RTSTRUCT by SOP Instance UID
        myStruct = myPatient.getRTStruct(myStructUID)
        # Get CT which is referenced by this RTStruct, and is linked to the same patient
        # mind that this can be None, as only a struct, without corresponding CT scan is found
        myCT = myPatient.getCTForRTStruct(myStruct)

        # check if the temperal CT/STRUCT folder is empty
        if not (os.listdir(CTWorkingDir)==[] and os.listdir(STRUCTWorkingDir)==[]):
          ct_files = glob.glob(os.path.join(CTWorkingDir,'*'))
          for f in ct_files:
            os.remove(f)

          struct_files = glob.glob(os.path.join(STRUCTWorkingDir,'*'))
          for f in struct_files:
            os.remove(f)
        
        #only show if we have both RTStruct and CT
        if myCT is not None:
            # copy RTSTRUCT file to tmp folder as 'struct.dcm'
            shutil.copy2(myStruct.getFileLocation(),os.path.join(STRUCTWorkingDir,'struct.dcm'))
            # copy DICOM slices to tmp folder as 'struct.dcm'
            slices = myCT.getSlices()
            for i in range(len(slices)):
                shutil.copy2(slices[i],os.path.join(CTWorkingDir,str(i)+".dcm"))
            #graph = ORAW_Docker.executeORAWbatch_all([ptid],roi,myStructUID,exportDir,export_format,export_name,[CTWorkingDir],[STRUCTWorkingDir],excludeStructRegex)
            if roi == 'all':
                ORAW.executeORAWbatch_all([ptid],roi,myStructUID,exportDir,export_format,export_name,[CTWorkingDir],[STRUCTWorkingDir],excludeStructRegex)
            else:
                ORAW.executeORAWbatch_roi([ptid],roi,myStructUID,exportDir,export_format,export_name,[CTWorkingDir],[STRUCTWorkingDir],excludeStructRegex)
            #####################
            # Load RDF store with new data
            #####################
            # get string of turtle triples (nt format)
            # turtle = graph.serialize(format='nt')
            # # upload to RDF store
            # loadRequest = requests.post(baseUrl + "/repositories/" + repo + "/rdf-graphs/" + localGraphName,
            #     data=turtle, 
            #     headers={
            #         "Content-Type": "text/turtle"
            #     }
            # )
        print("Done for struct %s of patient %s" % (myStructUID, ptid))
print("--- %s seconds ---" % (time.clock() - start_time)) 