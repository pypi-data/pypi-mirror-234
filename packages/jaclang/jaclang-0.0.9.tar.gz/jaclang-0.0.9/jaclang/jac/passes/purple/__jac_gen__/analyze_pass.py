"""Type Analyze Pass."""  # 0 1
from __future__ import annotations
import traceback as __jac_traceback__  # -1 0
from jaclang import handle_jac_error as __jac_error__  # -1 0
import jaclang.jac.absyntree as ast  # 0 2

from jaclang.jac.passes import Pass  # 0 4

from jaclang.jac.constant import Tokens as Tok  # 0 5

class AnalyzePass(Pass):  # 0 8
    def __init__(self,  # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
    def enter_arch_block(self,nd: ast.ArchBlock):  # 0 9
        try:      # 0 9
            if (isinstance(nd.parent, ast.Architype) and nd.parent.arch_type.name == Tok.KW_WALKER):  # 0 14
                for i in self.get_all_sub_nodes(nd, ast.VisitStmt, brute_force = False):  # 0 18
                    i.from_walker = True  # 0 19      # 0 18
                for i in self.get_all_sub_nodes(nd, ast.IgnoreStmt, brute_force = False):  # 0 21
                    i.from_walker = True  # 0 22      # 0 21
                for i in self.get_all_sub_nodes(nd, ast.DisengageStmt, brute_force = False):  # 0 24
                    i.from_walker = True  # 0 25      # 0 24
                for i in self.get_all_sub_nodes(nd, ast.EdgeOpRef, brute_force = False):  # 0 27
                    i.from_walker = True  # 0 28      # 0 27
            
        except Exception as e:      # 0 9
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 9
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 9
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 9
            raise e          # 0 9
    


r""" JAC DEBUG INFO
/home/ninja/jaclang/jaclang/jac/passes/purple/analyze_pass.jac
JAC DEBUG INFO """