## Ontology-guided Radiomics Analysis Workflow (O-RAW) verison 1.0

This is an open-source python package for radiomics analysis. With this pacakge we aim to allow users to use origial DICOM file and RTSTRUCT for radiomics calculation. 

## Disclaimer

O-RAW is still under development. Although we have tested and evaluated the workflow under many different situations, errors and bugs still happen unfortunately. Please use it cautiously. If you find any, please contact us and we would fix them ASAP.

### Features
1. Py-rex is allowed users use original DICOM files and RTstruture;
2. Internal module for creation of ROI binary mask;
3. Allow batch processing for all ROIs in RTSTRUCT or a given ROI.
4. Semi-automatic approach to handle multiple ROI names;
5. Radiomic features output in different formats (e.g., ttl and csv) with related ontologies (e.g., [Radiomics Ontology](https://bioportal.bioontology.org/ontologies/ROO) and [Radiation Oncology Ontology](https://bioportal.bioontology.org/ontologies/RO)).
6. Applicable for CT, PET and MRI.
7. Connection to online databse platform ([XNAT](https://xnat.bmia.nl/app/template/Index.vm)).

### Prerequisites 

O-RAW is dependent on several tools and packages that are listed below.

1. [Anaconda](https://www.anaconda.com/download/) python 2.7 version, which includes python and hundreds of popular data science packages and the conda package and virtual environment manager for Windows, Linux, and MacOS.
2. [Pyradiomics](https://github.com/Radiomics/pyradiomics) - radiomic extractor.
3. [RDFLib](https://github.com/RDFLib/rdflib) - a Python library for working with RDF, a simple yet powerful language for representing information as graphs.
4. [Pyxnat](https://pythonhosted.org/pyxnat/)- connect O-RAW to [XNAT](https://xnat.bmia.nl/app/template/Index.vm) online database platforms for upload and download data.

### Installation

1. Install Anaconda and add path the system environment.
2. Install the lastest Pyradiomics. More instruction, see [here](https://github.com/Radiomics/pyradiomics)
2. Clone/Download Py-rex to the sub-directory of Pyradiomics
3. Execute: `python -m pip install -r pyrex_requirements.txt` under command line to make sure you first install the required packages. 

		
### Getting Started
We provide a test dataset in `./data`. This dataset has a series of CT & MRI scans with RTSTRUCT. Change configuration file "./pyradiomics-master/Py-rex-master/ParamsSettings/Pyrex_Params.yaml"

Execute:
```
python ./HelloPyrex.py
```

Results in "./RFstore"

### License

Py-rex may not be used for commercial purposes. This package is freely available to browse, download, and use for scientific 
and educational purposes as outlined in the [Creative Commons Attribution 3.0 Unported License](https://creativecommons.org/licenses/by/3.0/).

### Developers
 - [Zhenwei Shi](https://github.com/zhenweishi)<sup>1</sup>
 - [Leonard Wee]<sup>1</sup>
 - [Andre Dekker]<sup>1</sup>
 
<sup>1</sup>Department of Radiation Oncology (MAASTRO Clinic), GROW-School for Oncology and Development Biology, Maastricht University Medical Centre, The Netherlands.
