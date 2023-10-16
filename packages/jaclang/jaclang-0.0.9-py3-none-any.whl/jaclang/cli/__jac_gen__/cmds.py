"""
This is the implementation of the command line interface tool for the
Jac language. It's built with the Jac language via bootstraping and
represents the first such production Jac program.
"""  # 2 1
from __future__ import annotations
from jaclang import jac_purple_import as __jac_import__  # -1 0
from jaclang.core import exec_ctx as _jac_exec_ctx_  # -1 0
from jaclang.core import Object as _jac_Object_  # -1 0
from jaclang.core import make_architype as _jac_make_architype_  # -1 0
import traceback as __jac_traceback__  # -1 0
from jaclang import handle_jac_error as __jac_error__  # -1 0
__jac_import__(target='cli', base_path=__file__)  # 2 6
from cli import cmd_registry as cmd_reg  # 2 6

__jac_import__(target='impl.cmds_impl', base_path=__file__)  # 2 8
from impl.cmds_impl import *  # 2 8

@cmd_reg.register  # 2 10
def run(filename: str):  # 2 11
    try:      # 2 11
        if filename.endswith(".jac"):  # 3 10
            [base, mod] = os.path.split(filename)  # 3 11
            base = './' if not base else base  # 3 11
            mod = mod[:-4]  # 3 11
            __jac_import__(target = mod, base_path = base, override_name = "__main__")  # 3 11
        
        else:  # 3 15
            print("Not a .jac file.")  # 3 16
        
    except Exception as e:      # 2 11
        tb = __jac_traceback__.extract_tb(e.__traceback__)          # 2 11
        __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 2 11
        e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 2 11
        raise e          # 2 11

@cmd_reg.register  # 2 13
def enter(filename: str, entrypoint: str, args: list):  # 2 14
    try:      # 2 14
        if filename.endswith(".jac"):  # 3 23
            [base, mod] = os.path.split(filename)  # 3 24
            base = './' if not base else base  # 3 24
            mod = mod[:-4]  # 3 24
            mod = __jac_import__(target = mod, base_path = base)  # 3 24
            if not mod:  # 3 28
                print('Errors occured while importing the module.')  # 3 29
                return  # 3 30
            
            else:  # 3 32
                (getattr(mod, entrypoint))()  # 3 33
            
        
        else:  # 3 35
            print("Not a .jac file.")  # 3 36
        
    except Exception as e:      # 2 14
        tb = __jac_traceback__.extract_tb(e.__traceback__)          # 2 14
        __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 2 14
        e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 2 14
        raise e          # 2 14

@cmd_reg.register  # 2 16
def test(filename: str):  # 2 17
    try:      # 2 17
        if filename.endswith(".jac"):  # 3 43
            [base, mod] = os.path.split(filename)  # 3 44
            base = './' if not base else base  # 3 44
            mod = mod[:-4]  # 3 44
            mod = __jac_import__(target = mod, base_path = base)  # 3 44
            unittest.TextTestRunner().run(mod.__jac_suite__)  # 3 44
        
        else:  # 3 49
            print("Not a .jac file.")  # 3 50
        
    except Exception as e:      # 2 17
        tb = __jac_traceback__.extract_tb(e.__traceback__)          # 2 17
        __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 2 17
        e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 2 17
        raise e          # 2 17

@cmd_reg.register  # 2 19
def ast_tool(tool: str):  # 2 20
    try:      # 2 20
        from jaclang.utils.lang_tools import AstTool  # 3 56
        if (hasattr(AstTool, tool)):  # 3 57
            print(getattr(AstTool(), tool)())  # 3 58
        
        else:  # 3 59
            print(f"Ast tool {tool} not found.")  # 3 60
        
    except Exception as e:      # 2 20
        tb = __jac_traceback__.extract_tb(e.__traceback__)          # 2 20
        __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 2 20
        e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 2 20
        raise e          # 2 20

@cmd_reg.register  # 2 22
def clean():  # 2 23
    try:      # 2 23
        current_dir = os.getcwd()  # 3 66
        py_cache = "__pycache__"  # 3 66
        for root,dirs,files in os.walk(current_dir, topdown = True):  # 3 68
            for folder_name in dirs[:]:  # 3 69
                if folder_name == C.JAC_GEN_DIR or folder_name == py_cache:  # 3 70
                    folder_to_remove = os.path.join(root, folder_name)  # 3 71
                    shutil.rmtree(folder_to_remove)  # 3 71
                    print(f"Removed folder: {folder_to_remove}")  # 3 71      # 3 69      # 3 68
        print("Done cleaning.")  # 3 66
    except Exception as e:      # 2 23
        tb = __jac_traceback__.extract_tb(e.__traceback__)          # 2 23
        __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 2 23
        e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 2 23
        raise e          # 2 23

@cmd_reg.register  # 2 25
def gen_dotfile(filename: str):  # 2 26
    try:      # 2 26
        from jaclang.jac.transpiler import jac_file_to_pass  # 3 83
        from jaclang.jac.passes.blue.schedules import DotGraphPass, full_ast_dot_gen  # 3 84
        if filename.endswith(".jac"):  # 3 85
            [base, mod] = os.path.split(filename)  # 3 86
            base = './' if not base else base  # 3 86
            jac_file_to_pass(filename, base, DotGraphPass, full_ast_dot_gen)  # 3 86
        
        else:  # 3 89
            print("Not a .jac file.")  # 3 90
        
    except Exception as e:      # 2 26
        tb = __jac_traceback__.extract_tb(e.__traceback__)          # 2 26
        __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 2 26
        e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 2 26
        raise e          # 2 26

r""" JAC DEBUG INFO
/home/ninja/jaclang/jaclang/cli/cli.jac
/home/ninja/jaclang/jaclang/cli/impl/cli_impl.jac
/home/ninja/jaclang/jaclang/cli/cmds.jac
/home/ninja/jaclang/jaclang/cli/impl/cmds_impl.jac
JAC DEBUG INFO """