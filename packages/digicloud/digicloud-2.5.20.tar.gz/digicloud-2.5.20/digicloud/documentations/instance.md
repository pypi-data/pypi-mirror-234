Instance, Digicloud virtual private servers (VPS)

DigiCloud virtual machines are called **instances**, mostly because they are instances of an 
**image** that is created upon request and that is configured when launched. 
DigiCloud provides a wide selection of **instance types** optimized to fit different use cases. 
Instance types comprise varying combinations of CPU, memory, storage, and networking capacity and 
give you the flexibility to choose the appropriate mix of resources for your applications.


## Examples:

1. **Listing available images**

    In order to list all available images to be used for instance creation one can use:

        $ digicloud image list
2. **list available instance types**

    The following command can be used for listing available instance types, one should choose one of
    these types for instance creation.

        $ digicloud instance type list
3. **Create instance**
    
    DigiCloud supports two types of instance creation simple and advanced, in the simple scenario
    both network and firewall options must not be provided due to simplicity but in the advanced 
    scenario, network is mandatory and firewall is optional. one can also add additional 
    volume and public IP on instance creation in both scenarios which will be handled automatically.

        # Creating a simple instance
        $ digicloud instance create master_server \
                        --simple \
                        --instance-type g1.micro \
                        --image Debian_9
    or

        # Creating a simple instance and also setting root volume parameters
        $ digicloud instance create master_server \
                        --simple \
                        --instance-type g1.micro \
                        --image Debian_9 \
                        --root-volume-size 50 \
                        --root-volume-type ULTRA_DISK
    or

        # Creating an advanced instance with two additional volumes
        $ digicloud instance create backup_server
                        --network my_network \
                        --instance-type g1.micro \
                        --image Debian_9
                        --additional-volume size=64,type=SSD
                        --additional-volume size=2048,type=ULTRA_DISK
    or

        # Creating an advanced (or simple) instance from an existing snapshot 
        $ digicloud instance create backup_server
                        --network my_network \
                        --instance-type g1.micro \
                        --snapshot My_Snapshot
    or

        # Creating an advanced instance with an ephemeral public ip
        $ digicloud instance create backup_server
                        --network my_network \
                        --instance-type g1.micro \
                        --image Debian_9 \
                        --with-public-ip

    or

        # Creating an advanced instance with an existing public-ip named 'api_ip'
        $ digicloud instance create backup_server
                        --network my_network \
                        --instance-type g1.micro \
                        --image Debian_9 \
                        --public-ip api_ip

4. **List instances**
    One can list simple as well as advanced instances using the following command:

        $ digicloud instance list        

    There are also `--simple` or `--advanced` switches which can be used to list simple or advanced
    instances.

5. **Instance basic operations**
    Operations such as *reboot*, *suspend*, *start*, *stop* and *resume* are of course supported.

        $ digicloud instance reboot my-instance

6. **Change Instance type**
    
    One can easily change instance type via: 
    
        $ digicloud instance resize my-instnace --instance-type new-instance-type    

    please have in mind that to resize an instance you have to stop it first.

7. **List instance snapshots**

   One can get the list of instance snapshots via:
   
      $ digicloud instance snapshot list my-instance
