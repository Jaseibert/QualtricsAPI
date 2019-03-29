# QualtricsAPI

This project has stemmed out of a need to work with the Qualtrics API for work, and not wanting to look up the example script from the Qualtrics website each time that I need it. The primary use of this is to collect survey responses, however I might dabble on including the XM API features.

# Basic Usage

```python
from QualtricsAPI import QualtricsSurveyResponses

#Create a class instance of QualtricsSurveyResponses()
Q = QualtricsSurveyResponses(token="<Your API Token>", survey_id="<Your Survey ID>", file_format="csv", data_center="<Your Data Center>",export_type="LegacyV3" )

#Call the Get Responses Method to get your responses
Q.get_responses()
```
The resulting file will be downloaded in your current working directory.
## Project Status

I am currently working on this project, and am working to combine the NewExport and LegacyV3 export methods in the QualtricsSurveyResponses class.
