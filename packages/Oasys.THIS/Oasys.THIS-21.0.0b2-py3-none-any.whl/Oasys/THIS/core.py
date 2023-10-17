import os
import subprocess
import time
import Oasys.gRPC


_connection = None
_debug      = False


def start(abspath, args=None, port=50052, memory=25, license=None, debug=False):
    if debug:
        print("Starting {}, listening on port {}".format(abspath, port))

    environ = os.environ.copy()
    if license:
        environ[ARUP_LICENSE_PATH] = license

    subprocess.Popen( [abspath, "-grpc={}".format(port)], env=environ)

# Sleep to give time for T/HIS to start
    time.sleep(5)

    return connect(port, memory, 'localhost', debug)


def connect(port=50052, memory=25, hostname='localhost', debug=False):
    if debug:
        print("Called connect with port {} and memory {}".format(port, memory))

    Oasys.THIS._debug      = debug
    Oasys.THIS._connection = Oasys.gRPC.Connection("T/HIS", port, memory, hostname, debug)
    return Oasys.THIS._connection


def disconnect(connection):
    if Oasys.THIS._debug:
        print("Called disconnect")

    connection.finalise()
    Oasys.THIS._connection = None


def terminate(connection):
    if Oasys.THIS._debug:
        print("Called terminate")

    connection.terminate()
    Oasys.THIS._connection = None


def createInstance(t, h):
# Classes in T/HIS
    if t == "Colour":
        instance = object.__new__(Oasys.THIS.Colour)
    elif t == "Component":
        instance = object.__new__(Oasys.THIS.Component)
    elif t == "Curve":
        instance = object.__new__(Oasys.THIS.Curve)
    elif t == "Datum":
        instance = object.__new__(Oasys.THIS.Datum)
    elif t == "Entity":
        instance = object.__new__(Oasys.THIS.Entity)
    elif t == "Graph":
        instance = object.__new__(Oasys.THIS.Graph)
    elif t == "Group":
        instance = object.__new__(Oasys.THIS.Group)
    elif t == "Include":
        instance = object.__new__(Oasys.THIS.Include)
    elif t == "LineStyle":
        instance = object.__new__(Oasys.THIS.LineStyle)
    elif t == "LineWidth":
        instance = object.__new__(Oasys.THIS.LineWidth)
    elif t == "Model":
        instance = object.__new__(Oasys.THIS.Model)
    elif t == "Operate":
        instance = object.__new__(Oasys.THIS.Operate)
    elif t == "Options":
        instance = object.__new__(Oasys.THIS.Options)
    elif t == "Page":
        instance = object.__new__(Oasys.THIS.Page)
    elif t == "Read":
        instance = object.__new__(Oasys.THIS.Read)
    elif t == "Symbol":
        instance = object.__new__(Oasys.THIS.Symbol)
    elif t == "UnitSystem":
        instance = object.__new__(Oasys.THIS.UnitSystem)
    elif t == "Units":
        instance = object.__new__(Oasys.THIS.Units)
    elif t == "Utils":
        instance = object.__new__(Oasys.THIS.Utils)
    elif t == "Workflow":
        instance = object.__new__(Oasys.THIS.Workflow)

# Generic object
    elif t == "ItemObject":
        instance = object.__new__(Oasys.THIS.ItemObject)

# Unsupported
    else:
        raise NotImplementedError("Instance type '{}' not implemented".format(t))

    instance.__dict__['_handle']  = h;
    instance.__dict__['_objtype'] = t;

    return instance

