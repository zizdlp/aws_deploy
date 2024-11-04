include .env
fetch:
	curl -H "Authorization: token ${ACT_TOKEN}" \
  	https://api.github.com/repos/${OWNER}/${REPO}/actions/runs/11515533351/artifacts
art:
	curl -L -H "Authorization: token ${ACT_TOKEN}" \
	-o spark_result.zip \
	https://api.github.com/repos/${OWNER}/${REPO}/actions/artifacts/2108722924/zip
login:
	ssh -i aws_test_us.pem ec2-user@ec2-184-73-88-74.compute-1.amazonaws.com
