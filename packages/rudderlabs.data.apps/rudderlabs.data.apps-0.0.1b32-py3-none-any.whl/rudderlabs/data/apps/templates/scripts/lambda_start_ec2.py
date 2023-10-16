import boto3

# Ref: https://stackoverflow.com/questions/49622575/schedule-to-start-an-ec2-instance-and-run-a-python-script-within-it

def lambda_handler(event, context):

    # change the region to your region
    ec2 = boto3.client("ec2", region_name="{{ region }}") 

    # Change the instance id to your instance id
    ec2.start_instances(InstanceIds=["{{ instance_id }}"]) 
    print("Started your instances")
    return
