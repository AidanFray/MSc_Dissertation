
cd ../frontend
./deploy.sh

cd ../production
rm -rvf ./website website.zip
mkdir website

cp -r ../backend/* ./website

rm -rvf ./website/env
rm -rvf ./website/__pycache__

zip -r website.zip website

rm -rvf website
