##########################################
#  Script to update existing KMS policy  #
# Developed by Mohd Irfan bin Mohd Nizam #
##########################################

import json
from urllib import response
import boto3

client = boto3.client('kms')


# Obtain KMS key alias from user
keyAlias = input("Enter KMS key alias to be updated: ")


# Extract existing KMS key policy
response = client.describe_key(
    KeyId="alias/" + keyAlias
)
keyARN = response["KeyMetadata"]["Arn"]

response = client.get_key_policy(
    KeyId=keyARN,
    PolicyName='default'
)

originalKMSPolicy = response["Policy"]


# Policy to be added
addPolicy = {
    "Sid": "Allow use of the key",
    "Effect": "Allow",
    "Principal": {
        "AWS": "arn:aws:iam::835217661988:user/weng"
    },
    "Action": [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:ReEncrypt*",
        "kms:GenerateDataKey*",
        "kms:DescribeKey"
    ],
    "Resource": "*"
}

# Update existing policy
updatedKMSPolicy = json.loads(originalKMSPolicy)
updatedKMSPolicy["Statement"].append(addPolicy)

response = client.put_key_policy(
    KeyId=keyARN,
    PolicyName='default',
    Policy=json.dumps(updatedKMSPolicy)
)


# Print key ARN, original KMS policy, policy to be added, updated KMS policy
print("\nKMS key ARN:", keyARN)
print("\nOriginal KMS policy: \n", originalKMSPolicy)
print("\nPolicy to be added:\n",json.dumps(addPolicy,indent=4))
print("\nUpdated policy for", keyAlias, ":\n",
      json.dumps(updatedKMSPolicy, indent=4))