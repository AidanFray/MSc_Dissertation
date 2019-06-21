rm -rvf ./website website.zip
mkdir website

cp -r ../frontend/build ./website
cp -r ../backend/ ./website

rm -rvf ./website/backend/env

zip -r website.zip website
