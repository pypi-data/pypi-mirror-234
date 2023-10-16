Namespaces, Organize your teams and projects


Digicloud Namespace allows you to organize your resources. For example if you have separate teams working on different projects
 or you want to keep different environments (like production, staging, QA) fully separated, Then you can use Digicloud namespaces. 
Every Namespace has its members and is also billed separately. 

## Examples


1. **Creating a namespace**
    
    You can create a namespace by using the following command, you just need to choose a name, for example myblog:

        $ digicloud namespace create myblog

2. **Listing your namespaces**
    
    Every user could be a member of different namespaces, you can check all your current namespaces:

        $ digicloud namespace list

3. **Current Namespace**
    
    In order to manage different namespaces using CLI, you should check and change active namespace in your CLI. to check 
your active namespace you can use:

        $ digicloud namespace current
    
    and to change it you can use:
 
        $ digicloud namespace select myblog

Quota

What is a Quota? It's a limitation for namespaces to use DigiCloud resources.
There are different type of limitations in DigiCloud.
For example a namespace may limited to create less than 2 instance in a specific region.
Quota has some rules for different resources that a namespace should obey.
If a namespace need more resources, it should create a quota request with new required value.


## Examples:

1 **List Quotas**

    $ digicloud namespace quota list

2 **List Quota Requests**

    $ digicloud namespace quota request list

3 **Request More Quota**

To request more quota on a certain quota. Use your desired quota id and your required value.

    $ digicloud namespace quota request
      --quota-id iaas.fip.namespace.count
      --value 10

Some of the quotas have same quota ids. To send your desired quota, you should mention it's quota index.
Quota index is an optional parameter, and command will ask you to provide it in certain quota requests.

    $ digicloud namespace quota request
      --quota-id dns.namespace.domain.record.count
      --value 20
      --quota-index 7 Required on certain rules
