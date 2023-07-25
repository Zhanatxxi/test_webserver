from db.base_model import Model

from sqlalchemy import Column, UUID, DateTime, String


class Image(Model):
    uuid = Column(UUID, primary_key=True)
    extension_type = Column(String)
    upload_date = Column(DateTime)
    finished_date = Column(DateTime)
    last_upload_date = Column(DateTime)

