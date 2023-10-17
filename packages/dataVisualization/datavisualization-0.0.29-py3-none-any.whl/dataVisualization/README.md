# Data Visualisation

## How to use:

### Setup

To run the software first clone and then in the directory create a virtual
environment ([tutorial here](https://docs.python.org/3/library/venv.html))

Run `pip install -r requirements.txt` to get all of the required packages for
the software and in the correct versions.

Run `python -m main.main.py <input_dir>` to run the software

### Command line arguments

`--ignore-bars` skips generation of bar charts
`--ignore-pies` skips generation of pie charts

### Testing
To test the code base run `pytest` in the data visualisation directory.
This will use `tests/resources/test_data.xlsx` as test data to generate the test charts to be compared.

Once generated these are saved in `result_images` and are compared against `tests/baseline_images/` where there is 2 directorys, 1 for bars and 1 for pies.

Once all the comparisons are done pytest will give you a rundown of what tests passed and what ones failed with brief descriptions on why they may have failed.

#### Updating baseline Images
*Baseline images should not be changed unless there is a change in design or an issue is found, they baseline images directory is quite large so this can take a while*

To update the baseline images first locally run pytest and find your output data (`result_images/`) copy any baselines you wish to update (e.g. test_bars) and paste it in `tests/baseline_images/` replacing the previous version.

Then commit your changes, your commit should inlcude a reason for updating the baseline. and push them to the gitlab.

---


## Format Sheet:

**Heading**|**Use Case**|**Example**
:-----:|:-----:|:-----:
Sheet No.|Indicates the sheet this row is for|1,2,3
Slide Title|The title of the slide|example title here
Chart Type|indicates the type of chart the be generated|"Stacked Bar", "100% Stacked Bar"
Chart Size|what width should the chart|full, half
Values Font Size|The font size for values|8,10,21
Legend|should a legend be present on the chart|"yes","no","shared"
Gridlines/X-Axis|should gridlines be used on the chart|yes, no
Segment Values|should individual segments have values|yes, no
Total Values|should total values be shown at the end of a row|yes, no
Comment|any additional comments for researchers|blah blah blah


## Graphs:

Example of all the chart types can be seen in 'tests/resources/test_data.xlsx'

All charts must follow these rules otherwise it can cause issues with the code:

- Data should start at A1.
- Tables should be formatted with headers along the top with data as rows.
- Extra information should not be placed beyond the last row of data, this can cause issues in the code that means files don't generate properly.
