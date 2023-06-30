<div align="left">
  <img src="https://user-images.githubusercontent.com/16392542/77208906-224aa500-6aba-11ea-96bd-e81806074030.png" width="350">
</div>

# AutoGluon-Dashboard

Follow the steps below to set up autogluon-dashboard::
1. Create a virtual environment by running: 
```
python3 -m venv .venv_dash 
source .venv_dash/bin/activate
``` 
2. Install all necessary libraries by running: `pip3 install -r requirements.txt`
3. Install the `autogluon_dashboard` package by running: `pip3 install -e .`. You can now interact with the dashboard through the CLI command `agdash`. 
4. To convert a Panel app to WebAssembly,  Panel provides a script that will convert the code in `app.py` into an HTML file and JS file. This can be done in one line of code as: `panel convert app.py --to pyodide-worker --out web_files/`
The generated HTML and JS files will be found in the `web_files` folder. These can be uploaded to the desired hosting service (eg: AWS S3). 
<br> A wrapper script (`dashboard.py`) has been created to run all the necessary commands in the backend to set up the Python web app, create the WebAssembly files and upload them to an S3 bucket for hosting. You can interact with the wrapper using the CLI command - `agdash`, as follows:
```
agdash --per_dataset_csv 'path_to_local_csv_file.csv' --all_dataset_csv 'path_to_local_csv_file.csv' --per_dataset_s3 'path_in_S3_to_store' --all_dataset_s3 'path_in_S3_to_store' --s3_bucket BUCKET_NAME
``` 


To run all unittests, run the following command in the root directory: `python3 -m unittest discover -s unittests -p 'test_*.py'`
