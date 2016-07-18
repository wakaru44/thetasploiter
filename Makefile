# A simple makefile to make things simpler

help:
	@echo "Troposphere code to generate a kali workstation in the cloud";
	@echo "";
	@echo "keygen         - create your personal keys. You should do this only once";
	@echo "";
	@echo "generate       - generate the cloud formation stack from py to json";
	@echo "bump           - Bump the version of the stack, as it will be identified in AWS";
	@echo "create         - make the call to the AWS cli to spin up the instance";
	@echo "magic          - Do everything. From the generation to the creation";
	@echo "";
	@echo "describe       - describe AWS instances in a nice way";
	@echo "long-describe  - describe AWS instances in a LONG way";
	@echo "todo           - Will print all the TODO's in the code";
	@echo "fab            - Show the tasks available in the fabfile";
	@echo "";

keygen:
	fab create_key

generate:
	cd spinup; python kalinstance.py > kalinstance.json

create:
	cd spinup; bash tool_createstack.sh

bump:
	$(shell echo $(shell python -c "fh=open('spinup/version.md');c=fh.readline();n=int(c.strip()); print '{0:03d}'.format(n+1) " ) > spinup/version.md)

describe:
	#aws  ec2 describe-instances  --query 'Reservations[*].Instances[*].[InstanceId,PublicDnsName,KeyName]'  --output json --filters "Name=tag-value,Values=KaliNstance$(shell cat version.md )" | grep -v "\]\|\["
	fab describe

magic: bump generate create describe


long-describe:
	aws  ec2 describe-instances  --query 'Reservations[*].Instances[*].[InstanceId,Tags,PublicDnsName,KeyName,State.Name]'


todo:
	grep  -r "TODO:" * --exclude-dir ENV --exclude Makefile


