
# webui_lib Library 2.4.0
#
# http://webui.me
# https://github.com/webui-dev/python-webui
#
# Copyright (c) 2020-2023 Hassan Draga.
# Licensed under MIT License.
# All rights reserved.
# Canada.


import os
import platform
import sys
import ctypes
from ctypes import *
import shutil


webui_lib = None
webui_path = os.path.dirname(__file__)
PTR_CHAR = ctypes.POINTER(ctypes.c_char)
PTR_PTR_CHAR = ctypes.POINTER(PTR_CHAR)


# Scripts Runtime
class browser:
    NoBrowser:int = 0 # No web browser
    any:int = 1 # Default recommended web browser
    chrome:int = 2 # Google Chrome
    firefox:int = 3 # Mozilla Firefox
    edge:int = 4 # Microsoft Edge
    safari:int = 5 # Apple Safari
    chromium:int = 6 # The Chromium Project
    opera:int = 7 # Opera Browser
    brave:int = 8 # The Brave Browser
    vivaldi:int = 9 # The Vivaldi Browser
    epic:int = 10 # The Epic Browser
    yandex:int = 11 # The Yandex Browser
    ChromiumBased:int = 12 # 12. Any Chromium based browser


# event
class event:
    window = 0
    event_type = 0
    element = ""
    event_num = 0
    bind_id = 0


# JavaScript
class javascript:
    error = False
    response = ""


# Scripts Runtime
class runtime:
    none = 0
    deno = 1
    nodejs = 2


# The window class
class window:


    window = 0
    window_id = ""
    c_events = None
    cb_fun_list = {}


    def __init__(self):
        global webui_lib
        try:
            # Load webui_lib Shared Library
            _load_library()
            # Check library if correctly loaded
            if webui_lib is None:
                print(
                    'Please download the latest webui_lib lib from https://webui.me')
                sys.exit(1)
            # Create new webui_lib window
            webui_wrapper = None
            webui_wrapper = webui_lib.webui_new_window
            webui_wrapper.restype = c_size_t
            self.window = c_size_t(webui_wrapper())
            # Get the window unique ID
            self.window_id = str(self.window)
            # Initializing events() to be used by
            # webui_lib library as a callback
            py_fun = ctypes.CFUNCTYPE(
                ctypes.c_void_p, # RESERVED
                ctypes.c_size_t, # window
                ctypes.c_uint, # event type
                ctypes.c_char_p, # element
                ctypes.c_size_t, # event number
                ctypes.c_uint) # Bind ID
            self.c_events = py_fun(self._events)
        except OSError as e:
            print(
                "webui_lib Exception: %s" % e)
            sys.exit(1)


    # def __del__(self):
    #     global webui_lib
    #     if self.window is not None and webui_lib is not None:
    #         webui_lib.webui_close(self.window)


    def _events(self, window: ctypes.c_size_t,
               event_type: ctypes.c_uint,
               _element: ctypes.c_char_p,
               event_number: ctypes.c_longlong,
               bind_id: ctypes.c_uint):
        element = _element.decode('utf-8')
        if self.cb_fun_list[bind_id] is None:
            print('webui_lib error: Callback is None.')
            return
        # Create event
        e = event()
        e.window = self # e.window should refer to this class
        e.event_type = int(event_type)
        e.element = element
        e.event_num = event_number
        e.bind_id = bind_id
        # User callback
        cb_result = self.cb_fun_list[bind_id](e)
        if cb_result is not None:
            cb_result_str = str(cb_result)
            cb_result_encode = cb_result_str.encode('utf-8')
            # Set the response
            webui_lib.webui_interface_set_response(window, event_number, cb_result_encode)


    # Bind a specific html element click event with a function. Empty element means all events.
    def bind(self, element, func):
        global webui_lib
        if self.window == 0:
            _err_window_is_none('bind')
            return
        if webui_lib is None:
            _err_library_not_found('bind')
            return
        # Bind
        bindId = webui_lib.webui_interface_bind(
            self.window,
            element.encode('utf-8'),
            self.c_events)
        # Add CB to the list
        self.cb_fun_list[bindId] = func


    # Show a window using a embedded HTML, or a file. If the window is already opened then it will be refreshed.
    def show(self, content="<html></html>", browser:int=browser.ChromiumBased):
        global webui_lib
        if self.window == 0:
            _err_window_is_none('show')
            return
        if webui_lib is None:
            _err_library_not_found('show')
            return
        # Show the window
        webui_lib.webui_show_browser(self.window, content.encode('utf-8'), ctypes.c_uint(browser))


    # Chose between Deno and Nodejs runtime for .js and .ts files.
    def set_runtime(self, rt=runtime.deno):
        global webui_lib
        if self.window == 0:
            _err_window_is_none('set_runtime')
            return
        if webui_lib is None:
            _err_library_not_found('set_runtime')
            return
        webui_lib.webui_set_runtime(self.window, 
                        ctypes.c_uint(rt))


    # Close the window.
    def close(self):
        global webui_lib
        if webui_lib is None:
            _err_library_not_found('close')
            return
        webui_lib.webui_close(self.window)


    def is_shown(self):
        global webui_lib
        if webui_lib is None:
            _err_library_not_found('is_shown')
            return
        r = bool(webui_lib.webui_is_shown(self.window))
        return r


    def get_str(self, e: event, index: c_size_t = 0) -> str:
        global webui_lib
        if webui_lib is None:
            _err_library_not_found('get_str')
            return
        c_res = webui_lib.webui_interface_get_string_at
        c_res.restype = ctypes.c_char_p
        data = c_res(self.window,
                    ctypes.c_uint(e.event_num),
                    ctypes.c_uint(index))
        decode = data.decode('utf-8')
        return decode


    def get_int(self, e: event, index: c_size_t = 0) -> int:
        global webui_lib
        if webui_lib is None:
            _err_library_not_found('get_str')
            return
        c_res = webui_lib.webui_interface_get_int_at
        c_res.restype = ctypes.c_longlong
        data = c_res(self.window,
                    ctypes.c_uint(e.event_num),
                    ctypes.c_uint(index))
        return data
    

    def get_bool(self, e: event, index: c_size_t = 0) -> bool:
        global webui_lib
        if webui_lib is None:
            _err_library_not_found('get_str')
            return
        c_res = webui_lib.webui_interface_get_bool_at
        c_res.restype = ctypes.c_bool
        data = c_res(self.window,
                    ctypes.c_uint(e.event_num),
                    ctypes.c_uint(index))
        return data
    

    # Run a JavaScript, and get the response back (Make sure your local buffer can hold the response).
    def script(self, script, timeout=0, response_size=(1024 * 8)) -> javascript:
        global webui_lib
        if self.window == 0:
            _err_window_is_none('script')
            return
        if webui_lib is None:
            _err_library_not_found('script')
            return
        # Create Buffer
        buffer = ctypes.create_string_buffer(response_size)
        buffer.value = b""
        # Create a pointer to the buffer
        buffer_ptr = ctypes.pointer(buffer)
        # Run JavaScript
        status = bool(webui_lib.webui_script(self.window, 
            ctypes.c_char_p(script.encode('utf-8')), 
            ctypes.c_uint(timeout), buffer_ptr,
            ctypes.c_uint(response_size)))
        # Initializing Result
        res = javascript()
        res.data = buffer.value.decode('utf-8')
        res.error = not status
        return res


    # Run JavaScript quickly with no waiting for the response
    def run(self, script):
        global webui_lib
        if self.window == 0:
            _err_window_is_none('run')
            return
        if webui_lib is None:
            _err_library_not_found('run')
            return
        # Run JavaScript
        webui_lib.webui_run(self.window, 
            ctypes.c_char_p(script.encode('utf-8')))


def _get_architecture() -> str:
    arch = platform.machine()
    if arch in ['x86_64', 'AMD64', 'amd64']:
        return 'x64'
    elif arch in ['aarch64', 'ARM64', 'arm', 'arm64']:
        return 'arm64'
    else:
        return arch


def _get_library_path() -> str:
    global webui_path
    arch = _get_architecture()
    if platform.system() == 'Darwin':
        file = f'/webui-macos-clang-{arch}/webui-2.dylib'
    elif platform.system() == 'Windows':
        file = f'\\webui-windows-msvc-{arch}\\webui-2.dll'
    elif platform.system() == 'Linux':
        file = f'/webui-linux-gcc-{arch}/webui-2.so'
    else:
        return ""
    path = os.getcwd() + file
    if os.path.exists(path):
        return path
    path = webui_path + file
    if os.path.exists(path):
        return path
    return path


# Load webui_lib Dynamic Library
def _load_library():
    global webui_lib
    global webui_path
    if webui_lib is not None:
        return
    if platform.system() == 'Darwin':
        webui_lib = ctypes.CDLL(_get_library_path())
        if webui_lib is None:
            print(
                "webui_lib error: Failed to load webui_lib lib.")
    elif platform.system() == 'Windows':
        if sys.version_info.major==3 and sys.version_info.minor<=8:
            os.chdir(os.getcwd())
            os.add_dll_directory(os.getcwd())
            webui_lib = ctypes.CDLL(_get_library_path())
        else:
            os.chdir(os.getcwd())
            os.add_dll_directory(os.getcwd())
            webui_lib = cdll.LoadLibrary(_get_library_path())
        if webui_lib is None:
            print("webui_lib error: Failed to load webui_lib lib.")
    elif platform.system() == 'Linux':
        webui_lib = ctypes.CDLL(_get_library_path())
        if webui_lib is None:
            print("webui_lib error: Failed to load webui_lib lib.")
    else:
        print("webui_lib error: Unsupported OS")


# Close all opened windows. webui_wait() will break.
def exit():
    global webui_lib
    if webui_lib is not None:
        webui_lib.webui_exit()


# Set startup timeout
def set_timeout(second):
    global webui_lib
    if webui_lib is None:
        _load_library()
        if webui_lib is None:
            _err_library_not_found('set_timeout')
            return
    webui_lib.webui_set_timeout(ctypes.c_uint(second))


def is_app_running():
    global webui_lib
    if webui_lib is None:
        _load_library()
        if webui_lib is None:
            _err_library_not_found('is_app_running')
            return
    r = bool(webui_lib.webui_interface_is_app_running())
    return r


# Wait until all opened windows get closed.
def wait():
    global webui_lib
    if webui_lib is None:
        _load_library()
        if webui_lib is None:
            _err_library_not_found('wait')
            return
    webui_lib.webui_wait()
    try:
        shutil.rmtree(os.getcwd() + '/__intcache__/')
    except OSError:
        pass


# 
def _err_library_not_found(f):
    print('webui_lib ' + f + '(): Library Not Found.')


#
def _err_window_is_none(f):
    print('webui_lib ' + f + '(): window is None.')


# Set the path to the webui_lib prebuilt dynamic lib
def set_library_path(Path):
    global webui_path
    webui_path = Path
