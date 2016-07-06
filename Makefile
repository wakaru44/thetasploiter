# A simple makefile to make things simpler

help:
	@echo "Troposphere code to generate a kali workstation in the cloud";
	@echo "";
	@echo "generate       - generate the cloud formation stack from py to json";
	@echo "bump           - Bump the version of the stack, as it will be identified in AWS";
	@echo "create         - make the call to the AWS cli to spin up the instance";
	@echo "spinup         - Do everything. From the generation to the creation";
	@echo "describe       - describe AWS instances in a nice way";
	@echo "long-describe  - describe AWS instances in a LONG way";
	@echo "todo           - Will print all the TODO's in the code";
	@echo "fab            - Show the tasks available in the fabfile";
	@echo "";

generate:
	cd spinup; python kalinstance.py > kalinstance.json







long-describe:
	aws  ec2 describe-instances  --query 'Reservations[*].Instances[*].[InstanceId,Tags,PublicDnsName,KeyName]'

describe:
	#aws  ec2 describe-instances  --query 'Reservations[*].Instances[*].[InstanceId,Tags,PublicDnsName,KeyName]'  --output text | grep -B 1 stack-name
	aws  ec2 describe-instances  --query 'Reservations[*].Instances[*].[InstanceId,PublicDnsName,KeyName]'  --output json --filters "Name=tag-value,Values=personal$(shell cat version.md )" | grep -v "\]\|\["


todo:
	grep  -r "TODO:" * --exclude-dir ENV --exclude Makefile


