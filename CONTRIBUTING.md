# Contributing Guidelines

Thank you for your interest in contributing to the AutoGluon Dashboard. Whether it's a bug report, new feature, correction, or additional
documentation, we greatly value feedback and contributions from our community.

Please read through this document before submitting any issues or pull requests to ensure we have all the necessary
information to effectively respond to your bug report or contribution.

## Reporting Bugs/Feature Requests

We welcome you to use the GitHub issue tracker to report bugs or suggest features.

When filing an issue, please check [existing open](https://github.com/autogluon/autogluon-dashboard/issues), or [recently closed](https://github.com/autogluon/autogluon-dashboard/issues?utf8=%E2%9C%93&q=is%3Aissue%20is%3Aclosed%20), issues to make sure somebody else hasn't already
reported the issue. Please try to include as much information as you can. Details like these are incredibly useful:

* A reproducible test case or series of steps
* The version of AutoGluon being used, the version of pytorch
* Any modifications you've made relevant to the bug
* Anything unusual about your environment or deployment

Ideally, you can install AutoGluon-Dashboard and its dependencies in a fresh virtualenv to reproduce the bug.


## Contributing via Pull Requests
Code contributions via pull requests are much appreciated. Before sending us a pull request, please ensure that:

1. You are working against the latest source on the *main* branch.
2. You check existing open, and recently merged, pull requests to make sure someone else hasn't addressed the problem already.
3. You open an issue to discuss any significant work - we would hate for your time to be wasted.

To send us a pull request, please:

1. Fork the repository.
2. Modify the source (see details below); please focus on the specific change you are contributing. If you also reformat all the code, it will be hard for us to focus on your change.
3. Ensure local tests pass.
4. Commit to your fork using clear commit messages.
5. Send us a pull request, answering any default questions in the pull request interface.

GitHub provides additional document on [forking a repository](https://help.github.com/articles/fork-a-repo/) and
[creating a pull request](https://help.github.com/articles/creating-a-pull-request/).


## Finding Contributions to Work On
Looking at the existing issues is a great way to find something to contribute on. As the project uses the default GitHub issue labels (enhancement/bug/duplicate/help wanted/invalid/question/wontfix), looking at any ['help wanted'](https://github.com/autogluon/autogluon-dashboard/labels/help%20wanted) issues is a great place to start.
Additionally, we welcome contributions regarding additional plots and visualizations to the dashboard.


# Dashboard Contribution


## Tips for Modifying the Source Code
- Refer to the [`README`](https://github.com/autogluon/autogluon-dashboard/blob/main/README.md) for setup+install instructions. 
- All code should adhere to the [PEP8 style](https://www.python.org/dev/peps/pep-0008/).
- After you have edited the code, ensure your changes pass the unit tests via: `python -m pytest tests/unittests/`
- Additionally, please test your changes by spinning up the dashboard website on your local server. Refer to the `README` for instructions. 


## Creating a widget
Widgets are tools to add interactivity to the plots by allowing the user to choose (select from, toggle between, etc.) what data to plot.
<br> Look at the documentation for `panel` widgets [here](https://panel.holoviz.org/reference/index.html#widgets) for more information regarding the different types of widgets and how to use them.

Each widget is an object of a specific class that inherits from a common, parent `Widget` class. Refer to the [`widget.py`](https://github.com/autogluon/autogluon-dashboard/blob/main/src/autogluon_dashboard/widgets/widget.py) file for more details regarding the parent class.
<br> You can use one of the existing widgets classes or create a brand new widget from the list of `panel` widgets. If you create a new widget, make sure the class has a `create_widget` method

To create a widget on the dashboard, use the following code: 
```
widget = WidgetClass(...).create_widget()
```

Note: If you would like each plot to be linked to it's own individual widget, make sure you do not reuse widget objects for different plots - even if they have the same functionality. 

Widgets can also be independent and not necessarily linked to a plot. For example, the download button for the csv files on the website. 


## Creating a plot
Each “plot” is an object of a specific class that inherits from a common, parent `Plot` class. Refer to the [`plot.py`](https://github.com/autogluon/autogluon-dashboard/blob/main/src/autogluon_dashboard/plotting/plot.py) file for more details regarding the attributes and methods contained within the parent class. The plots leverage the python library - `hvplot`. `hvplot` documentation can be found [here](https://hvplot.holoviz.org/user_guide/index.html). 

To add a new plot, create a new file under `src/autogluon_dashboard/plotting` with appropriate naming conventions. Make sure that it inherits the parent `Plot` class. For the `plot` method, you can either leverage the inherited `_create_hvplot` method in the `Plot` class, the additional plot methods provided, or define a brand new plot function.

If you would like to have an interactive plot with `panel` widgets included, you will need to pass in an interactive dataframe (which is an hvPlot representation) into the `hvplot` function. This can be done by calling the `interactive()` method on your `pandas` dataframe as: 
```
df = pd.read_csv('somefile.csv')
idf = df.interactive()
```
You can then call the `.hvplot()` function as you would call `.plot()` on a pandas dataframe.


### Linking widgets to plots
A widget is an independent object that gets linked to a plot when you pass it into the `hvplot` method
<br> For example: Say you have a widget for changing the y-axis metric called `yaxis_widget`. To automatically bind the widget to a plot, you must pass this widget into the `hvplot` method as: `idf.hvplot(yaxis=yaxis_widget, ...)`


## Adding a plot (w or w/o widgets) to the dashboard
To add the plot to the dashboard, follow the steps used in `app.py`. 
```
# Global list of panel objects to display on the website
panel_objs = []

# Create an object of the plot class
plot_obj = PlotClass(...)

# Create an object of the widget class
widget = WidgetClass(...).create_widget()

# Add the panel object to global list
create_panel_object(panel_objs, "some title", widgets=[widget], plots=[plot_obj])
```

Note: If you would like to pass in custom arguments to the `plot` method, you can create the plot in `app.py` itself; before passing it into `create_panel_object` as:
```
try: 
    plot_obj = PlotClass(...).plot(arg=arg)
except Exception:
    plot_obj = None
create_panel_object(panel_objs, "some title", plots=[plot_obj])
```


## The Aggregate File Script
One issue with `panel` is that it does not allow relative imports. The website generated by `panel` runs in a `pyodide` web-environment, where it installs the necessary python packages only from the official python index (PyPI). Therefore, to circumvent this, we created a script to aggregate all the files within the project directory into one big file to convert the web app into WebAssembly (HTML and JavaScript). For more details, refer to the [`aggregate_file.py`](https://github.com/autogluon/autogluon-dashboard/blob/main/src/autogluon_dashboard/utils/aggregate_file.py) file. 
<br> **NOTE**: The order of crawling in the aggregate script is very important! If the app imports module A before module B, then it is imperative that the script crawls through the folder corresponding to module A first. Therefore, pay attention to how the dependency of the subdirectories is affected by any changes you make to `app.py`. The order of crawling can be found and modified in the `aggregate_file.py` file.  


## Using the Dashboard wrapper locally
Once you have installed the package from source as per the instructions in the [`README`](https://github.com/autogluon/autogluon-dashboard/blob/main/README.md), you should have access to the `agdash` command. 
```
agdash --help
usage: agdash [-h] --per_dataset_csv  --agg_dataset_csv  [--hware_metrics_csv]  [--s3_bucket ] [--s3_prefix ] [--s3_region ]

optional arguments:
  -h, --help            show this help message and exit
  --per_dataset_csv     Location of csv file of all datasets+frameworks data to upload to S3 bucket 
  --agg_dataset_csv     Location of csv file of aggregated data across all frameworks to upload to S3 bucket                   
  --hware_metrics_csv   Location of csv file of hardware metrics to upload to S3 bucket
  --s3_bucket           Name of S3 bucket to upload dashboard contents to
  --s3_prefix           Prefix for S3 URL - subfolder
  --s3_region           S3 Region to deploy the dashboard website. Should be the same region as s3_bucket
```

The `per_dataset_csv` file refers to the evaluation file that is comprised of metrics pertaining to every individual dataset+framework pair benchmark run. It should not contain the frameworks that errored our on a given dataset since the error counts are calculated by looking at the missing rows. 
<br> Below is the schema for this csv:
```
dataset | framework | problem_type | time_train_s | metric_error | time_infer_s | bestdiff | loss_rescaled | time_train_s_rescaled | time_infer_s_rescaled | rank
```
The `agg_dataset_csv` is a much smaller file and refers to the metrics of all frameworks aggregated (or averaged) across all datasets in the benchmark run. 
<br> Below is the schema for this csv:
```
framework | winrate | > | < | = | % Less Avg. Errors | Avg Inf Speed Diff | time_train_s | metric_error | time_infer_s | bestdiff | loss_rescaled | time_train_s_rescaled | time_infer_s_rescaled | rank | rank=1_count | rank=2_count | rank=3_count | rank>3_count | error_count
```
Both of these csv files are mandatory for the dashboard.

For more information on benchmarks and evaluation, refer to [`autogluon-bench`](https://github.com/autogluon/autogluon-bench) as well as the [evaluation section](https://github.com/autogluon/autogluon-bench#evaluating-benchmark-runs). 


Finally, the `hware_metrics_csv` file refers to the EC2 instance hardware metrics of the benchmark run. This is a part of the evaluation module and is an optional CSV file to provide to the dashboard. It includes hardware metrics like CPU & GPU Utilization, Memory, and Disk Usage for every given benchmark run (which corresponds to unique framework+dataset pairs).
<br> Below is the schema for this csv:
```
framework | dataset | mode | fold | metric | statistic_type | statistic_value | unit
```

If a bucket and region is not specified, it will default to the AutoGluon bucket and region. You must have the requisite permissions to upload contents to the AutoGluon bucket. 
<br> If you provide your own bucket and region, you will need to the following: 
1. Make the bucket public so that the python web-app can access the csv files from it **CAUTION: Making a bucket public will expose any sensitive data in it. Proceed with caution when making your bucket publicly accessible. You can consider making your bucket public for a short period of time to test the website.**
2. Enable web hosting for the bucket
3. If you do not want a public bucket, you will have to use a service like [CloudFront](https://aws.amazon.com/cloudfront/) (an AWS service) to host the website through the bucket. You can use the cloudfront link for the csv files as well. 
    - For the AutoGluon main dashboard, we use CloudFront to host the website through the AutoGluon bucket.

If you are able to run the wrapper successfully, you will see the link to your website in the terminal.


## Simple Dashboard Tutorial
Refer to this [tutorial](https://anaconda.cloud/easiest-interactive-dashboard) for a brief intro on how to use `panel` and `hvplot` to create and deploy a simple dashboard. 


## Code of Conduct
This project has adopted the [Amazon Open Source Code of Conduct](https://aws.github.io/code-of-conduct).
For more information see the [Code of Conduct FAQ](https://aws.github.io/code-of-conduct-faq) or contact
opensource-codeofconduct@amazon.com with any additional questions or comments.


## Security Issue Notifications
If you discover a potential security issue in this project we ask that you notify AWS/Amazon Security via our [vulnerability reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public github issue.


## Licensing

See the [LICENSE](https://github.com/autogluon/autogluon-dashboard/blob/master/LICENSE) file for our project's licensing. We will ask you to confirm the licensing of your contribution.

We may ask you to sign a [Contributor License Agreement (CLA)](http://en.wikipedia.org/wiki/Contributor_License_Agreement) for larger changes.