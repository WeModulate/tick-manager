#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to create a directory if it doesn't exist
create_dir() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        echo "Created directory: $1"
    else
        echo "Directory already exists: $1"
    fi
}

# Function to create a file with content if it doesn't exist
create_file() {
    if [ ! -f "$1" ]; then
        cat << EOF > "$1"
$2
EOF
        echo "Created file: $1"
    else
        echo "File already exists: $1"
    fi
}

# Function to create an executable file with content if it doesn't exist
create_executable_file() {
    create_file "$1" "$2"
    chmod +x "$1"
    echo "Set executable permission for: $1"
}

# Root directory
ROOT_DIR="."

# Define directories to create
DIRS=(
    "$ROOT_DIR/bin"
    "$ROOT_DIR/tick_manager/cli"
    "$ROOT_DIR/tick_manager/api"
    "$ROOT_DIR/tick_manager/operations"
    "$ROOT_DIR/tick_manager/models"
    "$ROOT_DIR/tick_manager/utils"
    "$ROOT_DIR/tick_manager/config"
    "$ROOT_DIR/scripts"
)

# Create directories
echo "Creating directories..."
for dir in "${DIRS[@]}"; do
    create_dir "$dir"
done

# Define files to create with their respective content
declare -A FILES_CONTENT=(
    ["$ROOT_DIR/bin/tick_manager"]="#!/usr/bin/env python
import sys
from tick_manager.cli.main import cli

if __name__ == \"__main__\":
    cli()
"

    ["$ROOT_DIR/tick_manager/__init__.py"]="# This file makes this directory a Python package."

    ["$ROOT_DIR/tick_manager/cli/__init__.py"]="# This file makes the cli directory a Python package."

    ["$ROOT_DIR/tick_manager/cli/main.py"]="import click

@click.group()
def cli():
    \"\"\"Tick Manager CLI\"\"\"
    pass

@cli.command()
def greet():
    \"\"\"Greet the user.\"\"\"
    click.echo(\"Hello, Tick Manager!\")
"

    ["$ROOT_DIR/tick_manager/api/__init__.py"]="# This file makes the api directory a Python package."

    ["$ROOT_DIR/tick_manager/api/main.py"]="from fastapi import FastAPI

app = FastAPI(title=\"Tick Manager API\")

@app.get('/')
def read_root():
    return {\"message\": \"Welcome to Tick Manager API\"}
"

    ["$ROOT_DIR/tick_manager/operations/__init__.py"]="# This file makes the operations directory a Python package."

    ["$ROOT_DIR/tick_manager/operations/core.py"]="def add(a: float, b: float) -> float:
    \"\"\"Add two numbers.\"\"\"
    return a + b

def subtract(a: float, b: float) -> float:
    \"\"\"Subtract two numbers.\"\"\"
    return a - b

def multiply(a: float, b: float) -> float:
    \"\"\"Multiply two numbers.\"\"\"
    return a * b

def divide(a: float, b: float) -> float:
    \"\"\"Divide two numbers, raising an error if division by zero.\"\"\"
    if b == 0:
        raise ValueError(\"Cannot divide by zero.\")
    return a / b
"

    ["$ROOT_DIR/tick_manager/models/__init__.py"]="# This file makes the models directory a Python package."

    ["$ROOT_DIR/tick_manager/models/schemas.py"]="from pydantic import BaseModel, Field

class OperationRequest(BaseModel):
    a: float = Field(..., description=\"First operand\")
    b: float = Field(..., description=\"Second operand\")

class OperationResponse(BaseModel):
    result: float = Field(..., description=\"Result of the operation\")
"

    ["$ROOT_DIR/tick_manager/utils/__init__.py"]="# This file makes the utils directory a Python package."

    ["$ROOT_DIR/tick_manager/utils/helpers.py"]="def format_result(result: float) -> str:
    \"\"\"Format the result to two decimal places.\"\"\"
    return f\"{result:.2f}\"
"

    ["$ROOT_DIR/tick_manager/config/__init__.py"]="# This file makes the config directory a Python package."

    ["$ROOT_DIR/tick_manager/config/settings.py"]="from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = \"Tick Manager\"
    debug: bool = False

    class Config:
        env_file = \".env\"

settings = Settings()
"

    ["$ROOT_DIR/tests/__init__.py"]="# This file makes the tests directory a Python package."

    ["$ROOT_DIR/tests/test_cli.py"]="from click.testing import CliRunner
from tick_manager.cli.main import cli

def test_greet():
    runner = CliRunner()
    result = runner.invoke(cli, ['greet'])
    assert result.exit_code == 0
    assert 'Hello, Tick Manager!' in result.output
"

    ["$ROOT_DIR/tests/test_api.py"]="from fastapi.testclient import TestClient
from tick_manager.api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {\"message\": \"Welcome to Tick Manager API\"}
"

    ["$ROOT_DIR/tests/test_operations.py"]="import pytest
from tick_manager.operations.core import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2

def test_multiply():
    assert multiply(4, 3) == 12

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
"
)

declare -A EXECUTABLE_FILES=(
    ["$ROOT_DIR/bin/tick_manager"]=1
)

declare -A SPECIAL_FILES=(
    ["$ROOT_DIR/bin/tick_manager"]="executable"
)

declare -A MAIN_PY_FILES=(
    ["cli"]="tick_manager/cli/main.py"
    ["api"]="tick_manager/api/main.py"
)

# Create files with content
echo "Creating files with placeholder content..."
for file in "${!FILES_CONTENT[@]}"; do
    create_file "$file" "${FILES_CONTENT[$file]}"
    # Set executable permissions if necessary
    if [[ "${SPECIAL_FILES[$file]}" == "executable" ]]; then
        chmod +x "$file"
        echo "Set executable permission for: $file"
    fi
done

# Create executable files with content
echo "Creating executable files..."
for file in "${!EXECUTABLE_FILES[@]}"; do
    create_executable_file "$file" "${FILES_CONTENT[$file]}"
done

echo "Creating directories..."
for dir in "${DIRS[@]}"; do
    create_dir "$dir"
done

# list of dependencies to install
DEPS=(
    "click>=8.1.7"
    "databento>=0.41.0"
    "fastapi>=0.115.0"
    "uvicorn>=0.30.6"
)

# add the dependencies to pyproject.toml
echo "Creating deps..."
for dep in "${DEPS[@]}"; do
    uv add "$dep"
done


echo -e "\nTick Manager project structure created successfully!"
