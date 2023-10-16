from potatoPostgreSQL import PosgreSQL

db = 'tokyo_ldd'
host = 'localhost'
user = 'tokyo_ldd'
pw = 'tokyo_ldd'
port = '5432'
schemas = 'tokyo_ldd'

connect = PosgreSQL(db,host,user,pw,port,schemas) 

query_tokyo = """
    SELECT td_tokyo.lid2, td_tokyo."WAFER_NUM_BOTTOM_50C", COUNT(*) as count_tokyo
    FROM td_tokyo
    LEFT JOIN td_check ON td_tokyo.lid2 = td_check.lotno AND td_tokyo."WAFER_NUM_BOTTOM_50C" = td_check.wno
    WHERE td_check.lotno IS NULL AND td_check.wno IS NULL
    GROUP BY td_tokyo.lid2, td_tokyo."WAFER_NUM_BOTTOM_50C"
"""

result_tokyo = connect.fetchall(query_tokyo)

for row in result_tokyo:
    print(row)


