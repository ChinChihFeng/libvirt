from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, backref

Base = declarative_base()

class KVMHost(Base):
    __tablename__ = 'Host'
    
    id = Column(Integer, primary_key=True)
    hostname = Column(String)
    ip = Column(String)
    
    def __repr__(self):
        return "<KVMHost(hostname='%s', ip='%s')>" % (self.hostname, self.ip)
    
class GuestHost(Base):
    __tablename__ = 'Guest'
    
    host_id = Column(Integer, ForeignKey('Host.id'), primary_key=True)
    kvm_id = Column(Integer)
    guestname = Column(String, primary_key=True)
    ip = Column(String)
    status = Column(String)
    
    hosts = relationship("KVMHost", backref=backref('kvmhosts'))
    
    def __repr__(self):
        return "<GuestHost(host_id='%s', kvm_id='%s', guestname='%s', ip='%s', status ='%s')>" % (self.host_id, self.kvm_id, self.guestname, self.ip, self.status)
