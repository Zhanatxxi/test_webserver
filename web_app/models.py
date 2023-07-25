from db.base_model import Model

from sqlalchemy import Column, UUID, DateTime


class Image(Model):
    uuid = Column(UUID, primary_key=True)
    upload_date = Column(DateTime)
    finished_date = Column(DateTime)
    last_upload_date = Column(DateTime)
