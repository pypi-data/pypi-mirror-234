IPsec is a group of protocols for securing connections between devices. IPsec helps keep data sent over public networks secure. It is used to set up VPNs, and it works by encrypting IP packets, along with authenticating the source where the packets come from.


## Examples:

1. **Create IpSec**
    
    one can simply create a ipsec by specifying these args:

        $ digicloud ipsec create --auth-algorithm sha1\
         --encapsulation-mode tunnel\
         --encryption-algorithm aes-128\
         --pfs group2\
         --transform-protocol esp\
         --lifetime units=seconds,value=3600\
         my-ipsec
    choices for each attribute is as follows:

    auth-algorithm: `['sha1', 'sha256', 'sha384', 'sha512']` default: `sha1`

    encapsulation-mode: `['tunnel', 'transport']` default: `tunnel`

    encryption-algorithm: `['3des', 'aes-128', 'aes-192', 'aes-256']` default: `aes-128`

    pfs: `['group2', 'group5', 'group14']` default: `group5`

    transform-protocol: `['esp', 'ah', 'ah-esp']` default: `esp`

    lifetime units: `['seconds']` default: `seconds`

    lifetime value: `range of 60 - 86400` default: `3600`


2. **List IpSec policies**
    
       $ digicloud ipsec list

3. **IpSec policy details**

       $ digicloud ipsec show my-ipsec

5. **Delete IpSec**

   Always be careful about deleting IpSec policy, although DigiCloud will ask you for confirmation one 
   may bypass the confirmation by using `--i-am-sure` switch to delete command.

         $ digicloud ipsec delete my-ipsec

    Note: You can't remove IpSec policy when there is a VPN object using it
