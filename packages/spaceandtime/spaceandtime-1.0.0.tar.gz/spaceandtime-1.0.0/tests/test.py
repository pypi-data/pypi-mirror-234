import spaceandtime
from pprint import pprint 

pass

tbl = spaceandtime.SXTTable('Schema.MyTable',new_keypair=True)
tbl.add_biscuit('read', tbl.PERMISSION.SELECT)
tbl.add_biscuit('admin', tbl.PERMISSION.ALL)
tbl.create_ddl = tbl.create_ddl_sample

pprint( tbl.create_ddl )
pass 