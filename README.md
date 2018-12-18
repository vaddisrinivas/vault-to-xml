# vault-to-xml
python script that brings your passwords from Hashicorp vault and pushes 
them to 
'server.xml' of your web-services.  
As a piece of our effort to automate the flow on the admin side, or 
rather more like a touchless architechture, we have decided to use a 
"Vault" to
make sure the sensitive information flows but directly. 

At the time of writing this code, open-source vault solution 
from HasiCorp Vault, was chosen to store and secure passwords.

This piece of code intends to bring your secrets from Hashicorp Vault 
using 
"hvac client", a libraby created, maintained and updated by Community.


Here although the Vault supports the creation of Secrets Engine with 
Version 2,
at the time of writing this code, the API  support for the same was found 
to be 
flawed/inoperable. Hence, this code works for any secrets engine that was 
created by using "Version 1".

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\
----------------------------organisation of project----------------------
-------

|- setup.py ------------- installs the dependencies----------------------
-------
|- run.py  -------once, if your config file is set properly, just run 
this------
|-vault_config.yml---------replace the values here and, thats all it 
takes--NEW

You can add it to any of the cron jobs, so that it polls HashiCorp Vault 
and
                            gets things for you. 
--------------------------------How to use this--------------------------
-------
First run "python setup.py install"

now, 

Set  your environment variables , VAULT_CONFIG 
  if you are on linux-----
  export VAULT_CONFIG="yourfilelocation"
-------------------------------------------------------------------------
-------

Also works with json, just change the "config_yml" everywhere to 
"config_json"

-------------------------------------EOF---------------------------------
-------

He who writes the code,alone knows how to use it.
He who documents it, lets anyone yield from  it.
