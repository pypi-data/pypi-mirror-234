Public IP

Each instance has a private, fixed IP address and can also have a public IP address.
Private IP addresses are used for communication between instances,
and public addresses are used for communication with networks outside the cloud,
including the Internet.

When you launch an instance, it is automatically assigned a private IP address that
stays the same until you explicitly terminate the instance. Rebooting an instance has
no effect on the private IP address.

A pool of public IP addresses, is available in DigiCloud. The project quota defines
the maximum number of public IP addresses that you can allocate to the project.
After you allocate a public IP address to a project, you can Associate the public IP
address with an instance of the project. Only one public IP address can be allocated 
to an instance at any given time.

## Examples:

1 **Create a Public IP**

    $ digicloud public ip create
2 **List Public IPs**

    $ digicloud public ip list
3 **Public IP details**

    $ digicloud: public ip show my_public_ip
4 **Delete a Public IP**

    $ digicloud public ip delete my_public_ip
5 **Associating a Public IP to a Router interface and revoking it**

    $ digicloud public ip associate my_public_ip --interface-id my_router_interface_id
    $ digicloud public ip revoke my_public_ip
6 **Assigning a Public IP to an Instance**
    
    $ digicloud network create my_local_network_name
    $ digicloud subnet create my_local_subnet_name
    --network my_network_name
    --cidr 10.0.0.0/16
    $ digicloud instance create  my_instance_name
    --advance
    --image=Ubuntu_20.04_LTS
    --instance-type=g1.small
    --network=my_internal_network_name
    $ digicloud network create my_external_network_name
    $ digicloud subnet create my_external_subnet_name
    --network my_external_network_name
    --cidr 10.0.0.0/16
    $  digicloud instance interface attach  my_instance_name
    --network= my_external_network_name
    $ digicloud router create my_router_name
        --admin-state <state choice>
    $ digicloud router interface add my_router_name
    --subnet my_subnet_name
    $ digicloud public ip create
    $ digicloud public ip associate my_public_ip
    --interface-id my_router_interface_id
