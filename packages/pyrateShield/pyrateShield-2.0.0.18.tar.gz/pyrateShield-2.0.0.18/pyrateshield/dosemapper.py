import multiprocessing
from multiprocessing.sharedctypes import Value as mpValue
import ctypes
import queue
import time
import psutil

from pyrateshield.constants import CONSTANTS
from pyrateshield import labels
from pyrateshield.logger import Logger
from PyQt5.QtCore import QObject, pyqtSignal
from pyrateshield.radtracer import radtracer
from pyrateshield.pyshield.engine import Engine
import pandas as pd
from scipy.ndimage import zoom


NO_WORK = 0
DOSEMAP_WORK = 1
CRITICAL_POINT_WORK = 2


MAX_CORES = 8
LOG_LEVEL = Logger.LEVEL_DEBUG

UNSUPPORTED_PYSHIELD_ISOTOPES = ['Y-90']
CRITICAL_POINT_NAME         = 'Critical Point Name'
RADTRACER_DOSE              = 'RadTracer Dose [mSv]'
PYSHIELD_DOSE               = 'PyShield Dose [mSv]'
OCCUPANCY_FACTOR            = 'Occupancy factor'
RADTRACER_DOSE_CORRECTED    = 'RadTracer Dose corrected for occupancy [mSv]'
PYSHIELD_DOSE_CORRECTED     = 'PyShield Dose corrected for occupancy [mSv]'
SOURCE_NAME                 = 'Source Name'

COLUMNS = [CRITICAL_POINT_NAME, PYSHIELD_DOSE, RADTRACER_DOSE, 
           OCCUPANCY_FACTOR, PYSHIELD_DOSE_CORRECTED, RADTRACER_DOSE_CORRECTED]

SPLIT_COLUMNS = [CRITICAL_POINT_NAME, SOURCE_NAME, PYSHIELD_DOSE, 
                 RADTRACER_DOSE, OCCUPANCY_FACTOR, 
                 RADTRACER_DOSE_CORRECTED, PYSHIELD_DOSE_CORRECTED]

def resize_array(source_array, target_shape):
    # Need faster method for painting dosemap on top of the floorplan.
    # Obtain same size by interpolation
    zoom_factors = [float(t) / s for s, t in zip(source_array.shape, target_shape)]
    resized_array = zoom(source_array, zoom_factors, order=1)
    return resized_array

def is_supported_by_pyshield(src):
    supported = CONSTANTS.pyshield_supported_isotopes
    return src.label == labels.SOURCES_NM and src.isotope in supported


def is_supported_by_radtracer(src):
    supported = CONSTANTS.radtracer_supported_isotopes
    return src.label != labels.SOURCES_NM or src.isotope in supported


def get_radtracer_dosemap(source, project, pyshield_engine):
    if is_supported_by_radtracer(source):
        return radtracer.dosemap_single_source(source, project)
    elif is_supported_by_pyshield(source): # fallback to pyshield
        print(f'Source {source.name} not supported by radtracer, will use pyshield')   
        return pyshield_engine.source_dosemap(source)

def get_pyshield_dosemap(source, project, pyshield_engine):
    if is_supported_by_pyshield(source):    
        return pyshield_engine.source_dosemap(source)
    elif is_supported_by_radtracer(source): # fallback to radtracer
        # Xray will go through radtracer any how no need to warn
        if source.label == labels.SOURCES_NM:
            print(f'Source {source.name} not supported by pyshield, will use radtracer')
        return radtracer.dosemap_single_source(source, project)
    
def get_dosemap(source, project, pyshield_engine=None):
    if pyshield_engine is None:
        pyshield_engine = Engine.from_pyrateshield(project)
    # Pyshield set as engine
    if project.dosemap.engine == labels.PYSHIELD:
        return get_pyshield_dosemap(source, project, pyshield_engine=pyshield_engine)
    # Radtracer set as engine
    elif project.dosemap.engine == labels.RADTRACER:
        return get_radtracer_dosemap(source, project, pyshield_engine=pyshield_engine)

def empty_critical_point_format():
    return pd.DataFrame([{CRITICAL_POINT_NAME:      None,
                          SOURCE_NAME:              None,
                          RADTRACER_DOSE:           None,
                          PYSHIELD_DOSE:            None,
                          OCCUPANCY_FACTOR:         None,
                          RADTRACER_DOSE_CORRECTED: None,
                          PYSHIELD_DOSE_CORRECTED:  None
                          }])

def source_critical_point_format(source, 
                                 critical_point, 
                                 dose_radtracer, 
                                 dose_pyshield):
    
    factor = critical_point.occupancy_factor
    
    return {CRITICAL_POINT_NAME:        critical_point.name,
            SOURCE_NAME:                source.name,
            RADTRACER_DOSE:             dose_radtracer,
            PYSHIELD_DOSE:              dose_pyshield,
            OCCUPANCY_FACTOR:           factor,
            RADTRACER_DOSE_CORRECTED:   factor * dose_radtracer,
            PYSHIELD_DOSE_CORRECTED:    factor * dose_pyshield}
                          
def get_critical_point_for_source(project, critical_point, source,
                                  engine=labels.RADTRACER,
                                  pyshield_engine=None):
    
    if engine == labels.PYSHIELD and pyshield_engine is None:
        pyshield_engine = Engine.from_pyrateshield(project)
    
    def get_radtracer_dose(source):
        return radtracer.pointdose_single_source(
            critical_point.position, source, project)
    
    def get_pyshield_dose(source):
        return pyshield_engine.dose_at_point(
                critical_point.position, sources=[source])
    
    if not is_supported_by_pyshield(source)\
        and not is_supported_by_radtracer(source):
        raise RuntimeError('Unsupported source!')
        
    if engine == labels.PYSHIELD and is_supported_by_pyshield(source):
        dose = get_pyshield_dose(source)
    elif engine == labels.PYSHIELD:
        dose = get_radtracer_dose(source)
    elif engine == labels.RADTRACER and is_supported_by_radtracer(source):
        dose = get_radtracer_dose(source)
    elif engine == labels.RADTRACER:
        dose = get_pyshield_dose(source)
    return dose
    

def get_critical_point(project, critical_point, 
                       engine=labels.RADTRACER,
                       pyshield_engine=None,
                       sum_dose = True):
    
    sources = Dosemapper.project_sources(project)
    
    total_dose = {}
    for source in sources:
        dose = get_critical_point_for_source(project, critical_point, source, 
                                             engine=engine, 
                                             pyshield_engine=pyshield_engine)
        
        total_dose[(source.label, source.name)] = dose
    
    if sum_dose:
        total_dose = sum(total_dose.values())
        
    return total_dose


def get_formatted_critical_point_result(project, critical_point, source, 
                                        pyshield_engine=None):
    
    dose_pyshield = get_critical_point_for_source(
        project, critical_point, source,
        engine=labels.PYSHIELD,
        pyshield_engine=pyshield_engine)
        
    dose_radtracer = get_critical_point_for_source(
        project, critical_point, source,
        engine=labels.RADTRACER,
        pyshield_engine=pyshield_engine)
   
    formatted = source_critical_point_format(
        source, critical_point, 
        dose_radtracer=dose_radtracer,
        dose_pyshield=dose_pyshield)
    
    return formatted
    
class Worker(multiprocessing.Process):
    def __init__(self, project_queue, work_queue, 
                 source_queue, workt_type, update_flag, stop_flag):
        multiprocessing.Process.__init__(self)
        
   
        
        self.project_queue = project_queue
        
        self.source_queue = source_queue
        
        self.work_type = workt_type
        
        self.work_queue = work_queue
       
        self.update_flag = update_flag
        
        self.stop_flag = stop_flag      
        
    
    def update_project(self):
        
        if self.update_flag.value:        
        
            self.project = self.project_queue.get(timeout=2)
      
            self.pyshield_engine = Engine.from_pyrateshield(self.project)
        
        self.update_flag.value = False
        
    def run(self):
        while not self.stop_flag.value:  
            work_type = self.work_type.value
            if self.update_flag.value:
                self.update_project()
                
            if work_type == NO_WORK:
                time.sleep(0.1)
               
            elif work_type > NO_WORK and not self.source_queue.empty(): 
                try:
                    sources = self.source_queue.get(timeout=0.1)
                    # work type changed during time out 
                    if work_type != self.work_type.value:
                        self.source_queue.put(sources)
                        continue
                except queue.Empty:
                    continue

                
                for source in sources:
                    if work_type == DOSEMAP_WORK:

                        self.work_queue.put(get_dosemap(source, self.project))
                        
                    elif work_type == CRITICAL_POINT_WORK:
                        self.work_queue.put(self.get_critical_points(source))
                    else:
                        raise RuntimeError
                
        
            
    def get_critical_points(self, source):
        results = []
        for critical_point in self.project.critical_points:
            result = get_formatted_critical_point_result(self.project, 
                                                         critical_point, 
                                                         source,
                                                pyshield_engine=self.pyshield_engine)
            results.append(result)
        return results
    

   

class Dosemapper(QObject):
    _workers = None
    _work_queue = None
    _max_cpus = MAX_CORES
    _source_queue = None
    _cpus = None
    progress = pyqtSignal(float)
    calculation_time = pyqtSignal(float)
    interpolate = pyqtSignal(float)
    def __init__(self, multi_cpu=True):
        super().__init__()
        if not multi_cpu:
            self.set_cpus(1)

    
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._stop_workers(self._workers)
       
    def source_queue(self):
        if self._source_queue is None:
            self._source_queue = multiprocessing.Queue()
        return self._source_queue
    
    def work_queue(self):
        if self._work_queue is None:
            self._work_queue  = multiprocessing.Queue()
        return self._work_queue
    
    def set_cpus(self, cpus=None):
        if self._cpus != cpus:
            self._cpus = cpus
            
    def cpus(self):
        if self._cpus is None:
            max_cpus = psutil.cpu_count(logical=False)
            self._cpus = min(max_cpus, self._max_cpus)
            self._cpus = max(self._cpus, 1)
        return self._cpus
    
    def update_workers(self, project=None, work_type=None):
        
        while len(self.workers()) < self.cpus():
            self.workers().append(self._new_worker())
            
        while len(self.workers()) > self.cpus():
           
            self._stop_worker(self.workers()[0])
            
            self._workers.remove(self._workers[0])
        
        while any(w.update_flag.value for w in self.workers()):
            time.sleep(0.1)
        
        if project is not None:
            for w in self.workers():
                w.project_queue.put(project)
                w.work_type.value = work_type if work_type is not None else 0
                w.update_flag.value = True
        
        if work_type is not None:
            for w in self.workers():
                w.work_type.value = work_type
            
        return self.workers()
    
    def workers(self):
        if self._workers is None:
            self._workers = []
        return self._workers
    
    def _new_worker(self):
        project_queue   = multiprocessing.Queue()
        stop_flag       = mpValue(ctypes.c_bool, False)
        update_flag     = mpValue(ctypes.c_bool, False)
        work_type       = mpValue(ctypes.c_int8, NO_WORK)
        args = (
            project_queue,
            self.work_queue(),
            self.source_queue(),
            work_type,
            update_flag,
            stop_flag,
        )
        p = Worker(*args)            
        p.start()
        return p

    def _stop_worker(self, worker):
        worker.stop_flag.value = True
        worker.join()
        time.sleep(0.1)
        if worker.is_alive():
            worker.close()
    
    def _stop_workers(self, workers):
        while workers is not None and len(workers) > 0:
            self._stop_worker(workers[0])
            workers.remove(workers[0])

   
    @staticmethod
    def project_sources(project):
        sources = list(project.sources_nm) + list(project.sources_ct)\
            + list(project.sources_xray)
        return [source for source in sources if source.enabled]
        
        
   
    def get_single_cpu_dosemap(self, project, sources=None):
        # DEBUGGING Purpuses
    
        start = time.time()
        dosemap = None        
        update_dosemap = lambda dm: dm if dosemap is None else (dosemap + dm)
            
        
        sources = Dosemapper.project_sources(project)
        
        pyshield_engine = Engine.from_pyrateshield(project)
         
        for i, source in enumerate(sources):
            source_dosemap = get_dosemap(source, project, pyshield_engine=pyshield_engine)
            self.progress.emit(i/len(sources))
            
            dosemap = update_dosemap(source_dosemap)
        
        stop = time.time()
        self.progress.emit(1)
        self.calculation_time.emit(stop-start)
        
        if project.dosemap_style.interpolate:
            self.interpolate.emit(-1)
            start = time.time()
            dosemap = resize_array(dosemap, project.floorplan.image.shape)
            stop = time.time()
            
            self.interpolate.emit(stop-start)
            
            
            
        return dosemap
 
    def get_critical_point(self, project, sources=None):
        if sources is None:
            sources = self.project_sources(project)
        
        src_pos_dct = {}

        for source in sources:
            # Make a dictionary of source_positions and group the corresponding sources
            # I.e.: { (x,y,z): [src1, src2, src3 ], (x,y,z): [src4, src5, ... ] }
            src_pos_dct.setdefault(tuple(source.position), []).append(source)
            
        sources_grouped = [srcs for srcs in src_pos_dct.values()]
        
        self.update_project(project)
        
        for grp in sources_grouped:
            self.source_queue().put(grp)
            
        
    def get_dosemap(self, project, sources=None):
        #print(f'Using engine: {project.dosemap.engine}')
        
        
        if self.cpus() == 1 or not project.dosemap_style.multi_cpu:
            return self.get_single_cpu_dosemap(project, sources)
        
        start = time.time()
      
        self.update_workers(project=project)
        
        
        
        if sources is None:
            sources = self.project_sources(project)
     
        
        # Check if there is any work to be done
        if not len(sources):
            return None

        
        # Sources with the same position are processed by the same worker.
        # This allows PyShield to benefit from caching.
        # MS: Group sources by default won't affect radtracer
            
        src_pos_dct = {}

        for source in sources:
            # Make a dictionary of source_positions and group the corresponding sources
            # I.e.: { (x,y,z): [src1, src2, src3 ], (x,y,z): [src4, src5, ... ] }
            src_pos_dct.setdefault(tuple(source.position), []).append(source)
            
        sources_grouped = [srcs for srcs in src_pos_dct.values()]

        
        self.update_workers(work_type=DOSEMAP_WORK)
        
        for grp in sources_grouped:
            self.source_queue().put(grp)
            
        
        # Collect the results. Make sure to get as many results from the queue
        # as the number of sources
        nr_of_sources = sum(len(grp) for grp in sources_grouped)
                
        dosemap = None        
        update_dosemap = lambda dm: dm if dosemap is None else (dosemap + dm)
       

        self.progress.emit(0)
        for i in range(nr_of_sources):
            dosemap = update_dosemap(self.work_queue().get())
            self.progress.emit(i/nr_of_sources)
        
        stop = time.time()
        
        self.progress.emit(1)
        self.calculation_time.emit(stop-start)
        self.update_workers(work_type=NO_WORK)
        
        if not self.work_queue().empty(): raise RuntimeError()
        
        if project.dosemap_style.interpolate:
            self.interpolate.emit(-1)
            start = time.time()
            dosemap = resize_array(dosemap, project.floorplan.image.shape)
            stop = time.time()
            
            self.interpolate.emit(stop-start)
        return dosemap        
    
    def get_critical_points(self, project, sum_sources=True):
    
        
        
        self.update_workers(project=project)
       
        
        sources = self.project_sources(project)
        
        
        if not len(sources):
            return empty_critical_point_format()
       
        
        if self.cpus() == 1 or not project.dosemap_style.multi_cpu:
            start = time.time()
            results = []
            pyshield_engine = Engine.from_pyrateshield(project)
            self.progress.emit(0)
            for i, source in enumerate(sources): 
                for critical_point in project.critical_points:
                    result = get_formatted_critical_point_result(project, critical_point, source,
                                                                 pyshield_engine=pyshield_engine)
                    results += [result]
                    self.progress.emit(i/len(sources))
            stop = time.time()
            self.calculation_time.emit(stop-start)
            self.progress.emit(1)
            
        else:
            start = time.time()
            
            src_pos_dct = {}
            
            for source in sources:
                # Make a dictionary of source_positions and group the corresponding sources
                # I.e.: { (x,y,z): [src1, src2, src3 ], (x,y,z): [src4, src5, ... ] }
                src_pos_dct.setdefault(tuple(source.position), []).append(source)
           
            sources_grouped = [srcs for srcs in src_pos_dct.values()]
            
            
            
            for grp in sources_grouped:
                self.source_queue().put(grp)
            
            
            
            nr_of_sources = sum(len(grp) for grp in sources_grouped)
            
            
           
            
            
            results = None
            
            update_results = lambda result: result if results is None else (results+result)
          
            self.progress.emit(0)
            
            self.update_workers(work_type=CRITICAL_POINT_WORK)
           
            for i in range(nr_of_sources):
                result = self.work_queue().get()
                
                results = update_results( result)    
                
                self.progress.emit(i/nr_of_sources)
            stop = time.time()
            self.calculation_time.emit(stop-start)
            self.progress.emit(1)
            self.update_workers(work_type=NO_WORK)
            
        report = pd.DataFrame(results)[SPLIT_COLUMNS]
        
        if sum_sources:
            aggfunc = {RADTRACER_DOSE: sum, RADTRACER_DOSE_CORRECTED: sum,
                       PYSHIELD_DOSE: sum, PYSHIELD_DOSE_CORRECTED: sum,
                       OCCUPANCY_FACTOR: max}
                
            report = pd.pivot_table(report, index=CRITICAL_POINT_NAME, 
                                            aggfunc=aggfunc)
            
            # preserve order
            pnames = [crit_point.name for crit_point in project.critical_points\
                      if crit_point.enabled]
                
            report = report.reindex(pnames)
            
            report = report.reset_index()
           
            report = report[COLUMNS]
            
       
        
        return report
            
    
    # @staticmethod
    # def get_sources_critical_points(project, sum_sources=True):
    #     sources = list(project.sources_nm) + list(project.sources_ct) + list(project.sources_xray)
        
    #     # Exclude sources which are not set to Enabled
    #     sources = [src for src in sources if src.enabled]
        
    #     # Exclude points which are not set to Enabled
    #     crit_points = [crp for crp in project.critical_points if crp.enabled]
                
    #     if len(crit_points) == 0 or len(sources) == 0:            
    #         return Dosemapper.empty_critical_point_result()
        
    #     reports = []        
        
    #     pyshield_engine = Engine.from_pyrateshield(project)
        
    #     for crit_point in crit_points:            
    #         for source in sources:
    #             if is_supported_by_radtracer(source):
    #                 dose_radtracer = radtracer.pointdose_single_source(
    #                     crit_point.position, source, project)
    #             else:
    #                 # At least one isotope not supported by radtracer
    #                 dose_radtracer = None
                
    #             if is_supported_by_pyshield(source):
    #                 dose_pyshield = pyshield_engine.dose_at_point(crit_point.position,
    #                                                      sources=[source])
    #             else:
    #                 dose_pyshield = None
                    
    #             if dose_radtracer is None and dose_pyshield is None:
    #                 raise RuntimeError
    #             elif dose_radtracer is None:
    #                 dose_radtracer = dose_pyshield
    #             elif dose_pyshield is None:
    #                 dose_pyshield = dose_radtracer
                    
                
    #             reports += [Dosemapper.get_source_critical_point_result(
    #                 source, crit_point, dose_radtracer, dose_pyshield)]
    #     report = pd.DataFrame(reports)[SPLIT_COLUMNS]
        
    #     if sum_sources:
    #         aggfunc = {RADTRACER_DOSE: sum, RADTRACER_DOSE_CORRECTED: sum,
    #                    PYSHIELD_DOSE: sum, PYSHIELD_DOSE_CORRECTED: sum,
    #                    OCCUPANCY_FACTOR: max}
                
    #             report = pd.pivot_table(report, index=CRITICAL_POINT_NAME, 
    #                                             aggfunc=aggfunc)
                
    #             # preserve order
    #             pnames = [crit_point.name for crit_point in project.critical_points\
    #                       if crit_point.enabled]
                    
    #             report = summed_report.reindex(pnames)
                
    #             report = summed_report.reset_index()
               
    #             report = summed_report[COLUMNS]
                
        
    #     return report
        
    # @staticmethod
    # def get_critical_points(project):
        
        
    #     if len(project.sources_nm) + len(project.sources_ct) + len(project.sources_xray) == 0\
    #         or len(project.critical_points) == 0:
    #             return Dosemapper.empty_critical_point_result()
            
    #     report = Dosemapper.get_sources_critical_points(project)
        
    #     aggfunc = {RADTRACER_DOSE: sum, RADTRACER_DOSE_CORRECTED: sum,
    #                PYSHIELD_DOSE: sum, PYSHIELD_DOSE_CORRECTED: sum,
    #                OCCUPANCY_FACTOR: max}
        
    #     summed_report = pd.pivot_table(report, index=CRITICAL_POINT_NAME, 
    #                                    aggfunc=aggfunc)
        
    #     # preserve order
    #     pnames = [crit_point.name for crit_point in project.critical_points\
    #               if crit_point.enabled]
            
    #     summed_report = summed_report.reindex(pnames)
        
    #     summed_report = summed_report.reset_index()
       
    #     summed_report = summed_report[COLUMNS]
    #     return summed_report

    
        
            
if __name__ == "__main__":
    from pyrateshield.model import Model
    import timeit
    import time
    #model = Model.load_from_project_file('/Users/marcel/git/pyrateshield/example_projects/LargeProject/large_project.psp')
    #model = Model.load_from_project_file('../example_projects/LargeProject/project.zip')
    model = Model.load_from_project_file('../example_projects/SmallProject/project.zip')
    #model = Model.load_from_project_file('../example_projects/Stabin/Tb-161.zip')
    #model = Model.load_from_project_file('../example_projects/Lu-177.psp')
    model.dosemap.grid_matrix_size = 120
    
    
    
        
    with Dosemapper(multi_cpu=True) as dm:   
        dm.progress.connect(print)
        model.dosemap.engine = labels.PYSHIELD
        #dm = dm.get_dosemap(model)
        #print("PyShield", timeit.timeit(lambda: dm.get_dosemap(model), number=1) )
        print("PyShield", timeit.timeit(lambda: dm.get_dosemap(model), number=1) )
    
        #time.sleep(1) 
        #print()
        
        model.dosemap.engine = labels.RADTRACER
        #print("Radtracer", timeit.timeit(lambda: dm.get_dosemap(model), number=1) )
        #print("Radtracer", timeit.timeit(lambda: dm.get_dosemap(model), number=1) )
        #results = dm.get_critical_points(model)
        print(timeit.timeit(lambda: dm.get_critical_points(model), number=1))

    # from pyshield import Sources
    # sources = Sources.from_pyrateshield(model)
    # print("Pyshield single CPU:", end=" ", flush=True)
    # print(timeit.timeit(lambda: sources.get_dosemap(), number=1) )
    
    
    
    

