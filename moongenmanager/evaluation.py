import time
import moongenmanager
import subprocess
import logging

from datetime import datetime
from pathlib import Path




class Description:
    def __init__(self):
        
        self.__id_descr = 0
        self.os_descr = None
        self.type_descr = None
        self.eval_descr = None
        self.time_create_descr = datetime. \
            fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def get_id(self):
        return self.__id_descr

    def set_id(self, id):
        self.__id_descr = id


class Result:
    def __init__(self, **kwargs):
        self.__id_resul = 0
        self.id_descr = kwargs.get('id_descr')
        self.runtime_resul = kwargs.get('runtime_resul')
        self.trail_resul = kwargs.get('trail_resul')
        self.pkt_size_resul = kwargs.get('pkt_size_resul')
        self.avg_resul = kwargs.get('avg_resul')
        self.std_resul = kwargs.get('std_resul')
        self.low_qtl_resul = kwargs.get('low_qtl_resul')
        self.median_qtl_resul = kwargs.get('median_qtl_resul')
        self.up_qtl_resul = kwargs.get('up_qtl_resul')

    def set_id(self, id_resul):
        self.__id_resul = id_resul

    def get_id(self):
        return self.__id_resul


class Evaluation:

    def __init__(self, **kwargs):
        
        self.logger = logging.getLogger("moongenmanager.evaluation")
        self.pkt_size = [64, 128, 256, 512, 1024, 1280, 1518, 9218]
        self.runtime = [30, 60, 120, 240, 480]
        self.trails = 20
        self.config_db = kwargs.get('config_db')
        self.m_bin = kwargs.get('m_dir') + 'MoonGen/build/MoonGen'
        self.m_config = kwargs.get('m_dir') + 'trafficgen.lua'
        self.m_script = kwargs.get('m_dir') + 'opnfv-vsperf-cfg.lua'
        self.descr = kwargs.get('descr_obj')

    def start(self):
        
        self.descr = self.__set_description()
        
        for p in self.pkt_size:
            for rt in self.runtime:
                self.__runner(self.trails, p, rt)
                

    def __set_result(self, result: Result):

        
        db = moongenmanager.database.Database(**self.config_db)
        db.save(result)
        db.close()

    def __runner(self, trails, pkt_size, runtime):

        for trail in range(1, trails):
            result = moongenmanager.evaluation.Result()
            result.id_descr = int(self.descr.get_id())
            result.runtime_resul = int(runtime)
            result.pkt_size_resul = int(pkt_size)
            result.trail_resul = int(trail)
            self.logger.info("## Creating new evaluation with: ID (%s)", self.descr.get_id())
            self.logger.info("#= ID:       %s", self.descr.get_id())
            self.logger.info("#= Trail:    %s", trail)
            self.logger.info("#= Size:     %s", pkt_size)
            self.logger.info("#= Runtime:  %s", runtime)

            try:
                self.__config_eval(pkt_size, runtime)
            except RuntimeError as r_error:
                print(r_error)

            p1 = subprocess.Popen(
                ['/usr/src/lua-trafficgen/MoonGen/build/MoonGen', '/usr/src/lua-trafficgen/trafficgen.lua'],
                stdout=subprocess.PIPE)

            p2 = subprocess.Popen(['grep', 'Histogram'], stdin=p1.stdout, stdout=subprocess.PIPE)
            p1.stdout.close()
            output = p2.communicate()[0]

            result = self.__get_result(result, output.decode())
            self.logger.info("#= Results     ")
            self.logger.info("#= AVG:      %s ns", result.avg_resul)
            self.logger.info("#= STD:      %s ns", result.std_resul)
            self.logger.info("#= QTL       %s/%s/%s ns", result.low_qtl_resul,
                              result.median_qtl_resul, result.up_qtl_resul)
            self.__set_result(result)
            

    def __config_eval(self, size, runtime):

        conf = ("VSPERF {"
                "nrFlows = 1024,"
                "testType = \"latency\","
                "latencyRunTime = %i,"
                "runBidirec = false,"
                "searchRunTime = 120,"
                "validationRunTime = 120,"
                "acceptableLossPct = 0.002,"
                "frameSize = %i,"
                "mppsPerQueue = 5,"
                "queuesPerTask = 3,"
                "ports = {0,1}"
                "}" %(runtime+6, size))

        if Path(self.m_script).exists():
            f = open(self.m_script, 'w')
            f.write(conf)
            f.close()
        else:
            raise RuntimeError("Cannot access file")

    def __get_result(self, result: Result, output=''):

        o = output.split(",")

        result.avg_resul = float(o[1].strip().split(" ")[1])
        result.std_resul = float(o[2].strip().split(" ")[1])

        qtl = o[3].strip().split(" ")[1]

        result.low_qtl_resul = float(qtl.split("/")[0])
        result.median_qtl_resul = float(qtl.split("/")[1])
        result.up_qtl_resul = float(qtl.split("/")[2])

        return result

    def __set_description(self):

        db = moongenmanager.database.Database(**self.config_db)
        d = Result()
        d = db.save(self.descr)
        db.close()
        return d





































