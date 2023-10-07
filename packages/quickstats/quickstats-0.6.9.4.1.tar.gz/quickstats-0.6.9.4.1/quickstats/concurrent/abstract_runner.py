import os
from typing import Optional, Union, Dict, List, Any
from quickstats import semistaticmethod, AbstractObject, Timer
from quickstats.concurrent.logging import standard_log
from quickstats.utils.common_utils import execute_multi_tasks, is_valid_file

class AbstractRunner(AbstractObject):
    
    @property
    def config(self):
        return self._config
    
    def __init__(self, parallel:int=-1,
                 save_log:bool=True, cache:bool=True,
                 verbosity:Optional[Union[int, str]]="INFO"):
        super().__init__(verbosity=verbosity)

        self._config = {
            'cache': cache,
            'parallel': parallel,
            'save_log': save_log
        }

    def _prerun_batch(self):
        pass

    @semistaticmethod
    def _prerun_instance(self, **kwargs):
        pass
    
    @semistaticmethod
    def _run_instance(self, **kwargs):
        raise NotImplementedError
    
    @semistaticmethod
    def _cached_return(self, outname:str):
        raise NotImplementedError
        
    def _end_of_instance_cleanup(self):
        pass

    @semistaticmethod
    def get_instance_outpath(self, kwargs:Dict):
        outpath = kwargs.get("outname", None)
        return outpath

    @semistaticmethod
    def get_instance_logpath(self, kwargs:Dict):
        outpath = self.get_instance_outpath(kwargs)
        if outpath:
            return os.path.splitext(outpath)[0] + ".log"
        return None

    def _is_valid_cache(self, cached_result):
        return True
        
    def run_instance(self, kwargs:Dict[str, Any]):
        self._prerun_instance(**kwargs)
        outpath = self.get_instance_outpath(kwargs)
        
        if outpath and (self.config['cache'] and os.path.exists(outpath) and is_valid_file(outpath)):
            try:
                cached_result = self._cached_return(outpath)
                self.stdout.info(f"Cached output from {outpath}")
                if self._is_valid_cache(cached_result):
                    return cached_result
            except:
                self.stdout.info(f'Broken output: {outpath}. Retrying')
                pass
        
        logpath = self.get_instance_logpath(kwargs)
        if (logpath and self.config['save_log']) and (self.stdout.verbosity != 'DEBUG'):
            with standard_log(logpath) as logger:
                result = self._run_instance(**kwargs)
        else:
            result = self._run_instance(**kwargs)
            
        self._end_of_instance_cleanup()
        
        return result
        
    def run_batch(self, argument_list, auxiliary_args:Optional[Dict]=None):
        parallel = self.config['parallel']
        with Timer() as t:
            self._prerun_batch()
            raw_result = execute_multi_tasks(self.run_instance, argument_list, parallel=parallel)
            results = self.postprocess(raw_result, auxiliary_args)        
        self.stdout.info(f'All jobs have finished. Total time taken: {t.interval:.3f} s')
        return results
    
    def run(self):
        argument_list, auxiliary_args = self.prepare_task_inputs()
        return self.run_batch(argument_list, auxiliary_args=auxiliary_args)
    
    def prepare_task_inputs(self):
        raise NotImplementedError
    
    def postprocess(self, raw_result, auxiliary_args:Optional[Dict]=None):
        return raw_result