import time
import moongenmanager


from datetime import datetime
from subprocess import check_output
from pathlib import Path


class Description:
    def __init__(self):
        self.__id_descr = ''
        self.os_descr = ''
        self.type_descr = ''
        self.time_create_descr = datetime. \
            fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def get_id(self):
        return self.__id_descr

    def set_id(self, id):
        self.__id_descr = id


class Result:
    def __init__(self, **kwargs):
        self.__id_resul = ''
        self.id_descr = kwargs.get('id_descr')
        self.runtime_resul = kwargs.get('runtime_resul')
        self.trail_resul = kwargs.get('trail_resul')
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
        self.__pkt_size = [64, 128, 256, 512, 1024, 1280, 1518, 9218]
        self.__runtime = [30, 60, 120, 240, 480]
        self.__trails = 20
        self.__config_db = kwargs.get('config_db')
        self.__m_bin = kwargs.get('m_dir') + 'MoonGen/build/MoonGen'
        self.__m_config = kwargs.get('m_dir') + 'trafficgen.lua'
        self.__m_script = kwargs.get('m_dir') + 'opnfv-vsperf-cfg.lua'
        self.__descr = self.__set_description(kwargs.get('descr_obj'))

    def start(self):
        for p in self.__pkt_size:
            for rt in self.__runtime:
                self.__runner(self.__trails, p, rt)

    @staticmethod
    def __set_description(self, descr: Description):

        db = moongenmanager.database.Database(**self.__config_db)
        d = db.save(descr)
        db.close()
        return d

    def __set_result(self, result: Result):

        db = moongenmanager.database.Database(**self.__config_db)
        db.save(result)
        db.close()

    def __runner(self, trails, pkt_size, runtime):

        r = moongenmanager.evaluation.Result()

        for r in range(1, trails):
            try:
                self.__config_eval(pkt_size, runtime)
            except RuntimeError as r:
                print(r)

            output = check_output(self.__m_bin + " " + self.__m_config+"  | grep Histogram")

            r = self.__get_result(output)

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

        if Path(self.__m_script).exists():
            f = open(self.__m_script, 'w')
            f.write(conf)
            f.close()
        else:
            raise RuntimeError("Cannot access file")

    def __get_result(self, output=''):

        result = moongenmanager.evaluation.Result()
        o = output.split(",")
        result.avg_resul = o[1].strip().split(" ")[1]
        result.std_resul = o[2].strip().split(" ")[1]

        qtl = o[3].strip().split(" ")[1]

        result.low_qtl_resul = qtl.split("/")[0]
        result.median_qtl_resul = qtl.split("/")[1]
        result.up_qtl_resul = qtl.split("/")[2]

        result.id_descr = self.__descr.get_id()

        return result


































