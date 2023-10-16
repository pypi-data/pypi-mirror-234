Edge Service, a line in front of your servers

Edge service is one of the Digicloud services that provide DNS and CDN services for you.
For now services like dns records, locations, firewalls, clusters(upstreams) are in edge service.

DNS

What is a DNS? The Domain Name System (DNS) is the phonebook of the Internet.
Humans access information online through domain names, like digicloud.com or digikala.com.
Web browsers interact through Internet Protocol (IP) addresses.
DNS translates domain names to IP addresses so browsers can load Internet resources.

Domain

What is a domain? A domain name is the identity of one or more IP addresses.
Domain names are invented as it is easy to remember a name rather than a long string of numbers.

Digicloud present you DNS service. You can add your domain and records.
Notice that these operations are related to your digicloud namespace.

To active edge service on your domain after creating your domain in digicloud.
You should add digicloud NS records to your NS records.

> Please change your domain NS records to ns1.digikalacloud.com and ns2.digikalacloud.com .

## Examples:
    
1 **Create a Domain**

    $ digicloud edg domain create digicloud.com

2 **List Domains**

    $ digicloud edge domain list

3 **Delete a Domain**

    $ digicloud edge domain delete digicloud.com

4 **Show a Domain**

    $ digicloud edge domain show digicloud.com


Record

What is a record? DNS records are instructions that live in authoritative DNS servers and 
provide information about a domain including what IP address is associated with that domain
and how to handle requests for that domain.

All DNS records have a TTL, which stands for time-to-live, and indicates how often a DNS server will refresh that record.

Supported types of DNS record in DigiCloud:

* A Record:

    The record that holds the IP address of a domain.

* TXT Record:

    Lets an admin store text notes in the record.

* CNAME Record:

    Forwards one domain or subdomain to another domain, does NOT provide an IP address.

* MX Record:

    Directs mail to an email server.

* SRV Record:

    Specifies a port for specific services.

Record name hints:

    The `@` symbol in bellow examples indicates that this is a record for the root domain.
    Root domain is the name of your record domain.
    The `*` symbol stands for wildcard, it will match requests for non-existent domain names.

TTL choices:

    2m, 10m, 30m, 1h, 3h, 10h

Record type choices:

    A, TXT, CNAME, MX, SRV

SRV record proto choices:

    _tcp, _udp, _tls

## Examples:

1 **Create a Record type A**

    $ digicloud edge record create
      --domain your-domain-name-or-id
      --name @
      --ttl 2m
      --type A
      --proxy true
      --ip-address 10.10.10.10

2 **Create a Record type TXT**

    $ digicloud edge record create
      --domain your-domain-name-or-id
      --name '*'
      --ttl 2m
      --type TXT
      --content "my content"

3 **Create a Record type CNAME**

    $ digicloud edge record create
      --domain your-domain-name-or-id
      --name my-record
      --ttl 2m
      --type CNAME
      --proxy false
      --target digikala.com

4 **Create a Record type MX**

    $ digicloud edge record create
      --domain your-domain-name-or-id
      --name my-record
      --ttl 2m
      --type MX
      --mail-server mail.com
      --priority 100

5 **Create a Record type SRV**

    $ digicloud edge record create
      --domain your-domain-name-or-id
      --name my-record
      --ttl 2m
      --type SRV
      --port 8000
      --weight 100
      --proto _tcp
      --service _servicename
      --target digicloud.com
      --priority 100

6 **List Records of a domain**

    $ digicloud edge record list --domain your-domain-name-or-id

9 **Get a Record details**

    $ digicloud edge record show record-id --domain your-domain-name-or-id

8 **Update a Record**

Note record type can not be changed.

    $ digicloud edge record update record-id --name new_name --domain your-domain-name-or-id

9 **Delete a Record**

    $ digicloud edge record delete record-id --domain your-domain-name-or-id


CDN
Content Delivery Network

A content delivery network or content distribution network (CDN) refers to a geographically distributed group of servers
which work together to provide fast delivery of Internet content.

Upstream or Cluster is a set of servers for load balancing.

10 **Create an upstream**

    $ digicloud edge upstream create
      --domain your-domain-name-or-id
      --name my-upstream
      --ssl-policy http
      --lb-method round_robin
      --keep-alive 3

11 **List upstream a domain**

    $ digicloud edge upstream list --domain your-domain-name-or-id

12 **Get an upstream details**

    $ digicloud edge upstream show upstream-name-id --domain your-domain-name-or-id

13 **Update an upstream**

    $ digicloud edge upstream update upstream-name-id
      --name new-upstream
      --ssl-policy https
      --lb-method consistent_ip_hash
      --keep-alive 5

14 **Delete an upstream**

    $ digicloud edge upstream delete upstream-name-id --domain your-domain-name-or-id


15 **Create an upstream Server**

    $ digicloud edge upstream server create
      --domain your-domain-name-or-id
      --upstream upstream-name-id
      --ip-domain 10.25.36.78
      --port 8007
      --weight 10
      --fail-timeout 20

16 **List upstream Servers of a domain**

    $ digicloud edge upstream server list
      --domain your-domain-name-or-id
      --upstream upstream-name-id

17 **Get an upstream details**

    $ digicloud edge upstream server show server-id
      --domain your-domain-name-or-id
      --upstream upstream-name-id

18 **Update an upstream Server**

    $ digicloud edge upstream server update server-id
      --domain your-domain-name-or-id
      --upstream upstream-name-id
      --ip-domain localhost.com
      --port 8008
      --weight 20
      --fail-timeout 10

19 **Delete an upstream**

    $ digicloud edge upstream server delete server-id
      --domain your-domain-name-or-id
      --upstream upstream-name-id

Your domain has some default ssl settings. You can update those settings.

20 **Get a ssl details**

    $ digicloud edge ssl show your-domain-name-or-id

21 **Update a ssl Server**
    
    Type choices: custom, auto
    
    --Custom Type--

    $ digicloud edge ssl update your-domain-name-or-id
      --type custom
      --policy normal
      --enable true
      --hsts false
      --https-redirect true
      --public-key ~/.ssh/id_rsa.pub
      --private-key ~/.ssh/id_rsa
    
    --Auto Type--

    $ digicloud edge ssl update your-domain-name-or-id
      --type auto
      --policy normal
      --enable true
      --hsts false
      --https-redirect true

You can separate the path or extensions of your domain to different locations.
Each location should connect to an upstream. So you can have load balancing on each part of your domain.
Later on you can define firewall rules for the locations.

22 **Create a location**

    $ digicloud edge location create
      --domain your-domain-name-or-id
      --upstream upstream-id
      --name my-location
      --path /digicloud/
      --path-type extension
      --path-extensions .jpg .mp3
      --origin-headers ~/path/to/origin-headers-file
      --response-headers ~/path/to/response-headers-file

23 **List location of a domain**

    $ digicloud edge location list
      --domain your-domain-name-or-id

24 **Get a location details**

    $ digicloud edge location show location-name-id
      --domain your-domain-name-or-id

25 **Update a location**

    $ digicloud edg location update location-name-id
      --domain your-domain-name-or-id
      --upstream new-upstream-id
      --name my-location-new-name
      --path /digicloud/other
      --path-type prefix
      --origin-headers ~/path/to/new/origin-headers-file
      --response-headers ~/path/to/new/response-headers-file

26 **Delete a location**

    $ digicloud edge location delete location-name-id
      --domain your-domain-name-or-id

Firewall

Each firewall rule has an input type, and base on that you provide a value.
The requests to the location you provided will check with these rules.
Rules will order by priority ASC. When ever there is match. Firewall will run the rule action.
If there is no match the request will be allowed to continue his journey.
To have a list of available choices for country and continent you can visit: http://www.geonames.org/countries/
for countries check the ISO-3166 alpha2.
    
    input choices: ip, asn, country, continent
    action choices: allow, block, javascript_challenge, captcha_challenge
    operator choices: eq, neq
    priority should be unique the lower priority the higher impact in firewall list

27 **Create a firewall**

    $ digicloud edge firewall create
      --domain your-domain-name-or-id
      --location location-name-id
      --input country
      --value ir
      --action allow
      --operator neq
      --priority 20

28 **List firewall of a domain**

    $ digicloud edge firewall list
      --domain your-domain-name-or-id

29 **Get a firewall details**

    $ digicloud edge firewall show firewall-id
      --domain your-domain-name-or-id

30 **Update a firewall**

    $ digicloud edge firewall update firewall-id
      --domain your-domain-name-or-id
      --location location-name-id
      --input ip
      --value 12.34.56.78
      --action block
      --operator eq
      --priority 21

31 **Delete a firewall**

    $ digicloud edge firewall delete firewall-id
      --domain your-domain-name-or-id

Your domain has some default general settings. You can update those settings.

32 **Get a general setting details**

    $ digicloud edge general setting show your-domain-name-or-id

33 **Update a ssl Server**

    $ digicloud edge ssl update your-domain-name-or-id
      --developer-mode false
      --maintenance-mode true
      --redirect-to-www true
      --ip-geolocation true
      --intercept-errors true
      --max-upload-size 100
      ----custom-host-header MyHeader
      --origin-headers ~/sample_headers.txt
      --response-headers ~/sample_headers.txt

34 **Purge cache**

    $ digicloud edge purge cache your-domain-name-or-id
      --url https://digicloud.com/
      --method GET
      --cookies sample_path_file

>> cookies file content should json format. It should be a hashmap of key and values.

35 **Show Domain DNSSEC Details**

    $ digicloud edge domain dnssec show your-domain-name-or-id

36 **Enable Domain DNSSEC**

    $ digicloud edge domain dnssec enable your-domain-name-or-id

37 **Disable Domain DNSSEC**

    $ digicloud edge domain dnssec disable your-domain-name-or-id

38 **Show Domain NS Records settings**

    $ digicloud edge domain verify show your-domain-name-or-id

39 **Verify Domain NS Records**

    $ digicloud edge domain verify your-domain-name-or-id

40 **Create a rate limit**

    $ digicloud edge rate limit create
      --domain your-domain-name-or-id
      --name my-rate-limit
      --request 1000
      --burst 50
      --time m
      --exclusions 8.8.8.8

41 **List rate limits of a domain**

    $ digicloud edge rate limit list
      --domain your-domain-name-or-id

42 **Get a rate limit details**

    $ digicloud edge rate limit show rate-limit-name-id
      --domain your-domain-name-or-id

43 **Update a rate limit**

    $ digicloud edge rate limit update rate-limit-name-id
      --domain your-domain-name-or-id
      --name new-name
      --requests 23
      --burst 25
      --time s
      --exclusions 109.23.36.96 23.65.98.45 12.79.56.35

44 **Delete a rate limit**

    $ digicloud edge rate limit delete rate-limit-name-id
      --domain your-domain-name-or-id
