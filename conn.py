from models import *

hostList = ['10.1.10.128', '10.1.10.127', '10.1.10.120', '10.1.10.119', '10.1.10.122', '10.1.10.125', '10.1.10.130', '10.1.10.83', '10.1.10.173', '10.1.10.174', '10.1.10.175', '10.1.10.176', '10.1.10.177', '10.1.10.178', '10.1.10.179', '10.1.10.180', '10.1.10.181', '10.1.10.182', '10.1.10.183', '10.1.10.184']

for i in hostList:
    a = Host(i)
    info = []
    domainID = []
    hostname =  a.get_hostname()
    domainName = a.get_domain()
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
    
    a.conn.close()
    
    dash = '-' * 150
    print(dash)
    print('{:<30} {:<15} {:<45} {:<20} {:<20}'.format('<Hostname>', '<ID>', '<Name>', '<IP>', '<Status>'))
    #print(info)
    for i in range(len(info)):
        print('{:<30} {:<15} {:<45} {!s:<20} {:<20}'.format(info[i]['hostname'],info[i]['id'], info[i]['name'], info[i]['ip'], info[i]['status']))
    
#print(info)  