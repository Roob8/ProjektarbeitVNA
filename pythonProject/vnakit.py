from __future__ import unicode_literals
from sys import platform, maxsize
from ctypes import *
from os.path import exists, join
from os import getenv
from collections import namedtuple
from struct import calcsize
from itertools import product

# Error Codes
VNAKIT_RES_SUCCESS = 0
VNAKIT_RES_USERERR__NOT_INITIALIZED=1
VNAKIT_RES_USERERR__NO_SETTINGS_APPLIED=2
VNAKIT_RES_USERERR__NO_RECORDING=3
VNAKIT_RES_INPUTERR__OUT_OF_RANGE=4
VNAKIT_RES_INPUTERR__INVALID_SETTINGS=5
VNAKIT_RES_INPUTERR__BAD_RESULT_SIZE=6
VNAKIT_RES_INSTRUMENT_NOT_FOUND=7
VNAKIT_RES_DEVICE_ERROR=8
VNAKIT_RES_INIT_FAILED=9
VNAKIT_RES_BAD_CONFIG=10
VNAKIT_RES_GENERAL_ERROR=11

# RX Modes
VNAKIT_MODE_ONE_PORT=0
VNAKIT_MODE_TWO_PORTS=1

# Output file formats
VNAKIT_OUTFORMAT_MAT=0
VNAKIT_OUTFORMAT_CSV=1

VnaKitErrStrings = {
    VNAKIT_RES_SUCCESS:"Operation successful",
    VNAKIT_RES_USERERR__NOT_INITIALIZED:"An attempt was made to use the sdk before a call to VNAKit_Init()",
    VNAKIT_RES_USERERR__NO_SETTINGS_APPLIED:"Attempted use of setting-dependent methods, before a call to ApplySettings()",
    VNAKIT_RES_USERERR__NO_RECORDING:"Attempted use of VNAKit_WriteRecording(), before anything is recorded",
    VNAKIT_RES_INPUTERR__OUT_OF_RANGE:"A provided parameter value was out of its allowed range",
    VNAKIT_RES_INPUTERR__INVALID_SETTINGS:"Recording Settings are not valid -- outside of allowed range, or not matching allowed step",
    VNAKIT_RES_INPUTERR__BAD_RESULT_SIZE:"Provided size for a requested result parameter does not match actual result size",
    VNAKIT_RES_INSTRUMENT_NOT_FOUND:"The SDK is unable to communicate with the instrument",
    VNAKIT_RES_DEVICE_ERROR:"Device could not connect",
    VNAKIT_RES_INIT_FAILED:"Initialization failed",
    VNAKIT_RES_BAD_CONFIG:"Bad configuration",
    VNAKIT_RES_GENERAL_ERROR:"A general error occurred. Inspect the error logs for more information"                                                            
}

class VNAKitError(Exception):
    """ VNAKit's specific Exception object.
        Args:
            message:        Short explanation about the occured exception.
            code:           Code number of the exception.
    """
    def __init__(self, ctxt, code):
        super(Exception, self).__init__(ctxt + ": " + VnaKitErrStrings[code])
        self.code = code

# Make sure python is 64 bits
if (platform == 'win32') and  (8 * calcsize('P') != 64):
    raise VNAKitError('Python must be 64bits to use this library', VNAKIT_RES_GENERAL_ERROR)

def _GetDefaultPaths(): 
    depLibPaths = []
    if platform == 'win32':
        defaultBinPath = join(getenv('ProgramFiles'), 'Vayyar', 'VNAKit', 'bin')
        libPath = join(defaultBinPath, 'VNAKit.dll')
        configFilePath = join(defaultBinPath, '.config')
        depLibPaths = [ join(defaultBinPath, 'Qt5Core.dll'), join(defaultBinPath, 'libusb-1.0.dll')]
    elif platform.startswith('linux'):
        libPath = join('/usr', 'lib', 'libVNAKit.so')     
        configFilePath = join('/etc', 'vnakit.conf')
    else:
        return None, None, None
    return libPath, configFilePath, depLibPaths
_defaultLibPath, _defaultConfigFilePath, _depLibPaths = _GetDefaultPaths()

def _InitModule(libPath, depLibPaths):
    """Must be called before using VNAKit functions.
        Args:
            libPath:        Full path to VNAKit shared library. If not set, will use default path.
            depLibPaths:    List of full paths to shared libraries that VNAKit depends on.
                            This parameter is only necessary if shared libraries are not installed on your path,
                            and/or you want to use them from some other location.
    """
    for dlPath in depLibPaths:
        if not exists(dlPath):
            raise ValueError('Could not load library at:', dlPath)
        CDLL(dlPath, mode=RTLD_GLOBAL)

    if not exists(libPath):
        raise ValueError('Could not load VNAKit library at:', libPath)
    global _vnakit

    _vnakit = CDLL(libPath)

def IsModuleInitialized():
    if '_vnakit' in globals():
        return not (_vnakit == None)
    else:
        return False;

def _RaiseIfErr(funcName, res):
    """ Raises customized VNAKitError in case encounter one.
    """
    if res != VNAKIT_RES_SUCCESS:
        raise VNAKitError(funcName, res)
    
def _SetConfigFile(path = _defaultConfigFilePath):
    """ Obtains Sets location of VNAKit configuration file, if moved from
        default.
        Args:
            path           (Optional) config file path. Uses default location
                            if no path is given.
    """
    _RaiseIfErr(_SetConfigFile.__name__, _vnakit.VNAKit_SetConfigFile(path.encode('ascii')))
    
def Init(libPath = _defaultLibPath, depLibPaths = _depLibPaths, configPath = _defaultConfigFilePath):
    """ Init method must be called before using the VNAKit library.
        Optional arguments (necessary only for non-standard installations):
            libPath :       full path to VNAKit shared object (libVNAKit.dll).
            depLibPaths :   full path to dependency libraries of VNAKit (Qt5Core, libusb-1.0)
            configPath:     full path to configuration file
    """
    _InitModule(libPath, depLibPaths)
    assert(IsModuleInitialized())
    _SetConfigFile(configPath)
    _RaiseIfErr(Init.__name__, _vnakit.VNAKit_Init())
    
class _Ctypes_FrequencyRange(Structure):
    _fields_ = [("freqStartMHz", c_double), ("freqStopMHz", c_double), ("numFreqPoints", c_int)]
    
class _Ctypes_RecordingSettings(Structure):
    _fields_ = [("freqRange", _Ctypes_FrequencyRange),
        ("rbw_khz", c_double), ("outputPower_dbm", c_double),
        ("txtr", c_int), ("mode", c_int)]

class FrequencyRange:
    """A set of frequency points, evenly spaced through a defined range.

    Use GetFrequencyLimits() for minimal and maximal values.

    Attributes:
        freqStartMHz: Beginning of range (in MHz)
        freqStopMHz: End of range (in MHz)
        numFreqPoints: Number of points taken from range
    """
    def __init__(self, freqStartMHz, freqStopMHz, numFreqPoints):
        self.freqStartMHz = freqStartMHz
        self.freqStopMHz = freqStopMHz
        self.numFreqPoints = numFreqPoints

    def __repr__(self):
        return "<FrequencyRange: [%f-%f] MHz, %d points>" % (self.freqStartMHz, self.freqStopMHz, self.numFreqPoints)
        
class RecordingSettings:
    """Full specification of a recording sweep.

    Attributes:
        freqRange: of type FrequencyRange.
        rbw_khz: RBW (in KHz); use GetRbwLimits() for permitted values
        outputPower_dbm: Output power (in dbm); use GetPowerLimits() for permitted values
        txtr: Transmitter port -- integer from 1 to 6
        mode: One of VNAKIT_MODE_ONE_PORT ; VNAKIT_MODE_TWO_PORTS
    """
    def __init__(self, freqRange, rbw_khz, outputPower_dbm, txtr, mode):
        self.freqRange = freqRange
        self.rbw_khz = rbw_khz
        self.outputPower_dbm = outputPower_dbm
        self.txtr = txtr
        self.mode = mode
    def __repr__(self):
        return "<VNAKitSettings: %s, rbw: %f KHz, power: %f dbm, txtr: %d, mode: %d-port>" % (self.freqRange, self.rbw_khz, self.outputPower_dbm, self.txtr, (1 if self.mode==VNAKIT_MODE_ONE_PORT else 2))

def __PySettings2CSettings(settings):
    return _Ctypes_RecordingSettings(
        _Ctypes_FrequencyRange(
            settings.freqRange.freqStartMHz,
            settings.freqRange.freqStopMHz,
            settings.freqRange.numFreqPoints),
        settings.rbw_khz, settings.outputPower_dbm,
        settings.txtr, settings.mode)

def ApplySettings(settings):
    """Apply settings to board.

    Attributes:
        settings: a RecordingSettings structure.
    """
    ValidateSettings(settings)
    c_settings = __PySettings2CSettings(settings)
    _RaiseIfErr(ApplySettings.__name__, _vnakit.VNAKit_ApplySettings(c_settings))
    
def GetFreqVector_MHz():
    """Returns the frequency vector rounded to the nearest allowable frequency point.
    """
    nFreqs = c_int()
    _RaiseIfErr(GetFreqVector_MHz.__name__, _vnakit.VNAKit_GetFreqVectorSizeDouble(byref(nFreqs)))
    
    buf = (c_double * nFreqs.value)()
    _vnakit.VNAKit_GetFreqVector_MHz.argtypes = [c_int, POINTER(c_double)]
    _RaiseIfErr(GetFreqVector_MHz.__name__, _vnakit.VNAKit_GetFreqVector_MHz(nFreqs, buf))

    return list(buf)

def GetActualRBW_KHz():
    """Returns the actual RBW value used (which may be modified slightly from original input).
    """
    rbw_khz = c_double()
    _RaiseIfErr(GetActualRBW_KHz.__name__, _vnakit.VNAKit_GetActualRBW_KHz(byref(rbw_khz)))
    return rbw_khz.value

def Record():
    """Run recording sweep, with previously applied settings."""
    _RaiseIfErr(Record.__name__, _vnakit.VNAKit_Record())

def WriteRecording(outDir, format):
    """Write a recording sweep result into an output file.

    Attributes:
        outDir: Directory to write file to.
        format: One of VNAKIT_OUTFORMAT_MAT ; VNAKIT_OUTFORMAT_CSV
    """
    _RaiseIfErr(WriteRecording.__name__, _vnakit.VNAKit_WriteRecording(outDir.encode('ascii'), format))
    
class _ctypes_VNAKit_Complex(Structure):
    _fields_ = [
        ('real', c_double),
        ('imag', c_double)
    ]

def _vnaKitComplex_2Python(x):
    return float(x.real) + (float(x.imag) * 1j)
 
class _ctypes_VNAKit_RecordingResult(Structure):
    _fields_ = [
        ('resultBuffer', POINTER(POINTER(_ctypes_VNAKit_Complex))),
        ('nRxTr', c_int),
        ('nFrequenciesMeasured', c_int)
    ]
            
def GetRecordingResult():
    """Returns recording sweep result as dictionary, with a list of complex phasors for each port (1-6)."""
    freqVector = GetFreqVector_MHz()
    nFreqs = len(freqVector)
    
    c_resStruct = _ctypes_VNAKit_RecordingResult()
    _vnakit.VNAKit_InitResultStructure(byref(c_resStruct), nFreqs)
    res_code_getResult = _vnakit.VNAKit_GetRecordingResult(byref(c_resStruct))
    if res_code_getResult != VNAKIT_RES_SUCCESS:
        vnakit.VNAKit_FreeResultStructure(byref(c_resStruct))
        _RaiseIfErr(GetRecordingResult.__name__, res_code_getResult)

    nRxTr = int(c_resStruct.nRxTr)
    resMap = { rxPort_i+1 : [_vnaKitComplex_2Python(c_resStruct.resultBuffer[rxPort_i][freq_i]) for freq_i in range(nFreqs)] for rxPort_i in range(nRxTr) }

    _vnakit.VNAKit_FreeResultStructure(byref(c_resStruct))

    return resMap
    
def EnterStandbyMode():
    """Power board down into standby mode to save power.
    Board will power up again as needed, with no further intervention.
    """
    _RaiseIfErr(EnterStandbyMode.__name__, _vnakit.VNAKit_EnterStandbyMode())

VNAKIT_SETTINGS__VALID=0
VNAKIT_SETTINGS__FREQ_RANGE_MALFORMED=1
VNAKIT_SETTINGS__FREQ_OUT_OF_RANGE=2
VNAKIT_SETTINGS__FREQ_BAD_STEP=3
VNAKIT_SETTINGS__NPOINTS_OUT_OF_RANGE=4
VNAKIT_SETTINGS__RBW_OUT_OF_RANGE=5
VNAKIT_SETTINGS__RBW_BAD_STEP=6
VNAKIT_SETTINGS__POWER_OUT_OF_RANGE=7
VNAKIT_SETTINGS__POWER_BAD_STEP=8
VNAKIT_SETTINGS__NPOINTS_EXCEED_RBW=9


VnaKitSettingsErrStrings = {
	VNAKIT_SETTINGS__VALID:"Settings are valid",
    VNAKIT_SETTINGS__FREQ_RANGE_MALFORMED:"freqStop is not greater than freqStart",
	VNAKIT_SETTINGS__FREQ_OUT_OF_RANGE:"Frequency start/stop are out of range",
	VNAKIT_SETTINGS__FREQ_BAD_STEP:"freqStart and/or freqStop values do not observe permitted frequency step",
	VNAKIT_SETTINGS__NPOINTS_OUT_OF_RANGE:"Number of frequency points is out of range",
	VNAKIT_SETTINGS__RBW_OUT_OF_RANGE:"RBW is out of range",
	VNAKIT_SETTINGS__RBW_BAD_STEP:"RBW value does not observe permitted RBW step",
	VNAKIT_SETTINGS__POWER_OUT_OF_RANGE:"Output power is out of range",
	VNAKIT_SETTINGS__POWER_BAD_STEP:"Output power value does not observe permitted Power step",
	VNAKIT_SETTINGS__NPOINTS_EXCEED_RBW:"Cannot measure requested number of frequency points without increasing RBW; use GetNMaxPoints_ForRbw() and GetMinRbwKhz_ForNPoints() to adjust"
}

class VNAKitSettingsError(Exception):
    """ Exception thrown by ValidateSettings if settings are invalid.
        Args:
            message:        Short explanation of problem with provided settings.
            code:           Code number of the exception.
    """
    def __init__(self, code):
        super(Exception, self).__init__("Invalid settings: " + VnaKitSettingsErrStrings[code])
        self.code = code

def ValidateSettings(settings):
    """Check a RecordingSettings structure for invalid values.
    Raises a detailed VNAKitSettingsError if settings are invalid.
    """
    c_settings = __PySettings2CSettings(settings)
    errval = _vnakit.VNAKit_ValidateSettings(c_settings)
    if errval != VNAKIT_SETTINGS__VALID:
        raise VNAKitSettingsError(errval)

    
class _ctypes_VNAKit_FrequencyLimits(Structure):
    _fields_ = [
        ("min_MHz", c_double), ("max_MHz", c_double), ("step_MHz", c_double),
        ("nPointsMin", c_int), ("nPointsMax", c_int)
    ]
class FrequencyLimits:
    def __init__(self, c_struct):
        self.min_MHz = c_struct.min_MHz
        self.max_MHz = c_struct.max_MHz
        self.step_MHz = c_struct.step_MHz
        self.nPointsMin = c_struct.nPointsMin
        self.nPointsMax = c_struct.nPointsMax
    def __repr__(self):
        return "<FrequencyLimits: [%f-%f] MHz, step: %f MHz, #Points: [%d-%d]>" % (self.min_MHz, self.max_MHz, self.step_MHz, self.nPointsMin, self.nPointsMax)

class _ctypes_VNAKit_PowerLimits(Structure):
    _fields_ = [("min_dbm", c_double), ("max_dbm", c_double), ("step_dbm", c_double)]

class PowerLimits:
    def __init__(self, c_struct):
        self.min_dbm = c_struct.min_dbm
        self.max_dbm = c_struct.max_dbm
        self.step_dbm = c_struct.step_dbm
    def __repr__(self):
        return "<PowerLimits: [%f-%f] dbm, step: %f dbm>" % (self.min_dbm, self.max_dbm, self.step_dbm)

class _ctypes_VNAKit_RbwLimits(Structure):
    _fields_ = [("min_KHz", c_double), ("max_KHz", c_double), ("step_KHz", c_double)]

class RbwLimits:
    def __init__(self, c_struct):
        self.min_KHz = c_struct.min_KHz
        self.max_KHz = c_struct.max_KHz
        self.step_KHz = c_struct.step_KHz
    def __repr__(self):
        return "<RbwLimits: [%f-%f] KHz, step: %f KHz>" % (self.min_KHz, self.max_KHz, self.step_KHz)

def GetFrequencyLimits():
    _vnakit.VNAKit_GetFrequencyLimits.restype = _ctypes_VNAKit_FrequencyLimits
    return FrequencyLimits(_vnakit.VNAKit_GetFrequencyLimits())


def GetRbwLimits():
    _vnakit.VNAKit_GetRbwLimits.restype = _ctypes_VNAKit_RbwLimits
    return RbwLimits(_vnakit.VNAKit_GetRbwLimits())


def GetPowerLimits():
    _vnakit.VNAKit_GetPowerLimits.restype = _ctypes_VNAKit_PowerLimits
    return PowerLimits(_vnakit.VNAKit_GetPowerLimits())

def GetNMaxPoints_ForRbw(rbw_KHz):
    """More frequency point requires higher RBW. Therefore, RecordingSettings must fulfill:
    settings.freqRange.numFreqPoints <= GetNMaxPoints_ForRbw(settings.rbw_KHz)
    settings.rbw_KHz >= GetMinRbwKHz_ForNPoints(settings.freqRange.numFreqPoints)
    """
    _vnakit.VNAKit_nMaxPoints_ForRbw.restype = c_int
    _vnakit.VNAKit_nMaxPoints_ForRbw.argtypes = [c_double]
    return _vnakit.VNAKit_nMaxPoints_ForRbw(rbw_KHz)

def GetMinRbwKHz_ForNPoints(nFreqPoints):
    """More frequency point requires higher RBW. Therefore, RecordingSettings must fulfill:
    settings.freqRange.numFreqPoints <= GetNMaxPoints_ForRbw(settings.rbw_KHz)
    settings.rbw_KHz >= GetMinRbwKHz_ForNPoints(settings.freqRange.numFreqPoints)
    """
    _vnakit.VNAKit_MinRbwKhz_ForNPoints.restype = c_double
    _vnakit.VNAKit_MinRbwKhz_ForNPoints.argtypes = [c_int]
    return _vnakit.VNAKit_MinRbwKhz_ForNPoints(nFreqPoints)

def _GetLastErrString():
    _vnakit.VNAKit_GetLastErrString.restype = c_char_p
    return _vnakit.VNAKit_GetLastErrString().decode('utf-8')