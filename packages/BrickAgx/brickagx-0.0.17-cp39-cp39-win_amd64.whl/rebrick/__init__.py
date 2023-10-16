import os
__AGXVERSION__ = "2.36.1.5"
__version__ = "0.0.17"
try:
    import agx
    if agx.__version__ != __AGXVERSION__:
        print(f"This version of brickagx is compiled for AGX {__AGXVERSION__} only and may crash with your {agx.__version__} version, upgrade brickagx or AGX to make sure the versions are suited for eachother")
except:
    print(f"Failed finding AGX Dynamics, have you run setup_env?")
    exit(255)


if "DEBUG_AGXBRICK" in os.environ:
    print(f"#### Using Debug build ####")
    try:
        from .debug.api import *
        from .debug import Core
        from .debug import Math
        from .debug import Physics
        from .debug import Simulation
    except:
        print(f"Failed finding rebrick modules or libraries, did you set PYTHONPATH correctly? Should point to where rebrick directory with binaries are located")
        print(f"Also, make sure you are using the same Python version the libraries were built for.")
        exit(255)
else:
    try:
        from .api import *
        from . import Core
        from . import Math
        from . import Simulation
    except:
        print(f"Failed finding rebrick modules or libraries, did you set PYTHONPATH correctly? Should point to where rebrick directory with binaries are located")
        print(f"Also, make sure you are using the same Python version the libraries were built for.")
        exit(255)
