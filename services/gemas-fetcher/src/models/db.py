import mongoengine as me, os
from datetime import datetime

me.connect(host=os.getenv('MONGO_URI'))

class GemastikModel(me.Document):
    meta = {
        'abstract': True
    }
    
    created_at = me.DateTimeField(required=True, default=datetime.now)
    updated_at = me.DateTimeField(required=False)
    deleted_at = me.DateTimeField(required=False)

    pass