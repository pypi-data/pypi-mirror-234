from src.spaceandtime import SpaceAndTime, SXTBaseAPI

api = SXTBaseAPI()
sql = "Select 'complex \nstring   ' as A \n   \t from \n\t TableName  \n Where    A=1;"
newsql = api.prep_sql(sql)
newsql == "Select 'complex \nstring   ' as A from TableName Where A=1"

biscuits = sxt.user.base_api.prep_biscuits(['a',['b','c'], 'd'])
success, access_token = sxt.authenticate()




pass 