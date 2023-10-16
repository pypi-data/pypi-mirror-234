"""
This is the implementation of the command line interface tool for the
Jac language. It's built with the Jac language via bootstraping and
represents the first such complete Jac program.
"""  # 0 1
from __future__ import annotations
from jaclang import jac_purple_import as __jac_import__  # -1 0
import traceback as __jac_traceback__  # -1 0
from jaclang import handle_jac_error as __jac_error__  # -1 0
from jaclang.core import exec_ctx as _jac_exec_ctx_  # -1 0
from jaclang.core import Object as _jac_Object_  # -1 0
from jaclang.core import make_architype as _jac_make_architype_  # -1 0
import inspect  # 0 7

import argparse  # 0 8

import cmd  # 0 9

__jac_import__(target='impl.cli_impl', base_path=__file__)  # 0 10
from impl.cli_impl import *  # 0 10

@_jac_make_architype_(_jac_Object_)  # 0 13
class Command:  # 0 13
    def __init__(self,  # 0 0
        func = None,      # 0 0
        sig = None,      # 0 0
        *args, **kwargs):      # 0 0
        self.func = func      # 0 0
        self.sig = sig      # 0 0
        self.func = func  # 1 4
        self.sig = inspect.signature(func)  # 1 4
    
    def call(self,*args: list, **kwargs: dict):  # 0 18
        try:      # 0 18
            return self.func(*args, **kwargs)  # 1 9
        except Exception as e:      # 0 18
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 18
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 18
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 18
            raise e          # 0 18      # 0 13

@_jac_make_architype_(_jac_Object_)  # 0 22
class CommandRegistry:  # 0 22
    def __init__(self,  # 0 0
        registry = None,      # 0 0
        sub_parsers = None,      # 0 0
        parser = None,      # 0 0
        *args, **kwargs):      # 0 0
        self.registry = registry      # 0 0
        self.sub_parsers = sub_parsers      # 0 0
        self.parser = parser      # 0 0
        self.registry = {}  # 1 13
        self.parser = argparse.ArgumentParser(prog = "CLI")  # 1 13
        self.sub_parsers = self.parser.add_subparsers(title = "commands", dest = "command")  # 1 13
    
    def register(self,func: callable):  # 0 28
        try:      # 0 28
            name = func.__name__  # 1 20
            cmd = Command(func)  # 1 20
            self.registry[name] = cmd  # 1 20
            cmd_parser = self.sub_parsers.add_parser(name)  # 1 20
            param_items = cmd.sig.parameters.items  # 1 20
            first = True  # 1 20
            for param_name,param in cmd.sig.parameters.items():  # 1 26
                if param_name == "args":  # 1 27
                    cmd_parser.add_argument('args', nargs = argparse.REMAINDER)  # 1 28
                
                elif param.default is param.empty:  # 1 31
                    if first:  # 1 32
                        first = False  # 1 33
                        cmd_parser.add_argument(f"{param_name}", type = eval(param.annotation))  # 1 33
                    
                    else:  # 1 37
                        cmd_parser.add_argument(f"-{param_name[:1]}", f"--{param_name}", required = True, type = eval(param.annotation))  # 1 38
                    
                
                else:  # 1 44
                    if first:  # 1 45
                        first = False  # 1 46
                        cmd_parser.add_argument(f"{param_name}", default = param.default, type = eval(param.annotation))  # 1 46
                    
                    else:  # 1 50
                        cmd_parser.add_argument(f"-{param_name[:1]}", f"--{param_name}", default = param.default, type = eval(param.annotation))  # 1 51      # 1 26
            return func  # 1 57
        except Exception as e:      # 0 28
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 28
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 28
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 28
            raise e          # 0 28
    
    def get(self,name: str) -> Command:  # 0 29
        try:      # 0 29
            return self.registry.get(name)  # 1 61
        except Exception as e:      # 0 29
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 29
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 29
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 29
            raise e          # 0 29
    
    def items(self,) -> dict[str, Command]:  # 0 30
        try:      # 0 30
            return self.registry.items()  # 1 65
        except Exception as e:      # 0 30
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 30
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 30
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 30
            raise e          # 0 30      # 0 22

@_jac_make_architype_(_jac_Object_)  # 0 34
class CommandShell(cmd.Cmd):  # 0 34
    intro: str = "Welcome to the Jac CLI!"  # 0 35
    prompt: str = "jac> "  # 0 35
    
    def __init__(self,  # 0 0
        cmd_reg = None,      # 0 0
        *args, **kwargs):      # 0 0
        self.cmd_reg = cmd_reg      # 0 0
        self.cmd_reg = cmd_reg  # 1 70
        cmd.Cmd.__init__(self)  # 1 70
    
    def do_exit(self,arg: list) -> bool:  # 0 40
        try:      # 0 40
            return True  # 1 75
        except Exception as e:      # 0 40
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 40
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 40
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 40
            raise e          # 0 40
    
    def default(self,line: str):  # 0 41
        try:      # 0 41
            try:  # 1 79
                args = vars(self.cmd_reg.parser.parse_args(line.split()))  # 1 80
                command = self.cmd_reg.get(args["command"])  # 1 80
                if command:  # 1 82
                    args.pop("command")  # 1 83
                    ret = command.call(**args)  # 1 83
                    if ret:  # 1 85
                        print(ret)  # 1 86      # 1 79
            except Exception as e:  # 1 90
                print(e)  # 1 91      # 1 90  # 1 90  # 1 79
        except Exception as e:      # 0 41
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 41
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 41
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 41
            raise e          # 0 41      # 0 34

cmd_registry = CommandRegistry()  # 0 45

def start_cli():  # 0 46
    try:      # 0 46
        parser = cmd_registry.parser  # 1 96
        args = parser.parse_args()  # 1 96
        command = cmd_registry.get(args.command)  # 1 96
        if command:  # 1 99
            args = vars(args)  # 1 100
            args.pop("command")  # 1 100
            ret = command.call(**args)  # 1 100
            if ret:  # 1 103
                print(ret)  # 1 104
            
        
        else:  # 1 107
            shell = CommandShell(cmd_registry).cmdloop()  # 1 108
        
    except Exception as e:      # 0 46
        tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 46
        __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 46
        e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 46
        raise e          # 0 46

r""" JAC DEBUG INFO
/home/ninja/jaclang/jaclang/cli/cli.jac
/home/ninja/jaclang/jaclang/cli/impl/cli_impl.jac
JAC DEBUG INFO """