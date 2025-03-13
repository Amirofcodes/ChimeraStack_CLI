#!/bin/bash
# Build executables for all platforms

# Ensure PyInstaller is installed
pip install pyinstaller

# Clean previous PyInstaller builds without removing PyPI packages
if [ -d "build" ]; then
  rm -rf build
fi

if [ -d "dist" ]; then
  # Remove only executable files, not wheel (.whl) or source (.tar.gz) packages
  find dist -type f -not -name "*.whl" -not -name "*.tar.gz" -delete
fi

# Build for current platform
echo "Building executable for $(uname -s)"
pyinstaller chimera-stack-cli.spec

# Create release directory
mkdir -p releases
cp dist/chimera-stack-cli* releases/

echo "Build complete! Executables are in the 'releases' directory."