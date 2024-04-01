<div align="left">
  <img src="https://user-images.githubusercontent.com/16392542/77208906-224aa500-6aba-11ea-96bd-e81806074030.png" width="350">
</div>

# AutoGluon-Dashboard

Welcome to AutoGluon-Dashboard, a tool for visualizing your metrics - one benchmark at a time!

The latest version of the AutoGluon-Dashboard can be found [here](https://d24iwcyhf6yavw.cloudfront.net/index.html)! 

## Setup
Follow the steps below to set up autogluon-dashboard::
1. Create a virtual environment and upgrade pip by running: 
```
python -m venv .venv_dash 
source .venv_dash/bin/activate
python -m pip install --upgrade pip
``` 

2. Install the `autogluon_dashboard` package by running: `pip install -e .`. You can now interact with the dashboard through the CLI command `agdash`. 

3. To convert a Panel app to WebAssembly (HTML and JavaScript),  Panel provides a script that will convert the code in `app.py` into an HTML file and JS file. This can be done in one line of code as: `panel convert app.py --to pyodide-worker --out web_files/`
The generated HTML and JS files will be found in the `web_files` folder. These can be uploaded to the desired hosting service (eg: AWS S3). 
<br> A wrapper script (`dashboard.py`) has been created to run all the necessary commands in the backend to set up the Python web app, create the WebAssembly files and upload them to an S3 bucket for hosting. You can interact with the wrapper using the CLI command - `agdash`, as follows:
```
agdash --per_dataset_csv 'path_to_csv_file.csv' --agg_dataset_csv 'path_to_csv_file.csv' --hware_metrics_csv 'path_to_csv_file.csv' --per_dataset_s3 'path_in_S3_to_store' --all_dataset_s3 'path_in_S3_to_store' --s3_bucket 'BUCKET_NAME' --s3-prefix 'sub-folder'
``` 

To view unittest coverage, run the following command in the root directory: `python -m pytest tests/unittests/`

## Run dashboard locally 
If you would like to view the dashboards on your local machine, you can use a `localhost` server by running the following `panel` command: 
```
panel serve src/autogluon_dashboard/app.py --autoreload
```
You can then open http://localhost:5006/app in your web browser.
<br> The `--autoreload` flag will automatically reload the website when you make a change the source code (as long as the `localhost` server port is still open)


## Contributing to AutoGluon-Dashboard

We are actively accepting code contributions to the AutoGluon-Dashboard project. If you are interested in contributing to AutoGluon-Dashboard, please read the [Contributing Guide](https://github.com/autogluon/autogluon-dashboard/blob/main/CONTRIBUTING.md) to get started.
