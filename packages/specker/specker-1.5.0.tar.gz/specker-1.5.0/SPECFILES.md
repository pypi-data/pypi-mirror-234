# Configuration Options
Auto generated from .spec files
## Spec for specker

Option: `required` - Whether or not this Option is required
 - Type: bool
 - Required: False
 - Default: False

Option: `default` - Default Value if not required and not set
 - Type: any
 - Required: False

Option: `type` - Type the Value must be.
 - Type: str
 - Required: True
 - Default: any
 - Acceptable Values: any, str, int, list, dict, float, bool, file, dir, file:exist, dir:exist, path, path:exist

Option: `comment` - Informational Comment about this Option and Value
 - Type: str
 - Required: False

Option: `example` - Example Data for this Option and Value
 - Type: any
 - Required: False

Option: `values` - List of Acceptable Values
 - Type: list
 - Required: False
 - Example: [ "value1", "value2" ]

Option: `format` - Regex Acceptable Value
 - Type: str
 - Required: False
 - Example: ^\d+\w+$

Option: `spec_chain` - Add a specker spec which maps into this spec
 - Type: str
 - Required: False
 - Example: mysecond_spec_name
