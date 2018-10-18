from sqlalchemy import create_engine
from db import *
from models import *

engine = create_engine('postgresql://postgres@192.168.99.100:5432/kvm')
db = scoped_session(sessionmaker(bind=engine))

hostlist = []

for i in hostList:
    a = Host(i)
    info = []
    domainID = []
    hostname =  a.get_hostname()
    domainName = a.get_domain()
        
    """Check hostname whether is exist or not."""
    chkhostbyip = db.query(KVMHost).filter(KVMHost.ip == i).first()
    
    """Update hostname and insert into the table."""
    if chkhostbyip == None:
        kvmhost = KVMHost(hostname=hostname, ip=i)
        db.add(kvmhost)
    else:
        chkhostbyip.hostname = hostname
            
    """Find current host id from Host table."""
    hostid = db.query(KVMHost.id).filter(KVMHost.ip == i).one()

    for i in domainName:
        domainID.append(a.get_domainID(i))
    for i in range(len(domainName)):
        domainID[i][0].update({'name': domainName[i]})

    #print(domainID)
    #print(domainName)

    for i in range(len(domainID)):
        if domainID[i][0]['state'] == 'RUNNING':
            inet = a.retrive_interface(domainName[i])
            data = {'hostname': hostname, 'id': domainID[i][0]['id'], 'name': domainID[i][0]['name'], 'ip': inet , 'status': domainID[i][0]['state']}
            info.append(data)

        else:
            data = {'hostname': hostname, 'id':  domainID[i][0]['id'], 'name': domainID[i][0]['name'], 'ip': 'None', 'status': domainID[i][0]['state']}
            info.append(data)
        
        """Check guest whether is exist or not."""
        """Update hostname and insert into the table."""
        chkguest = db.query(GuestHost).filter(GuestHost.host_id==hostid).filter(GuestHost.guestname==domainID[i][0]['name']).first()
        if chkguest == None:
            if  info[i]['id'] == 'None':
                guesthost = GuestHost(host_id=hostid, kvm_id=None, guestname=info[i]['name'], ip=info[i]['ip'], status=info[i]['status'])
                db.add(guesthost)
            else:
                guesthost = GuestHost(host_id=hostid, kvm_id= info[i]['id'], guestname=info[i]['name'], ip=info[i]['ip'], status=info[i]['status'])
                db.add(guesthost)
        else:
            if info[i]['id'] == 'None':
                chkguest.kvm_id = None
                chkguest.hostid = hostid
                chkguest.guestname = info[i]['name']
                chkguest.ip = info[i]['ip']
                chkguest.status = info[i]['status']
            else:
                chkguest.kvm_id = info[i]['id']
                chkguest.hostid = hostid
                chkguest.guestname = info[i]['name']
                chkguest.ip = info[i]['ip']
                chkguest.status = info[i]['status']
                
    z = []
    for i in info:
        z.append(i['name'])
    b = [value for value, in db.query(GuestHost.guestname).filter(GuestHost.host_id==hostid).all()]
    y = list(set(b)-set(z))
    if len(y) != 0:
        for i in y:
            delitem = db.query(GuestHost).filter(GuestHost.host_id==hostid).filter(GuestHost.guestname == i).one()
            db.delete(delitem)
            #print(delitem)
            #print(i)

    db.commit()
    a.conn.close()

    #print(info)

    
    #dash = '-' * 130
    #print(dash)
    #print('{:<30} {:<15} {:<45} {:<20} {:<20}'.format('<Hostname>', '<ID>', '<Name>', '<IP>', '<Status>'))
    #print(info)
    #for i in range(len(info)):
    #    print('{:<30} {:<15} {:<45} {!s:<20} {:<20}'.format(info[i]['hostname'],info[i]['id'], info[i]['name'], info[i]['ip'], info[i]['status']))