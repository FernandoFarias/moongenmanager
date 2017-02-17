from mysql.connector import connect

from moongenmanager.evaluation import Descrption, Result


class Database:
    def __init__(self, *args, **kwargs):
        self.__connection = connect(**kwargs)
        self.__connection.autocommit = True

    def save(self, *args):
        for arg in args:
            if isinstance(arg, Descrption):
                query = self.__connection.cursor()
                _add_description = ("INSERT INTO evaluation"
                                    "(desc_create_time, operating_sytem, "
                                    "type_evaluation, desc_evaluation)"
                                    "VALUES "
                                    "(%(os_descr)s, %(time_create_descr)s, %(type_descr)s) ")
                query.execute(_add_description, arg.__dict__)
                id_descr = query.lastrowid
                arg.set_id(id_descr)
                query.close()
            elif isinstance(arg, Result):
                query = self.__connection.cursor()
                _add_measured = ("INSERT INTO measured "
                                 "(desc_evaluation_id, runtime, trail,"
                                 "pkt_size, avg, std, low_qtl, media_qtl,up_qtl)"
                                 "VALUES"
                                 "(%(id_descr)i, %(runtime_resul)i,%(trail_resul)i,"
                                 "%(avg_resul)f, %(std_resul)f, %(low_qtl_resul)f,"
                                 "%(median_qtl_resul)f, %(up_qtl_resul)f)")

                query.execute(_add_measured, arg.__dict__)
                id_resul = query.lastrowid
                arg.set_id(id_resul)
                query.close()
            else:
                raise TypeError('Type object unknown')

        def delete(self, table, id):

            query = self.__connection.cursor()
            _del_action = ("DELETE FROM %s WHERE id=%i" % (table, id))
            query.execute(_del_action)
            query.close()
