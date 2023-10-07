from typing import Optional, List
import fnmatch

from .rooproc_hybrid_action import RooProcHybridAction

from quickstats.utils.common_utils import is_valid_file, filter_by_wildcards

class RooProcSave(RooProcHybridAction):
    
    def __init__(self, treename:str, filename:str, 
                 columns:Optional[List[str]]=None,
                 exclude:Optional[List[str]]=None,
                 frame:Optional[str]=None):
        super().__init__(treename=treename,
                         filename=filename,
                         columns=columns,
                         exclude=exclude,
                         frame=frame)
        
    @classmethod
    def parse(cls, main_text:str, block_text:Optional[str]=None):
        kwargs = cls.parse_as_kwargs(main_text)
        return cls(**kwargs)
    
    def _execute(self, rdf:"ROOT.RDataFrame", processor:"quickstats.RooProcessor", **params):
        treename = params['treename']
        filename = params['filename']
        if processor.cache and is_valid_file(filename):
            processor.stdout.info(f'INFO: Cached output from "{filename}".')
            return rdf, processor
        all_columns = [str(c) for c in rdf.GetColumnNames()]
        columns = params.get('columns', None)
        exclude = params.get('exclude', None)
        self.makedirs(filename)
        if isinstance(columns, str):
            columns = self.parse_as_list(columns)
        if columns is None:
            columns = list(all_columns)
        if exclude is None:
            exclude = []
        save_columns = filter_by_wildcards(all_columns, columns)
        save_columns = filter_by_wildcards(save_columns, exclude, exclusion=True)
        save_columns = list(set(save_columns))
        if processor.use_template:
            from quickstats.utils.root_utils import templated_rdf_snapshot 
            rdf_next = templated_rdf_snapshot(rdf, save_columns)(treename, filename, save_columns)
        else:
            rdf_next = rdf.Snapshot(treename, filename, save_columns)
        processor.stdout.info(f'Writing output to "{filename}".')
        return rdf_next, processor