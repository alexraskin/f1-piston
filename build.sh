ACCOUNT="088966585880"
REGION="us-west-2"
REPO="streamlit-app"

echo "Please enter Docker image tag:"
read -s TAG

docker build -t ${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/${REPO} $TAG

aws ecr get-login-password \
    --profile personal \
    --region ${REGION} \
| docker login \
    --username AWS \
    --password-stdin ${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com

docker push ${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/${REPO}