Welcome to Digicloud CLI

Digicloud-CLI is a command line interface to access all Digicloud services.
To start, you need to have a digicloud account which you can create by visiting https://digicloud.ir

let's review a few features of Digicloud, and then create a server

# Login

$ digicloud account login


# checking list of images you can use to create a server

$ digicloud image list


# checking list of available server configurations you can use:

$ digicloud instance type list


# You can import your own SSH key, in this way you can access your server using SSH-key instead of a password

$ digicloud ssh key create work_key --public-key /path/to/you/public/key.pub

# Now let's create a simple server (a server without a fancy network configuration)
# you need to pick an image and instance-type for you server.

$ digicloud instance create my_first_server --simple --image Debian_9 --instance-type g1.tiny


# You should see the details of your new server, usually it takes some time until your server becomes operational,
# meanwhile we can check a few more features of Digicloud.
# Let's create a SSD volume (storage disk) with 10 Gigabytes size:

$ digicloud volume create my_first_volume --type SSD --size 10

# Now you should be able to see your volume details
# you can always check list of your objects using `list` command, for example:

$ digicloud volume list
or
$ digicloud instance list

# Now you can easily attach your volume to your instance:

$ digicloud instance volume attach my_first_server --volume my_first_volume
or
$ digicloud volume attach  my_first_volume --instance my_first_server

# These two commands do the same thing.


# Remember you can get more information about a command by using --help switch, like
$ digicloud instance create --help
