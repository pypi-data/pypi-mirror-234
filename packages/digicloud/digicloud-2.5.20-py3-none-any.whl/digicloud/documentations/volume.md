Volumes are persistent storage solutions in DigiCloud.

When an instance is created, a root volume with the size defined by instance type is created and 
attached to the instance automatically, instance image is copied to this root volume and basic 
instance operations can use the root volume, but that's not all DigiCloud offers, for extra
storage space one can create volumes and attach/detach them to/from an instance, 
please note that one should prefer these volumes over root volume for important data. 

there are two types of volume types `SSD` and `Ultra Disk` one can choose when creating a volume.

## Examples:

1. **Create volume**
    
    one can simply create a volume by specifying its size and type:

        $ digicloud volume create my-volume --type SSD --size 10

2. **List volumes**
    
       $ digicloud volume list

3. **volume details**

       $ digicloud volume show my-volume

4. **volumes and instances**

   Attaching/detaching a volume from/to an instance is simply done via:

          $ digicloud volume attach my-volume --instance my-instance

   Note that only volumes with *available* *status* are allowed to be attached.

          $ digicloud volume detach my-volume --instance my-instance

5. **Delete Volume**

   Always be careful about deleting volumes, although DigiCloud will ask you for confirmation one 
   may bypass the confirmation by using `--i-am-sure` switch to delete command.

      $ digicloud volume delete my-volume
