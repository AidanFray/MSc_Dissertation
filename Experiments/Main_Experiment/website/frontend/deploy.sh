# Clean up
rm -rf ../backend/build
rm -rf build

npm run build

cp -r build ../backend
rm -rf build