# Ontology-guided Radiomics Analysis Workflow (O-RAW) verison 2.2


Radiomics is high-throughput automated tumour feature extraction from medical images. This has shown potential for quantifying tumour phenotype and predicting treatment response. The three major challenges  of radiomics research and clinical adoption are: 
1. lack of standardized methodology for radiomics analyses;
2. lack of universal lexicon to denote features that are semantically equivalent;
3. lists of feature values alone do not sufficiently capture the details of feature extraction that might nonetheless strongly affect feature values (e.g. image normalization or interpolation parameters).  

We propose an open-source Ontology-guided Radiomics Analysis Workflow (O-RAW) to address the above challenges in the following manner: (i) distributing a free and open-source software package for radiomics analysis, (ii) deploying a standard lexicon to uniquely describe features in common usage and (iii) provide methods to publish radiomic features as a semantically-interoperable data graph object complying to FAIR (Findable Accessible Interoperable Reusable) data principles. 

![radiomics_workflow chart](https://user-images.githubusercontent.com/17007301/49441973-5cf6d400-f7c8-11e8-80d7-9b6c8e02777d.png)

## This repository accompanies the publication 'Technical Note: Ontology-guided Radiomics Analysis Workflow (O-RAW)'
**If you publish any work which uses this package, please cite the following publication:**
*Shi, Zhenwei, Alberto Traverso, Johan van Soest, Andre Dekker, and Leonard Wee. "Ontology‐guided Radiomics Analysis Workflow (O‐RAW)." Medical Physics (2019). https://aapm.onlinelibrary.wiley.com/doi/pdf/10.1002/mp.13844*


## Disclaimer

O-RAW is still under development. Although we have tested and evaluated the workflow under many different situations, errors and bugs still happen unfortunately. Please use it cautiously. If you find any, please contact us and we would fix them ASAP.

## Two componenets

1. [PyRadiomcs] (https://github.com/Radiomics/pyradiomics)
2. [Py-rex] (https://github.com/zhenweishi/Py-rex)

## Features

1. Py-rex is allowed users use original DICOM files and RTSTRUCT;
2. Internal module for creation of ROI binary mask;
3. Allow batch processing for all ROIs in RTSTRUCT or a given ROI.
4. Semi-automatic approach to handle multiple ROI names;
5. Radiomic features output in different formats (e.g., ttl and csv) with related ontologies (e.g., [Radiomics Ontology](https://bioportal.bioontology.org/ontologies/ROO) and [Radiation Oncology Ontology](https://bioportal.bioontology.org/ontologies/RO)).
6. Applicable for CT, PET and MRI.

## Prerequisites 

O-RAW is dependent on several tools and packages that are listed below.

1. [Anaconda](https://www.anaconda.com/download/) python 2 or 3 version, which includes python and hundreds of popular data science packages and the conda package and virtual environment manager for Windows, Linux, and MacOS.
2. [Pyradiomics](https://github.com/Radiomics/pyradiomics) - radiomic extractor.
3. [RDFLib](https://github.com/RDFLib/rdflib) - a Python library for working with RDF, a simple powerful language for representing information as graphs.

## Installation

1. Install Anaconda and add path the system environment.
2. Install the lastest Pyradiomics. More instruction, see [here](https://github.com/Radiomics/pyradiomics)
2. Clone/Download O-RAW to local directory, and go to the O-RAW working directory.
3. Execute: `python -m pip install -r pyrex_requirements.txt` under command line to install the required packages. 

		
## Getting Started
We provide a test dataset in `./data`. This dataset has a series of CT, PET & MRI scans with RTSTRUCT. The configuration file for test "./pyradiomics-master/Py-rex-master/ParamsSettings/Pyradiomics_Params.yaml"

Execute:
```
python ./HelloORAW.py
```
Or try ./Notebook/O-RAW-notebook.ipynb

Results in `./RFstore`

## License

O-RAW may not be used for commercial purposes. This package is freely available to browse, download, and use for scientific 
and educational purposes as outlined in the [Creative Commons Attribution 3.0 Unported License](https://creativecommons.org/licenses/by/3.0/).

## Developers
 - [Zhenwei Shi](https://github.com/zhenweishi)<sup>1</sup>
 - [Leonard Wee]<sup>1</sup>
 - [Andre Dekker]<sup>1</sup>
 
<sup>1</sup>Department of Radiation Oncology (MAASTRO Clinic), GROW-School for Oncology and Development Biology, Maastricht University Medical Centre, The Netherlands.
