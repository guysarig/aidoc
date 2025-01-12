#!/bin/bash

# Usage: ./lambda_packer.sh <source_directory> <requirements_file> <s3_bucket_name>

SOURCE_DIR=$1
FUNCTION_NAME=$2
REQUIREMENTS_FILE=${3:-requirements.txt}
LAMBDA_PAYLOADS_DIR=$4
S3_BUCKET=$5
BUILD_DIR="build"
ZIP_FILE="lambda_package.zip"

# Create build directory
mkdir -p $BUILD_DIR

# Install dependencies
pip3 install -r $SOURCE_DIR/$FUNCTION_NAME/$REQUIREMENTS_FILE -t $BUILD_DIR

# Copy source files
cp -R $SOURCE_DIR/$FUNCTION_NAME/* $BUILD_DIR/

# Create zip package
cd $BUILD_DIR && zip -r ../$ZIP_FILE .
cd ..

echo "Lambda payloads built successfully."

echo "Uploading to S3"
# Upload to S3
aws s3 cp $ZIP_FILE s3://$S3_BUCKET/lambda_payloads/$FUNCTION_NAME.zip

echo "Lambda payloads uploaded successfully."