Snapshots, are point-in-time backup of an Instance (DigiCloud virtual machines)

A snapshot can be defined as a copy of Instance state at a specific point of time.
You can use a snapshot to create a new Instance.


## Examples:

1. **Create Snapshot**

       $ digicloud snapshot create my-snapshot --instance my-instance

2. **Get a Snapshot detail**

       $ digicloud snapshot show my-snapshot


3. **List Snapshots**

        $ digicloud snapshot list 

4. **Update Snapshot**

        $ digicloud snapshot update my-snapshot \
                     --name new-name \
                     --description "new description for my snapshot"

5. **Delete Snapshot**

   Always be careful about deleting snapshots, although DigiCloud will ask you for confirmation. you can bypass the confirmation by using --i-am-sure switch in delete command, otherwise Digicloud will ask if you are sure.
        
        $ digicloud snapshot delete my-snapshot

6. **Create Instance using Snapshot**

   Creating an instance (advanced or simple) from an existing snapshot

        $ digicloud instance create backup_server \
                        --network my_network \
                        --instance-type g1.micro \
                        --snapshot my-snapshot