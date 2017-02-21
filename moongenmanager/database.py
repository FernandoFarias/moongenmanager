
from mysql.connector import connect

from moongenmanager.evaluation import Description, Result

class Database:
    def __init__(self, **kwargs):
        self.__connection = connect(**kwargs)
        self.__connection.autocommit = True

    def save(self, *args):
        for arg in args:
            if isinstance(arg, Description):
                query = self.__connection.cursor()
                _add_description = ("INSERT INTO evaluation"
                                    "(desc_create_time, operating_sytem, "
                                    "type_evaluation, desc_evaluation)"
                                    "VALUES "
                                    "(%(time_create_descr)s, %(os_descr)s, %(type_descr)s, %(eval_descr)s) ")
                query.execute(_add_description, arg.__dict__)
                id_descr = query.lastrowid
                arg.set_id(id_descr)
                query.close()
                return arg
            elif isinstance(arg, Result):
                try:
                    query = self.__connection.cursor()
                    _add_measured = ("INSERT INTO measured "
                                     "(desc_evaluation_id, runtime, trail,"
                                     "pkt_size, avg, std, low_qtl, media_qtl, up_qtl)"
                                     "VALUES"
                                     "(%(id_descr)s, %(runtime_resul)s, %(trail_resul)s, %(pkt_size_resul)s,"
                                     "%(avg_resul)s, %(std_resul)s, %(low_qtl_resul)s, %(median_qtl_resul)s,"
                                     "%(up_qtl_resul)s)")

                    query.execute(_add_measured, arg.__dict__)
                    id_resul = query.lastrowid
                    arg.set_id(id_resul)
                    query.close()
                    return arg
                except ValueError as vr:
                    print (vr)
            else:
                raise TypeError('Type object unknown')

    def delete(self, table, id):

        query = self.__connection.cursor()
        _del_action = ("DELETE FROM %s WHERE id=%i" % (table, id))
        query.execute(_del_action)
        query.close()

    def close(self):
        self.__connection.close()
