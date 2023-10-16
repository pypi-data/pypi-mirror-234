Internet Key Exchange (IKE) is a key management protocol that is used to authenticate IPsec peers, negotiate and distribute IPsec encryption keys, and automatically establish IPsec security associations 


## Examples:

1. **Create IKE**
    
    one can simply create a ike by specifying these args:

        $ digicloud ike create --auth-algorithm sha1\
         --encryption-algorithm aes-128\
         --pfs group2\
         --ike-version v1\
         --lifetime units=seconds,value=3600\
         my-ike
    choices for each attribute is as follows:

    auth-algorithm: `['sha1', 'sha256', 'sha384', 'sha512']` default: `sha1`

    encryption-algorithm: `['3des', 'aes-128', 'aes-192', 'aes-256']` default: `aes-128`

    pfs: `['group2', 'group5', 'group14']` default: `group5`

    ike-version: `['v1', 'v2']` default: `v1`

    lifetime units: `['seconds']` default: `seconds`

    lifetime value: `range of 60 - 86400` default: `3600`


2. **List IKE policies**
    
       $ digicloud ike list

3. **IKE policy details**

       $ digicloud ike show my-ike

5. **Delete IKE**

   Always be careful about deleting IKE policy, although DigiCloud will ask you for confirmation one 
   may bypass the confirmation by using `--i-am-sure` switch to delete command.

         $ digicloud ike delete my-ike
   Note: You can't remove IpSec policy when there is a VPN object using it
