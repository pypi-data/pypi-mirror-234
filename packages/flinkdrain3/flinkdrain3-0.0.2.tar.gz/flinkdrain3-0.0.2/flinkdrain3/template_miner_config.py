import ast
import configparser
import json
import logging
from typing import Union

from flinkdrain3.masking import MaskingInstruction

logger = logging.getLogger(__name__)

class TemplateMinerConfig:
    def __init__(self,json_path = None):
        def _fallback(jsonobj,list2len,default):
            if jsonobj is None:
                return default
            try:
                return jsonobj[list2len[0]][list2len[1]]
            except:
                return default
        
        confi = None
        if json_path is not None:
            with open(file=json_path, mode='r') as f:
                confi = json.load(f)
            
        self.engine = "Drain" #Backend engine for parsing :Current Drain, JaccardDrain
        
        self.drain_sim_th:float = _fallback(confi,('drain','similar_threshold'),0.4)
        self.drain_depth:int = _fallback(confi,('drain','depth'),4)
        self.drain_max_children:int = _fallback(confi,('drain','max_children'),100)
        self.drain_max_clusters:Union[int,None] = _fallback(confi,('drain','max_clusters'),None)
        if self.drain_max_clusters == -1:
            self.drain_max_clusters = None
        
        self.profiling_enabled:bool = _fallback(confi,('profiling','enabled'),False)
        self.profiling_report_sec:int = _fallback(confi,('profiling','enabled'),60)
        
        self.snapshot_enabled:bool = _fallback(confi,('persist','enabled'),False)
        self.snapshot_interval_minutes:int = _fallback(confi,('persist','snapshot_interval_minutes'),10)
        self.snapshot_compress_state:bool = _fallback(confi,('persist','snapshot_compress_state'),False)
        
        
        self.drain_extra_delimiters:list = _fallback(confi,('mask','extra_delimiters'),[])
        self.mask_prefix:str = _fallback(confi,('mask','extra_delimiters'),"<~")
        self.mask_suffix:str = _fallback(confi,('mask','extra_delimiters'),"~>")
        self.masking_instructions = []
        for i in _fallback(confi,('mask','regex_pattern_list'),[]):
            instruction = MaskingInstruction(i['regex_pattern'], i['mask_with'])
            self.masking_instructions.append(instruction)
            
        self.parameter_extraction_cache_capacity = _fallback(confi,('other','parameter_extraction_cache_capacity'),3000)
        self.parametrize_numeric_tokens = _fallback(confi,('other','parametrize_numeric_tokens'),True)
