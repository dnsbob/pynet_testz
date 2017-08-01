# ciscoread_w1e8.py

from ciscoconfparse import CiscoConfParse

cisco_cfg=CiscoConfParse("cisco_ipsec.txt")
crypto = cisco_cfg.find_objects(r"^crypto map CRYPTO")
for i in crypto:
    print i.text
    for j in i.all_children:
        print j.text

