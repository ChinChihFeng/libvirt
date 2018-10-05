from __future__ import print_function
import libvirt
import sys
from xml.dom import minidom

        
class Host:
    
    def __init__(self, ip):
        
        # Which ip of KVM host you want to acsess.
        self.ip = ip
        self.url = 'qemu+ssh://root@' + ip +'/system?socket=/run/libvirt/libvirt-sock'
        self.conn = libvirt.open(self.url)
        
        if self.conn == None:
            print(f"Failed to open connection to {url}", file=sys.stderr)
            sys.exit(1)
        #print('success')
    def get_hostname(self):
        name = self.conn.getHostname()
        return name
    
    def get_domain(self):
        #domains = self.conn.listAllDomains(libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE)
        domains = self.conn.listAllDomains(0)
        alist = []
        if len(domains) != 0:
            for i in domains:
                aname = i.name()
                alist.append(aname)
            return alist
        else:
            print('None')
            sys.exit(1)
            
    def get_domainID(self, nameList):        
        dom = self.conn.lookupByName(nameList)
        #print(dom.state())
        domainIDs = []
        #domainIDs = self.conn.listDomainsID()
        if dom == None:
            print('Failed to find the domain '+domName, file=sys.stderr)
            sys.exit(1)

        id = dom.ID()
        state, reason = dom.state()
        
        if id == -1 and state:
            if state == libvirt.VIR_DOMAIN_NOSTATE:
                status = 'NOSTATE'
            elif state == libvirt.VIR_DOMAIN_RUNNING:
                status = 'RUNNING'
            elif state == libvirt.VIR_DOMAIN_BLOCKED:
                status = 'BLOCKED'
            elif state == libvirt.VIR_DOMAIN_PAUSED:
                status = 'PAUSED'
            elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
                status = 'SHUTDOWN'
            elif state == libvirt.VIR_DOMAIN_SHUTOFF:
                status = 'SHUTOFF'
            elif state == libvirt.VIR_DOMAIN_CRASHED:
                status = 'CRASHED'
            elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
                status = 'PMSUSPENDED'
            else:
                status = 'UNKNOWN'
            domainIDs.append(dict({'id': 'None', 'state': status}))
            #print('The domain is not running so has no ID.')
        else:
            domainIDs.append(dict({'id': id, 'state': 'RUNNING'}))
            #print('The ID of the domain is ' + str(id))
        #print(domainIDs)
        return domainIDs
            
    def retrive_interface(self, domainName):
        dom = self.conn.lookupByName(domainName)
        if dom == None:
            print('Failed to get the domain object', file=sys.stderr)
            sys.exit(1)
        else:
            #print(domainName)
            ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
            for (name, val) in ifaces.items():
                if val['addrs'] and name != 'lo':
                    for ipaddr in val['addrs']:
                        if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                            inet = ipaddr['addr']
                            return inet
    
    
    