import ncclient

from ncclient import manager


device = manager.connect(host='v-mivpe015', port=830, username='EspositoA1', password='admin', hostkey_verify=False, device_params={}, allow_agent=False, look_for_keys=False)

subtree_filter = """

<platform xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-platform-oper">
        <racks>
          <rack/>
        </racks>
      </platform>
"""

str_nc_get_reply = device.get(('subtree', subtree_filter)).data_xml

print(str_nc_get_reply)



