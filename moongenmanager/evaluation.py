import time
from datetime import datetime

from moongenmanager.database import Database


class Description:
    def __init__(self):
        self.__id_descr = ''
        self.os_descr = ''
        self.type_descr = ''
        self.time_create_descr = datetime. \
            fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


    def get_id(self):
        return self._id_descr

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
        self.__db = Database(**kwargs)
        self.__m_bin = kwargs.get('m_dir') + 'MoonGen/build/MoonGen'
        self.__m_config = ''
        self.__m_script = ''
        self.__descr = self.__set_description(self.__db,_kwargs.get('descr_obj'))

    def run(self):
        for p in self._pkt_size:

    def __set_description(db: Database, descr : Description):
        d = db.save(descr)
        return d
