# Spatial Extractions App

## Setup the project

### Using Conda
```sh
conda env create -f environment.yml
conda activate flask_app
./run
```

### Using Docker (recommended)
```sh
docker build -t flask-spatial-extractions .
docker run -p 5000:5000 flask-spatial-extractions
```