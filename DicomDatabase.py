import pydicom
import os

class DicomDatabase:
    def __init__(self):
        self.patient = dict()
    
    def parseFolder(self, folderPath):
        for root, subdirs, files in os.walk(folderPath):
            for filename in files:
                file_path = os.path.join(root, filename)
                if(file_path.endswith(".dcm") or file_path.endswith(".DCM")):
                    dcmHeader = pydicom.dcmread(file_path)
                    patientId = dcmHeader[0x10,0x20].value
                    patient = self.getOrCreatePatient(patientId)
                    patient.addFile(file_path, dcmHeader)

    def getOrCreatePatient(self, patientId):
        if not (patientId in self.patient):
            self.patient[patientId] = Patient()
        return self.patient[patientId]
    
    def countPatients(self):
        return len(self.patient)
    
    def getPatient(self, patientId):
        return self.patient[patientId]
    
    def getPatientIds(self):
        return self.patient.keys()
    
    def doesPatientExist(self, patientId):
        # return self.patient.has_key(patientId)
        return patientId in self.patient
class Patient:
    def __init__(self):
        self.ct = dict()
        self.rtstruct = dict()

    def addFile(self, filePath, dcmHeader):
        modality = dcmHeader[0x8,0x60].value
        sopInstanceUid = dcmHeader[0x8,0x18].value
        seriesInstanceUid = dcmHeader[0x20,0xe].value
        if(modality == "CT") or (modality == "PT") or (modality == "MR"):
            if not (seriesInstanceUid in self.ct):
                self.ct[seriesInstanceUid] = CT()
            myCT = self.ct[seriesInstanceUid]
            myCT.addCtSlice(filePath)
        if(modality == "RTSTRUCT"):
            struct = RTStruct(filePath)
            self.rtstruct[sopInstanceUid] = struct
    
    def countCTScans(self):
        return len(self.ct)
    def countRTStructs(self):
        return len(self.rtstruct)
    
    def getCTScan(self, seriesInstanceUid):
        if seriesInstanceUid is not None:
            if self.doesCTExist(seriesInstanceUid):
                return self.ct[seriesInstanceUid]
        return None
    def getRTStruct(self, sopInstanceUid):
        return self.rtstruct[sopInstanceUid]
    
    def getCTScans(self):
        return self.ct.keys()
    def getRTStructs(self):
        return self.rtstruct.keys()
    
    def doesCTExist(self, seriesInstanceUid):
        # return self.ct.has_key(seriesInstanceUid)
        return seriesInstanceUid in self.ct
    def doesRTStructExist(self, sopInstanceUid):
        # return self.rtstruct.has_key(sopInstanceUid)
        return sopInstanceUid in self.rtstruct
    
    def getCTForRTStruct(self, rtStruct):
        if rtStruct.getReferencedCTUID() is not None:
            return self.getCTScan(rtStruct.getReferencedCTUID())
        else:
            return None

class CT:
    def __init__(self):
        self.filePath = list()
    def addCtSlice(self, filePath):
        self.filePath.append(filePath)
    def getSlices(self):
        return self.filePath
    def getSliceCount(self):
        return len(self.filePath)
    def getSliceHeader(self, index):
        return pydicom.dcmread(self.filePath[index])

class RTStruct:
    def __init__(self, filePath):
        self.filePath = filePath
    def getHeader(self):
        return pydicom.dcmread(self.filePath)
    def getReferencedCTUID(self):
        dcmHeader = self.getHeader()
        if len(list(dcmHeader[0x3006,0x10])) > 0:
            refFrameOfRef = (dcmHeader[0x3006,0x10])[0]
            if len(list(refFrameOfRef[0x3006, 0x0012])) > 0:
                rtRefStudy = (refFrameOfRef[0x3006, 0x0012])[0]
                if len(list(rtRefStudy[0x3006,0x14])) > 0:
                    rtRefSerie = (rtRefStudy[0x3006,0x14])[0]
                    return rtRefSerie[0x20,0xe].value
        return None
    def getFileLocation(self):
        return self.filePath