## Usage
For each work session, you will need to activate the python virtual environment
prior to executing any commands.  Once the environment is activated, you can
execute the [Slide Generator Workflow](#slide-generator-workflow), the
[Spreadsheet Images Workflow](#spreadsheet-images-workflow) as outlined
below or run any of the commands independently as needed.

### Session Setup
Session setup comprises the following steps:

* Activate the previously created python virtual environment.

```{tab} Windows PowerShell
    "$HOME\python_venvs\venv_artemis\Scripts\Activate.ps1"
```

```{tab} Windows CMD
    "$HOME\python_venvs\venv_artemis\Scripts\activate.bat"
```

```{tab} Linux
    source "$HOME/python_venvs/venv_artemis/bin/activate"
```

### Slide Generator Workflow
In order to produce a slide deck, the following workflow is prescribed.
These elements are broken into separate components so that they might be
executed without a defined pipeline if needed.

The package includes a set of subcommands under the unified CLI command
`artemis_sg` once it is installed to facilitate this workflow.  See
the complete [CLI Command Reference](#cli-command-reference) for more
detail on each of these commands.

Steps in the workflow that are a manual task not handled by the software
are highlighted with the *Manual* tag.

* [Create Spreadsheet](#create-spreadsheet) (*Manual*)
* [Add/Update Vendor](#add/update-vendor) (*Manual*)
* [Scrape Data](#scrape-data)
* [Download Images](#download-images)
* [Upload Images to Google Cloud](#upload-images-to-google-cloud)
* [Generate Slide Deck](#generate-slide-deck)

Workflow
```{mermaid}
flowchart LR
  W[/Add/Update Vendor\]
  X[/Create Spreadsheet\] --> A
  X --> B
  A[/Google Sheet ID/] --> C
  B[/XLSX File/] --> C
  C(scrape) --> D(download)
  C <--> Z((Internet))
  C --> Y[(local db)]
  Y --> D
  D --> E[local storage]
  D --> F(upload)
  E --> F
  F --> G[Google Cloud Storage]
  F --> H(generate)
  G --> H
  Y --> H
  H --> I[/Google Slides/]
```

#### Create Spreadsheet
*Manual*

Create spreadsheet that includes the field titles in row 1 and the desired
slide records in subsequent rows.  The spreadsheet must include a column for
ISBN numbers.  The ISBN numbers are assumed to be in the
[ISBN-13 format](https://www.isbn.org/about_ISBN_standard).  Make a
note of the location of this spreadsheet in your file system.
You may want to re-use this location in the
[spreadsheet images workflow](#spreadsheet-images-workflow).

#### Add/Update Vendor
*Manual*

The vendors are defined in the `[asg.vendors]` field of the `config.toml` file.
They contain three keys:

* `code`: This is the VENDOR code used to reference the VENDOR when using the
  `artemis_sg` command set.
* `name`: This is the full name of the vendor as it will appear on the Google
  Slide Decks created by the `artemis_sg generate` command.
* `isbn_key`:  This is the value used to identify ISBN data columns in
  spreadsheets.

Open `config.toml` in your favorite text editor.  If there is not an existing
record for the vendor, add one with the following pattern, including the field
key used for ISBN numbers.

If there is an existing record, update the appropriate values.

The format is as follows:
```
[asg]
vendors = [
    { code = "sample", name = "Sample Vendor", isbn_key = "ISBN-13" },
]
```

#### Scrape Data
Run the `artemis_sg scrape` command to save the item descriptions and image
URLs gathered for each item record in the spreadsheet to the file defined by the
configuration field `[asg.data.file.scraped]`.  The base command needs a valid
vendor code argument to map to the applicable vendor record updated in the
`[asg.vendors]` configuration field in the
[workflow step above](#add/update-vendor).  The base command also needs a valid
WORKBOOK identifier.  The WORKBOOK identifier can be a Google Sheet ID or an
Excel file location in which the item data
resides.

Example:
```shell
artemis_sg --verbose --vendor sample_vendor --workbook MY_GOOGLE_SHEET_ID scrape
```

#### Download Images
Download images from the scraped data using the `artemis_sg download` command.

Example:
```shell
artemis_sg --verbose download
```

#### Upload Images to Google Cloud
Run the `artemis_sg upload` command to upload previously download images to
Google Cloud.

Example:
```shell
artemis_sg --verbose upload
```

#### Generate Slide Deck
Run the `artemis_sg generate` command to create a Google Slide deck of the
items in the spreadsheet including the description and images gathered by the
[scrape workflow step](#scrape-data).  You should set a desired slide title
using the `--title` option.  The base command needs a valid vendor code, and a
valid WORKBOOK (Google Sheet ID or Excel file path) in which the item data
resides.

Example:
```{tab} Windows
    artemis_sg --verbose --vendor sample_vendor --workbook MY_GOOGLE_SHEET_ID ^
               generate --title "Badass presentation"
```

```{tab} Linux
    artemis_sg --verbose --vendor sample_vendor --workbook MY_GOOGLE_SHEET_ID \
               generate --title "Badass presentation"
```

#### Command Chaining
The above `artemis_sg` sub-commands can be "chained" together to perform the
automated steps of the workflow using a single "chained" command.  The command
chain will run in the order specified. The base command needs a valid vendor
code, and a valid WORKBOOK (Google Sheet ID or Excel file path) in which the
item data resides.  The `generate` command can take an optional `--title`.

Example:
```{tab} Windows
    artemis_sg --vendor sample_vendor ^
               --workbook MY_GOOGLE_SHEET_ID ^
               scrape download upload generate --title "Badass presentation"
```

```{tab} Linux
    artemis_sg --vendor sample_vendor \
               --workbook MY_GOOGLE_SHEET_ID \
               scrape download upload generate --title "Badass presentation"
```


### Spreadsheet Images Workflow
In order to produce a spreadsheet with thumbnail images added for items, the
following workflow is suggested.

The following steps are shared with the
[slide generator workflow](#slide-generator-workflow).  These steps are linked
to the appropriate step in that workflow rather then duplicating them here.

* [Create Spreadsheet](#create-spreadsheet) (*Manual*)
* [Add/Update Vendor](#add/update-vendor) (*Manual*)
* [Scrape Data](#scrape-data)
* [Download Images](#download-images)

The unique steps for this workflow are:

* [Create Thumbnails](#create-thumbnails)
* [Add Thumbnails to Spreadsheet](#add-thumbnails-to-spreadsheet)

Workflow
```{mermaid}
flowchart LR
  W[/Add/Update Vendor\]
  X[/Create Spreadsheet\] --> A
  X --> B
  A[/Google Sheet ID/] --> C
  B[/XLSX File/] --> C
  C(scrape) --> D(download)
  C <--> Z((Internet))
  C --> Y[(local db)]
  Y --> D
  D --> E[local storage]
  D --> F(mkthumbs)
  F --> E
  F --> H(sheet-image)
  E --> H
  H --> I[/XLSX File/]
```

#### Create Thumbnails
Create thumbnail images from previously downloaded images using the `artemis_sg
mkthumbs` command.

Example:
```shell
artemis_sg --verbose mkthumbs
```

#### Add Thumbnails to Spreadsheet
Create a new Excel spreadsheet containing a thumbnail images column populated
with available thumbnails using the `artemis_sg sheet-image` command.
The base command needs a valid vendor code, and a valid WORKBOOK
(Excel file path) in which the item data resides.
This file path can be noted from
the [Create Spreadsheet](#create-spreadsheet) step.

**NOTE:** Currently, `artemis_sg sheet-image` does not support Google Sheet IDs
as a valid WORKBOOK type.

By default, the new Excel file is saved as "out.xlsx" in the directory from
which the command was run.  The
`--output` option can be used to specify a desired output file.  The
specification for the `--output` file can include either an absolute or
relative path location for the file as well.

Example:
```{tab} Windows
    artemis_sg --verbose ^
               --vendor sample_vendor ^
               --workbook "C:\Users\john\Documents\spreadsheets\my_spreadsheet.xlsx" ^
               sheet-image
```

```{tab} Linux
    artemis_sg --verbose \
               --vendor sample_vendor \
               --workbook "/home/john/Documents/spreadsheets/my_spreadsheet.xlsx" \
               sheet-image
```

Example, specifying output file with an absolute file path:
```{tab} Windows
    artemis_sg --verbose ^
               --vendor sample_vendor ^
               --workbook "C:\Users\john\Documents\spreadsheets\my_spreadsheet.xlsx" ^
               sheet-image ^
               --output "C:\Users\john\Documents\spreadsheets\my_new_spreadsheet.xlsx"
```

```{tab} Linux
    artemis_sg --verbose \
               --vendor sample_vendor \
               --workbook "/home/john/Documents/spreadsheets/my_spreadsheet.xlsx" \
               sheet-image \
               --output "/home/john/Documents/spreadsheets/my_new_spreadsheet.xlsx"
```

Example, specifying output file with a relative file path:
```{tab} Windows
    artemis_sg --verbose ^
               --vendor sample_vendor ^
               --workbook "C:\Users\john\Documents\spreadsheets\my_spreadsheet.xlsx" ^
               sheet-image ^
               --output "..\..\my_new_spreadsheet.xlsx"
```

```{tab} Linux
    artemis_sg --verbose \
               --vendor sample_vendor \
               --workbook "/home/john/Documents/spreadsheets/my_spreadsheet.xlsx" \
               sheet-image \
               --output "../../my_new_spreadsheet.xlsx"
```

#### Command Chaining
The above `artemis_sg` sub-commands can be "chained" together to perform the
automated steps of the workflow using a single "chained" command.  The command
chain will run in the order specified. The base command needs a valid vendor
code, and a valid WORKBOOK (Excel file path) in which the
item data resides.  The `sheet-image` command can take an optional `--output`.

Example:
```{tab} Windows
    artemis_sg --vendor sample_vendor ^
               --workbook "C:\Users\john\Documents\spreadsheets\my_spreadsheet.xlsx" ^
               scrape download mkthumbs sheet-image ^
               --output "..\..\my_new_spreadsheet.xlsx"
```

```{tab} Linux
    artemis_sg --vendor sample_vendor \
               --workbook "/home/john/Documents/spreadsheets/my_spreadsheet.xlsx" \
               scrape download mkthumbs sheet-image \
               --output "../../my_new_spreadsheet.xlsx"
```
