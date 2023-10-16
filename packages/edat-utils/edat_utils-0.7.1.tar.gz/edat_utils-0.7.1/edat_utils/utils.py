from strawberry.types import Info
import re
from sqlalchemy.engine.row import Row
from typing import List
from edat_utils.schema import EdatGrouped

EDAT_USER = 'X-EDAT-USER'


class EdatUtils:
    @staticmethod
    def get_fields(info: Info):
        selected_fields = {item.name for field in info.selected_fields
                           for selection in field.selections for item in selection.selections}
        return selected_fields
    
    @staticmethod
    def get_user(info: Info):
        request = info.context['request']
        user =  None
        if EDAT_USER in request.headers:
            user = request.headers[EDAT_USER]
        return user
    
    def get_table_name(info: Info):
        name = list(info.return_type.__dict__['_type_definition'].type_var_map.values())[0].__name__
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    

    def get_list(info: Info, rows: List[Row]):
        obj_list = []

        class_ = list(info.return_type.__dict__['_type_definition'].type_var_map.values())[0]
        args = class_.__init__.__code__.co_varnames[1:]

        for row in rows:
            params = row._asdict()
            params_to_pass = {argname: params[argname] if argname in params else None  for argname in args}    
            instance = class_(**params_to_pass)
            obj_list.append(instance)
        return obj_list
    
    def is_grouped(info: Info):
        class_ = list(info.return_type.__dict__['_type_definition'].type_var_map.values())[0]
        return issubclass(class_, EdatGrouped)