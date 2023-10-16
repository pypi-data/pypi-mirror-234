Firewalls, Full Control over your instance traffic

In Digicloud, a Firewall is a set of rules to control the network traffic of an instance. in order to use Firewalls,
first you create one, and then add your rules in it, finally you can apply your firewall on an instance.
Each rule requires the following parameters:
* **direction**: Ingress or egress, which is the direction in which the firewall rule is applied.
* **ethertype**: Must be IPv4 or IPv6, and addresses represented in CIDR must match the ingress or egress rules.
* **port-range-min**: The minimum port number in the range that is matched by the firewall rule.
* **port-range-max**: The maximum port number in the range that is matched by the firewall rule.
* **protocol**: ICMP, TCP and lovely UDP, the protocol you want to apply this rule on it.
* **remote-ip-prefix**: The remote IP you want to apply this rule on it, could ba single IP or a range IP

So pretty easy, right? let's see some examples


## Examples:

1. **Checking default Firewall**

    When your namespace got created, we create a default firewall for you, let's check it out

        $ digicloud firewall list
     You can check the rules in the `default` firewall via:
        $ digicloud firewall rule list default
        
2. **Creating your own Firewall**

    Creating the firewall itself is just a single command:

        $ digicloud firewall create my-awesome-firewall --description "I love Digicloud <3"
        
    Now you have a firewall with some default rules in it, let's get rid of them:
    
        $ digicloud firewall rule list my-awesome-firewall \ 
            -c id -f value | \
            xargs -I{} digicloud firewall rule delete {} --firewall my-awesome-firewall
    
    Let's allow ICMP packets, both ways:

        $ digicloud firewall rule create my-awesome-firewall --protocol icmp --direction ingress
        $ digicloud firewall rule create my-awesome-firewall --protocol icmp --direction egress
       
    Let's allow SSH connections:

        $ digicloud firewall rule create my-awesome-firewall --protocol tcp \
            --port-range-min 22 \
            --port-range-max 22 \
            --direction ingress 
    
3. **Applying our awesome firewall on an instance**
    you can apply your firewall on an instance while creating it:

        # Creating of an advanced instance with our firewall
        $ digicloud instance create master_server \
                        --network net8 \
                        --instance-type g1.micro \
                        --image Debian_9 \
                        --firewall my-awesome-firewall

    