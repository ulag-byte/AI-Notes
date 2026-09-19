# AWS cheat sheet

## CLI basics
- `aws configure` set access key, secret, default region
- `aws sts get-caller-identity` which account/user am I?
- `aws ec2 describe-instances --query "Reservations[].Instances[].[InstanceId,State.Name]" --output table`
- `aws s3 ls` list buckets; `aws s3 cp file.txt s3://my-bucket/`

## EC2
- Free-plan instance types: `t3.micro` / `t4g.micro` (check your region)
- Security group = instance firewall. Open only 22 (your IP) and 80/443.
- Stopped instances don't cost compute, but EBS volumes and Elastic IPs still cost money.

## IAM
- Never use the root user day to day; create an IAM user or use IAM Identity Center.
- Give EC2 permissions through an IAM role (instance profile), not access keys on the server.
- Least privilege: e.g. only `bedrock:InvokeModel` for the Bedrock model you use.

## Bedrock
- Call models with the `bedrock-runtime` Converse API.
- Amazon Nova Micro (`amazon.nova-micro-v1:0`) is one of the cheapest text models.

## Cost safety
- Create an AWS Budget alert at $1 before creating resources.
- Avoid EKS (~$73/month control plane) and NAT Gateways (~$32/month + data).
- `terraform destroy` at the end of every session.
