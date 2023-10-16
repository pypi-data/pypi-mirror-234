Network

Networking handles the creation and management of a virtual networking infrastructure,
including networks, subnets, and routers for instances inside the DigiCloud.

Networking provides networks, subnets, and routers as object abstractions.
Each abstraction has functionality that mimics its physical counterpart:
networks contain subnets, and routers route traffic between different subnets and networks.

## Examples:
    
1 **Create a Network**

Note admin state choices are UP and DOWN. Default is UP.      

    $ digicloud network create my_network

2 **List Networks**

    $ digicloud network list
3 **Network details**

    $ digicloud network show my_network
4 **Update a Network**

Note admin state choices are UP and DOWN.

    $ digicloud network update my_network
        --name my_network_new_name
        --admin-state <state choice>
    
5 **Delete a Network**

    $ digicloud network delete my_network
