import json
import sqlalchemy as sa
from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            dt_dict = {}
            for field in [fld for fld in dir(obj) if not fld.startswith('_') and fld != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    dt_dict[field] = data
                except TypeError:
                    dt_dict[field] = None
            return dt_dict
        return json.JSONEncoder.default(self,obj)

# example: students = session.execute(sa.select(Student).where(Student.actual_SAT > 1000))
# json_payload = json.dumps(students, cls=AlchemyEncoder)