from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)


class Cache(db.Model):
    __tablename__ = 'cacheDB'
    cacheID = db.Column(db.String(80), primary_key=True)
    nodeName = db.Column(db.String(80), nullable=False)
    highAvailabilityMode = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    comment = db.Column(db.String(80), nullable=False)
    creationDate = db.Column(db.String(80), nullable=False)
    modificationDate= db.Column(db.String(80), nullable=False)
    asset_status = db.Column(db.String(80), nullable=False)
    ip = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    availabilityZone = db.Column(db.String(80), nullable=False)
    network = db.Column(db.String(80), nullable=False)

    def json(self):
        return {
            "cacheID": self.cacheID,
            "nodeName": self.nodeName,
            "highAvailabilityMode": self.highAvailabilityMode,
            "status": self.status,
            "comment": self.comment,
            "creationDate": self.creationDate,
            "modificationDate": self.modificationDate,
            "asset_status": self.asset_status,
            "ip": self.ip,
            "type": self.type,
            "availabilityZone": self.availabilityZone,
            "network": self.network
        }

    def add_instance(_cacheID, _nodeName, _highAvailabilityMode, _status, _comment, _creationDate, _modificationDate, _asset_status, _ip, _type, _availabilityZone, _network):
        new_cache = Cache(cacheID=_cacheID, nodeName=_nodeName, highAvailabilityMode=_highAvailabilityMode, status=_status, comment=_comment, creationDate=_creationDate, modificationDate=_modificationDate, asset_status=_asset_status, ip=_ip, type=_type, availabilityZone=_availabilityZone, network=_network)
        db.session.add(new_cache)
        db.session.commit()
        return new_cache

    def get_all_cache():
        return [Cache.json(cache_inst) for cache_inst in Cache.query.all()]
        # return Cache.query.all()

    def get_cache_by_id(_cacheID):
        return Cache.json(Cache.query.filter_by(cacheID=_cacheID).first())

    def get_cache_by_name(_nodeName):
        return Cache.json(Cache.query.filter_by(nodeName=_nodeName).first())

    def get_cache_by_ip(_ip):
        return Cache.json(Cache.query.filter_by(ip=_ip).first())

    def delete_cache_by_id(_cacheID):
        is_successful = Cache.query.filter_by(cacheID=_cacheID).delete()
        db.session.commit()
        return _cacheID

    def delete_cache_by_name(_nodeName):
        is_successful = Cache.query.filter_by(nodeName=_nodeName).delete()
        db.session.commit()
        return bool(is_successful)

    def delete_cache_by_ip(_ip):
        is_successful = Cache.query.filter_by(ip=_ip).delete()
        db.session.commit()
        return bool(is_successful)

    def update_name(_cacheID, _nodeName):
        cache_to_update = Cache.query.filter_by(cacheID=_cacheID).first()
        cache_to_update.nodeName = _nodeName
        db.session.commit()
        return cache_to_update

    # def __repr__(self):
    #     cache_instance = {
    #         "cacheID": self.cacheID,
    #         "nodeName": self.nodeName,
    #         "highAvailabilityMode": self.highAvailabilityMode,
    #         "status": self.status,
    #         "comment": self.comment,
    #         "creationDate": self.creationDate,
    #         "modificationDate": self.modificationDate,
    #         "asset_status": self.asset_status,
    #         "ip": self.ip,
    #         "type": self.type,
    #         "availabilityZone": self.availabilityZone,
    #         "network": self.network
    #     }
    #     return json.dumps(cache_instance)
