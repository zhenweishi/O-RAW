1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
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
# Function to store readiomics in different types of formats, such as csv and RDF.
def RadiomicsRDF(featureVector,exportDir,patientID,myStructUID,ROI,export_format,export_name):
    graph = Graph() # Create a rdflib graph object
    feature_type = [] # Create a list for feature type
    feature_uri = [] # Create a list for feature uri (ontology)
    software = Literal('pyRadiomics_1.3.0')
 
    # Adding Radiomics Ontology to namespace
    ro = Namespace('http://www.radiomics.org/RO/')
    roo = Namespace('https://www.cancerdata.org/roo/')
    #graph.bind('ro',ro)
    #graph.bind('roo',roo)
 
    # ------------------------- URI of related entities
    patient_uri = URIRef('http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16960')
    scan_uri = URIRef('http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C17999')
    image_volume_uri = URIRef('http://www.radiomics.org/RO/0271')
    image_space_uri = URIRef('http://www.radiomics.org/RO/0225')
    GTV_uri = URIRef('http://www.cancerdata.org/roo/100006')
 
    #-------------------------- URI of units ------------------
    mm_uri = URIRef('http://www.radiomics/org/RO/MilliMeter')
    mm2_uri = URIRef('http://www.radiomics/org/RO/SquareMillimeter')
    mm3_uri = URIRef('http://www.radiomics/org/RO/CubicMillimeter')
     
    # ---------------------- URI of predicates --------------------
    has_pacs_study = URIRef('www.cancerdata.org/roo/100284') # patient to scan
    converted_to = URIRef('www.radiomics.org/RO/0310') # scan to image volume
    contains = URIRef('www.radiomics.org/RO/0295') # image space to GTV
    is_part_of = URIRef('www.radiomics.org/RO/0298') # image splace to 
    used_to_compute = URIRef('www.radiomics.org/RO/0296') # image space to radiomic feature
    has_value = URIRef('http://www.radiomics.org/RO/010191')
    has_unit = URIRef('http://www.radiomics.org/RO/010198')
    # ----------------------- localhost URIs ---------------------------
    localhost_patient = 'http://localhost/data/patient_'
    localhost_scan = 'http://localhost/data/scan_'
    localhost_imagevolume = 'http://localhost/data/imagevolume_'
    localhost_imagespace = 'http://localhost/data/imagespace_'
    localhost_GTV = 'http://localhost/data/GTV_'
    localhost_feature = 'http://localhost/data/feature_'
    #-----------------------
    localhost_mm = 'http://localhost/data/mm'
    localhost_mm2 = 'http://localhost/data/mm2'
    localhost_mm3 = 'http://localhost/data/mm3'
     
    #------------------------RDF entities---------------------------------
    RDF_patid = URIRef(localhost_patient+patientID)
    RDF_scan = URIRef(localhost_scan + myStructUID)
    RDF_imagevolume = URIRef(localhost_imagevolume + myStructUID + '_' + urllib.quote(ROI))
    RDF_imagespace = URIRef(localhost_imagespace + myStructUID + '_' + urllib.quote(ROI))
    RDF_GTV = URIRef(localhost_GTV)
    RDF_mm = URIRef(localhost_mm)
    RDF_mm2 = URIRef(localhost_mm2)
    RDF_mm3 = URIRef(localhost_mm3)
 
    #-------------------------------------------------------------------
    # Load the radiomics_ontology mapping table based on Radiomics Ontology
    pyradiomics_ro = os.path.join(os.getcwd(),'RadiomicsOntology','RadiomicsOntology_Table.csv')
    with open(pyradiomics_ro,'rb') as mydata:
        reader = csv.reader(mydata)
        for row in reader:
            feature_type.append(row[0])
            feature_uri.append(row[1])
    #extract feature keys and values from featureVector that is the output of pyradiomcis
 
    for i in range(len(feature_type)):
        tmp_uri = URIRef(feature_uri[i])
        tmp_value = Literal(featureVector[feature_type[i]])
        #---------------------------------RDF entity for feature
        RDF_feature = URIRef(localhost_feature + myStructUID + '_' + urllib.quote(ROI) + '_'  + feature_type[i])
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
        graph.add((RDF_imagespace,contains,RDF_GTV))
        graph.add((RDF_GTV,RDF.type,GTV_uri))
        graph.add((RDF_imagespace,used_to_compute,RDF_feature))
        # ------------ feature layer ---------------
        graph.add((RDF_feature,RDF.type,tmp_uri))
        graph.add((RDF_feature,has_value,tmp_value))
        # add unit to feature, if it has
        if feature_type[i] == 'original_shape_Volume':
            #tmp_unit = Literal('mm^3')
            graph.add((RDF_feature,has_unit,RDF_mm3))
            graph.add((RDF_mm3,RDF.type,mm3_uri))
        if feature_type[i] == 'original_shape_SurfaceArea':
            #tmp_unit = Literal('mm^2')
            graph.add((RDF_feature,has_unit,RDF_mm2))
            graph.add((RDF_mm2,RDF.type,mm2_uri))
        if feature_type[i] == 'original_shape_Maximum3DDiameter':
            #tmp_unit = Literal('mm')
            graph.add((RDF_feature,has_unit,RDF_mm))
            graph.add((RDF_mm,RDF.type,mm_uri))    
    return graph