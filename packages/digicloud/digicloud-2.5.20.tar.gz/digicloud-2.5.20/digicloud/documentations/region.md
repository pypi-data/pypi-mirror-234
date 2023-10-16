Regions, Don't Put All your Eggs in One Basket


Digicloud is a multi-region cloud service provider, so it allows you to keep your resources in different geographical 
locations, to avoid having a single point of failure in your system. to be clear, objects in a namespace could be located
in different regions, for example you might have a namespace for your production environment, and in that namespace you have
different instances in different regions.


## Examples


1. **Listing available regions**
    
    You can list all the available regions using the following command:

        $ digicloud region list

2. **Changing current region**
    
    In order to manage different objects in different regions using CLI, you need to have set an active region:

        $ digicloud region select

2. **Check your current region**
    
    You can also check you currently active region via:

        $ digicloud region current

