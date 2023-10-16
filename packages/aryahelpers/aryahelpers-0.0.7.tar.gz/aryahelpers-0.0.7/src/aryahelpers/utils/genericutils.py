"""Configuration"""

# ================================================
## Generic utilities functions
# ================================================
import sys, os, json, pickle
import gzip, zipfile
import pandas as pd
import numpy as np
import re, time
import wx
import inspect
import logging
import xlsxwriter
from io import StringIO
from datetime import datetime, timedelta
from copy import copy, deepcopy
from concurrent.futures import ThreadPoolExecutor
from undecorated import undecorated
from ..config import BUCKET_DICT
LOGGER = logging.getLogger(__name__)
# ================================================

# ==================================
# Decorator to compute elapsed time for any function
# ==================================
def elapsedTime(func):
    """"This is a decorator to compute elapsed time for any function.
    Add arguments inside the ``calcTime()`` func if the target func uses arguments.
    The ``print_el_time`` parameter controls the printing and it should be present in the target 
    function. Else, by default elapsed time will be printed after that function call.
    """
    def calcTime(*args, **kwargs):
        # storing time before function execution
        st_time = time.monotonic()
        ret_val = func(*args, **kwargs)
        end_time = time.monotonic()
        el_time = timedelta(seconds=end_time - st_time)  # find elapsed time
        argsDict = {k: v for k, v in kwargs.items()}
        if 'print_el_time' in argsDict:
            if argsDict['print_el_time']:
                print('Elapsed time for <{0}> func is: {1}'.format(func.__name__, el_time))
        else:
            print('Elapsed time for <{0}> func is: {1}'.format(func.__name__, el_time))
        return ret_val
    return calcTime

"""
# Quick helps on decorated functions
# from undecorated import undecorated ##[for stripping decorator from a function]
%load inspect.getsource(function_name)
# =================
For loading the base function that is decorated
%load inspect.getsource(base_func_name.__closure__[0].cell_contents)
%load inspect.getsource(undecorated(base_func_name))
help(undecorated(base_func_name)) #for console help
# =================
func_2 = base_func_name.__closure__[0].cell_contents
func_2 = undecorated(base_func_name)
"""

# ==================================
# Function for file import/save
# ==================================
def get_file_path(**kwargs):
    """
    Get the file path through a selection prompt.
    
    Returns
    -------
    The full file path.
    """
    argsDict = {k: v for k, v in kwargs.items()}
    wx_app = wx.App(None)
    wx_style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, style=wx_style, **argsDict)
    if dialog.ShowModal() == wx.ID_OK:
        file_path = dialog.GetPath()
    else:
        file_path = None
    dialog.Destroy()
    return file_path


def import_file(file_path=None, msg_str='Enter the file path', *args, **kwargs):
    """
    Imports a file (json, dict, list, dataframe etc.) from a given path. The accepted formats are: 
    '.csv','.xlsx','.p','.zip','.gz','.json','.txt'. Also, imports from a '.zip' file, 
    having multiple .csv/.xlsx files is supported.
    
    Parameters
    ----------
    file_path : str or bool, optional
        The full path of the file to import. if ``None`` or ``True``, the function will ask for the file 
        path in a dialogue box.
    msg_str: str, default ``None``
        The file selection prompt message.
    compression: str, default 'infer'
        The file compression type. Valid options are: {'p_zip', 'p_gzip', 'infer', 'gzip', 'bz2', 'zip', 'xz', None}.
        The types 'p_zip' and 'p_gzip' mean 'pickle zip' and 'pickle gzip' files respectively, while others are
        <pd.read_csv> permissible 'compression' options.
    *args/**kwargs
        The required arguments for <pd.read_csv> or <pd.read_excel> functions.

    Returns
    -------
    The imported dataframe or dictionary.
    """
    # =======================
    getPath, getFile = deepcopy(file_path), None
    # Return the path itself if it is not str, bool or None -- dataframe/Series/list etc.
    if not isinstance(getPath, (type(None), bool, str, bytes)):
        return getPath
    if isinstance(getPath, str) and not os.path.exists(getPath):
        return getPath
    if getPath in [None, True]:
        getPath = get_file_path() if msg_str is None else get_file_path(message=msg_str)
    if getPath in [None, False]:
        return getFile
    # =======================
    argsDict = {k: v for k, v in kwargs.items()}
    fileType = os.path.splitext(getPath)[1]
    # Recursive import for zip file containing multiple files
    if (fileType == '.zip') and (kwargs.get("compression") not in ['p_zip', 'p_gzip']):
        getFile = dict()
        zip_file = zipfile.ZipFile(getPath, 'r', compression=zipfile.ZIP_DEFLATED)
        filesList = zipfile.ZipFile.namelist(zip_file)
        for idx in filesList:
            idxType = os.path.splitext(idx)[1]
            getFile[idx] = json.loads(zip_file.read(idx)) if idxType == '.json' else \
                import_file(file_path=zip_file.read(idx), *args, **kwargs)
        if all([getFile[key] is None for key in getFile]):
            getFile = None
    
    # =======================
    # Individual file imports
    # =======================
    excludeType = ['.json', '.txt', '.p', '.pkl', '.pickle', '.zip', '.gzip']
    # Import '.csv'
    funcArgs = dict(inspect.signature(pd.read_csv).parameters)
    subArgsDict = {x: argsDict[x] for x in argsDict.keys() if x in funcArgs.keys()}
    if (getFile is None) and (fileType not in excludeType):
        try:
            getFile = pd.read_csv(getPath, **subArgsDict) 
        except Exception:
            pass
    if (getFile is None) and (fileType not in excludeType):
        try:
            getFile = pd.read_csv(StringIO(str(getPath, 'utf-8')), **subArgsDict)
        except Exception:
            pass
    # +++++++++++++++++
    # Import '.xlsx'
    funcArgs = dict(inspect.signature(pd.read_excel).parameters)
    subArgsDict = {x: argsDict[x] for x in argsDict.keys() if x in funcArgs.keys()}
    if (getFile is None) and (fileType not in excludeType):   
        try:
            getFile = pd.read_excel(getPath, **subArgsDict)
        except Exception:
            pass
    # +++++++++++++++++
    # Import '.p','.pkl','.pickle' file
    if getFile is None:
        try:
            getFile = pickle.load(open(getPath, "rb"))
        except Exception:
            pass
    # +++++++++++++++++
    # Import 'p_zip' file
    if getFile is None:
        try:
            zip_file = zipfile.ZipFile(getPath, 'r', compression=zipfile.ZIP_DEFLATED)
            getFile = pickle.loads(zip_file.read(zipfile.ZipFile.namelist(zip_file)[0]))
            zip_file.close()
        except Exception:
            pass
    # +++++++++++++++++
    # Import 'p_gzip' file
    if getFile is None:
        try:
            gz_file = gzip.GzipFile(getPath, 'rb')
            getFile = pickle.loads(gz_file.read())
            gz_file.close()
        except Exception:
            pass
    # +++++++++++++++++
    # Import '.json' file
    if (getFile is None) and (fileType == '.json'):
        try:
            with open(getPath) as json_file:
                getFile = json.load(json_file)
            json_file.close()
        except Exception:
            pass
    # +++++++++++++++++
    # Import '.txt' file
    if (getFile is None) and (fileType == '.txt'):
        try:
            with open(getPath) as text_file:
                getFile = text_file.read()
            text_file.close()
        except Exception:
            pass
    # +++++++++++++++++
    # Import '.pkl','.p.zip','.p.gzip' files
    if getFile is None:
        try:
            getFile = pd.read_pickle(getPath)
        except Exception:
            pass

    # =======================
    # Further formatting
    # =======================
    if isinstance(getFile, dict) and (len(getFile) == 1):
        getFile = getFile[list(getFile.keys())[0]]
    if isinstance(getFile,pd.DataFrame):
        getFile.index.name = None
        # Remove 'Unnamed' columns
        unnamed_cols = getFile.columns[getFile.columns.str.contains(
            'unnamed', flags=re.IGNORECASE, regex=True)].tolist()
        getFile = getFile.drop(columns=unnamed_cols)
    return getFile


def save_files(fileToSave, file_path=None, file_name=None, save_file_type=None, file_name_suffix='filecount', **kwargs):
    """
    Saves a file (``dataframe``, ``series`` or ``dict`` of ``dataframes``/``series``) to the specified path.
    In case of a dict, the components will be saved in different sheets of an excel file or as a pickled zip file.

    Parameters
    ----------
    fileToSave : ``dataframe`` or ``dict``
        The file to save.
    file_path :  str, bool, default ``None``
        The full path of the file to import. if ``None`` or ``True``, the file will be saved in working 
        directory. If ``False``, the function will just return ``False`` without saving anything.
    file_name : str, default ``None``
        The save file name. if ``None``, the file will be saved with the name: 'saved_file.<file_type>'
    file_name_suffix : str, default 'filecount'
        The suffix to add with the file name. This param is helpful if `<save_files(...)>` is run multiple
        times with the same `file_path` and `file_name`, e.g. during codes testing etc. The options are:

        - 'filecount' : incremental suffix based on count of the files with name `file_name` in `file_path`.
        It is the default value.
        - 'datetime' : current date and time str is used as suffix.
        - In case of any other str passed, it will be simply added after 'file_name'.
        
    save_file_type : 
        The type to which the file is to be saved. Valid options are: {'.csv', '.xlsx', '.p', '.zip', '.gz', 
        'p_zip','p_gzip','.pkl','.pickle','.json','.txt'}. If ``None``, then a '.csv' will be used to save a 
        ``dataframe`` and '.xlsx' will be used to save the components of a ``dict``.
    **kwargs
        The valid arguments for <pd.DataFrame.to_csv> or <pd.DataFrame.to_excel>.

    Returns
    -------
    The function returns ``True`` if file save is a success, else ``False``.
    """
    # =======================
    # Obtain file save path and save name
    if file_path is False:
        return False
    file_path_ = os.getcwd() if file_path in [True, None] else file_path
    file_name_ = 'saved_file_' + datetime.today().strftime('%d%b%y-%H%M%S') if file_name is None else file_name
    try:
        os.makedirs(file_path_)
    # except OSError: pass
    except Exception:
        pass
    # =================
    # Set the file suffix
    if file_name_suffix == 'datetime':
        name_suffix_ = '_' + datetime.today().strftime('%d%b%y-%H%M%S')
    # Finally get file suffix, based on filecount in 'file_path_'
    elif file_name_suffix == 'filecount':
        name_suffix_ = ''
        list_files, sfx_clist, checkFlag = os.listdir(file_path_), [], False
        for f in list_files:
            if file_name_ in f.split('.')[0]:
                checkFlag = True
                sfx_val = f.split('.')[0].split(file_name_)[-1].split('_')[-1]
                try:
                    sfx_clist.append(int(sfx_val))
                except Exception:
                    pass
        try:
            name_suffix_ = '_' + str(max(sfx_clist)+1)
        except Exception:
            name_suffix_ = '_1'
        if not checkFlag:
            name_suffix_ = ''  # file with name substr: `file_name_` not present in 'file_path_'
    else:
        name_suffix_ = str(file_name_suffix)  # also handles the case: suffix = ''
                                              # careful -- if suffix = '' as it will override existing file
                                              # if present with the same name
    file_name_ = file_name_ + name_suffix_
    
    # =======================
    # Individual files saving
    # =======================
    argsDict = {k: v for k, v in kwargs.items()}
    fileType = '.csv' if (save_file_type is None) and (not isinstance(fileToSave, dict)) else save_file_type
    # Save as '.csv'
    funcArgs = dict(inspect.signature(pd.DataFrame.to_csv).parameters)
    subArgsDict = {x: argsDict[x] for x in argsDict.keys() if x in funcArgs.keys()}
    if fileType == '.csv':
        try:
            fileToSave.to_csv(os.path.join(file_path_, file_name_+fileType), **subArgsDict)
            return True
        except Exception:
            pass
    # +++++++++++++++++
    # Save as '.zip'
    if fileType == '.zip':
        try:
            compression_opts = dict(method='zip', archive_name=file_name_+'.csv')  
            fileToSave.to_csv(os.path.join(file_path_, file_name_+fileType),
                              compression=compression_opts, **subArgsDict)
            return True
        except Exception:
            pass
        # For saving components of a dict in one zip folder
        funcArgs = dict(inspect.signature(pd.DataFrame.to_csv).parameters)
        subArgsDict = {x: argsDict[x] for x in argsDict.keys() if x in funcArgs.keys()}
        try:
            zip_file = zipfile.ZipFile(os.path.join(file_path_, file_name_+'.zip'), 'w',
                                       compression=zipfile.ZIP_DEFLATED)
            for key in fileToSave: 
                zip_file.writestr(key+'.csv', fileToSave[key].to_csv(**subArgsDict), zipfile.ZIP_DEFLATED)
            zip_file.close()
            return True
        except Exception:
            pass
    # +++++++++++++++++
    # Save as '.xlsx'
    funcArgs = dict(inspect.signature(pd.DataFrame.to_excel).parameters)
    subArgsDict = {x: argsDict[x] for x in argsDict.keys() if x in funcArgs.keys()}
    if fileType == '.xlsx':
        try: 
            fileToSave.to_excel(os.path.join(file_path_, file_name_+fileType), **subArgsDict)
            return True
        except Exception:
            pass
    # +++++++++++++++++
    # Save as Save as pickled zip
    funcArgs = dict(inspect.signature(pickle.dumps).parameters)
    subArgsDict = {x: argsDict[x] for x in argsDict.keys() if x in funcArgs.keys()}
    if fileType == 'p_zip':
        try:
            zip_file = zipfile.ZipFile(os.path.join(file_path_, file_name_+'.zip'), 'w',
                                       compression=zipfile.ZIP_DEFLATED)
            zip_file.writestr(file_name_+'.p', pickle.dumps(fileToSave, **subArgsDict))
                            # Can specify "protocol=pickle.HIGHEST_PROTOCOL" or a no. between 0-5
            zip_file.close()
            return True
        except Exception:
            pass
    # +++++++++++++++++
    # Save dict as gz
    if fileType == '.gz':
        try:
            gz_file = gzip.GzipFile(os.path.join(file_path_, file_name_+fileType), 'wb')
            gz_file.write(pickle.dumps(fileToSave, **subArgsDict))
                            # Can specify "protocol=pickle.HIGHEST_PROTOCOL" or a no. between 0-5
            gz_file.close()
            return True
        except Exception:
            pass
    # +++++++++++++++++
    # Save as '.p' or '.pickle' pickle file
    funcArgs = dict(inspect.signature(pickle.dump).parameters)
    subArgsDict = {x: argsDict[x] for x in argsDict.keys() if x in funcArgs.keys()}
    if fileType in ['.p', '.pickle']:
        try:
            pickle.dump(fileToSave, open(os.path.join(file_path_, file_name_+fileType), "wb"), **subArgsDict)  
                            # Can specify "protocol=pickle.HIGHEST_PROTOCOL" or a no. between 0-5
            return True
        except Exception:
            pass
    # +++++++++++++++++
    # Save dataframe as '.pkl' file
    funcArgs = dict(inspect.signature(pd.to_pickle).parameters)
    subArgsDict = {x: argsDict[x] for x in argsDict.keys() if x in funcArgs.keys()}
    if isinstance(fileToSave, pd.DataFrame) and fileType in ['.pkl', 'p_zip', 'p_gzip']:
        try:
            fileToSave.to_pickle(os.path.join(file_path_, file_name_+fileType), **subArgsDict)
                            # Can specify "protocol=pickle.HIGHEST_PROTOCOL" or a no. between 0-5
            return True
        except Exception:
            pass
    # +++++++++++++++++
    # Save as '.json' file
    funcArgs = dict(inspect.signature(json.dump).parameters)
    subArgsDict = {x: argsDict[x] for x in argsDict.keys() if x in funcArgs.keys()}
    if fileType == '.json':
        try:
            json.dump(fileToSave, open(os.path.join(file_path_, file_name_+fileType), 'w'),**subArgsDict)
            return True
        except Exception:
            pass
    # +++++++++++++++++
    # Save as '.txt' file
    if fileType == '.txt':
        try:
            with open(os.path.join(file_path_, file_name_+fileType), 'w') as text_file:
                text_file.write(fileToSave)
            text_file.close()
            return True
        except Exception:
            pass
    # +++++++++++++++++
    # Saving components of a dict
    if isinstance(fileToSave, dict) and fileType is None:
        try:
            dictKeys = list(fileToSave.keys())
            if (len(fileToSave) == 1) and (not isinstance(fileToSave[dictKeys[0]], dict)):
                funcArgs = dict(inspect.signature(pd.DataFrame.to_csv).parameters)
                subArgsDict = {x: argsDict[x] for x in argsDict.keys() if x in funcArgs.keys()}
                fileToSave[dictKeys[0]].to_csv(os.path.join(file_path_, file_name_+'.csv'),**subArgsDict)
            else:
                funcArgs = dict(inspect.signature(pd.DataFrame.to_excel).parameters)
                subArgsDict = {x: argsDict[x] for x in argsDict.keys() if (
                    x in funcArgs.keys()) and (x != 'sheet_name')}
                writer = pd.ExcelWriter(os.path.join(file_path_, file_name_+'.xlsx'))
                for indKey in dictKeys:
                    if not isinstance(fileToSave[indKey], dict):
                        fileToSave[indKey].to_excel(writer, sheet_name =indKey, **subArgsDict)
                    else:
                        save_files(fileToSave=fileToSave[indKey], file_path=file_path_,
                                   file_name=indKey, file_name_suffix=file_name_suffix, **argsDict)
                writer.save()
                # writer.close()
            return True
        except Exception:
            pass
    # =======================
    return False
# ==================================


def __form_boolean_str(key: str, lst: list):
    """This function forms the bool str from `key:['AND','OR','NOT]` and the keywords list: `lst`"""
    ckey = 'OR' if key == 'AND' else 'AND' if key == 'OR' else None  # complement key
    if key == 'NOT':
        lst = [lst]
    form_str = ''
    for kw in lst:
        if isinstance(kw, str):
            form_str += ' {} "{}"'.format(key, kw) if bool(form_str) else '"{}"'.format(kw)
        elif isinstance(kw, list):
            _rec_str = __form_boolean_str(ckey, kw)
            if all([isinstance(v, list) for v in kw]):
                form_str += ' {} ({})'.format(key, _rec_str) if bool(form_str) else _rec_str
            else:
                form_str += ' {} ({})'.format(key, _rec_str) if bool(form_str) else '({})'.format(_rec_str)
        else:
            pass
    if key == 'NOT':
        form_str = 'NOT ' + form_str.replace('None', 'OR')
    return form_str


def append_to_sstr(append_key: str, kwds_dict: dict, base_sstr=None):
    """A wrapper function for appending additional string to a given search string.

    Args:
        append_key (str): The append key: `new_sstr = base_sstr + append key + append_sstr`
            The valid options are: "AND", "OR", "NOT".
        kwds_dict (dict): The dict (len=1) for append kwds list, it's key being one of: "AND", "OR", "NOT".
        base_sstr (str, optional):The base str to which the additional str is to be appended. Defaults to ``None``.
    """
    [_key, _kwlst] = [v[0] for v in zip(*kwds_dict.items())];
    # _apkey = 'AND' if _key=='NOT' else append_key
    append_str = __form_boolean_str(_key, _kwlst)
    if not base_sstr:
        return append_str
    if _key == 'NOT':
        return '{} {} ({})'.format(base_sstr, append_key, append_str)
    return '{} {} {}'.format(base_sstr, append_key, append_str)


def map_processing(func, args, to_unpack=False):
    """Map lambda processing of multiple calls of a func"""
    res = map(lambda p: func(*p), args) if to_unpack else map(func, args)
    return list(res)


def multi_threading(func, args, workers, to_unpack=False):
    """Multithreading execution of a func"""
    with ThreadPoolExecutor(max_workers=workers) as executor:
        res = executor.map(lambda p: func(*p), args) if to_unpack else executor.map(func, args)
    return list(res)


def bucket_numeric_values(numericVal: (int, float), bucketList=[]):
    """Function to bucket large numeric values"""
    # from_pow, to_pow = math.floor(math.log10(numericVal)), math.ceil(math.log10(numericVal))
    if not bucketList:
        bucketList = [v[0] for v in BUCKET_DICT.values()]
    if not numericVal:
        return numericVal
    repl_list = [('K', ''.join(['0']*3)), ('M', ''.join(['0']*6)), ('B', ''.join(['0']*9)), ('\\+', '-np.inf')]
    modif_bucket_dict = {}
    for idx, _item in enumerate(bucketList):
        if not (idx or '-' in _item):
            _item = f'-np.inf--{_item}'
        for tup in repl_list:
            _item = re.sub(tup[0], tup[1], _item)
        modif_bucket_dict[idx] = _item
    # Derive the bucket for 'numericVal'
    for key, bucket in modif_bucket_dict.items():
        bucket_split = bucket.split('-') if '--' not in bucket else bucket.split('--')
        brange = [eval(v) for v in bucket_split]
        if brange[0] <= numericVal < brange[1]:
            return bucketList[key]


def minmax_map(lst: list, map_range=(0, 1), round_digit=None):
    """Map a given list of numbers within `map_range`"""
    minmax_mapped = []
    lst = [v for i, v in enumerate(lst) if isinstance(v, (int, float))]
    if lst:
        map_min, map_max = map_range
        nos_mn, nos_mx = min(lst), max(lst)
        minmax_mapped = [map_min]*len(lst) if map_min == map_max else [
            (x - nos_mn) / (nos_mx - nos_mn) * (map_max - map_min) + map_min for x in lst]
        minmax_mapped = [round(x, round_digit) for i, x in enumerate(minmax_mapped)]
    return minmax_mapped


def distribute_list(lst: list, gen_size=None, round_digit=None):
    """Distribute a list of numbers to generate a new list of given size"""
    distr_list = []
    if lst:
        gen_size = len(lst) if not gen_size else gen_size
        nos_mn, nos_mx = min(lst), max(lst)
        gen_interval = (nos_mx - nos_mn) / (gen_size - 1)
        distr_list = [nos_mn + gen_interval * i for i in range(gen_size)]
        if round_digit is not False:
            distr_list = [round(v, round_digit) for v in distr_list]
    return distr_list


def list_percentiles(lst: list, ptile_range=(0, 50, 100), round_digit=None):
    """Compute percentiles of the given list"""
    lst = [v for v in lst if isinstance(v, (int, float))]
    if not (lst and ptile_range):
        return []
    ptile_range = ptile_range if isinstance(ptile_range, (list, tuple)) else [ptile_range]
    ptiles = [int(p) if p.is_integer() else round(p, round_digit) for p in np.percentile(lst, ptile_range)]
    ptiles = ptiles[0] if len(ptiles) == 1 else ptiles
    return ptiles


# Get dict of func attributes
def get_func_attrs(attrs_dict: dict, func_obj, to_print=True):
    """Returns valid attributes for func: `func_name` from the passed `attrs_dict`.
    The func_obj can accept class too in some cases."""
    # dict of <func_name> (args, default_vals)
    try:
        func_attrs = inspect.signature(undecorated(func_obj)).parameters
        func_attrs = {k: str(v) for k, v in func_attrs.items()}
        for k, v in func_attrs.items():
            assign_v = v.replace("{}=".format(k), '').replace("{}: ".format(k), '') if any(
                re.findall(r'=|:', v)) else "__NON_DEFAULT__"
            try:
                assign_v = eval(assign_v)
            except Exception:
                pass
            func_attrs[k] = assign_v
        # +++++++++++++++++
        if attrs_dict:
            func_attrs = dict(inspect.signature(undecorated(func_obj)).parameters)
            func_attrs = {k: v for k, v in attrs_dict.items() if k in func_attrs.keys()}
    except Exception:
        func_attrs = {}
    if to_print:
        print(json.dumps(func_attrs, indent=4, default=str))
    return func_attrs


def get_obj_attributes(class_obj, is_callable=True, exclude_attrs=[]):
    """Extract custom attributes (not functions or built-in attribute) from an object, e.g. `class`"""
    obj_attrs, all_attrs = {}, dir(class_obj)
    for attr_name in all_attrs:
        if (attr_name.startswith("__") and attr_name.endswith("__")) or attr_name in exclude_attrs:
            continue
        attr_value = getattr(class_obj, attr_name)
        if (is_callable and callable(attr_value)) or not (is_callable or callable(attr_value)):
            obj_attrs[attr_name] = attr_value
    return obj_attrs


def null_handler(obj, ret_val):
    """Return `ret_val` if 'obj' is `None` or empty"""
    if not obj:
        return ret_val
    return obj


def merge_dicts(iter_dicts):
    """Merge iterable (list/tuple) of dicts to a single dict"""
    merged_dict = {}
    [merged_dict.update(d) for d in iter_dicts]
    return merged_dict


def flatten_iterable(iterable, seqtypes=(list, tuple)):
    """This func flattens an arbitrarily nested list/tuple."""
    flattened_item = list(iterable.copy()) if isinstance(iterable, tuple) else iterable.copy()
    try:
        for i, x in enumerate(flattened_item):
            while isinstance(x, seqtypes):    
                flattened_item[i:i+1] = x
                x = flattened_item[i]
    except IndexError:
        pass
    if isinstance(iterable, tuple):
        return tuple(flattened_item)
    return flattened_item
