VPN is a virtual private network is like bridge between your network in DigiCloud and outside network.

You can extend your DigiCloud private network across internet.
VPN is an encrypted connection over the Internet from a device to a network.
The encrypted connection helps ensure that sensitive data is safely transmitted.
It prevents unauthorized people from eavesdropping on the traffic and allows the user to conduct work remotely.

## Examples:

1. **Create VPN**
    
    One can simply create a vpn with bellow command:

        $ digicloud vpn external create  \
            --description "some description"  \
            --local-endpoint-group "my-subnet"  \
            --peer-id 1.1.1.1  \
            --peer-address 1.1.1.1  \
            --peer-endpoint-group "10.10.0.0/24"  \
            --psk "some secret here"  \
            --vpn-router-id "my-router"  \
            --ike-policy "my-ike-policy" \
            --ipsec-policy "my-ipsec-policy" \
            ---psk "secrete string" \
            --mtu=68  \
            "my-vpn-connection"
        
        Required arguments:
   
            --local-endpoint-group:
           
                List of local subnet names or ids. E.g: subnet_1 subnet_2
           
            --peer-id:
                
                The peer router identity for authentication.
                A valid value is an IPv4 address, IPv6 address or FQDN.
                Typically, this value matches the --peer-address.
           
            --peer-address:
           
                The peer gateway public IPv4 or IPv6 address or FQDN.
           
            --peer-endpoint-group:
           
                list of peer networks in CIDR format. E.g: cidr_1 cidr_2
           
            --psk:
           
                Pre-shared key for the VPN connection.
           
            --ipsec-policy:
           
                ipsec policy name or id for the VPN connection.
           
            --ike-policy:
           
                ike policy name or id for the VPN connection.
           
            --vpn-router-id:
           
                The id of the router to be used with the VPN
           
            --mtu:
           
                The maximum transmission unit (MTU) value to address fragmentation.
                Minimum value is 68 for IPv4, and 1280 for IPv6.
        
        Optional arguments:
            
            --initiator:
                
                Indicates whether this VPN can only respond to connections or both respond to and initiate connections. 
                A valid value is 'response-only' or 'bi-directional'. Default is 'bi-directional'.
            
            --admin-state-down:
                
                Sets the administrative state of the resource to 'down',
                Including this switch means 'down' state. Omitting this switch means 'up' state
  
            --vpn-router-id:
                
                The id of the router to be used with the VPN
    Note: Share the following information with your network team to create the VPN connection on their side:

    - Subnet configuration details
    - Public IP address of the router that serves as the gateway on the cloud side
    - Endpoint group information for both local and peer networks
    - Pre-shared key (PSK) for authentication

  

2. **List VPNs**
    
       $ digicloud vpn external list

3. **VPN details**

       $ digicloud vpn external show my-vpn-connection

4. **VPN update**

       $ digicloud vpn external show my-vpn-connection  \
            --name my-vpn-new-name  \
            --desription "my new description"  \
            --admin-state-down or --admin-state-up \
            --psk my-psk

5. **Delete VPN**

      $ digicloud vpn external delete my-vpn-connection
