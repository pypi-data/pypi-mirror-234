"""Jac's Key Elemental Abstractions"""  # 0 1
from __future__ import annotations
from jaclang import jac_blue_import as __jac_import__  # -1 0
import traceback as __jac_traceback__  # -1 0
from jaclang import handle_jac_error as __jac_error__  # -1 0
from enum import Enum as __jac_Enum__, auto as __jac_auto__  # -1 0
from datetime import datetime  # 0 3

from uuid import UUID, uuid4  # 0 4

from jaclang.jac.constant import EdgeDir  # 0 5

__jac_import__(target='impl.memory_impl', base_path=__file__)  # 0 7
from impl.memory_impl import *  # 0 7

__jac_import__(target='impl.exec_ctx_impl', base_path=__file__)  # 0 8
from impl.exec_ctx_impl import *  # 0 8

__jac_import__(target='impl.element_impl', base_path=__file__)  # 0 9
from impl.element_impl import *  # 0 9

__jac_import__(target='impl.arch_impl', base_path=__file__)  # 0 10
from impl.arch_impl import *  # 0 10

class AccessMode(__jac_Enum__):  # 0 13
    READ_ONLY = __jac_auto__()  # 3 4
    READ_WRITE = __jac_auto__()  # 3 4
    PRIVATE = __jac_auto__()  # 3 4

class Memory:  # 0 15
    def __init__(self,  # 0 0
        index = None,      # 0 0
        save_queue = None,      # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
        self.index = index      # 0 0
        self.save_queue = save_queue      # 0 0
    def get_obj(self,caller_id: UUID, item_id: UUID, override: bool = False) -> Element:  # 0 19
        try:      # 0 19
            ret = self.index.get(item_id)  # 1 6
            if override or (ret.__is_readable(ret is not None and caller_id)):  # 1 7
                return ret  # 1 8
            
        except Exception as e:      # 0 19
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 19
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 19
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 19
            raise e          # 0 19
    
    def has_obj(self,item_id: UUID) -> bool:  # 0 21
        try:      # 0 21
            return item_id in self.index  # 1 14
        except Exception as e:      # 0 21
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 21
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 21
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 21
            raise e          # 0 21
    
    def save_obj(self,caller_id: UUID, item: Element):  # 0 22
        try:      # 0 22
            if item.is_writable(caller_id):  # 1 19
                self.index[item.id] = item  # 1 20
                if item._persist:  # 1 21
                    self.save_obj_list.add(item)  # 1 22
                
            
            self.mem[item.id] = item  # 1 19
            if item._persist:  # 1 26
                self.save_obj_list.add(item)  # 1 27
            
        except Exception as e:      # 0 22
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 22
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 22
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 22
            raise e          # 0 22
    
    def del_obj(self,caller_id: UUID, item: Element):  # 0 23
        try:      # 0 23
            if item.is_writable(caller_id):  # 1 33
                self.index.pop(item.id)  # 1 34
                if item._persist:  # 1 35
                    self.save_obj_list.remove(item)  # 1 36
                
            
        except Exception as e:      # 0 23
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 23
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 23
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 23
            raise e          # 0 23
    
    def get_object_distribution(self,) -> dict:  # 0 26
        try:      # 0 26
            dist = {}  # 1 42
            for i in self.index.keys():  # 1 43
                t = type(self.index[i])  # 1 44
                if t in dist:  # 1 45
                    dist[t] += 1  # 1 46
                
                else:  # 1 48
                    dist[t] = 1  # 1 49      # 1 43
            return dist  # 1 52
        except Exception as e:      # 0 26
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 26
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 26
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 26
            raise e          # 0 26
    
    def get_mem_size(self,) -> float:  # 0 27
        try:      # 0 27
            return (sys.getsizeof(self.index)) / 1024.0  # 1 56
        except Exception as e:      # 0 27
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 27
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 27
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 27
            raise e          # 0 27
    

class ExecutionContext:  # 0 30
    def __init__(self,  # 0 0
        master = None,      # 0 0
        memory = None,      # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
        self.master = uuid4() if master is None else master      # 0 0
        self.memory = Memory() if memory is None else memory      # 0 0
    def reset(self,):  # 0 34
        try:      # 0 34
            self.__init__()  # 2 13
        except Exception as e:      # 0 34
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 34
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 34
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 34
            raise e          # 0 34
    
    def get_root(self,) -> Node:  # 0 35
        try:      # 0 35
            if type(self.master) == UUID:  # 2 6
                self.master = Master()  # 2 7
            
            return self.master.root_node  # 2 9
        except Exception as e:      # 0 35
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 35
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 35
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 35
            raise e          # 0 35
    

"Global Execution Context, should be monkey patched by the user."  # 0 39
exec_ctx = ExecutionContext()  # 0 39

class ElementInterface:  # 0 41
    def __init__(self,  # 0 0
        jid = None,      # 0 0
        py_obj = None,      # 0 0
        timestamp = None,      # 0 0
        persist = None,      # 0 0
        access_mode = None,      # 0 0
        rw_access = None,      # 0 0
        ro_access = None,      # 0 0
        owner_id = None,      # 0 0
        mem = None,      # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
        self.jid = uuid4() if jid is None else jid      # 0 0
        self.py_obj = None if py_obj is None else py_obj      # 0 0
        self.timestamp = datetime.now() if timestamp is None else timestamp      # 0 0
        self.persist = False if persist is None else persist      # 0 0
        self.access_mode = AccessMode.PRIVATE if access_mode is None else access_mode      # 0 0
        self.rw_access = set() if rw_access is None else rw_access      # 0 0
        self.ro_access = set() if ro_access is None else ro_access      # 0 0
        self.owner_id = exec_ctx.master if owner_id is None else owner_id      # 0 0
        self.mem = exec_ctx.memory if mem is None else mem      # 0 0
    def make_public_ro(self,):  # 0 52
        try:      # 0 52
            self.__jinfo.access_mode = AccessMode.READ_ONLY  # 3 10
        except Exception as e:      # 0 52
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 52
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 52
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 52
            raise e          # 0 52
    
    def make_public_rw(self,):  # 0 53
        try:      # 0 53
            self.__jinfo.access_mode = AccessMode.READ_WRITE  # 3 14
        except Exception as e:      # 0 53
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 53
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 53
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 53
            raise e          # 0 53
    
    def make_private(self,):  # 0 54
        try:      # 0 54
            self.__jinfo.access_mode = AccessMode.PRIVATE  # 3 18
        except Exception as e:      # 0 54
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 54
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 54
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 54
            raise e          # 0 54
    
    def is_public_ro(self,) -> bool:  # 0 55
        try:      # 0 55
            return self.__jinfo.access_mode == AccessMode.READ_ONLY  # 3 22
        except Exception as e:      # 0 55
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 55
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 55
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 55
            raise e          # 0 55
    
    def is_public_rw(self,) -> bool:  # 0 56
        try:      # 0 56
            return self.__jinfo.access_mode == AccessMode.READ_WRITE  # 3 26
        except Exception as e:      # 0 56
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 56
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 56
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 56
            raise e          # 0 56
    
    def is_private(self,) -> bool:  # 0 57
        try:      # 0 57
            return self.__jinfo.access_mode == AccessMode.PRIVATE  # 3 30
        except Exception as e:      # 0 57
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 57
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 57
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 57
            raise e          # 0 57
    
    def is_readable(self,caller_id: UUID) -> bool:  # 0 58
        try:      # 0 58
            return (caller_id == self.owner_id or self.is_public_read() or caller_id in self.ro_access or caller_id in self.rw_access)  # 3 35
        except Exception as e:      # 0 58
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 58
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 58
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 58
            raise e          # 0 58
    
    def is_writable(self,caller_id: UUID) -> bool:  # 0 59
        try:      # 0 59
            return (caller_id == self.owner_id or self.is_public_write() or caller_id in self.rw_access)  # 3 45
        except Exception as e:      # 0 59
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 59
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 59
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 59
            raise e          # 0 59
    
    def give_access(self,caller_id: UUID, read_write: bool = False):  # 0 60
        try:      # 0 60
            if read_write:  # 3 54
                self.rw_access.add(caller_id)  # 3 55
            
            else:  # 3 57
                self.ro_access.add(caller_id)  # 3 58
            
        except Exception as e:      # 0 60
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 60
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 60
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 60
            raise e          # 0 60
    
    def revoke_access(self,caller_id: UUID):  # 0 61
        try:      # 0 61
            self.ro_access.discard(caller_id)  # 3 64
            self.rw_access.discard(caller_id)  # 3 64
        except Exception as e:      # 0 61
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 61
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 61
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 61
            raise e          # 0 61
    

class DataSpatialInterface:  # 0 64
    ds_entry_funcs: list[dict] = []  # 0 65
    ds_exit_funcs: list[dict] = []  # 0 65
    
    def __init__(self,  # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
    @classmethod  # 0 68
    def on_entry(cls: type, triggers: list[type]):  # 0 68
        try:      # 0 68
            def decorator(func: callable) -> callable:  # 3 71
                try:      # 3 71
                    cls.ds_entry_funcs.append({'func': func, 'types': triggers})  # 3 72
                    def wrapper(*args: list, **kwargs: dict) -> callable:  # 3 73
                        try:      # 3 73
                            return func(*args, **kwargs)  # 3 74
                        except Exception as e:      # 3 73
                            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 3 73
                            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 3 73
                            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 3 73
                            raise e          # 3 73
                    return wrapper  # 3 76
                except Exception as e:      # 3 71
                    tb = __jac_traceback__.extract_tb(e.__traceback__)          # 3 71
                    __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 3 71
                    e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 3 71
                    raise e          # 3 71
            return decorator  # 3 78
        except Exception as e:      # 0 68
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 68
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 68
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 68
            raise e          # 0 68
    
    @classmethod  # 0 69
    def on_exit(cls: type, triggers: list[type]):  # 0 69
        try:      # 0 69
            def decorator(func: callable) -> callable:  # 3 83
                try:      # 3 83
                    cls.ds_exit_funcs.append({'func': func, 'types': triggers})  # 3 84
                    def wrapper(*args: list, **kwargs: dict) -> callable:  # 3 85
                        try:      # 3 85
                            return func(*args, **kwargs)  # 3 86
                        except Exception as e:      # 3 85
                            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 3 85
                            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 3 85
                            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 3 85
                            raise e          # 3 85
                    return wrapper  # 3 88
                except Exception as e:      # 3 83
                    tb = __jac_traceback__.extract_tb(e.__traceback__)          # 3 83
                    __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 3 83
                    e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 3 83
                    raise e          # 3 83
            return decorator  # 3 90
        except Exception as e:      # 0 69
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 69
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 69
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 69
            raise e          # 0 69
    

class ObjectInterface(ElementInterface):  # 0 72
    def __init__(self,  # 0 72
        *args, **kwargs):      # 0 72
        super().__init__(*args, **kwargs)      # 0 72

class NodeInterface(ObjectInterface):  # 0 74
    def __init__(self,  # 0 0
        edges = None,      # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
        self.edges = {EdgeDir.OUT: [], EdgeDir.IN: []} if edges is None else edges      # 0 0
    def connect_node(self,nd: Node, edg: Edge) -> Node:  # 0 78
        try:      # 0 78
            edg.attach(self.py_obj, nd)  # 4 7
            return self  # 4 8
        except Exception as e:      # 0 78
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 78
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 78
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 78
            raise e          # 0 78
    
    def edges_to_nodes(self,dir: EdgeDir) -> list[Node]:  # 0 79
        try:      # 0 79
            ret_nodes = []  # 4 13
            if dir in [EdgeDir.OUT, EdgeDir.ANY]:  # 4 14
                for i in self.edges[EdgeDir.OUT]:  # 4 15
                    ret_nodes.append(i.target)  # 4 16      # 4 15
            
            elif dir in [EdgeDir.IN, EdgeDir.ANY]:  # 4 18
                for i in self.edges[EdgeDir.IN]:  # 4 19
                    ret_nodes.append(i.source)  # 4 20      # 4 19
            
            return ret_nodes  # 4 23
        except Exception as e:      # 0 79
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 79
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 79
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 79
            raise e          # 0 79
    

class EdgeInterface(ObjectInterface):  # 0 82
    def __init__(self,  # 0 0
        source = None,      # 0 0
        target = None,      # 0 0
        dir = None,      # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
        self.source = source      # 0 0
        self.target = target      # 0 0
        self.dir = dir      # 0 0
    def apply_dir(self,dir: EdgeDir) -> Edge:  # 0 87
        try:      # 0 87
            self.dir = dir  # 4 28
            return self  # 4 29
        except Exception as e:      # 0 87
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 87
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 87
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 87
            raise e          # 0 87
    
    def attach(self,src: Node, trg: Node) -> Edge:  # 0 88
        try:      # 0 88
            if self.dir == EdgeDir.IN:  # 4 34
                self.source = trg  # 4 35
                self.target = src  # 4 35
                src._jac_.edges[EdgeDir.IN].append(self)  # 4 35
                trg._jac_.edges[EdgeDir.OUT].append(self)  # 4 35
            
            else:  # 4 39
                self.source = src  # 4 40
                self.target = trg  # 4 40
                src._jac_.edges[EdgeDir.OUT].append(self)  # 4 40
                trg._jac_.edges[EdgeDir.IN].append(self)  # 4 40
            
            return self  # 4 46
        except Exception as e:      # 0 88
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 88
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 88
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 88
            raise e          # 0 88
    

class WalkerInterface(ObjectInterface):  # 0 91
    def __init__(self,  # 0 0
        path = None,      # 0 0
        next = None,      # 0 0
        ignores = None,      # 0 0
        disengaged = None,      # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
        self.path = [] if path is None else path      # 0 0
        self.next = [] if next is None else next      # 0 0
        self.ignores = [] if ignores is None else ignores      # 0 0
        self.disengaged = False if disengaged is None else disengaged      # 0 0
    def visit_node(self,nds: list[Node]|list[Edge]|Node|Edge):  # 0 97
        try:      # 0 97
            if isinstance(nds, list):  # 4 51
                for i in nds:  # 4 52
                    if (i not in self.ignores):  # 4 53
                        self.next.append(i)  # 4 53      # 4 52
            
            elif nds not in self.ignores:  # 4 55
                self.next.append(nds)  # 4 55
            
            return len(nds) if isinstance(nds, list) else 1  # 4 56
        except Exception as e:      # 0 97
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 97
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 97
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 97
            raise e          # 0 97
    
    def ignore_node(self,nds: list[Node]|list[Edge]|Node|Edge):  # 0 98
        try:      # 0 98
            if isinstance(nds, list):  # 4 61
                for i in nds:  # 4 62
                    self.ignores.append(i)  # 4 63      # 4 62
            
            else:  # 4 65
                self.ignores.append(nds)  # 4 65
            
        except Exception as e:      # 0 98
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 98
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 98
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 98
            raise e          # 0 98
    
    def disengage_now(self,):  # 0 99
        try:      # 0 99
            self.next = []  # 4 69
            self.disengaged = True  # 4 69
        except Exception as e:      # 0 99
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 99
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 99
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 99
            raise e          # 0 99
    

class Element:  # 0 102
    def __init__(self,  # 0 0
        _jac_ = None,      # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
        self._jac_ = ElementInterface(py_obj = self) if _jac_ is None else _jac_      # 0 0

class Object(Element):  # 0 106
    _jac_ds_: DataSpatialInterface = DataSpatialInterface()  # 0 108
    
    def __init__(self,  # 0 0
        _jac_ = None,      # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
        self._jac_ = ObjectInterface(py_obj = self) if _jac_ is None else _jac_      # 0 0

class Node(Object):  # 0 111
    def __init__(self,  # 0 0
        _jac_ = None,      # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
        self._jac_ = NodeInterface(py_obj = self) if _jac_ is None else _jac_      # 0 0
    def __call__(self,walk: Walker):  # 0 113
        try:      # 0 113
            if not isinstance(walk, Walker):  # 4 76
                raise TypeError(("Argument must be a Walker instance"))  # 4 77
            
            walk(self)  # 4 76
        except Exception as e:      # 0 113
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 113
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 113
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 113
            raise e          # 0 113
    

class Edge(Object):  # 0 116
    def __init__(self,  # 0 0
        _jac_ = None,      # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
        self._jac_ = EdgeInterface(py_obj = self) if _jac_ is None else _jac_      # 0 0
    def __call__(self,walk: Walker):  # 0 118
        try:      # 0 118
            if not isinstance(walk, Walker):  # 4 85
                raise TypeError(("Argument must be a Walker instance"))  # 4 86
            
            walk(self._jac_.target)  # 4 85
        except Exception as e:      # 0 118
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 118
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 118
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 118
            raise e          # 0 118
    

class Walker(Object):  # 0 121
    def __init__(self,  # 0 0
        _jac_ = None,      # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
        self._jac_ = WalkerInterface(py_obj = self) if _jac_ is None else _jac_      # 0 0
    def __call__(self,nd: Node):  # 0 123
        try:      # 0 123
            self._jac_.path = []  # 4 93
            self._jac_.next = [nd]  # 4 93
            walker_type = self.__class__.__name__  # 4 93
            while len(self._jac_.next):  # 4 96
                nd = self._jac_.next.pop(0)  # 4 97
                node_type = nd.__class__.__name__  # 4 97
                for i in nd._jac_ds_.ds_entry_funcs:  # 4 100
                    if i['func'].__qualname__.split(".")[0] == node_type and type(self) in i['types']:  # 4 101
                        i['func'](nd, self)  # 4 103
                    
                    if self._jac_.disengaged:  # 4 105
                        return  # 4 105      # 4 100
                for i in self._jac_ds_.ds_entry_funcs:  # 4 107
                    if i['func'].__qualname__.split(".")[0] == walker_type and (type(nd) in i['types'] or nd in i['types']):  # 4 108
                        i['func'](self, nd)  # 4 110
                    
                    if self._jac_.disengaged:  # 4 112
                        return  # 4 112      # 4 107
                for i in self._jac_ds_.ds_exit_funcs:  # 4 114
                    if i['func'].__qualname__.split(".")[0] == walker_type and (type(nd) in i['types'] or nd in i['types']):  # 4 115
                        i['func'](self, nd)  # 4 117
                    
                    if self._jac_.disengaged:  # 4 119
                        return  # 4 119      # 4 114
                for i in nd._jac_ds_.ds_exit_funcs:  # 4 121
                    if i['func'].__qualname__.split(".")[0] == node_type and type(self) in i['types']:  # 4 122
                        i['func'](nd, self)  # 4 124
                    
                    if self._jac_.disengaged:  # 4 126
                        return  # 4 126      # 4 121
                self._jac_.path.append(nd)  # 4 97      # 4 96
            self._jac_.ignores = []  # 4 93
        except Exception as e:      # 0 123
            tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 123
            __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 123
            e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 123
            raise e          # 0 123
    

class Master(Element):  # 0 126
    def __init__(self,  # 0 0
        root_node = None,      # 0 0
        *args, **kwargs):      # 0 0
        super().__init__(*args, **kwargs)      # 0 0
        self.root_node = Node() if root_node is None else root_node      # 0 0

def make_architype(base_class: type) -> type:  # 0 128
    try:      # 0 128
        def class_decorator(cls: type) -> type:  # 3 94
            try:      # 3 94
                if not issubclass(cls, base_class):  # 3 96
                    cls = type(cls.__name__, (cls, base_class), {})  # 3 98
                
                return cls  # 3 106
            except Exception as e:      # 3 94
                tb = __jac_traceback__.extract_tb(e.__traceback__)          # 3 94
                __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 3 94
                e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 3 94
                raise e          # 3 94
        return class_decorator  # 3 108
    except Exception as e:      # 0 128
        tb = __jac_traceback__.extract_tb(e.__traceback__)          # 0 128
        __jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)          # 0 128
        e.args = (f'{e.args[0]}\n' + __jac_tmp__,) + e.args[1:] if 'Jac error originates from...' not in str(e) else e.args          # 0 128
        raise e          # 0 128

r""" JAC DEBUG INFO
/home/ninja/jaclang/jaclang/core/primitives.jac
/home/ninja/jaclang/jaclang/core/impl/memory_impl.jac
/home/ninja/jaclang/jaclang/core/impl/exec_ctx_impl.jac
/home/ninja/jaclang/jaclang/core/impl/element_impl.jac
/home/ninja/jaclang/jaclang/core/impl/arch_impl.jac
JAC DEBUG INFO """