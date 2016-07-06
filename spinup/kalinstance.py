
# Import troposphere
from troposphere import Template, Ref, Output, Join, GetAtt, Parameter, Base64
import troposphere.ec2 as ec2
from troposphere.route53 import RecordSetType

# Create a template for resources to live in
template = Template()

keypair = template.add_parameter(Parameter(
    "KeyPair",
    Type="String",
    Description="The name of the keypair to use for SSH access",
))

# Create a security group
sg = ec2.SecurityGroup('ThetasploiterSecurityGroup')
sg.GroupDescription = "Allow access to the Thetasploiter project instances from anywhere"
sg.SecurityGroupIngress = [
    ec2.SecurityGroupRule(
        IpProtocol="tcp",
        FromPort="22",
        ToPort="22",
        CidrIp="0.0.0.0/0",
    )]

# Add security group to template
template.add_resource(sg)

# Create a volume

storage01=[
   ec2.BlockDeviceMapping(
       DeviceName="/dev/sdb1",
       Ebs=ec2.EBSBlockDevice(
           VolumeSize="16"
       )
   ),
]

# Create an instance
instance = ec2.Instance("ThetasploiterInstance")
instance.ImageId = "ami-5a60c229" # TODO: Change  this to the kali minimal
instance.InstanceType = "m1.small"
instance.SecurityGroups = [Ref(sg)]
instance.KeyName = Ref(keypair)
instance.BlockDeviceMappings = storage01
instance.UserData = Base64("""
#!/bin/bash
curl http://juanantonio.fm/HIBOY
echo "this should be a script or sumzin"
""")

# Add instance to template
template.add_resource(instance)

# Add output to template
template.add_output(Output(
    "InstanceAccess",
    Description="Command to use to SSH to instance",
    Value=Join("", ["ssh -i ", Ref(keypair), " ubuntu@", GetAtt(instance, "PublicDnsName")]) #TODO: the kali default username
))


# Print out CloudFormation template in JSON
print template.to_json()


