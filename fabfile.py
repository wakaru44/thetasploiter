#!/usr/bin/python
# -*- utf-8 -*-

from fabric.api import local,task


def do(command):
    """
    fabric is still uncomfortable
    """
    output = None # by default
    try:
        output=local(command,capture=True)
        print output
    except Exception as pokemon:
        print pokemon
        print "Standard output"
        print output.stdout
        print "Standard Error"
        print output.stderr

    return output


def current_version():
    with open("version.md") as fh:
        return fh.readline()


def show_table(content):
    """
    try to paint a table with labels
    """
    #print "{:<8} {:<15} {:<10}".format('Key','Label','Number') #Headers
    for k, v in content.iteritems():
        num = v
        print "{:<8} {:<15}".format(k, num)


def create_json_params(keyname=None, dry=False):
    """
    receive the key name, and 
    return a json with the params for aws
    """
    with open("kalikey.pub") as fh:
        c = fh.readlines()
        pub = "".join(map(lambda x: x.strip(), c[1:-1]))
        params = { "KeyName":"kalikey", "DryRun":dry, "PublicKeyMaterial":pub}
        import json
        return json.dumps(params)

    # If something fails,  return None
    return None


@task
def describe():
    """
    show the minimum details required for an stack
    """
    query="""  'Reservations[*].Instances[*].[InstanceId,PublicDnsName,KeyName]' """
    filters = """ "Name=tag-value,Values=KaliNstance$(cat version.md )" """
    output = do("""aws  ec2 describe-instances  --query {query}  --output json --filters {filters} """.format(query=query,filters=filters))
    import json
    details=json.loads(output)
    key = details[0][0][2]
    dns = details[0][0][1]
    print("ssh -i ./{0}.pem ubuntu@{1}".format(key,dns))


@task
def long_describe():
    """
    show the interesting details for all the instances
    """
    query="""  'Reservations[*].Instances[*].[InstanceId,Tags,PublicDnsName,KeyName]' """
    filters = ""
    output = do("""aws  ec2 describe-instances  --query {query}  --output json --filters {filters} """.format(query=query,filters=filters))
    import json
    details=json.loads(output)
    print details
    datad= {"key":  details[0][0][2],
            "Public DNS":  details[0][0][3],
            "Tags": details[0][0][1]
            }
    show_table(datad)

@task
def bump_version():
    """Add a number to the version file"""
    # NOTE: for begginers. remember to add the r to the 2 quotes,
    #       specially when using newlines inside the script
    script = r"""
echo "Updating the version file"
echo "$(cat version.md ) +1" | bc | while read foo; do printf  "%03d\n" $foo; done > version.next.md
rm version.md 
mv version.next.md version.md
echo "Current version will be $(cat version.md)"
    """
    print(
            map(do, 
            map( lambda x: x.strip(),
                script.split("\n"))
            )
        )
################################################################################

@task
def list_stacks():
    """ print the list of the ALIVE stacks
    (creation completed and not destroyed) """

    do("aws cloudformation list-stacks --stack-status-filter=CREATE_COMPLETE")


@task
def con():
    """Print connection details"""
    # The public name of the instance
    instance = {}
    instance["dns"] = do(r"""aws  ec2 describe-instances  --query 'Reservations[*].Instances[*].[PublicDnsName]'  --output json --filters "Name=tag-value,Values=thetasploiter$( cat version.md )" | grep -v "\]\|\[" """ )
    print("Instance Id: {0}".format(instance["dns"]))
    if len(instance["dns"]) < 3:
        print("ERROR: the instance might not yet started. run 'fab start_instance'")

    instance["key"] = do("""cat create-stack-parameters.json  | jq '.[]' | grep -A 3 -B 1 KeyPair  | jq '.ParameterValue' | tr '"' ' ' """)
    print( "Your key should be in a file named: {0}".format(instance["key"]) )

    # The keystore where you normally keep your keys. 
    ssh_key_dir="./secret"
    print("{0}".format(ssh_key_dir))
    print( "You need to place your ssh key here or change 'ssh_key_dir' in this file:")
    from os.path import join
    ssh_keypath=join(ssh_key_dir,instance["key"])
    print(ssh_keypath)
    print("\nSorry, you have to copy paste that manually:\n")
    print("\tssh -F ssh_config -i {0}   ubuntu@{1}\n".format(ssh_keypath,instance["dns"]))
    local("\tssh -F ssh_config -i {0}   ubuntu@{1}\n".format(ssh_keypath,instance["dns"]))


@task
def create_stack(dry=True):
    """
    draft. creates a stack.
    """
    print( "Any parameter passed after calling the script will be appended to the aws cloudformation command")
    dry_run = "--dry-run" if dry else " "
    script = r"""
        NAME=thetasploiter$(cat version.md)
        TMPL=kalinstance.json
        CFNPARAMS=create-stack-parameters.json
        aws {0} cloudformation create-stack  --stack-name $NAME --template-body file://$TMPL  --cli-input-json file://$CFNPARAMS ${{@:2}}  | tee -a stack_id.log
    """.format(dry_run)
    # and run all of it in a single line
    # TODO: How to test the creation of cloud formation without real creation?
    do( 
        "; ".join(
            map( lambda x: x.strip(),
                script.split("\n")
            )
        )
    )


@task
def create_key(keyname="kalikey", dry=False):
    """
    get the key name and create the key, upload to aws and all that
    """
    # we can run dry too
    dryrun= "--dry-run" if dry else " "

    # first create a key using openssl
    do("openssl genrsa -out {0}.pem 2048".format(keyname))
    do("chmod 400 {0}.pem".format(keyname))

    # then extract the public one
    do(" openssl rsa -in {0}.pem -pubout > {0}.pub".format(keyname))

    # then put the public one in a command line params
    params = create_json_params(keyname, dry)
    with open("spinup/params.json","w") as fh:
        fh.writelines(params)

    # then run it against aws
    do("aws ec2 import-key-pair {0} --cli-input-json file://spinup/params.json".format(dryrun))

