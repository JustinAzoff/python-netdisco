from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.exceptions import SQLError

import datetime
import time
import sys
import md5
import socket

import ieeemac

import ConfigParser

c = ConfigParser.ConfigParser()
c.read(['/etc/netdisco/db.cfg','db.cfg'])
DOMAIN = c.get('misc','domain')
engine = create_engine(c.get('db','uri'))
Session = scoped_session(sessionmaker(autoflush=True, transactional=False, bind=engine))
metadata = MetaData(bind=engine)
mapper = Session.mapper

try:
    set
except NameError:
    from sets import Set as set

def resolve(ip):
    """Resolve ip, stripping off the domain if it exists"""
    try :
        name=socket.gethostbyaddr(ip)[0]
        return name.replace(DOMAIN, '')
    except :
        return ""


#device = Table('device', engine, autoload=True)
device = Table('device', metadata,
    Column('ip',           String(15), primary_key=True),
    Column('creation',     DateTime),
    Column('dns',          String),
    Column('description',  String),
    Column('uptime',       Integer),
    Column('contact',      String),
    Column('name',         String),
    Column('location',     String),
    Column('layers',       String(8)),
    Column('ports',        Integer, key='numports'),
    Column('mac',          String(20)),
    Column('serial',       String),
    Column('model',        String),
    Column('ps1_type',     String),
    Column('ps2_type',     String),
    Column('ps1_status',   String),
    Column('ps2_status',   String),
    Column('fan',          String),
    Column('slots',        Integer),
    Column('vendor',       String),
    Column('os',           String),
    Column('os_ver',       String),
    Column('log',          String),
    Column('snmp_ver',     Integer),
    Column('snmp_comm',    String),
    Column('vtp_domain',   String),   
    Column('last_discover',DateTime),
    Column('last_macsuck', DateTime),
    Column('last_arpnip',  DateTime)
)

device_ip = Table('device_ip', metadata,
    Column('ip',           String(15), ForeignKey("device.ip"), primary_key=True),
    Column('alias',        String(15), primary_key=True),
    Column('port',         String),
    Column('dns',          String),
    Column('creation',     DateTime)
)

device_port = Table('device_port', metadata,
    Column('ip',           String(15), ForeignKey("device.ip"), primary_key=True),
    Column('port',         String, primary_key=True),
    Column('creation',     DateTime),
    Column('descr',        String),       
    Column('up',           String),
    Column('up_admin',     String),
    Column('type',         String),
    Column('duplex',       String),
    Column('duplex_admin', String),
    Column('speed',        String),
    Column('name',         String),
    Column('mac',          String(20)),
    Column('mtu',          Integer),
    Column('stp',          String),
    Column('remote_ip',    String(15)),
    Column('remote_port',  String),
    Column('remote_type',  String),
    Column('remote_id',    String),
    Column('vlan',         String),
    Column('lastchange',   Integer, key="_lastchange")
)

device_port_log = Table('device_port_log', metadata,
    Column('id',           Integer, primary_key=True),
    Column('ip',           String(15), ForeignKey("device_port.ip")),
    Column('port',         String,     ForeignKey("device_port.port")),
    Column('reason',       String),
    Column('log',          String),
    Column('username',     String),#, ForeignKey("users.username"),
    Column('userip',       String(15)),
    Column('action',       String),
    Column('creation',     DateTime)
)

node = Table('node', metadata,
    Column('mac',          String(20), primary_key=True),
    Column('switch',       String(20), ForeignKey("device_port.ip"), primary_key=True),
    Column('port',         String(20), ForeignKey("device_port.port"), primary_key=True),
    Column('active',       Boolean),
    Column('oui',          String(8), ForeignKey("oui.oui")),
    Column('time_first',   DateTime),
    Column('time_last',    DateTime),
    Column('time_recent',  DateTime),
)

node_ip = Table('node_ip', metadata,
    Column('mac',          String(20), ForeignKey("node.mac"), primary_key=True),
    Column('ip',           String(20), primary_key=True),
    Column('active',       Boolean),
    Column('time_first',   DateTime),
    Column('time_last',    DateTime),
)

node_nbt = Table('node_nbt', metadata,
    Column('mac',          String(20), ForeignKey("node.mac"), primary_key=True),
    Column('ip',           String(15), ForeignKey("node_ip.ip")),
    Column('nbname',       String),
    Column('domain',       String),
    Column('server',       Boolean),
    Column('nbuser',       String),
    Column('active',       Boolean),
    Column('time_first',   DateTime),
    Column('time_last',    DateTime),
)

oui = Table('oui',  metadata,
    Column('oui',          String(8), primary_key=True),
    Column('company',      String)
)


admin = Table('admin', metadata,
    Column('job',          Integer, primary_key=True),
    Column('entered',      DateTime),
    Column('started',      DateTime),
    Column('finished',     DateTime),
    Column('device',       String(15), ForeignKey("device.ip"), key="device_ip"),
    Column('port',         String, ForeignKey("device_port.port"), key="port_name"),
    Column('action',       String),
    Column('subaction',    String),
    Column('status',       String),
    Column('username',     String, ForeignKey("users.username")),
    Column('userip',       String(15)),
    Column('log',          String),
    Column('debug',        Boolean),
)

users = Table('users', metadata,
    Column('username',     String(50), primary_key=True),
    Column('password',     String),
    Column('creation',     DateTime),
    Column('last_on',      DateTime),
    Column('port_control', Boolean),
    Column('admin',        Boolean, default=False),
    Column('fullname',     String),
    Column('note',         String),
)

blacklist = Table('blacklist', metadata,
    Column('b_id',         Integer, primary_key=True, key='id'),
    Column('ip',           String(15)),
    Column('switch',       String(15), ForeignKey("device.ip"),    key="device_ip"),
    Column('port',         String, ForeignKey("device_port.port"), key="port_name"),
    Column('reason',       String),
    Column('time',         DateTime),
    Column('blacklisttime',DateTime),
    Column('enable',       Boolean),
)

#blacklist_with_extra = select([blacklist, (func.now() - blacklist.c.blacklisttime).label('time_suspended')]).alias("blacklist_with_extra")

blacklist_pending = Table('blacklist_pending',metadata,
    Column('p_id',         Integer, primary_key=True, key='id'),
    Column('ip',           String(15)),
    Column('reason',       String),
    Column('time',         String),
)



class Oui(object):
    pass

class Port_Log(object):
    pass

class Device_IP(object):
    pass

class Node_NBT(object):
    pass

class Device(object):
    def __repr__(self):
        return "[%s %s]" % (self.ip, self.name)

    @classmethod
    def find(self, ip):
        """Find a device by IP address, either directly, or via an alias"""
        d = Device.query.filter(Device.ip==ip).first()
        if d:
            return d
        alias = Device_IP.query.filter(Device_IP.alias==ip).first()
        if alias:
            return alias.device
        

    @property
    def neighbors(self):
        """Return a list of dictionaries containing information about any CDP neighbors to this device

         * port - The :class:`netdisco.db.Port` that the remote device was seen on
         * remote_type - the type of remote device
         * remote_id   - the name of the remote device
         * remote_port - the port seen on the remote device
         * repore_ip   - the ip of the remote device
         * device - The :class:`netdisco.db.Device` object if one can be found
        """

        res = []
        for x in self.ports:
            if not x.remote_id:
                continue
            ip = x.remote_ip
            device = Device.find(ip)
            r = dict(port=x.port, remote_type=x.remote_type, remote_id=x.remote_id, remote_port=x.remote_port, remote_ip=ip, device=device)
            res.append(r)
        return res

    def generate_descriptions(self):
        ports = {}
        for info in self.neighbors:
            port = info['port']
            info['ip'] = info['remote_ip']
            #info['outport'] = abbreviate(info['remote_port'])

            description = "%(remote_type)s %(ip)s %(remote_id)s %(remote_port)s" % info
            ports.setdefault(port,[]).append(description)

        for port in ports:
            ports[port] = "feed to " + " AND ".join(ports[port])

        return ports

    @property
    def active_ips(self):
        ips = []
        for x in self.ports:
            if x.up != 'up': continue
            for node in x.nodes:
                if not node.active: continue
                for ip in node.ips:
                    if ip.active:
                        ips.append(ip.ip)
        return ips
        
    @property
    def active_nodes(self):
        nodes = []
        for p in self.ports:
            nodes.extend(p.active_nodes)
        return nodes

    @property
    def active_node_ips(self):
        return [n.ip for n in self.active_nodes]
    
    def discover(self, user=None):
        return self._do_something('discover',user=user)

    def refresh(self, user=None):
        return self._do_something('refresh',user=user)
    
    def arpnip(self, user=None):
        return self._do_something('arpnip',user=user)

    def macsuck(self, user=None):
        return self._do_something('macsuck',user=user)

    def change_ip(self, new_ip, user=None):
        return self._do_something('change_ip', new_ip, user)

    def _do_something(self, thing, subaction=None,user=None):
        if not user:
            user = User.query.get("backend")
        return Admin.add(user=user, device=self, action=thing, subaction=subaction)

    @property
    def ports_as_dict(self):
        ports = []
        for p in self.ports:
            d = {}
            for attr in 'name', 'duplex', 'duplex_admin', 'vlan', 'up', 'up_admin', 'speed', 'port':
                d[attr] = getattr(p,attr)
                if p.up_admin=='down' and p.log:
                    d['log']=p.log[-1].log
            d['last_discover'] = self.last_discover
            d['last_macsuck'] = self.last_macsuck
            ports.append(d)
        return ports


    def has_layer(self, layer):
        layers = [bool(int(x)) for x in reversed(self.layers)]
        return layers[layer-1]

    @classmethod
    def last_to_be_macsucked(self):
        """Return the last device to be macsucked
           for monitoring, if the time it was macsucked was too long ago,
           something is wrong
        """
        return Device.query.filter(Device.last_macsuck!=None).order_by(Device.last_macsuck.desc()).first()

    @classmethod
    def find_aps(self):
        return Device.query.filter(Device.model.like("%AIR%")).all()

    @classmethod
    def find_by_subnet(self, subnet):
        params = [bindparam('subnet',subnet)]
        return Device.query.filter(engine.text(":subnet >> ip",bindparams=params)).order_by([device.c.ip])

class Port(object):

    def __repr__(self):
        return "[%s %s]" % (self.ip, self.port)

    @classmethod
    def get_num_incorrect_descriptions(self):
        return Port.query.filter(and_(
                    not_(device_port.c.port.like("VLAN%")),
                    or_(device_port.c.name=='', device_port.c.name=='no device attached'),
                    device_port.c.up=='up')).count()

    @classmethod
    def find_incorrect_descriptions(self):
        mapper = Port.query.options(eagerload('device'),lazyload('nodes'))
        return mapper.filter(and_(
                not_(device_port.c.port.like("VLAN%")),
                or_(device_port.c.name=='', device_port.c.name=='no device attached'),
                device_port.c.up=='up'),
            order_by=[device_port.c.ip,func.length(device_port.c.port), device_port.c.port ])

    @classmethod
    def find_admin_disabled(self):
        return Port.query.filter_by(up_admin='down').join('log').filter_by(action='disable').all()

    @classmethod
    def get_by_ip(self, ip):
        macs = util.get_macs_for_ip(ip)
        if macs:
            return self.get_by_mac(macs[0])

    @classmethod
    def get_by_mac(self, mac):
        n = Node.query.filter(Node.mac==mac).order_by(desc(Node.time_last)).first()
        if n:
            return n.device_port

    @property
    def status(self):
        if self.up_admin == 'down':
            return 'disabled'
        elif self.up == 'up':
            return 'up'
        else :
            return 'down'

    @property
    def is_disabled(self):
        return self.up_admin == 'down'

    @classmethod
    def find(self, switch=None, port=None, ip=None,mac=None):
        if ip:
            return self.get_by_ip(ip)
        if mac:
            return self.get_by_mac(mac)

        if switch and port:
            return Port.query.get((switch,port))

    @classmethod
    def find_all(self, ip=None, mac=None):
        if not (ip or mac):
            raise ValueError, "Specify an ip or a mac"

        crit = [Port.ip==Node.switch, Port.port==Node.port]
        if mac:
            crit.append(Node.mac==mac)
        elif ip:
            crit.extend((Node.mac==Node_IP.mac,Node_IP.ip==ip))
        newmapper = Port.query.options(lazyload('nodes'))
        return newmapper.filter(and_(*crit)).order_by(desc(Node.time_last))

    @classmethod
    def find_by_vlan(self, vlan, load_nodes=False):
        vlan = str(vlan)
        q = Port.query
        if load_nodes:
            q = q.options(eagerload('device'),eagerload('nodes.ips'))
        ports = q.filter(Port.vlan==vlan).order_by([Port.ip,func.length(Port.port),Port.port])
        return ports

    @classmethod
    def find_with_neighbors(self):
        """Returns a list of ports that see a CDP neighbor"""
        return Port.query.filter(Port.remote_id != None).order_by([Port.remote_ip])

    @classmethod
    def find_non_trunking(self):
        """Returns a list of ports that see a CDPneighbor, but are not trunking"""
        q = Port.query.options(lazyload('nodes'))
        return q.filter(and_(not_(Port.vlan==None), Port.remote_id!=None)).order_by([Port.ip])
    
    @property
    def active_nodes(self):
        nodes = []
        for n in self.nodes:
            #if not n.active: continue
            if (datetime.datetime.now() - n.time_last).days > 30: continue
            for i in n.ips:
                if not i.active: continue
                if (datetime.datetime.now() - i.time_last).days > 30: continue
                nodes.append(i)
        return nodes

    @property
    def unique_recent_active_nodes(self):
        nodes = []
        for n in self.nodes:
            #if not n.active: continue
            if (datetime.datetime.now() - n.time_last).days > 1: continue
            for i in n.ips:
                if not i.active: continue
                if (datetime.datetime.now() - i.time_last).days > 1: continue
                nodes.append(i)
                continue
        return nodes

    @property
    def lastchange(self):
        # lastchange is a timestamp of the sysUpTime
        # we subtract it from the current uptime to find out how many
        # seconds*100 it was, then we subtract that from the current time to
        # see when that was.
        #my $diff_sec = ($device->{uptime} - $val) / 100;
        #$val = scalar localtime($device->{last_discover} - $diff_sec);

        diff_sec = (self.device.uptime - self._lastchange)/100
        delta = datetime.timedelta(seconds=diff_sec)
        return self.device.last_discover - delta
    

class Node(object):
    @property
    def company(self):
        return self.manuf and self.manuf.company

class Node_IP(object):
    @classmethod
    def get_active_ips(self):
        """Return a list of active client ips"""
        ips = []
        for node in engine.execute(node_ip.select(and_(node_ip.c.active==True, "time_last > current_timestamp - interval '1 day' "),order_by=[node_ip.c.ip])):
            ips.append(node.ip)
        return ips
        
    @property
    def dns(self):
        return resolve(self.ip)

    @property
    def company(self):
        nodes = self.nodes
        if not nodes:
            return
        return nodes[0].company

class Admin(object):
    Column('job',          Integer, primary_key=True),
    Column('entered',      DateTime),
    Column('started',      DateTime),
    Column('finished',     DateTime),
    Column('device',       String(15), ForeignKey("device.ip"), key="device_ip"),
    Column('port',         String, ForeignKey("device_port.port"), key="port_name"),
    Column('action',       String),
    Column('subaction',    String),
    Column('status',       String),
    Column('username',     String, ForeignKey("users.username")),
    Column('userip',       String(15)),
    Column('log',          String),
    Column('debug',        Boolean),

    def __init__(self, entered=None, started=None, finished=None, device=None, port=None, action=None, subaction=None, status=None, username=None, userip=None, log=None, debug=None):
        if not entered:
            entered = datetime.datetime.now()
            
        self.job = None
        self.entered = entered
        self.started = started
        self.finished = finished
        self.device = device
        self.port = port
        self.action = action
        self.subaction = subaction
        self.status = status
        self.username = username
        self.userip = userip
        self.log = log
        self.debug=debug

    @classmethod
    def get_pending(self):
        return Admin.query.filter(Admin.status.in_(['queued','running'])).all()

    @classmethod
    def add(self, user, userip='127.0.0.1', device=None, port=None, action=None, subaction=None, debug=False):
        if (not device or not action) and (action!='discover' and subaction):
            return False

        #try and find the same job already queued
        crit = [Admin.finished==None, Admin.action==action, Admin.subaction==subaction]
        if port:
            crit.append(Admin.port_name==port.name)
        if device:
            crit.append(Admin.device_ip==device.ip)

        j = Admin.query.filter(and_(*crit)).first()
        if j:
            return j

        j = Admin(userip=userip, action=action,subaction=subaction, debug=debug, status='queued')
        j.user=user
        j.device=device
        j.port=port
        Session.save(j)
        Session.flush()
        return j

    def wait(self, timeout=30):
        timeout_time=time.time()+timeout

        while time.time() < timeout_time:
            Session.refresh(self)
            status=self.status
            print status
            sys.stdout.flush()
            if status in ('done','error'):
                break
            time.sleep(1)

        return status


class User(object):
    @classmethod
    def add(self, username, password, fullname, note=None, port_control=False,admin=False):
        password = md5.md5(password).hexdigest()
        u = User(username=username, password=password, fullname=fullname, note=note, port_control=port_control, admin=admin)
        Session.save(u)
        Session.flush()
        return u

    @classmethod
    def authenticate(self, username, password):
        return User.query.filter(and_(
            User.username==username,
            User.password==func.md5(password)
            )).first()

class Blacklist(object):
    pass

class Blacklist_pending(object):
    pass

mapper(User, users)

mapper(Oui, oui)

mapper(Node_NBT, node_nbt, order_by=node_nbt.c.time_last.desc())

mapper(Node_IP, node_ip, order_by=node_ip.c.time_last.desc(), properties = {
    'nbt': relation(Node_NBT, backref=backref('ips',uselist=True, order_by=node.c.time_last.desc()), lazy=True, 
        primaryjoin=node_ip.c.ip==node_nbt.c.ip),
})
    

mapper(Node, node, order_by=node.c.time_last.desc(), properties = {
    'ips': relation(Node_IP, backref=backref('nodes', uselist=True,order_by=node.c.time_last.desc()), lazy=True),
    'nbt': relation(Node_NBT, backref=backref('nodes',uselist=True, order_by=node.c.time_last.desc()), lazy=True), 
    'manuf': relation(Oui, backref='nodes')
})

mapper(Device_IP, device_ip)

mapper(Port_Log, device_port_log)

mapper(Port, device_port, order_by=[func.length(device_port.c.port), device_port.c.port], properties = {
    'nodes': relation(Node, backref='device_port', lazy=False, order_by=node.c.time_last.desc(),
        primaryjoin=and_(device_port.c.ip==node.c.switch, device_port.c.port==node.c.port)
    ),
    'log':  relation(Port_Log, backref='device_port', order_by=[asc(device_port_log.c.creation)],
        primaryjoin=and_(device_port.c.ip==device_port_log.c.ip, device_port.c.port==device_port_log.c.port)
    ),
})

mapper(Device, device, order_by=[device.c.ip], properties = {
    'aliases': relation(Device_IP, backref='device'),
    'ports':   relation(Port, backref='device', order_by=[func.length(device_port.c.port), device_port.c.port]) #, lazy=False)
})


mapper(Admin, admin, properties = {
    'user': relation(User),
    'device': relation(Device),
    'port':   relation(Port,primaryjoin=and_(admin.c.device_ip==device_port.c.ip, admin.c.port_name==device_port.c.port))
})

#mapper(Blacklist, blacklist_with_extra, properties = {
#    'device': relation(Device),
#    'port':   relation(Port,primaryjoin=and_(blacklist_with_extra.c.device_ip==device_port.c.ip, blacklist_with_extra.c.port_name==device_port.c.port))
#})
mapper(Blacklist, blacklist, properties = {
    'device': relation(Device),
    'port':   relation(Port,primaryjoin=and_(blacklist.c.device_ip==device_port.c.ip, blacklist.c.port_name==device_port.c.port))
})

mapper(Blacklist_pending, blacklist_pending)


class util:
    @classmethod
    def get_macs_for_ip(self, ip):
        """Return a list of mac addresses for this ip"""
        nodes = Node_IP.query.filter(Node_IP.ip==ip).order_by(desc(Node_IP.time_last))
        return [x.mac for x in nodes]

    @classmethod
    def get_ips_for_mac(self, mac):
        """Return a list of ip addresses for this mac"""
        nodes = Node_IP.query.filter(Node_IP.mac==mac).order_by(desc(Node_IP.time_last))
        return [x.ip for x in nodes]


    @classmethod
    def get_all_ips(self, ciscoonly=False):
        """Return a list of (ip, name) tuples for every device"""
        ips = []
        for x in self.get_all_ips_dict(ciscoonly):
            ips.append((x['ip'],x['name']))
        return ips

    @classmethod
    def get_all_ips_dict(self, ciscoonly=False):
        """return a list of dictionaries full of info"""
        if ciscoonly:
            crit = [device.c.vendor=='cisco',device.c.os=='ios']
        else :
            crit = []

        seen=set()
        for node in engine.execute(device.select(and_(*crit), order_by=[device.c.ip])):
            name=node.name
            ip=node.ip
            model = node.model
            version = node.os_ver

            if name not in seen:
                yield dict(ip=ip, name=name, model=model,version=version)
                seen.add(name)

    @classmethod
    def get_dead_links(self):
        """Return a list of ports containing cdp neighbors without entries in the device table"""
        real_ips = select([device.c.ip],     distinct=True)
        aliases = select([device_ip.c.alias],distinct=True)
        all_ips = union(real_ips, aliases)
        return Port.query.filter(not_(Port.remote_ip.in_(all_ips))).all()


    @classmethod
    def find_aps(self):
        """Return a list of tuples of (ip, name, type)"""
        for p in Port.query.filter(and_(Port.remote_type.like('%AIR%'),Port.remote_ip!=None)):
            yield p.remote_ip, p.remote_id, p.remote_type

    @classmethod
    def is_disabled(self, ip=None, mac=None):
        """Are any of the port that this ip or mac is on disabled?"""
        for p in Port.find_all(ip=ip,mac=mac):
            if p.is_disabled:
                return True
        return False


    @classmethod
    def get_old_macs_by_subnet(self, subnet, months=2):
        months = int(months)
        res = engine.text("""SELECT mac, MAX(time_last)
                             FROM node_ip WHERE :subnet >> ip
                             GROUP BY mac HAVING MAX(time_last) < CURRENT_TIMESTAMP - INTERVAL '%d months'
                             ORDER BY MAX(time_last) ASC""" % months
                         ).execute({'subnet':subnet})
        return res.fetchall()



    @classmethod
    def get_wireless_macs(self):
        devices = {}
        ret = []
        all_ips = dict(util.get_all_ips())
        for p in engine.execute(device_port.select(or_(device_port.c.port=='Dot11Radio0',device_port.c.port=='FastEthernet0'))):
            d = devices.setdefault(p.ip,{})
            if not d:
                d['wireless'] = d['wired'] = None
            if p.port=='Dot11Radio0':
                d['wireless'] = p.mac
            else:
                d['wired']    = p.mac
                
        for ip, macs in sorted(devices.items()):
            ret.append(dict(ip=ip, hostname=all_ips.get(ip), **macs))
        return ret
            
    @classmethod
    def find_ports_with_many_macs(self):
        """Return a list of ports that see more than 3 MAC addresses"""
        n = node.c
        midnight = datetime.date.today()
        q = select([n.switch,n.port,func.count(n.mac)],
            and_(n.active, n.time_last > midnight, not_(n.port.like("Dot11%"))),
            group_by=[n.switch,n.port],
            having=func.count(n.mac) > 3,
            order_by=[n.switch,n.port]
        )
        return engine.execute(q).fetchall()

    @classmethod
    def find_many_ports_from_string(self, s):
        data = []
        import findipsandmacs
        for x in findipsandmacs.find(s):
            p = None
            mac = None
            ip = None
            dns = None
            try :
                if ieeemac.ismac(x):
                    p = Port.find(mac=x)
                    mac = x
                else:
                    p = Port.find(ip=x)
                    ip = x

                if p and not ip:
                    ips = util.get_ips_for_mac(x)
                    if ips:
                        ip = ips[0]
                if p and not mac:
                    macs = util.get_macs_for_ip(x)
                    if macs:
                        mac = macs[0]

                if ip:
                    dns = resolve(ip)

                data.append((mac, ip, dns, p))
            except Exception, e:
                pass

        return data

    @classmethod
    def add_device(self, ip):
        return add_device(ip)

    @classmethod
    def refresh_device(self, ip):
        return refresh_device(ip)


    @classmethod
    def get_all_active_nodes(self):
        return engine.execute(node_ip.select(node_ip.c.active==True)).fetchall()


    @classmethod
    def get_vlan_counts(self, device_list):
        """Return a list of vlans and the number of ports that are on that vlan

        :param device_list: List of IP addresses of devices to search
        """
        vlan = func.COALESCE(device_port.c.vlan,'TRUNK')
        return engine.execute(select(
                [vlan,func.count(vlan)],
                device_port.c.ip.in_(device_list),
                group_by=[vlan])
            ).fetchall()

def add_device(ip):
    u = User.query.get('backend')
    return Admin.add(u, action='discover', subaction=ip)

def add_device_entry():
    for ip in sys.argv[1:]:
        add_device(ip)

def refresh_device(ip):
    d = Device.find(ip)
    u = User.query.get('backend')
    jobs = [
        d.refresh(u),
        d.macsuck(u),
        d.arpnip(u),
    ]
    return jobs

def refresh_device_entry():
    for ip in sys.argv[1:]:
        refresh_device(ip)

def wait_for_jobs():
    jobs = Admin.get_pending()
    tot = len(jobs)
    print "%d total jobs" % tot
    for i,j in enumerate(jobs):
        d = j.device
        print "%d/%d %s %s %s %s" %(i+1, tot, d and d.ip, d and d.name, j.action, j.subaction)
        j.wait()
        print
