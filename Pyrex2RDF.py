"""
###############################
@author: zhenwei.shi, Maastro##
###############################
"""

from rdflib import Graph, Literal
from rdflib.namespace import Namespace,URIRef,RDF,RDFS
import urllib.parse
import os
import csv
from datetime import datetime
import pandas as pd
import yaml

# Function to store readiomics in different types of formats, such as csv and RDF.
def RadiomicsRDF(featureVector,patientID,myStructUID,ROI):

	#&&&&&&&&&&&&&&&&&&& reading ORAW universal template yaml file &&&&&&&&&&&&&&&&&&&&&&
	with open(os.path.join(os.getcwd(),'ParamsSettings', 'ORAW_UniversalTemplate.yaml')) as data:
		try:
			Utemplate = yaml.safe_load(data)
		except yaml.YAMLError as exc:
			print(exc)
	# ----------------------------------For PyRadiomics ---------------------------------
	# Mapping O-RAW setting to universal template. Some are already there, but some are needed to update
	Utemplate['General']['Software']['name'] = 'PyRadiomics'
	Utemplate['General']['Software']['version'] = featureVector['diagnostics_Versions_PyRadiomics']
	Utemplate['General']['Software']['programminglanguage'] = 'Python'
	Utemplate['ImageProcessing']['Processing'] = featureVector['diagnostics_Configuration_Settings']['resampledPixelSpacing']
	Utemplate['ROISegmentation']['ROIType']  = ROI

	Utemplate['Interpolation']['ImageInterplationMethod'] = featureVector['diagnostics_Configuration_Settings']['interpolator']
	Utemplate['ROIResegmentation']['ResegmentRange'] = featureVector['diagnostics_Configuration_Settings']['resegmentRange']
	Utemplate['ROIResegmentation']['ResegmentMode'] = featureVector['diagnostics_Configuration_Settings']['resegmentMode']

	# ----------------------------------------------------- ---------------------------------


	# def ToRDF(featureVector,exportDir,patientID,myStructUID,ROI,export_format,export_name):
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
	has_imaging_modality = URIRef(ro + 'P02928312341') # scan has_imaging_modality CT, PET, MR
	image_volume_uri = URIRef(ro + '0271')
	is_part_of = URIRef(ro + '0298') # image_volume is_part_of image_space 
	has_processing = URIRef(ro + 'P00080') # image_volume has_processing method 
	has_voxel_dimension = URIRef(ro + 'P00118') # image_volume has_has_voxel_dimension voxel_size
	has_voxel_dimensionx = URIRef(ro + 'P00118') # image_volume has_has_voxel_dimension voxel_size
	has_voxel_dimensiony = URIRef(ro + 'P00123') # image_volume has_has_voxel_dimension voxel_size
	has_voxel_dimensionz = URIRef(ro + 'P00149') # image_volume has_has_voxel_dimension voxel_size
	image_space_uri = URIRef(ro + '0225')
	# ROImask_uri = URIRef(roo + '0272') # ROImask is_part_of image_space
	is_label_of = URIRef(ro + 'P00190') #  GTV/... is_label_of ROImask 
	has_label = URIRef(ro+'P00051')
	has_segmentation_method = URIRef(ro+'P00092')
	# GTV_uri = URIRef(roo + '100006')
	used_to_compute = URIRef(ro + '0296') # image_space used_to_compute RadiomicsFeature
	# tempral
	has_property = URIRef(roo + '100212')

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
	featureparameterspace_uri = URIRef(ro + '001000')
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


	# ---------------------- info from yaml file ------------------
	# O-RAW_config:
	#   export_format: rdf
	#   export_name: ORAW_RDF_test
	# General
	RDF_General_ImageAcquisition_ImagingModality = Literal(Utemplate['General']['ImageAcquisition']['ImagingModality'])
	RDF_General_VolumetricAnalysis = Literal(Utemplate['General']['VolumetricAnalysis'])
	RDF_General_WorkflowStructure = Literal(Utemplate['General']['WorkflowStructure'])
	RDF_General_Software_name = Literal(Utemplate['General']['Software']['name'])
	RDF_General_Software_version = Literal(Utemplate['General']['Software']['version'])
	RDF_General_Software_programminglanguage = Literal(Utemplate['General']['Software']['programminglanguage'])
	# ImageProcessing
	RDF_ImageProcessing_Conversion = Literal(Utemplate['ImageProcessing']['Conversion'])
	RDF_ImageProcessing_Processing = Literal(Utemplate['ImageProcessing']['Processing'])
	# ROISegmentation
	RDF_ROISegmentation_SegmentationMethod = Literal(Utemplate['ROISegmentation']['SegmentationMethod'])
	RDF_ROISegmentation_ROIType = Literal(Utemplate['ROISegmentation']['ROIType'])
	# Interpolation
	RDF_Interpolation_VoxelDimensions = Literal(Utemplate['Interpolation']['VoxelDimensions'])
	RDF_Interpolation_ImageInterplationMethod = Literal(Utemplate['Interpolation']['ImageInterplationMethod'])
	RDF_Interpolation_IntensityRounding = Literal(Utemplate['Interpolation']['IntensityRounding'])
	RDF_Interpolation_ROIInterplationMethod = Literal(Utemplate['Interpolation']['ROIInterplationMethod'])
	RDF_Interpolation_ROIPartialVolume = Literal(Utemplate['Interpolation']['ROIPartialVolume'])
	# ROIResegmentation
	RDF_ROIResegmentation_ResegmentRange = Literal(Utemplate['ROIResegmentation']['ResegmentRange'])
	RDF_ROIResegmentation_ResegmentMode = Literal(Utemplate['ROIResegmentation']['ResegmentMode'])
	# ImageDiscretization
	# RDF_ImageDiscretization_DiscretizationMethod = Literal(Utemplate['ImageDiscretization']['DiscretizationMethod'])
	# RDF_ImageDiscretization_DiscretizationParameters = Literal(Utemplate['ImageDiscretization']['DiscretizationParameters'])

	#------------------------RDF entities--------------------------------------------------
	RDF_patid = URIRef(localhost_patient+patientID)
	RDF_scan = URIRef(localhost_scan + myStructUID)
	RDF_imagevolume = URIRef(localhost_imagevolume + myStructUID + '_' + urllib.parse.quote(RDF_ROISegmentation_ROIType))
	RDF_imagespace = URIRef(localhost_imagespace + myStructUID + '_' + urllib.parse.quote(RDF_ROISegmentation_ROIType))
	RDF_featureparameter = URIRef(localhost_featureparameter + myStructUID + '_' + urllib.parse.quote(RDF_ROISegmentation_ROIType))
	RDF_ROI = URIRef(localhost_ROI+ myStructUID + '_' + urllib.parse.quote(RDF_ROISegmentation_ROIType))
	RDF_Datetime = Literal(datetime.now().strftime("%Y-%m-%d")) # run at_date_time
	RDF_mm = URIRef(localhost_mm)
	RDF_mm2 = URIRef(localhost_mm2)
	RDF_mm3 = URIRef(localhost_mm3) 
	#------------------------read Radiomics Ontology Table---------------------------------
	df_RO = pd.read_csv(os.path.join(os.getcwd(),'RadiomicsOntology','ORAW_RO_Table.csv'))

	#extract feature keys and values from featureVector cumputed by pyradiomcis
	f_key = list(featureVector.keys())
	f_value = list(featureVector.values())
	# # remove columns with general info from pyradiomics results
	f_index = []
	for i in range(len(f_key)):
		if 'diagnostics' not in f_key[i]: # filter out 'general_info' from featureVector
			f_index.append(i)
	radiomics_key =  []
	radiomics_value = []
	for j in f_index:
		radiomics_key.append(f_key[j])
		radiomics_value.append(f_value[j])

	#-----------------Adding elements to graph --------------------------------------------
	for i in range(len(radiomics_key)): # -3 means filter out patientid, RTid, and countour
		try:
			ImageFilterSpace = Utemplate['FeatureCalculation']['FeatureParameter']['ImageFilterSpace']
			for j in range(len(ImageFilterSpace)):
				imagetype = ImageFilterSpace[j]
				if imagetype.lower() in radiomics_key[i]:
					RDF_ImageFilterSpace = Literal(Utemplate['FeatureCalculation']['FeatureParameter']['ImageFilterSpace'][j])
					RDF_ImageFilterMethod = Literal(Utemplate['FeatureCalculation']['FeatureParameter']['DiscretizationMethod'][j])
					# RDF_ImageFilterDiscretizationParameters = Literal(Utemplate['FeatureCalculation']['FeatureParameter']['DiscretizationParameters'])
		except:
			print('radiomic features do not match the used filter method, please check the Universal Template and Radiomics Table !!!')

		if 'original' in radiomics_key[i]:
			radiomics_feature = radiomics_key[i][9:]
		elif 'log' in radiomics_key[i]:
			radiomics_feature = radiomics_key[i][20:]
		elif 'wavelet' in radiomics_key[i]:
			radiomics_feature = radiomics_key[i][12:]
		else:
			radiomics_feature = radiomics_feature		

		## --------------------------------------------------
		ind = pd.Index(df_RO.iloc[:,0]).get_loc(radiomics_feature)
		tmp_ROcode = df_RO.iloc[:,1][ind]
		tmp_uri = URIRef(tmp_ROcode)
		tmp_value = Literal(radiomics_value[i]) # radiomics_feature
		#---------------------------------RDF entity for feature
		RDF_feature = URIRef(localhost_feature + myStructUID + '_' + urllib.parse.quote(RDF_ROISegmentation_ROIType) + '_'  + radiomics_key[i])
		RDF_featureparameterspace = URIRef(featureparameterspace_uri + '_'  + radiomics_key[i])

		# ----------------------------------------------------
		# start adding
		# ------------ patient layer ---------------
		graph.add((RDF_patid,RDF.type,patient_uri))
		graph.add((RDF_patid,has_pacs_study,RDF_scan))
		# ------------ scan layer -----------------
		graph.add((RDF_scan,RDF.type,scan_uri))
		graph.add((RDF_scan,converted_to,RDF_imagevolume))
		graph.add((RDF_scan,has_imaging_modality,RDF_General_ImageAcquisition_ImagingModality))
		# ------------ image_volume layer ---------
		graph.add((RDF_imagevolume,RDF.type,image_volume_uri))
		graph.add((RDF_imagevolume,has_processing,RDF_ImageProcessing_Processing))
		graph.add((RDF_imagevolume,has_property,RDF_ImageProcessing_Conversion))
		graph.add((RDF_imagevolume,has_voxel_dimension,RDF_Interpolation_VoxelDimensions))
		graph.add((RDF_imagevolume,is_part_of,RDF_imagespace))
		# ------------ image_space layer ------------
		graph.add((RDF_imagespace,RDF.type,image_space_uri))
		graph.add((RDF_imagespace,used_to_compute,RDF_feature))
		# ------------ ROI mask layer ---------------
		graph.add((RDF_ROI,is_part_of,RDF_imagespace))
		graph.add((RDF_ROI,has_label,RDF_ROISegmentation_ROIType))
		graph.add((RDF_ROI,has_segmentation_method,RDF_ROISegmentation_SegmentationMethod))
		graph.add((RDF_ROI,has_property,RDF_Interpolation_ROIInterplationMethod))
		graph.add((RDF_ROI,has_property,RDF_Interpolation_ROIPartialVolume))
		# ------------ feature layer ----------------
		graph.add((RDF_feature,RDF.type,tmp_uri))
		graph.add((RDF_feature,has_value,tmp_value))
		# ------------ calculatin run layer ---------
		graph.add((RDF_feature,computed_using,calculationrun_space_uri))
		graph.add((calculationrun_space_uri,performed_by,softwareproperties_uri))
		### missing ontology of at_date_time --------
		graph.add((calculationrun_space_uri,at_date_time,RDF_Datetime))
		graph.add((softwareproperties_uri,has_programming_language,RDF_General_Software_programminglanguage))
		graph.add((softwareproperties_uri,has_version,RDF_General_Software_version))
		graph.add((softwareproperties_uri,has_property,RDF_General_Software_name))
		# ------------feature parameter layer--------
		graph.add((RDF_feature,computed_using,RDF_featureparameterspace))
		graph.add((RDF_featureparameterspace,defined_by,RDF_featureparameter))
		graph.add((RDF_featureparameterspace,defined_by,RDF_ROIResegmentation_ResegmentRange))
		graph.add((RDF_featureparameterspace,defined_by,RDF_ROIResegmentation_ResegmentMode))
		# graph.add((RDF_featureparameterspace,defined_by,RDF_ImageDiscretization_DiscretizationMethod))
		# graph.add((RDF_featureparameterspace,defined_by,RDF_ImageDiscretization_DiscretizationParameters))
		graph.add((RDF_featureparameterspace,defined_by,RDF_Interpolation_ImageInterplationMethod))
		graph.add((RDF_featureparameterspace,defined_by,RDF_Interpolation_IntensityRounding))
		graph.add((RDF_featureparameterspace,defined_by,RDF_ImageFilterSpace))
		graph.add((RDF_featureparameterspace,defined_by,RDF_ImageFilterMethod))
		# graph.add((RDF_featureparameterspace,defined_by,RDF_ImageFilterDiscretizationParameters))

		# ----------- add unit to feature, if it has ------------------
		if tmp_ROcode == 'www.radiomics.org/RO/RNU0':
			graph.add((RDF_feature,has_unit,RDF_mm3))
			graph.add((RDF_mm3,RDF.type,mm3_uri))
		if tmp_ROcode == 'www.radiomics.org/RO/C0JK':
			graph.add((RDF_feature,has_unit,RDF_mm2))
			graph.add((RDF_mm2,RDF.type,mm2_uri))
		# if tmp_ROcode == 'original_shape_LeastAxis':
		# 	graph.add((RDF_feature,has_unit,RDF_mm))
		# 	graph.add((RDF_mm,RDF.type,mm_uri))      
		# if tmp_ROcode == 'original_shape_MajorAxis':
		# 	graph.add((RDF_feature,has_unit,RDF_mm))
		# 	graph.add((RDF_mm,RDF.type,mm_uri))
		if tmp_ROcode == 'www.radiomics.org/RO/2150':
			graph.add((RDF_feature,has_unit,RDF_mm))
			graph.add((RDF_mm,RDF.type,mm_uri)) 
		if tmp_ROcode == 'www.radiomics.org/RO/2140':
			graph.add((RDF_feature,has_unit,RDF_mm))
			graph.add((RDF_mm,RDF.type,mm_uri))
		if tmp_ROcode == 'www.radiomics.org/RO/2130':
			graph.add((RDF_feature,has_unit,RDF_mm))
			graph.add((RDF_mm,RDF.type,mm_uri))
		if tmp_ROcode == 'www.radiomics.org/RO/L0JK':
			graph.add((RDF_feature,has_unit,RDF_mm))
			graph.add((RDF_mm,RDF.type,mm_uri))
		# if tmp_ROcode == 'original_shape_MinorAxis':
		# 	graph.add((RDF_feature,has_unit,RDF_mm))
		# 	graph.add((RDF_mm,RDF.type,mm_uri))  
	return graph