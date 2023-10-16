Subnet

A subnet is a block of IP addresses and associated configuration state.
Subnets are used to allocate IP addresses when new ports are created on a network.

## Examples:

1 **Create a Subnet**

    $ digicloud subnet create my_subnet_name
        --network my_network_name
        --cidr 10.0.0.0/16
2 **List subnets**

    $ digicloud subnet list
3 **Subnet details**

    digicloud subnet show my_subnet_name
4 **Update a Subnet**

    $ digicloud subnet update my_subnet_name
5 **Delete a Subnet**

    $ digicloud subnet delete my_subnet_name
