#!/usr/bin/python
from connectDatabase import Connect

class executeQuery:

    def __init__(self):
        print

    def query(self):

        con = Connect()

        query = con.cur()

        # execute a statement
        query.execute('SELECT fc.fator_detalhe_fator from fatores_contribuintes fc where fc.fator_detalhe_fator is not null '
                      'order by fc.codigo_ocorrencia desc'
                      )

        return query.fetchall()

    def insert(text_transformed):

        #monta string para fazer insert
        sql = """INSERT INTO public.resultado ( texto_transformado )
                     VALUES('%s');"""

        con = Connect()

        query = con.cur()

        # execute a statement
        print(sql %text_transformed)
        query.execute(sql %text_transformed)

        con.commit()

    def __del__(self):
        del self
