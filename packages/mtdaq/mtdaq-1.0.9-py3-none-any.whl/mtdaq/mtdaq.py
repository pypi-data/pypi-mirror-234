# -*- coding: utf-8 -*-

# from ctypes import *
from ctypes import cdll,c_char_p,POINTER,c_int32,create_string_buffer,byref,c_uint32,pointer,c_float,\
c_doule,c_uint16,c_uint64,Structure,c_ubyte,c_char,cast
import platform
import os

system = platform.system()
bit = platform.architecture()
if system == 'Windows': #Win
    if bit[0] == '32bit':
        dllpath = os.getenv('SystemDrive') + r'\ProgramData\MangoTree\DLL\x86\MTDAQ_x86.dll'
    elif bit[0] == '64bit':
        dllpath = os.getenv('SystemDrive') + r'\ProgramData\MangoTree\DLL\x64\MTDAQ_x64.dll'
elif system == 'Darwin': #MacOS
    if bit[0] == '64bit':
        dllpath = r'/Library/Application Support/MangoTree/DLL/MTDAQ.framework/MTDAQ'
    else:
        raise Exception("Python 64-bit Required on MacOS.")
elif system == "Linux": #Linux
    if bit[0] == '64bit':
        dllpath = r'/usr/local/MangoTree/DLL/MTDAQ_x64.so'
    else:
        raise Exception("Python 64-bit Required on Linux.")
else:
    raise Exception("Unsupported System.")

if os.path.isfile(dllpath):
    dll = cdll.LoadLibrary(dllpath)
else:
    raise Exception("MT-Master not Installed!")
    
_REFLEN = 20000
def _dev_start(config):    
    dll.MTDAQ_Start.argtypes = [c_char_p, c_char_p, POINTER(c_int32)]
    config_ = c_char_p(config.encode())
    task = create_string_buffer(_REFLEN)
    dll.MTDAQ_Start(config_, task, byref(c_int32(_REFLEN)))
    return task

def _dev_close(task):
    dll.MTDAQ_Close.argtypes = [c_char_p]
    dll.MTDAQ_Close(task)
    
def _reg_write(task, reg_name, reg_value):
    dll.MTDAQ_Custom_WriteU32.argtypes = [c_char_p, c_char_p, c_uint32]
    c_reg_name = c_char_p(reg_name.encode())
    dll.MTDAQ_Custom_WriteU32(task, c_reg_name, c_uint32(reg_value))
    
def _reg_read(task, reg_name):
    dll.MTDAQ_Custom_ReadU32.argtypes = [c_char_p, c_char_p, POINTER(c_uint32)]
    c_reg_name = c_char_p(reg_name.encode())
    reg_ptr = pointer(c_uint32())
    dll.MTDAQ_Custom_ReadU32(task, c_reg_name, reg_ptr)
    return reg_ptr.contents.value

def _data_ai(task, samples, channel_num, timeout):
#     int32_t __cdecl MTDAQ_ReadAI(char PXIString[], uint32_t AI_ReadElements, 
# 	int32_t AI_TimeoutMs, float ReadIn[], int32_t ReadLen, 
# 	uint32_t *ElementsCanRead, uint32_t *ActualSize);
    datalen = samples * channel_num
    ctype_aidata = c_float * datalen
    dll.MTDAQ_ReadAI.argtypes = [c_char_p, c_uint32, c_int32, ctype_aidata, c_int32, POINTER(c_uint32), POINTER(c_uint32)]
    c_aidata = ctype_aidata()
    dll.MTDAQ_ReadAI(task, c_uint32(samples), timeout, c_aidata, datalen, pointer(c_uint32()), pointer(c_uint32()))
    return c_aidata
    
def _data_ao(task, aodata, timeout):
#     int32_t __cdecl MTDAQ_WriteAO(char PXIString[], float AO_WriteData[], 
# 	int32_t AO_WriteDataLen, int32_t AO_Timeout, uint32_t *AO_ElementsCanWrite);
    ctype_aodata = c_float * len(aodata)    
    c_aodata = ctype_aodata(*aodata)
    dll.MTDAQ_WriteAO.argtypes = [c_char_p, ctype_aodata, c_int32, c_int32, POINTER(c_uint32)]
    dll.MTDAQ_WriteAO(task, c_aodata, len(aodata), timeout, pointer(c_uint32()))
    
def _data_ldi(task):
#   int32_t __cdecl MTDAQ_ReadLDI(char MTRefIn[], uint64_t *LDI);
    dll.MTDAQ_ReadLDI.argtypes = [c_char_p, POINTER(c_uint64)]
    c_ldi = c_uint64()
    dll.MTDAQ_ReadLDI(task, pointer(c_ldi))
    return c_ldi

def _data_ldo(task, ldo_data):
#   int32_t __cdecl MTDAQ_WriteLDO(char MTRefIn[], uint64_t LDO);
    dll.MTDAQ_WriteLDO.argtypes = [c_char_p, c_uint64]
    dll.MTDAQ_WriteLDO(task, c_uint64(ldo_data))

def _data_hdi(task, samples, timeout):
#     int32_t __cdecl MTDAQ_ReadDI(char PXIString[], uint32_t HDI_ReadElements, 
# 	int32_t HDI_Timeout, uint32_t HDI_ReadData[], int32_t HDI_ReadLen, 
# 	uint32_t *ElementsCanRead);
    ctype_didata = c_uint32 * samples
    dll.MTDAQ_ReadDI.argtypes = [c_char_p, c_uint32, c_int32, ctype_didata, c_int32, POINTER(c_uint32)]
    c_didata = ctype_didata()
    dll.MTDAQ_ReadDI(task, c_uint32(samples), timeout, c_didata, samples, pointer(c_uint32()))
    return c_didata

def _data_hdo(task, hdodata, timeout):
#     int32_t __cdecl MTDAQ_WriteDO(char PXIString[], uint32_t HDO_WriteData[], 
# 	int32_t HDO_WriteLen, int32_t HDO_Timeout, uint32_t *HDO_ElementsCanWrite);
    ctype_dodata = c_uint32 * len(hdodata)
    dll.MTDAQ_WriteDO.argtypes = [c_char_p, ctype_dodata, c_int32, c_int32, POINTER(c_uint32)]
    c_dodata = ctype_dodata(*hdodata)
    dll.MTDAQ_WriteDO(task, c_dodata, len(hdodata), timeout, pointer(c_uint32()))    
    
def _data_ci(task, samples, timeout):
#     int32_t __cdecl MTDAQ_ReadCI(char PXIString[], uint32_t CI_ReadElements, 
# 	int32_t CI_Timeout, float CI_ReadData[], int32_t CI_ReadLen, 
# 	uint32_t *ElementsCanRead);
    ctype_ci = c_float * samples
    dll.MTDAQ_ReadCI.argtypes = [c_char_p, c_uint32, c_int32, ctype_ci, c_int32, POINTER(c_uint32)]
    c_cidata = ctype_ci()
    dll.MTDAQ_ReadCI(task, c_uint32(samples), timeout, c_cidata, samples, pointer(c_uint32()))    
    return c_cidata    

def _data_pwm(task, count):
    # int32_t __cdecl MTDAQ_WritePWM(char PXIString[], float PusleCounter);
    dll.MTDAQ_WritePWM.argtypes = [c_char_p, c_float]
    dll.MTDAQ_WritePWM(task, c_float(count))
    
def _data_encoder(task, samples, channel_num, timeout):
#     int32_t __cdecl MTDAQ_ReadEncoder(char PXIStringIn[], 
# 	uint32_t Encoder_ReadElements, int32_t Encoder_Timeout, 
# 	int32_t Encoder_ReadData[], int32_t Encoder_ReadLen, 
# 	uint32_t *ElementCanRead);
    datalen = samples * channel_num * 2
    ctype_encoder = c_int32 * datalen
    dll.MTDAQ_ReadEncoder.argtypes = [c_char_p, c_uint32, c_int32, ctype_encoder, c_int32, POINTER(c_uint32)]
    c_encoderdata = ctype_encoder()
    dll.MTDAQ_ReadEncoder(task, c_uint32(datalen), timeout, c_encoderdata, datalen, pointer(c_uint32()))
    return c_encoderdata
    
def _data_temperature(task, channel_num):
#     int32_t __cdecl MTDAQ_ReadTemp(char PXIString[], double Temperature[], 
# 	float *TC_CJC_Temperature, int32_t len);
    ctype_temp = c_doule * channel_num 
    dll.MTDAQ_ReadTemp.argtypes = [c_char_p, ctype_temp, POINTER(c_float), c_int32]
    c_temp = ctype_temp()
    c_cjc = c_float()
    dll.MTDAQ_ReadTemp(task, c_temp, pointer(c_cjc), channel_num)
    return c_temp, c_cjc
    
def _get_channel_num(task, channel_name):
#     int32_t __cdecl MTDAQ_ComputingBinary(char PXIString[], 
# 	uint16_t ChanneName, uint32_t *BinaryNumber);
    chnnel_num_dict = {
        "AI": 0,
        "AO": 1,
        "HSDI": 2,
        "HSDO": 3,
        "CI": 4,
        "CO": 5,
        "Encoder": 6,
        }
    ch = chnnel_num_dict.get(channel_name)
    if ch is not None:
        dll.MTDAQ_ComputingBinary.argtypes = [c_char_p, c_uint16, POINTER(c_uint32)]
        c_channel_num = pointer(c_uint32())
        dll.MTDAQ_ComputingBinary(task, c_uint16(ch), c_channel_num)
        return c_channel_num.contents.value
    return None

from enum import IntEnum
class Mode(IntEnum):
    General = 0
    AOSyncAI = 1
    AISyncEncoder = 2
    EncoderSyncAI = 3
    DITrigerAISyncAO = 4
    DITrigerAI = 5
    DITrigerAO = 6
    Custom = 7


# ###############################

# def _c_char_p_init(char, default):
#     return c_char_p(char.encode() if char is not None else default.encode())

# class LStr(Structure):
#     _fields_ = [('cnt', c_int32),
#                 ('str', c_ubyte * 1)]
# LStrPtr = POINTER(LStr)
# LStrHandle = POINTER(LStrPtr)
    
# class DeviceInfo(Structure):
#     _fields_ = [('Model', LStrHandle),
#                 ('ID', LStrHandle),
#                 ('Slot', LStrHandle)]

# def string2LStrHandle(string):
#     string_ = string.encode()
#     len_ = len(string)
#     class LStr_(Structure):
#         _fields_ = [('cnt', c_int32),
#                     ('str', c_char * len_)]
#     lstrptr = cast(pointer(LStr_(len_, string_)), LStrPtr)
#     return pointer(lstrptr)

# def lStrHandle2String(lstrhandle):
#     lstr = lstrhandle.contents.contents
#     lstrptr_ = cast(lstr.str, POINTER(c_char * lstr.cnt))
#     return lstrptr_.contents.raw.decode()

# class LStrHandleArrayBase(Structure):
#     _fields_ = [('cnt', c_int32),
#                 ('str', LStrHandle * 1)]
# LStrHandleArray = POINTER(POINTER(LStrHandleArrayBase))

# def getConfig(mode=0, ip=None, device_name=None, device_id=None, slot=None, custom_rom_path=None):
#     dll.MTDAQ_Config_Module.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_uint16, c_char_p, c_char_p, c_int32]
#     c_ip = _c_char_p_init(ip, "")
#     c_device = _c_char_p_init(device_name, "")
#     c_id = _c_char_p_init(device_id, "*")
#     c_slot = _c_char_p_init(slot, "*")
#     c_mode = c_uint16(mode)    
#     c_path = _c_char_p_init(custom_rom_path, "")
#     c_config = create_string_buffer(_REFLEN)
#     ret = dll.MTDAQ_Config_Module(c_ip, c_device, c_id, c_slot, c_mode, c_path, c_config, _REFLEN)
#     if ret == 12:
#         raise Exception("Unknown Device.")
#     return c_config.value.decode()

# ##################################
    

from functools import wraps

class Device():
    def __init__(self, config):
        self.config = config
        self._task = None
        self._run = False
        self._chnum = {}
        
    def start(self):
        self._run = False
        self._chnum = {}
        self._task = _dev_start(self.config)
        if len(self._task.value) == 0:
            raise Exception("Failed to Open Device!")
        self._run = True
        
    def close(self):
        _dev_close(self._task)
        self._run = False
    
    
    def is_running(func):
        @wraps(func)
        def wrapper(obj, *args, **kwargs):
            if not obj._run:
                raise Exception("Device not Running!")
            return func(obj, *args, **kwargs)
        return wrapper
    
    
    @is_running
    def analogRead(self, samples, timeout=2500):
        if "AI" not in self._chnum.keys():
            self._chnum["AI"] = _get_channel_num(self._task, "AI")
        return _data_ai(self._task, samples, self._chnum["AI"], timeout)
    
    @is_running
    def analogWrite(self, aodata, timeout=2500):
        _data_ao(self._task, aodata, timeout)
    
    @is_running
    def digitalRead(self):
        return _data_ldi(self._task)
    
    @is_running
    def digitalWrite(self, dodata):
        _data_ldo(self._task, dodata)
    
    @is_running
    def digitalWaveformRead(self, samples, timeout=2500):
        return _data_hdi(self._task, samples, timeout)
    
    @is_running
    def digitalWaveformWrite(self, dodata, timeout=2500):
        _data_hdo(self._task, dodata, timeout)
        
    @is_running
    def counterRead(self, samples, timeout=2500):
        return _data_ci(self._task, samples, timeout)
    
    @is_running
    def pwmWrite(self, count):
        return _data_pwm(self._task, count)
    
    @is_running
    def encoderRead(self, samples, timeout=2500):
        if "Encoder" not in self._chnum.keys():
            self._chnum["Encoder"] = _get_channel_num(self._task, "Encoder")
        return _data_ai(self._task, samples, self._chnum["Encoder"])
    
    @is_running
    def temperatureRead(self):
        if "AI" not in self._chnum.keys():
            self._chnum["AI"] = _get_channel_num(self._task, "AI")
        return _data_temperature(self._task, self._chnum["AI"])



























    
    
    
    
    
    
    