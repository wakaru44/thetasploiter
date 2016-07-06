# Thetasploiter

Spin up a minimal linux instance with [Metasploit](metasploit.com), add some modules, and lets you run it.

- The instance is created with a cloudformation stack created with troposphere
- The configuration is done with Ansible
- And the scaner will be one day done with a custom Python script. #TODO

![theta symbol](http://www.wallquotes.com/sites/default/files/arts0158-88.png)

# Usage

To install, you can use the damn curl|bash

    curl https://raw.github.com/wakaru44/thetasploit/install.sh | bash -x

At least i left debug enabled so you can see what is it doing.


Then, you will need your virtualenv shit in order.

    make install
    source ENV/bin/activate

and check that you have everything with 

    pip freeze
    which pip

For the full list of commands, just run

    make

in the root of the repo
