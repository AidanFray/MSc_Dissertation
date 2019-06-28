
cd ../frontend
./deploy.sh

cd ../production
rm -rf ./website website.zip
mkdir website

cp -r ../backend/* ./website

rm -rf ./website/env
rm -rf ./website/__pycache__
rm -rf ./website/audio

echo "BASE_FILE_LOCATION = \"/home/AFray/website/\"" > ./website/CONFIG.py

zip -s 90M -r website.zip website

rm -rf website