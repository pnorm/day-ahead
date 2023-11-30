#!/bin/bash

# Directory structure
directories=(
    "api/utils"
    "data/external"
    "data/interim"
    "data/processed"
    "data/raw/"
    # "models"
    "notebooks"
    # "references"
    # "reports/figures"
    "src/data/logs"
    "src/data/tests"
    "src/data/utils"
    # "src/features"
    "src/models"
    "src/visualization"
)

# Create dirs
for dir in "${directories[@]}"; do
    mkdir -p "$dir"
done

echo "Directory structure created successfully!"

src_directories=(
    "api"
    "api/utils"
    "src"
    "src/data"
    # "src/features"
    "src/models"
    "src/visualization"
)

# Create __init__.py files in the specified directories
for dir in "${src_directories[@]}"; do
    touch "$dir/__init__.py"
done

echo "__init__.py files created successfully in src/ and its subdirectories!"

unzip data.zip

echo "data.zip extracted successfully."

touch README.md
touch .gitignore
touch env.sample

echo "README.md .gitignore env.sample files created."

unzip model.zip

echo "Model unzipped successfully"