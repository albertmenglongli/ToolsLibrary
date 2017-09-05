'''
Usages:
db_config = {
    'db_host': '***',
    'db_port': '5439',
    'db_username': '***',
    'db_password': '***',
    'db_database': '***'
}

with redshift_db_connect(db_config) as (conn, cur):
    select_str = 'select * from db_usage.s3_usage limit 10;'
    cur.execute(select_str)
    results = cur.fetchall()
    print results

'''

import contextlib


@contextlib.contextmanager
def redshift_db_connect(conf):
    import psycopg2 as pg

    def __get_db_config(conf):
        return dict(user=conf['db_username'],
                    password=conf['db_password'],
                    host=conf['db_host'],
                    database=conf['db_database'],
                    port=conf['db_port'])

    redshift_conn = pg.connect(**__get_db_config(conf))
    try:
        yield redshift_conn, redshift_conn.cursor()
    finally:
        redshift_conn.commit()
        redshift_conn.close()

