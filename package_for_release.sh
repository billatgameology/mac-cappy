#!/bin/bash
# Package mac-cappy for distribution

echo "Packaging mac-cappy for release..."

# Clean and build
echo "Building application..."
rm -rf build dist
source venv/bin/activate
python setup.py py2app

# Create a zip file for distribution
echo "Creating zip archive..."
cd dist
zip -r mac-cappy.zip mac-cappy.app
cd ..

echo ""
echo "✅ Package created: dist/mac-cappy.zip"
echo ""
echo "Next steps:"
echo "1. Go to: https://github.com/billatgameology/mac-cappy/releases/new"
echo "2. Create a new tag (e.g., v1.0.0)"
echo "3. Add release notes"
echo "4. Upload dist/mac-cappy.zip as a release asset"
echo "5. Publish the release"
echo ""
echo "Users can then download and unzip to use the app!"
