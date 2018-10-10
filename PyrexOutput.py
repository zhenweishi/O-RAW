"""
###############################
@author: zhenwei.shi, Maastro##
###############################
"""

from rdflib import Graph, Literal
from rdflib.namespace import Namespace,URIRef,RDF,RDFS
import urllib
#import json
import os
import csv
from datetime import datetime
import pandas as pd

# Function to store readiomics in different types of formats, such as csv and RDF.
def RadiomicsRDF(featureVector,exportDir,patientID,myStructUID,ROI,export_format,export_name):
	graph = Graph() # Create a rdflib graph object
	# feature_name = [] # Create a list for features
	# feature_uri = [] # Create a list for feature uri (ontology)

	# Namespaces used in O-RAW
	ro = Namespace('http://www.radiomics.org/RO/')
	roo = Namespace('http://www.cancerdata.org/roo/')
	IAO = Namespace('http://purl.obolibary.org/obo/IAO_')
	SWO = Namespace('http://www.ebi.ac.uk/swo/SWO_')
	NCIT = Namespace('http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#')
	# Adding namespace to graph space
	graph.bind('ro',ro)
	graph.bind('roo',roo)
	graph.bind('IAO',IAO)
	graph.bind('SWO',SWO)
	graph.bind('NCIT',NCIT)

	# ------------------------- URI of related entities -----------------
	# ^^^^^^^^^^^^^^^^^^^^^^^^^ Level-1 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	patient_uri = URIRef(NCIT+'C16960')
	has_pacs_study = URIRef(roo + '100284') # patient has_pacs_study scan
	scan_uri = URIRef(NCIT+'C17999')
	converted_to = URIRef(ro + '0310') # scan converted_to image_volume
	image_volume_uri = URIRef(ro + '0271')
	is_part_of = URIRef(ro + '0298') # image_volume is_part_of image_space 
	image_space_uri = URIRef(ro + '0225')
	# ROImask_uri = URIRef(roo + '0272') # ROImask is_part_of image_space
	is_label_of = URIRef(ro + 'P00190') #  GTV/... is_label_of ROImask 
	has_label = URIRef(ro+'P00051')
	# GTV_uri = URIRef(roo + '100006')
	used_to_compute = URIRef(ro + '0296') # image_space used_to_compute RadiomicsFeature

	# ^^^^^^^^^^^^^^^^^^^^^^^^^ Level-2 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	mm_uri = URIRef(ro + 'I0020')
	mm2_uri = URIRef(ro + 'I0027')
	mm3_uri = URIRef(ro + 'I0011')
	has_value = URIRef(ro + '010191') # RadiomicsFeature has_value
	has_unit = URIRef(ro + '010198') # RadiomicsFeature has_unit

	# ^^^^^^^^^^^^^^^^^^^^^^^^^ Level-3 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	computed_using = URIRef(ro + 'P00002') # RadiomicsFeature computed_using calculationrun_space
	calculationrun_space_uri = URIRef(ro + '0297')
	# run_on = URIRef(ro + '00000002') # calclulationrun run_on datetime
	at_date_time = URIRef(roo + '100041')
	performed_by = URIRef(ro + '0283') # calculationrun_space performed_by softwareproperties_uri
	softwareproperties_uri = URIRef(ro + '010215') # software has_label literal(SoftwareProperties)
	has_programming_language = URIRef(ro + '0010195') # software has_programming_language programminglanguage
	# programminglanguage_uri = URIRef(IAO + '0000025')
	# python_uri = URIRef(SWO + '000018')
	has_version = URIRef(ro + '0010192') # software has_version
	# version_uri = URIRef(ro + '010166')

	# ^^^^^^^^^^^^^^^^^^^^^^^^^ Level-4 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	featureparameterspace_uri = URIRef(roo + '0213')
	defined_by = URIRef(ro + 'P000009') # featureparameterspace defined_by settings

	# filterproperties_uri = URIRef(roo + '0255') # has_value wavelet right/not?
	# aggregationparameters = URIRef(roo + '0218')
	# discretizationparameters = URIRef(roo + '0214')
	# featureSpecificparameters = URIRef(roo + '0215')
	# interpolationparameters = URIRef(roo + '0217')
	# reSegmentationparameters = URIRef(roo + '0216')
	# -------------- localhost URIs ---------------------------
	localhost_patient = 'http://localhost/data/patient_'
	localhost_scan = 'http://localhost/data/scan_'
	localhost_imagevolume = 'http://localhost/data/imagevolume_'
	localhost_imagespace = 'http://localhost/data/imagespace_'
	localhost_ROI = 'http://localhost/data/ROI_'
	localhost_feature = 'http://localhost/data/feature_'
	localhost_featureparameter = 'http://localhost/data/localhost_featureparameter_'
	#-----------------------
	localhost_mm = 'http://localhost/data/mm'
	localhost_mm2 = 'http://localhost/data/mm2'
	localhost_mm3 = 'http://localhost/data/mm3'

	#------------------------RDF entities---------------------------------
	RDF_patid = URIRef(localhost_patient+patientID)
	RDF_scan = URIRef(localhost_scan + myStructUID)
	RDF_imagevolume = URIRef(localhost_imagevolume + myStructUID + '_' + urllib.quote(ROI))
	RDF_imagespace = URIRef(localhost_imagespace + myStructUID + '_' + urllib.quote(ROI))
	RDF_featureparameter = URIRef(localhost_featureparameter + myStructUID + '_' + urllib.quote(ROI))
	RDF_ROI = URIRef(localhost_ROI+ '_' + urllib.quote(ROI))
	RDF_mm = URIRef(localhost_mm)
	RDF_mm2 = URIRef(localhost_mm2)
	RDF_mm3 = URIRef(localhost_mm3)
	# --------------------
	RDF_python = Literal('Python')
	RDF_softwareversion = Literal('PyRadiomics_' + featureVector['general_info_Version'])
	RDF_featureparameter = Literal(featureVector['general_info_GeneralSettings'])
	RDF_ROItype = Literal(ROI)
	RDF_Datetime = Literal(datetime.now().strftime("%Y-%m-%d"))
	#----------------------------------------------------------------
	# Load Radiomics Ontology table
	df_RO = pd.read_csv(os.path.join(os.getcwd(),'RadiomicsOntology','ORAW_RO_Table.csv'))
	#extract feature keys and values from featureVector cumputed by pyradiomcis
	f_key = featureVector.keys()
	f_value = featureVector.values()
	# info_setting, We call it FeatureParameters in Radiomics Ontology, which is used to compute radiomic feature. 

	# # remove columns with general info from pyradiomics results
	f_index = []
	for i in range(len(f_key)):
		if 'general' not in f_key[i]: # filter out 'general_info' from featureVector
			f_index.append(i)
	radiomics_key =  []
	radiomics_value = []
	for j in f_index:
		radiomics_key.append(f_key[j])
		radiomics_value.append(f_value[j])

	# Adding elements to graph
	for i in range(len(radiomics_key)-3): # -3 means filter out patientid, RTid, and countour
		ind = pd.Index(df_RO.iloc[:,0]).get_loc(radiomics_key[i])
		tmp_uri = URIRef(df_RO.iloc[:,1][ind])
		tmp_value = Literal(radiomics_value[i])
		#---------------------------------RDF entity for feature
		RDF_feature = URIRef(localhost_feature + myStructUID + '_' + urllib.quote(ROI) + '_'  + radiomics_key[i])
		# start adding
		# ------------ patient layer ---------------
		graph.add((RDF_patid,RDF.type,patient_uri))
		graph.add((RDF_patid,has_pacs_study,RDF_scan))
		# ------------ scan layer ---------------
		graph.add((RDF_scan,RDF.type,scan_uri))
		graph.add((RDF_scan,converted_to,RDF_imagevolume))
		# ------------ image volume layer ---------------
		graph.add((RDF_imagevolume,RDF.type,image_volume_uri))
		graph.add((RDF_imagevolume,is_part_of,RDF_imagespace))
		# ------------ image space layer ---------------
		graph.add((RDF_imagespace,RDF.type,image_space_uri))
		graph.add((RDF_imagespace,used_to_compute,RDF_feature))
		graph.add((RDF_ROI,is_part_of,RDF_imagespace))
		# graph.add((RDF_ROItype,is_label_of,RDF_ROI))
		graph.add((RDF_ROI,has_label,RDF_ROItype))
		# ------------ feature layer ---------------
		graph.add((RDF_feature,RDF.type,tmp_uri))
		graph.add((RDF_feature,has_value,tmp_value))

		# ------------ calculatin run layer ------------
		graph.add((RDF_feature,computed_using,calculationrun_space_uri))
		graph.add((calculationrun_space_uri,performed_by,softwareproperties_uri))
		### missing ontology of at_date_time -------------
		graph.add((calculationrun_space_uri,at_date_time,RDF_Datetime))
		# graph.add((datetime_uri,has_value,Literal(str(datetime.now()))))
		graph.add((softwareproperties_uri,has_programming_language,RDF_python))
		graph.add((softwareproperties_uri,has_version,RDF_softwareversion))
		# %%%%%%%%%%%%%%%%%%%%%%
		# ------------feature parameter layer----------
		graph.add((RDF_feature,computed_using,featureparameterspace_uri))
		graph.add((featureparameterspace_uri,defined_by,RDF_featureparameter))
		#--------------------------------------------------------------

		# ----------- add unit to feature, if it has ------------------
		if radiomics_key[i] == 'original_shape_Volume':
			graph.add((RDF_feature,has_unit,RDF_mm3))
			graph.add((RDF_mm3,RDF.type,mm3_uri))
		if radiomics_key[i] == 'original_shape_SurfaceArea':
			graph.add((RDF_feature,has_unit,RDF_mm2))
			graph.add((RDF_mm2,RDF.type,mm2_uri))
		if radiomics_key[i] == 'original_shape_LeastAxis':
			graph.add((RDF_feature,has_unit,RDF_mm))
			graph.add((RDF_mm,RDF.type,mm_uri))      
		if radiomics_key[i] == 'original_shape_MajorAxis':
			graph.add((RDF_feature,has_unit,RDF_mm))
			graph.add((RDF_mm,RDF.type,mm_uri))
		if radiomics_key[i] == 'original_shape_Maximum2DDiameterColumn':
			graph.add((RDF_feature,has_unit,RDF_mm))
			graph.add((RDF_mm,RDF.type,mm_uri)) 
		if radiomics_key[i] == 'original_shape_Maximum2DDiameterRow':
			graph.add((RDF_feature,has_unit,RDF_mm))
			graph.add((RDF_mm,RDF.type,mm_uri))
		if radiomics_key[i] == 'original_shape_Maximum2DDiameterSlice':
			graph.add((RDF_feature,has_unit,RDF_mm))
			graph.add((RDF_mm,RDF.type,mm_uri))
		if radiomics_key[i] == 'original_shape_Maximum3DDiameter':
			graph.add((RDF_feature,has_unit,RDF_mm))
			graph.add((RDF_mm,RDF.type,mm_uri)) 
		if radiomics_key[i] == 'original_shape_MinorAxis':
			graph.add((RDF_feature,has_unit,RDF_mm))
			graph.add((RDF_mm,RDF.type,mm_uri))     
	return graph