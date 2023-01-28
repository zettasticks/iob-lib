#!/usr/bin/env python3
import os
import re

import iob_colors
from latex import write_table

def params_vh(params, top_module, out_dir):
    file2create = open(f"{out_dir}/{top_module}_params.vh", "w")
    file2create.write("//This file was generated by script mk_configuration.py\n")
    core_prefix = f"{top_module}_".upper()
    for parameter in params:
        if parameter['type'] in ['P','F']:
            p_name = parameter['name'].upper()
            file2create.write(f"\n\tparameter {p_name} = `{core_prefix}{p_name},")
    file2create.close()
    file2create = open(f"{out_dir}/{top_module}_params.vh", "rb+")
    file2create.seek(-1, os.SEEK_END)
    file2create.write(b'\n')
    file2create.close()

    file2create = open(f"{out_dir}/{top_module}_inst_params.vh", "w")
    file2create.write("//This file was generated by script mk_configuration.py\n")
    core_prefix = f"{top_module}_".upper()
    for parameter in params:
        if parameter['type'] in ['P','F']:
            p_name = parameter['name'].upper()
            file2create.write(f"\n\t.{p_name}(`{core_prefix}{p_name}),")
    file2create = open(f"{out_dir}/{top_module}_inst_params.vh", "rb+")
    file2create.seek(-1, os.SEEK_END)
    file2create.write(b'\n')
    file2create.close()

def conf_vh(macros, top_module, out_dir):
    file2create = open(f"{out_dir}/{top_module}_conf.vh", "w")
    file2create.write("//This file was generated by script mk_configuration.py\n\n")
    core_prefix = f"{top_module}_".upper()
    fname = f"{core_prefix}CONF"
    file2create.write(f"`ifndef VH_{fname}_VH\n")
    file2create.write(f"`define VH_{fname}_VH\n\n")
    for macro in macros:
        #Only insert macro if its is not a bool define, and if so only insert it if it is true
        if macro['type'] != 'D':
            m_name = macro['name'].upper()
            m_default_val = macro['val']
            file2create.write(f"`define {core_prefix}{m_name} {m_default_val}\n")
    file2create.write(f"\n`endif // VH_{fname}_VH\n")

def conf_h(macros, top_module, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    file2create = open(f"{out_dir}/{top_module}_conf.h", "w")
    file2create.write("//This file was generated by script mk_configuration.py\n\n")
    core_prefix = f"{top_module}_".upper()
    fname = f"{core_prefix}CONF"
    file2create.write(f"#ifndef H_{fname}_H\n")
    file2create.write(f"#define H_{fname}_H\n\n")
    for macro in macros:
        #Only insert macro if its is not a bool define, and if so only insert it if it is true
        if macro['type'] != 'D':
            m_name = macro['name'].upper()
            # Replace any Verilog specific syntax by equivalent C syntax
            m_default_val = re.sub("\d+'h","0x",macro['val'])
            file2create.write(f"#define {m_name} {str(m_default_val).replace('`','')}\n") #Remove Verilog macros ('`')
    file2create.write(f"\n#endif // H_{fname}_H\n")

    file2create.close()

def config_build_mk(meta_data, build_dir):
    file2create = open(f"{build_dir}/config_build.mk", "w")
    file2create.write("#This file was generated by script mk_configuration.py\n\n")
    file2create.write(f"NAME={meta_data['name']}\n")
    file2create.write(f"VERSION={meta_data['version']}\n")
    file2create.write(f"BUILD_DIR_NAME={build_dir.split('/')[-1]}\n")
    file2create.write(f"FLOWS={meta_data['flows']}\n\n")

    file2create.close()


# This function append a list of flows to the existing config_build.mk file
# Usually called by submodules that have flows not contained in the top core/system
#flows_list:  list of flows of module
#flows_filter: list of flows that should be appended if they exist in flows_list
#build_dir: build directory containing config_build.mk
def append_flows_config_build_mk(flows_list, flows_filter, build_dir):
    flows2append=""
    for flow in flows_filter:
        if flow in flows_list: flows2append += f"{flow} "

    if not flows2append: return
    file = open(f"{build_dir}/config_build.mk", "a")
    file.write(f"FLOWS+={flows2append}\n\n")
    file.close()

def append_defines_config_build_mk(defines, build_dir):
    file = open(f"{build_dir}/config_build.mk", "a")

    for macro in defines:
        if macro['type'] == 'D':
            d_name = macro['name'].upper()
            d_val = macro['val']
            file.write(f"{d_name} ?= {d_val}\n")
            file.write(f"ifeq ($({d_name}),1)\n")
            file.write(f"DEFINES+= -D{d_name}\n")
            file.write(f"endif\n\n")

    file.close()

# Generate TeX table of confs
def generate_confs_tex(confs, out_dir):
    tex_table = []
    for conf in confs:
        tex_table.append([conf['name'].replace('_','\_'), conf['type'], conf['min'], conf['val'].replace('_','\_'), conf['max'], conf['descr'].replace('_','\_')])

    write_table(f"{out_dir}/confs",tex_table)


def config_for_board(board, build_dir, confs):
    available_boards = {\
        'CYCLONEV-GT-DK':{'BAUD':'115200', 'FREQ':'50000000', 'MEM_NO_READ_ON_WRITE':'1', 'DDR_DATA_W':'32', 'DDR_ADDR_W':'30'}, 
        'AES-KU040-DB-G':{'BAUD':'115200', 'FREQ':'100000000', 'MEM_NO_READ_ON_WRITE':'0', 'DDR_DATA_W':'32', 'DDR_ADDR_W':'30'}
        }
    if board not in available_boards.keys(): 
        sim_conf = {'BAUD':'3000000', 'FREQ':'100000000', 'MEM_NO_READ_ON_WRITE':'0', 'DDR_DATA_W':'32', 'DDR_ADDR_W':'24'}
        print(f"{iob_colors.INFO}Board name is not in the available boards.\nDefaulting to the simulation configuration.{iob_colors.ENDC}")
        edit_config_for_board(confs, sim_conf)
    else:
        for key in available_boards.keys():
            if board == key:
                print(f"{iob_colors.INFO}Configuring IP core to run in {board}.{iob_colors.ENDC}")
                edit_config_for_board(confs, available_boards[key])

    file = open(f"{build_dir}/config_build.mk", "a")
    file.write(f"BOARD={board}\n")
    file.close()


def edit_config_for_board(confs, board):
    edit_confs = [ \
        {'name':'BAUD', 'type':'M', 'val':board['BAUD'], 'min':'1', 'max':'NA', 'descr':"UART baud rate"},
        {'name':'FREQ', 'type':'M', 'val':board['FREQ'], 'min':'1', 'max':'NA', 'descr':"System clock frequency"},
        {'name':'MEM_NO_READ_ON_WRITE', 'type':'M', 'val':board['MEM_NO_READ_ON_WRITE'], 'min':'0', 'max':'1', 'descr':"Disable simultaneous read and writes to RAM."},
        {'name':'DDR_DATA_W', 'type':'M', 'val':board['DDR_DATA_W'], 'min':'1', 'max':'32', 'descr':"DDR data bus width"},
        {'name':'DDR_ADDR_W', 'type':'M', 'val':board['DDR_ADDR_W'], 'min':'1', 'max':'32', 'descr':"DDR address bus width"},
    ]
    for edit_conf in edit_confs:
        for conf in confs:
            if edit_conf['name']==conf['name']:
                conf['val'] = edit_conf['val']
                break
        else: confs.append(edit_conf)