
cd ../frontend
./deploy.sh

cd ../production
rm -rf ./website website.zip
mkdir website

cp -r ../backend/* ./website

rm -rf ./website/env
rm -rf ./website/__pycache__
rm -rf ./website/audio
rm     ./website/results/*.pkl

sed -i "s/\"\" #B700/\"\/home\/AFray\/website\/\"/g" ./website/CONFIG.py 

zip -s 90M -r website.zip website

rm -rf website
