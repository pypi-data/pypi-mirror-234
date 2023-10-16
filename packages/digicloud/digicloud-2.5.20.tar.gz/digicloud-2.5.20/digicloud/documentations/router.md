Router

A router is a logical component that forwards data packets between networks.
It also provides Layer 3 and NAT forwarding to provide external network access
for servers on project networks.

For the outside network to access VMs, and vice versa, routers between the networks
are needed. Each router has one gateway that is connected to an external network
and one or more interfaces connected to internal networks. Like a physical router,
subnets can access machines on other subnets that are connected to the same router,
and machines can access the outside network through the gateway for the router.

## Examples:

1 **Create a Router**

Note admin state choices are UP and DOWN.

    $ digicloud router create my_router_name
        --admin-state <state choice>
2 **List Routers**

    $ digicloud router list
3 **Router details**

    $ digicloud router show my_router_name
4 **Update a Router**

Note admin state choices are UP and DOWN.

    $ digicloud router update my_router_name
        --name my_new_router_name
        --admin-state <state choice>
        --enable-gateway or --disable-gateway
5 **Delete a Router**

    $ digicloud router delete my_router_name
6 **Enable and disable Router Gateway**

    $ digicloud router external add my_router_name
    $ digicloud router external remove my_router_name
7 **Create a Router Interface**

    $ digicloud router interface add my_router_name
        --subnet my_subnet_name
8 **List Router Interfaces**

    $ digicloud router interface list my_router_name
9 **Router Interface details**

    $ digicloudrouter interface show my_router_name
        --interface-id my_interface_id
10 **Remove a Router Interface**

    $digicloud router interface remove my_router_name
11 **Add a Static Route to a Router**

    $ digicloud router static add my_router_name
        --destination <IP_address>
        --nexthop <IP_address>
12 **List Static Routes in a Router**

    $ digicloud router static list my_router_name
13 **Remove Static Route from a Router**

    $ digicloud router static delete my_router_name
        --destination <IP_address>
        --nexthop <IP_address>
