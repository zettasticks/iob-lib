from build_srcs import lib_module_setup, create_Vheaders, copy_files, module_dependency_setup
import iob_colors
import sys
from pathlib import Path

def lib_sim_setup (module_name):
    
    for mod_path in Path("hardware").rglob(f"{module_name}_tb.v"):
        tb_path = mod_path
        break
    else: sys.exit(f"{iob_colors.FAIL} {module_name} is not a LIB module.{iob_colors.ENDC}")

    hardware_srcs = []
    Vheaders = []
    sim_srcs = []
    lib_dir="."
    lib_module_setup(Vheaders, hardware_srcs, module_name, lib_dir=".", add_sim_srcs=True)
    module_dependency_setup(hardware_srcs, Vheaders, "src", [], lib_dir=".", add_sim_srcs=True)

    #Copy Hw
    if Vheaders: create_Vheaders( "src", Vheaders )
    if hardware_srcs: copy_files( ".", "src", hardware_srcs, '*.v' )
    
    # Copy TB
    copy_files(".", "src", [], f"{module_name}_tb.v", copy_all = True)
    # Copy LIB hw files
    copy_files( "hardware/include", "src", [], '*.vh', copy_all = True )
    
if __name__ == "__main__":
    lib_sim_setup(sys.argv[1])
