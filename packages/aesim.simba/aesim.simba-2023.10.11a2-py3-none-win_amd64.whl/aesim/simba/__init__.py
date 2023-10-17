#%% Load modules...
__version__ = "2023.10.11a2"

import pythonnet, clr_loader, os
resources_folder_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),'Resources')

dotnet_folder_name = os.path.join(resources_folder_name,"dotnet")
if os.path.exists(dotnet_folder_name):
    # print("[aesim.simba debug] DOTNET_ROOT=" + dotnet_folder_name )
    os.environ["DOTNET_ROOT"] = dotnet_folder_name

runtime_config_path = os.path.join(resources_folder_name,'Simba.Data.runtimeconfig.json')


def get_required_dotnet_runtime_version(runtime_config_path):
    import json,os
    f = open(runtime_config_path)
    data = json.load(f)
    f.close()
    name = data["runtimeOptions"]["framework"]["name"];
    version = data["runtimeOptions"]["framework"]["version"];
    return (name,version)


try:
    pythonnet.set_runtime(clr_loader.get_coreclr(runtime_config=runtime_config_path))
except Exception as e:
    (name,version) = get_required_dotnet_runtime_version(runtime_config_path)
    print("[aesim.simba debug] Impossible to load dotnet " + name + " version: " + version )
    print("[aesim.simba debug] dotnet_folder_name " + dotnet_folder_name + " (exist:"+ str(os.path.exists(dotnet_folder_name))+")")
    raise e 


import clr,sys

sys.path.append(resources_folder_name)
simba_dll_filepath = os.path.join(resources_folder_name,'Simba.Data.dll')
clr.AddReference(simba_dll_filepath)

from Simba.Data.Repository import ProjectRepository, JsonProjectRepository
from Simba.Data import License, Design, Circuit, DesignExamples, ACSweep, SweepType, Status, Subcircuit, ThermalComputationMethodType, ThermalDataType, ThermalDataSemiconductorType
from Simba.Data.Thermal import ThermalData,IV_T,EI_VT
from System import Array
import Simba.Data

Simba.Data.FunctionsAssemblyResolver.RedirectAssembly()

import Python.Runtime
Python.Runtime.PyObjectConversions.RegisterEncoder(Simba.Data.DoubleArrayPythonEncoder.Instance);
Python.Runtime.PyObjectConversions.RegisterEncoder(Simba.Data.Double2DArrayPythonEncoder.Instance);
Python.Runtime.PyObjectConversions.RegisterEncoder(Simba.Data.ParameterToPythonEncoder.Instance);
Python.Runtime.PyObjectConversions.RegisterEncoder(Simba.Data.DoubleArrayPythonEncoder.Instance);
Python.Runtime.PyObjectConversions.RegisterDecoder(Simba.Data.PythonToParameterDecoder.Instance);
Python.Runtime.PyObjectConversions.RegisterDecoder(Python.Runtime.Codecs.IterableDecoder.Instance);
Python.Runtime.PyObjectConversions.RegisterDecoder(Python.Runtime.Codecs.ListDecoder.Instance);


if os.environ.get('SIMBA_DEPLOYMENT_KEY') is not None:
    License.Activate(os.environ.get('SIMBA_DEPLOYMENT_KEY'))