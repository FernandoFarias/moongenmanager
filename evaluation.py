import time
from datetime import datetime

from moongenmanager.database import Database


class Descrption:
    def __init__(self, os_descr, type_descr):
        self.__id_descr = ''
        self.os_descr = os_descr
        self.time_create_descr = datetime. \
            fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        self.type_descr = type_descr

    def get_id(self):
        return self._id_descr

    def set_id(self, id):
        self.__id_descr = id


class Result:
    def __init__(self, *args, **kwargs):
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
        self._pkt_size = [64, 128, 256, 512, 1024, 1280, 1518, 9218]
        self._runtime = [30, 60, 120, 240, 480]
        self._trails = 20
        self._db = Database()

    def run(self, descr: Descrption):
        db
        for p in self._pkt_size:
