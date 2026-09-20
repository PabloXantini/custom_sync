import time

_TAGS = {
    "MSG": ">",
    "WARN": "!",
    "ERROR": "X",
    "FATAL": ":c"
}

def _log(tag:str, text:str):
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{_TAGS[tag]} [{ts}] : {text}")
    
def msg(text:str):
    _log("MSG", text)

def warn(text:str):
    _log("WARN", text)

def error(text:str):
    _log("ERROR", text)

def fatal(text:str):
    _log("FATAL", text)