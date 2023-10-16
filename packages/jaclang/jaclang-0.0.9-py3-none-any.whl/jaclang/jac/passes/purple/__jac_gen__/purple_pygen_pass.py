"""First Jac pass bootstrapped in Jac"""  # 0 1
from __future__ import annotations
from jaclang import jac_blue_import as __jac_import__  # -1 0
import traceback as __jac_traceback__  # -1 0
from jaclang import handle_jac_error as __jac_error__  # -1 0
import jaclang.jac.absyntree as ast  # 0 2

from jaclang.jac.passes.blue import BluePygenPass  # 0 3

from jaclang.core import Object, Node, Edge, Walker  # 0 4

__jac_import__(target='impl.purple_pygen_pass_impl', base_path=__file__)  # 0 7
from impl.purple_pygen_pass_impl import *  # 0 7

class PurplePygenPass(BluePygenPass):  # 0 13
    """
    This pass leverages data spacial lib to provide code
    gen for full Jac language. It is bootstrapped in Jac blue.
    """      # 0 13
    def __init__(self,  # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
    def add_element_import(self,arch: str):  # 0 19
        try:      # 0 19
            self.emit_ln_unique(self.preamble, f"from jaclang.core import {arch} as _jac_{arch}_")  # 1 6
            self.emit_ln_unique(self.preamble, f"from jaclang.core import make_architype as _jac_make_architype_")  # 1 6
        except Exception as e:      # 0 19
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 19
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 19
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 19
            raise e          # 0 19
    
    def add_exec_context(self,):  # 0 20
        try:      # 0 20
            self.emit_ln_unique(self.preamble, f"from jaclang.core import exec_ctx as {C.EXEC_CONTEXT}")  # 1 13
        except Exception as e:      # 0 20
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 20
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 20
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 20
            raise e          # 0 20
    
    def add_edge_directions(self,):  # 0 21
        try:      # 0 21
            self.emit_ln_unique(self.preamble, f"from jaclang.jac.constant import EdgeDir as {C.EDGE_DIR}")  # 1 18
        except Exception as e:      # 0 21
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 21
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 21
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 21
            raise e          # 0 21
    
    def needs_jac_import(self,):  # 0 22
        try:      # 0 22
            self.emit_ln_unique(self.preamble, "from jaclang import jac_purple_import as __jac_import__")  # 1 23
        except Exception as e:      # 0 22
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 22
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 22
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 22
            raise e          # 0 22
    
    def exit_architype(self,nd: ast.Architype):  # 0 24
        try:      # 0 24
            self.add_exec_context()  # 1 40
            if nd.decorators:  # 1 41
                self.emit_ln(nd, nd.decorators.meta["py_code"])  # 1 42
            
            arch_type = nd.arch_type.name  # 1 40
            arch_insert = ""  # 1 40
            if arch_type == Tok.KW_OBJECT:  # 1 46
                self.add_element_import("Object")  # 1 47
                arch_insert = C.OBJECT_CLASS  # 1 47
                self.emit_ln(nd, f"@_jac_make_architype_({arch_insert})")  # 1 47
            
            elif arch_type == Tok.KW_NODE:  # 1 51
                self.add_element_import("Node")  # 1 52
                arch_insert = C.NODE_CLASS  # 1 52
                self.emit_ln(nd, f"@_jac_make_architype_({arch_insert})")  # 1 52
            
            elif arch_type == Tok.KW_EDGE:  # 1 51
                self.add_element_import("Edge")  # 1 57
                arch_insert = C.EDGE_CLASS  # 1 57
                self.emit_ln(nd, f"@_jac_make_architype_({arch_insert})")  # 1 57
            
            elif arch_type == Tok.KW_WALKER:  # 1 51
                self.add_element_import("Walker")  # 1 62
                arch_insert = C.WALKER_CLASS  # 1 62
                self.emit_ln(nd, f"@_jac_make_architype_({arch_insert})")  # 1 62
            
            if len(nd.base_classes.base_classes):  # 1 66
                self.emit_ln(nd, f"class {nd.name.meta['py_code']}"f"({nd.base_classes.meta['py_code']}):")  # 1 67
            
            else:  # 1 70
                self.emit_ln(nd, f"class {nd.name.meta['py_code']}:")  # 1 71
            
            self.indent_level += 1  # 1 40
            if nd.doc:  # 1 74
                self.emit_ln(nd, nd.doc.meta["py_code"])  # 1 75
            
            if nd.body:  # 1 76
                self.emit_ln(nd, nd.body.meta["py_code"])  # 1 77
            
            else:  # 1 78
                self.decl_def_missing(nd.name.meta["py_code"])  # 1 79
            
            self.indent_level -= 1  # 1 40
        except Exception as e:      # 0 24
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 24
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 24
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 24
            raise e          # 0 24
    
    def exit_ability(self,nd: ast.Ability):  # 0 25
        try:      # 0 25
            ability_name = nd.py_resolve_name()  # 1 98
            if nd.arch_attached and ability_name == "__init__":  # 1 99
                return  # 1 100
            
            if type(nd.signature) == ast.EventSignature and nd.arch_attached and nd.signature.event.name == Tok.KW_ENTRY:  # 1 102
                self.add_element_import("Object")  # 1 104
                type_list = _jac_tmp if (_jac_tmp := (((nd.signature.arch_tag_info.meta if nd.signature.arch_tag_info is not None else None)["py_code"] if (nd.signature.arch_tag_info.meta if nd.signature.arch_tag_info is not None else None) is not None else None))) is not None else ""  # 1 104
                self.emit_ln(nd, f"@{C.OBJECT_CLASS}.{C.ON_ENTRY}([{type_list.replace('|', ', ')}])")  # 1 104
            
            elif type(nd.signature) == ast.EventSignature and nd.arch_attached and nd.signature.event.name == Tok.KW_EXIT:  # 1 108
                self.add_element_import("Object")  # 1 110
                type_list = _jac_tmp if (_jac_tmp := (((nd.signature.arch_tag_info.meta if nd.signature.arch_tag_info is not None else None)["py_code"] if (nd.signature.arch_tag_info.meta if nd.signature.arch_tag_info is not None else None) is not None else None))) is not None else ""  # 1 110
                self.emit_ln(nd, f"@{C.OBJECT_CLASS}.{C.ON_EXIT}([{type_list.replace('|', ', ')}])")  # 1 110
            
            super().exit_ability((nd))  # 1 98
        except Exception as e:      # 0 25
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 25
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 25
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 25
            raise e          # 0 25
    
    def exit_event_signature(self,nd: ast.EventSignature):  # 0 26
        try:      # 0 26
            if nd.arch_tag_info:  # 1 126
                self.emit(nd, f"{C.HERE}: {nd.arch_tag_info.meta['py_code']}")  # 1 127
            
            else:  # 1 129
                self.emit(nd, f"{C.HERE}")  # 1 130
            
            if nd.return_type:  # 1 132
                self.emit(nd, f" -> {nd.return_type.meta['py_code']}")  # 1 133
            
        except Exception as e:      # 0 26
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 26
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 26
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 26
            raise e          # 0 26
    
    def exit_ctrl_stmt(self,nd: ast.CtrlStmt):  # 0 27
        try:      # 0 27
            if nd.ctrl.name == Tok.KW_SKIP:  # 1 144
                self.emit_ln(nd, "return")  # 1 145
            
            else:  # 1 146
                super().exit_ctrl_stmt(nd)  # 1 147
            
        except Exception as e:      # 0 27
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 27
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 27
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 27
            raise e          # 0 27
    
    def exit_report_stmt(self,nd: ast.ReportStmt):  # 0 28
        try:      # 0 28
            pass  # 0 28
        except Exception as e:      # 0 28
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 28
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 28
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 28
            raise e          # 0 28
    
    def exit_ignore_stmt(self,nd: ast.IgnoreStmt):  # 0 29
        try:      # 0 29
            loc = 'self' if nd.from_walker else C.HERE  # 1 159
            self.emit_ln(nd, f"{loc}.{C.WALKER_IGNORE}({nd.target.meta['py_code']})")  # 1 159
        except Exception as e:      # 0 29
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 29
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 29
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 29
            raise e          # 0 29
    
    def exit_visit_stmt(self,nd: ast.VisitStmt):  # 0 30
        try:      # 0 30
            vis_type = _jac_tmp if (_jac_tmp := ((nd.vis_type.value if nd.vis_type is not None else None))) is not None else ""  # 1 174
            loc = 'self' if nd.from_walker else C.HERE  # 1 174
            self.emit_ln(nd, f"if not {loc}.{C.WALKER_VISIT}({nd.target.meta['py_code']}): ")  # 1 174
            self.indent_level += 1  # 1 174
            if nd.else_body:  # 1 179
                self.emit(nd, nd.else_body.body.meta["py_code"])  # 1 180
            
            else:  # 1 181
                self.emit_ln(nd, 'pass')  # 1 182
            
            self.indent_level -= 1  # 1 174
        except Exception as e:      # 0 30
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 30
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 30
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 30
            raise e          # 0 30
    
    def exit_revisit_stmt(self,nd: ast.RevisitStmt):  # 0 31
        try:      # 0 31
            pass  # 0 31
        except Exception as e:      # 0 31
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 31
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 31
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 31
            raise e          # 0 31
    
    def exit_await_stmt(self,nd: ast.AwaitStmt):  # 0 32
        try:      # 0 32
            pass  # 0 32
        except Exception as e:      # 0 32
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 32
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 32
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 32
            raise e          # 0 32
    
    def exit_disengage_stmt(self,nd: ast.DisengageStmt):  # 0 33
        try:      # 0 33
            loc = 'self' if nd.from_walker else C.HERE  # 1 193
            self.emit_ln(nd, f"return {loc}.{C.DISENGAGE}()")  # 1 193
        except Exception as e:      # 0 33
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 33
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 33
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 33
            raise e          # 0 33
    
    def exit_binary_expr(self,nd: ast.BinaryExpr):  # 0 34
        try:      # 0 34
            if (type(nd.op)) == ast.ConnectOp:  # 1 206
                self.emit(nd, f"{nd.left.meta['py_code']}.{C.CONNECT_NODE}({nd.right.meta['py_code']}, {nd.op.meta['py_code']})")  # 1 207
            
            elif (type(nd.op)) == ast.DisconnectOp:  # 1 209
                self.ds_feature_warn()  # 1 210
            
            elif nd.op.name == Tok.PIPE_FWD and isinstance(nd.right, ast.TupleVal):  # 1 209
                self.ds_feature_warn()  # 1 212
            
            else:  # 1 214
                super().exit_binary_expr(nd)  # 1 215
            
        except Exception as e:      # 0 34
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 34
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 34
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 34
            raise e          # 0 34
    
    def exit_edge_op_ref(self,nd: ast.EdgeOpRef):  # 0 35
        try:      # 0 35
            loc = C.HERE if nd.from_walker else 'self'  # 1 229
            edge_dir = f"{C.EDGE_DIR}.IN" if nd.edge_dir == EdgeDir.IN else f"{C.EDGE_DIR}.OUT" if nd.edge_dir == EdgeDir.OUT else f"{C.EDGE_DIR}.ANY"  # 1 229
            if nd.filter_type and nd.filter_cond:  # 1 233
                self.emit(nd, f"[{C.JAC_TMP} for {C.JAC_TMP} in {loc}.{C.EDGES_TO_NODE}({edge_dir})"f" if isinstance({C.JAC_TMP}, {nd.filter_type.meta['py_code']})"f" and {nd.filter_cond.meta['py_code'].replace(C.PATCH, C.JAC_TMP)}]")  # 1 234
            
            elif nd.filter_type:  # 1 239
                self.emit(nd, f"[{C.JAC_TMP} for {C.JAC_TMP} in {loc}.{C.EDGES_TO_NODE}({edge_dir})"f" if isinstance({C.JAC_TMP}, {nd.filter_type.meta['py_code']})]")  # 1 240
            
            else:  # 1 244
                self.emit(nd, f"{loc}.{C.EDGES_TO_NODE}({edge_dir})")  # 1 245
            
        except Exception as e:      # 0 35
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 35
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 35
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 35
            raise e          # 0 35
    
    def exit_connect_op(self,nd: ast.ConnectOp):  # 0 36
        try:      # 0 36
            self.add_element_import("Edge")  # 1 259
            self.add_edge_directions()  # 1 259
            if nd.conn_type:  # 1 262
                self.emit(nd, f"{nd.conn_type.meta['py_code']}.{C.WITH_DIR}({C.EDGE_DIR}.{nd.edge_dir.name}")  # 1 263
            
            else:  # 1 264
                self.emit(nd, f"{C.EDGE_CLASS}().{C.WITH_DIR}({C.EDGE_DIR}.{nd.edge_dir.name}")  # 1 265
            
            if nd.conn_assign:  # 1 267
                self.emit(nd, f", {nd.conn_assign.meta['py_code']})")  # 1 268
            
            else:  # 1 269
                self.emit(nd, ")")  # 1 270
            
        except Exception as e:      # 0 36
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 36
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 36
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 36
            raise e          # 0 36
    
    def exit_disconnect_op(self,nd: ast.DisconnectOp):  # 0 37
        try:      # 0 37
            pass  # 1 281
        except Exception as e:      # 0 37
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 37
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 37
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 37
            raise e          # 0 37
    

r""" JAC DEBUG INFO
/home/ninja/jaclang/jaclang/jac/passes/purple/purple_pygen_pass.jac
/home/ninja/jaclang/jaclang/jac/passes/purple/impl/purple_pygen_pass_impl.jac
JAC DEBUG INFO """