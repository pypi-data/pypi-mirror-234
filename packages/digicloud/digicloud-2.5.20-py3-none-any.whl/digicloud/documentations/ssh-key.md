SSH Keys, Asymmetric Authentication for accessing your instances 

Once you have a Linux server, you need some sort of authentication mechanism so only authorized personal could access
the server. One way is to use the password which will be sent via Email, but there is a better way: using your SSH Key
Once you generated your own SSH keys, you will have a pair of keys: Public and private, the private key is your identity 
you should keep it somewhere safe an don't share it with anybody ever. The public key is on the other hand is what let 
others identify you as you.
For example you give your public key to Digicloud, and we can inject it to instances so you don't need to use the password
to access your instances.
Although there are a limitation, Digicloud can only inject your key in the instance creation process, and once 
an instance is created, Digicloud can't inject your SSH key in it, since we don't  have access to your instance, and you
 need to do it yourself.
Please remember, if you upload a SSH-key, it's yours and it does not belong to the namespace, it belongs to your account.
 


## Examples:

1. **Listing Your SSH keys**

    You can check your current SSH keys via:

        $ digicloud ssh key list
        
2. **Upload You SSH key**

    Assuming you have a valid SSH key in `~/.ssh/id_rsa.pub`, you can upload it to digicloud via: 

        $ digicloud ssh key create red_key --public-key ~/.ssh/id_rsa.pub
        
3. **Create instance using your SSH key**
    
    Once you uploaded you SSH key, using it is easy as follow:

        # Creating of a simple instance with our new SSH key
        $ digicloud instance create master_server \
                        --simple \
                        --instance-type g1.micro \
                        --image Debian_9
                        --ssh-key red_key
