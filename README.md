# ORCID Checker for ACM XML Files

This script scans all `.xml` files in a folder and checks whether each author has an ORCID.

It reports:

- Total number of ORCID tags found
- Number of authors with ORCIDs
- Number of authors with missing ORCIDs
- The article number of each paper with a missing ORCID
- The author name
- The XML filename

Example output:

```text
===================================
ORCID SUMMARY
===================================
Total ORCID tags : 10
With ORCID       : 8
Empty ORCID      : 2

===================================
AUTHORS WITH MISSING ORCID
===================================
Article: 1919 | Author: John Doe | File: sample.xml
Article: 1920 | Author: Jane Doe | File: sample.xml
```

## Requirements

You need Python 3 installed.

Check whether Python is installed:

```bash
python3 --version
```

If Python is installed, you should see something similar to:

```text
Python 3.14.0
```

On macOS, if Python is not installed and you use Homebrew:

```bash
brew install python
```

Then verify:

```bash
python3 --version
```

## Files

Place the Python script in the same folder as the XML files you want to check.

For example:

```text
orcid-checker/
├── check_orcid.py
├── sample.xml
├── sample-round2.xml
├── sample-companion.xml
└── README.md
```

The script automatically scans every file ending in `.xml` in the current folder.

## Running the Script

Open Terminal and navigate to the folder containing the script and XML files.

For example:

```bash
cd ~/Desktop/orcid-checker
```

Then run:

```bash
python3 check_orcid.py
```

The results will be printed directly in Terminal.

## What the Script Checks

For every author, the script looks for an ORCID tag such as:

```xml
<ORCID>0000-000X-XXXX-XXXX</ORCID>
```

This is an anonymized example of a populated ORCID.

The following are considered missing:

```xml
<ORCID></ORCID>
```

or:

```xml
<ORCID />
```

The script then identifies the corresponding author and the paper containing that author.

For example:

```xml
<paper>
    <published_article_number>1919</published_article_number>

    <authors>
        <author>
            <first_name>John</first_name>
            <last_name>Doe</last_name>
            <ORCID />
        </author>

        <author>
            <first_name>Jane</first_name>
            <last_name>Smith</last_name>
            <ORCID>0000-000X-XXXX-XXXX</ORCID>
        </author>
    </authors>
</paper>
```

The script will report only the author with the missing ORCID:

```text
Article: 1919 | Author: John Doe
```

Jane Smith will not be listed because the ORCID field is populated.

## Article Number

The script primarily uses:

```xml
<published_article_number>
```

For example:

```xml
<published_article_number>1919</published_article_number>
```

If `published_article_number` is empty or unavailable, the script falls back to:

```xml
<event_tracking_number>
```

For example:

```xml
<event_tracking_number>1919</event_tracking_number>
```

## Multiple Papers in One XML File

A single XML file may contain multiple `<paper>` elements.

For example:

```xml
<proceedings>

    <paper>
        <paper_title>Sample Paper A</paper_title>
        <published_article_number>1919</published_article_number>

        <authors>
            <author>
                <first_name>John</first_name>
                <last_name>Doe</last_name>
                <ORCID />
            </author>
        </authors>
    </paper>

    <paper>
        <paper_title>Sample Paper B</paper_title>
        <published_article_number>1920</published_article_number>

        <authors>
            <author>
                <first_name>Jane</first_name>
                <last_name>Doe</last_name>
                <ORCID />
            </author>
        </authors>
    </paper>

</proceedings>
```

The script finds the specific `<paper>` containing each author.

The result will therefore be:

```text
Article: 1919 | Author: John Doe | File: sample.xml
Article: 1920 | Author: Jane Doe | File: sample.xml
```

This prevents the script from incorrectly assigning the first article number in the XML file to every author.

## Example Workflow

1. Create a folder for the XML files.

2. Copy `check_orcid.py` into that folder.

3. Copy all XML files to be checked into the same folder.

4. Open Terminal.

5. Navigate to the folder:

```bash
cd /path/to/folder
```

6. Run:

```bash
python3 check_orcid.py
```

7. Review the summary:

```text
ORCID SUMMARY
```

8. Review the list under:

```text
AUTHORS WITH MISSING ORCID
```

## Example Result

A complete run may look like this:

```text
===================================
ORCID SUMMARY
===================================
Total ORCID tags : 124
With ORCID       : 119
Empty ORCID      : 5

===================================
AUTHORS WITH MISSING ORCID
===================================
Article: 1919 | Author: John Doe | File: sample-fullpapers.xml
Article: 1920 | Author: Jane Doe | File: sample-fullpapers.xml
Article: 1931 | Author: Alex Smith | File: sample-fullpapers.xml
Article: 2055 | Author: Chris Jones | File: sample-companion.xml
Article: 2072 | Author: Taylor Brown | File: sample-companion.xml
```

## No Additional Packages Required

The script only uses Python's built-in libraries:

```python
os
xml.etree.ElementTree
```

You do not need to install any additional Python packages using `pip`.

## Troubleshooting

### `python3: command not found`

Python 3 is not installed or is not available in your Terminal path.

On macOS with Homebrew:

```bash
brew install python
```

Then check again:

```bash
python3 --version
```

### No XML files are found

Make sure:

- The XML files end in `.xml`
- The XML files are in the same folder as `check_orcid.py`
- You are running the command from that folder

You can check your current folder with:

```bash
pwd
```

You can list the contents of the folder with:

```bash
ls
```

### XML parsing error

If an XML file is malformed, the script will report something similar to:

```text
Could not parse sample.xml: ...
```

The script will continue processing the remaining XML files.

## Privacy Note

All author names, filenames, article titles, article numbers, and ORCID values shown in this README are illustrative or anonymized examples.

Example ORCIDs use a deliberately invalid pattern such as:

```text
0000-000X-XXXX-XXXX
```

This avoids exposing or accidentally reproducing real ORCID identifiers.
