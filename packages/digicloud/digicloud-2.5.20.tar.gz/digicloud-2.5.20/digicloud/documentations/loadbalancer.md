LoadBalancer

DigiCloud LoadBalancer is capable of distributing TCP traffic to multiple TCP worker servers based 
on several predefined algorithms; such a capability is made possible by several objects:

 - LoaDBalancer: The object encloses all necessary objects in order to configure a TCP LoadBalancer. 
 An IP address is assigned to the object automatically after creation, 
 this is the LoadBalancer public accessible address.
 - BackEnd: The object contains the actual workers called backend members, 
 each member is uniquely identified by an IP-Port combination and should listen on the specified TCP port.
 - Health check: An object declared inside a Backend in order to monitor its members 
 with a couple of attributes to tune the monitoring process. 
 Health check object has an "operating_status" attribute by which the status of the member is represented,
 these statuses are as follows:

| Status   | Description                                     |
|----------|-------------------------------------------------|
| ONLINE   | All backend members are healthy                 |
| DEGRADED | One or more of the backend members are in ERROR |
| ERROR    | All of the backend members are in ERROR         |

Note that only one health check is available per backend.
 - BackEnd Member: The object represent a worker server and is created by an IP address and a port.
 Each backend member has an "operating_status" attribute by which the status of the member is represented,
 these statuses are as follows:

| Status     | Description                                                                            |
|------------|----------------------------------------------------------------------------------------|
| ONLINE     | The member is operating normally                                                       |
| DRAINING   | The member is not accepting new connections                                            |
| ERROR      | The member is failing it’s health monitoring checks                                    |
| NO_MONITOR | No health monitor is configured for this member(its backend) and its status is unknown |

 - FrontEnd: The object is responsible for listening to incoming TCP traffic on a specified port.  

## Examples:

### LoadBalancer

1 **Create a Load Balancer**

    $ digicloud loadbalancer create my_load_balancer_name
        --description "My load balancer description"
2 **List Load Balancer**

    $ digicloud loadbalancer list
3 **Load Balancer details**

    $ digicloud loadbalancer show my_load_balancer_name
4 **Update a Load balancer**

    $ digicloud loadbalancer update my_load_balancer_name
        --name my_new_load_balancer_name
        --description "My load balancer description"
5 **Delete a Load Balancer**

    $ digicloud loadbalancer delete my_load_balancer_name

### Backend

6 **Create backend**

    $ digicloud loadbalancer backend create my_load_balancer_name 
        --algorithm round_robin
7 **List backends**

    $ digicloud loadbalancer backend list my_load_balancer_name
8 **Delete a backend**

    $ digicloud loadbalancer backend delete my_load_balancer_name 
        --backend-id 7a9542d71aea41508462d4b55eb58e1a

### Backend member

9 **Add a backend member**

    $ digicloud loadbalancer backend member add my_load_balancer_name 
        --backend-id 7a9542d71aea41508462d4b55eb58e1a 
        --ip-address 192.168.1.42 --port 42
10 **List backend members**

    $ digicloud loadbalancer backend member list  
        --backend-id 41779a0b4ad14d11873ed1876c5bbbd0
11 **Remove a backend member**

    $ digicloud loadbalancer backend member remove my_load_balancer_name 
        --backend-id 7a9542d71aea41508462d4b55eb58e8a  
        --member-id fe6a484ac6874b09a87d568952b1c103

### Health Check

12 **Create a health check**
    
    $ digicloud loadbalancer backend health check create my_load_balancer_name 
        --backend-id 365fc22d8be64b59aa14085109c46cd1 
        --name hc-42 
        --delay 5 
        --timeout 5 
        --max-retries 2
        --max-retries-down 2

13 **list health checks**
    
    $ digicloud loadbalancer backend health check list my_load_balancer_name 
        --backend-id 365fc22d8be64b59aa14085109c46cd1
13 **Delete a health check**
    
    $ digicloud loadbalancer backend health check delete my_load_balancer_name 
        --backend-id 5b19cce6d109430f97f19611817e38f1 
        --health-check-id 6fd453429ce44152b27a4f3d3dc35554

### Frontend

14 **Create a frontend**

    $ digicloud loadbalancer frontend create my_load_balancer_name 
        --timeout-client-data 5000 
        --timeout-tcp-inspect 3000 
        --timeout-member-connect 2000 
        --timeout_member_data 1000 
        --connection-limit 10 
        --default-backend 365fc22d8be64b59aa14085109c46cd1 
        --port 80
15 **List frontends**

    $ digicloud loadbalancer frontend list my_load_balancer_name
16 **Delete a Frontend**
    
    $ digicloud loadbalancer frontend delete asghar --frontend-id 7c74f6342d7b44628519dc4c7ad499ac
17 **Set Default backend for a frontend**
    
    $ digicloud loadbalancer frontend set backend my_load_balancer_name 
      --frontend-id 5d83e06892af403ca17ad937a002bc49 
      --default-backend c27df98c72ba4c218d51b48bb1c77465
18 **Delete default backend for a frontend**

    $ digicloud loadbalancer frontend delete backend my_load_balancer_name 
      --frontend-id 5d83e06892af403ca17ad937a002bc49 
