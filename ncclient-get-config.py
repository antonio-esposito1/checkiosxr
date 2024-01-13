import lxml. etree as ET
from argparse import ArgumentParser
from ncclient import manager
from ncclient.operations import RPCError

if __name__ == '__main__':
    parser = ArgumentParser(description='Usage:')
    
    #script argument
    parser.add_argument('-a', '--host', type=str, required = True, help="Device IP address or Hostname")
    parser.add_argument('-u', '--username', type=str, required = True, help="Device Username (netconf agent username)")
    parser.add_argument('-p', '--password', type=str, required = True, help="Device Password (netconf agent Password")
    parser.add_argument('--port', type=int, default=830, help="Netconf agent Port")
    args = parser.parse_args()
    
    #connect to netconf
    with manager.connect(host=args.host, port=args.port, username=args.username, password=args.password, timeout=90, hostkey_verify=False, device_params={}) as m:
        try:
            response = m.get_config(source='running').xml
            data = ET.fromstring(response)
        except RPCError as e:
            data = e._raw
            
    #beauty output
    print(ET.tostring(data, pretty_print=True))
    