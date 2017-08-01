# ciscoread_w1e8.py

from ciscoconfparse import CiscoConfParse
import re

cisco_cfg=CiscoConfParse("cisco_ipsec.txt")
crypto = cisco_cfg.find_objects_wo_child(parentspec=r"^crypto map CRYPTO", childspec=r"transform-set AES")
for i in crypto:
    #print i.text
    for j in i.all_children:
        #print j.text
        match=re.search(r"set transform-set (.*)$",j.text)
        if match:
            encrypt=match.group(1)
    #print "alt----"
    print "{0} -uses- {1}".format(i.text.strip(),encrypt)
