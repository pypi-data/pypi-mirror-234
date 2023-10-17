# Specker

The JSON Configuration Validator

- [Specker](#specker)
  - [About](#about)
    - [How does it work?](#how-does-it-work)
  - [Usage](#usage)
    - [Spec Files](#spec-files)
      - [Value Types](#value-types)
    - [Validation](#validation)
  - [Examples](#examples)
    - [Example Data](#example-data)
      - [Example Spec: `myfile.json.spec`](#example-spec-myfilejsonspec)
      - [Example Spec: `myfile.json_time.spec`](#example-spec-myfilejson_timespec)
      - [Example Spec: `myfile.json_env.spec`](#example-spec-myfilejson_envspec)
      - [Example Spec: `myfile.json_env.deep.spec`](#example-spec-myfilejson_envdeepspec)
      - [Example Spec: `many_item.spec`](#example-spec-many_itemspec)
    - [Example - Validation without Chaining](#example---validation-without-chaining)
    - [Example - Validation with Chaining](#example---validation-with-chaining)
    - [Example - Deep Chain Validation](#example---deep-chain-validation)
    - [Example - Any Item (`__any_item__`) Validation](#example---any-item-__any_item__-validation)
    - [Example - Constructing Specs in Code](#example---constructing-specs-in-code)
  - [Utils](#utils)

## About

Specker is a way to validate a configuration (Dictonary, or JSON) against a defined set of rules, while also providing defaults. Additionally, because the configuration is now documented as one of the Spec files, documentation for the specific configuration can be generated from the Spec file!

### How does it work?

Specker uses a dictionary block for each specified parameter in order to validate that it is the correct type, and that it exists, if required. If it is not a required value, a default can also be set. Spec files contain a defined group or configuration file, for example, if we wanted to validate `myconfig.json`, we would create a Spec called `myconfig.json.spec`. This Spec would be loaded, and then the contents of `myconfig.json` would be compared against it.

## Usage

### Spec Files

See [`SPECFILES.md`](SPECFILES.md) for information on the required values for each entry in a Spec. Spec files must be saved as a `.spec` file. For speed, specs should be kept in their own directory, so no other files need to be searched through.

Spec Files are made up of many blocks of Spec rules which define what a configuration block must look like. Specker is even capable of self-specing itself! You can see the Spec file for which all specs must follow, by examining the [`specs/specker.spec`](specs/specker.spec) file.

Specs can also be assembled in code, by use of the static method `SpecContent.create`, followed by using the `add()` function for your instanced `SpecLoader`

Additional Spec dirs can be added via the instanced `SpecLoader` by calling `load_specs()`

#### Value Types

Specker provides a number of value types for validation:

 - `any`: Accept Any Type, including those not listed here
 - `str`: Strings
 - `int`: Integers
 - `list`: Lists
 - `dict`: Dictionaries
 - `float`: Floating Points
 - `bool`: Booleans
 - `path`: A Valid file or directory path (does not have to exist)
 - `path:exist`: A Valid Path, which must exist. Can be any type (including sockets, devices, etc)
 - `file` A Valid file path (does not have to exist), cannot end with a trailing slash
 - `file:exist`: A Valid File, which must exist
 - `dir`: A Valid file path (does not have to exist), must end with a trailing slash
 - `dir:exist`: A VAlid Directory, which must exist

As of 1.5.0 Specker provides a `format` field for each Spec, this allows to perform regex validation (**only on strings**). Please note that you must escape things like `\d` (should be `\\d`).

### Validation

Using Specker is easy! Once you've made your Spec file(s), you only need to load Specker, and your configuration, then compare the two!

`SpeckerLoader.compare()` will return a boolean pass/fail. Failure will occur if any of the spec validation fails. Validation messages are logged in via `logging.*`. This includes having values that are not in the spec file.

```
### Load Your Configuration
import json
try:
    with open("myfile.json", "r", encoding="utf-8") as f:
        config_content = json.loads(f.read())
except BaseException as e:
    print(f"Failed to load myfile, {e}")
    exit(1)

### Load and Use Specker
# Import the Specker Loader
from specker.loader import SpeckerLoader

# Initialize the Loader, and point it to your Spec directory
spec_loader = SpecLoader("../specs/") # Load all .spec files from this directory
```

Specker by default will only validate the dictionary you pass, and no further dictionaries or lists within it. By adding `spec_chain`s, Specker can traverse deeper into the tree.

The Example below describes a 'root' level spec, as well as a 'sub' level spec, and how to validate a configuration against them.

## Examples

### Example Data

#### Example Spec: `myfile.json.spec`
```
{
    "name": {
        "required": true,
        "default": "",
        "type": "str",
        "comment": "Job Name (Identifier)",
        "example": "myexample"
    },
    "time": {
        "required": true,
        "default": {},
        "type": "dict",
        "comment": "Time Configuration"
    },
    "environment": {
        "required": false,
        "default": {},
        "type": "dict",
        "comment": "Environment Variables to use during Command execution"
    },
    "visibility": {
        "required": false,
        "default": "hidden",
        "type": "str",
        "values": [ "hidden", "visible", "admin", "deleted" ],
        "comment": "Visbility of Command Information"
    }
}
```

#### Example Spec: `myfile.json_time.spec`
```
{
    "minute": {
        "required": true,
        "default": "",
        "type": "str",
        "comment": "Minute(s) to Run at",
        "example": "*/5"
    },
    "hour": {
        "required": true,
        "default": "",
        "type": "str",
        "comment": "Hour(s) to Run at",
        "example": "*/2"
    },
    "day-of-month": {
        "required": true,
        "default": "",
        "type": "str",
        "comment": "Day(s) of Month to Run at",
        "example": "*"
    },
    "month": {
        "required": true,
        "default": "",
        "type": "str",
        "comment": "Month(s) to Run at",
        "example": "*"
    },
    "day-of-week": {
        "required": true,
        "default": "",
        "type": "str",
        "comment": "Day(s) of Week to Run at",
        "example": "1"
    }
}
```

#### Example Spec: `myfile.json_env.spec`
```
{
    "my_special_var": {
        "type": "str",
        "required": true,
        "default": "",
        "comment": "My Special Variable",
        "example": "a_cool_thing"
    },
    "my_deep_validation": {
        "type": "dict",
        "required": true,
        "default": {},
        "comment": "A Deeper dictionary",
        "spec_chain": "myfile.json_env.deep"
    }
}
```

#### Example Spec: `myfile.json_env.deep.spec`

```
{
    "my_other_var": {
        "type": "str",
        "required": true,
        "default": "not_set",
        "comment": "Some other deep level variable",
        "values": [ "a", "b", "foo", "bar", "not_set" ]
    }
}
```

#### Example Spec: `many_item.spec`
```
{
    "__any_item__": {
        "type": "dict",
        "required": false,
        "comment": "Allow Items of Any name, but matching this spec"
        "spec_chain": "myfile.json_env.spec"
    }
}
```

### Example - Validation without Chaining

Now that we have our Specs, we can compare them against our configuration data.

```
# Initialize the Loader, and point it to your Spec directory
spec_loader = SpecLoader("../specs/") # Load all .spec files from this directory

# Load `myfile.json.spec` and compare `config_content` against it.
spec_result = spec_loader.compare("myfile.json",config_content)
if not spec_result:
    exit(1)
# Because we are not chaining specs together, the `time` dictionary must be validated separately
spec_result = spec_loader.compare("myfile.json_time",config_content["time"])
if not spec_result:
    exit(1)
exit(0)
```

### Example - Validation with Chaining

Before we compare our specs, we will make one modification to `myspec.json.spec`. Within the `time` definition, we will add `"spec_chain": "myspec.json_time"`.
```
{
    "name": {
        ...
    },
    "time": {
        "required": true,
        "default": {},
        "type": "dict",
        "comment": "Time Configuration",
        "spec_chain": "myspec.json_time"
    },
    "environment": {
        ...
    },
    ....
}
```

Now that we have our Specs, we can compare them against our configuration file:

```
# Initialize the Loader, and point it to your Spec directory
spec_loader = SpecLoader("../specs/") # Load all .spec files from this directory

# Load `myfile.json.spec` and compare `config_content` against it.
spec_result = spec_loader.compare("myfile.json",config_content)
if not spec_result:
    exit(1)
exit(0)
```

### Example - Deep Chain Validation

If we additionally change the `environment` definition in `myspec.json.spec` to add `"spec_chain": "myspec.json_env"`, we can show deeper chained validation.

In this case, `myspec.json.spec` will be the starting point. Upon reaching the `environment` definition, it will utilize the `myspec.json_env.spec` spec to validate the `environment` dictionary. Upon reaching the `my_deep_validation` definition, it will utilize the `myspec_json_env.deep.spec` spec to validate the `my_deep_validation` dictionary.

No code is shown, as this case would be exactly the same code as the [validation with chaining example](#example---validation-with-chaining)

### Example - Any Item (`__any_item__`) Validation

To facilitate the need for blocks which can have any key name, but must follow a valid spec, the `__any_item__` key (see `many_item.spec`) may be used. This allows for a dictionary (see below) to contain any key name, but still be validated against a specific spec. In the case of `many_item.spec`, it checks that each value of the dictionary matches the chained spec `myspec.json_env.spec` (which then matches against `myspec_json_env.deep.spec`).

Example Dictionary
```
{
    "mykeyname1": {
        "my_special_var": "cool special var",
        "my_deep_validation": {
            "my_other_var": "not_set"
        }
    },
    "other_key_name": {
        "my_special_var": "cool special var",
        "my_deep_validation": {
            "my_other_var": "not_set"
        }
    }
}
```

The Any Item method operates somewhat differently from defined items:

| Description                      | defined   | `__any_item__` |
|----------------------------------|-----------|----------------|
| Follows `required` flag          | Y         | **N**          |
| Defaults Applied from `default`  | Y         | **N**          |
|||

The `required` is not followed because any item cannot be simultaneously required, and not a defined key name. Defaults are additionally not applied, because a key name must be known to apply a default.

Any Item entries may be of any type, or include a `spec_chain` as well.

### Example - Constructing Specs in Code

While this method is what I would consider 'somewhat messy', Specs can also be constructed in code. The code below shows how to create a spec called `root.spec`, with the required entries

```
spec_loader = SpecLoader("../specs/") # Load all .spec files from this directory
new_spec_part_A:SpecContent = SpecContent.create("test",value_type=dict,required=True, default={}, comment="Test Dict", example="This is a code test",spec_chain="root.test2")
new_spec_part_B:SpecContent = SpecContent.create("foo",value_type=int,required=True, default=10, comment="Test Foo", example="This is a code test")
new_spec_part_C:SpecContent = SpecContent.create("bar",value_type=str,required=True, default="baz", comment="Test Bar", example="This is a code test")
spec_loader.add("root",new_spec_part_A)
spec_loader.add("root",new_spec_part_B)
spec_loader.add("root",new_spec_part_C)

# Note that new_spec_part_A had a `spec_chain` defined. We will create that here too.
new_sub_spec_part:SpecContent = SpecContent.create("sub",value_type=str,required=True, default="foobar", comment="Test Sub Item", example="This is a code test")
spec_loader.add("root.test2",new_sub_spec_part)
```

This would be the same as if you had done the following in a file called `root.spec` and `root.test2.spec`:

`root.spec`
```
{
    "test": {
        "required": true,
        "type": "dict",
        "default": {},
        "comment": "Test Dict",
        "example": "This is a code test",
        "spec_chain": "root.test2"
    },
    "foo": {
        "required": true,
        "type": "int",
        "default": 10,
        "comment": "Test Foo",
        "example": "This is a code Test"
    },
    "bar": {
        "required": true,
        "type": "str",
        "default": "baz",
        "comment": "Test Bar",
        "example": "This is a code test"
    }
}
```

`root.test2.spec`
```
{
    "sub": {
        "required": true,
        "type": "str",
        "default": "foobar",
        "comment": "Test Sub Item",
        "example": "This is a code test"
    }
}
```

## Utils

 - **`generate-spec-docs`** - Generate a Markdown (`.md`) file from a directory of Spec files. (See [`SPECFILES.md`](SPECFILES.md), this is a generated document).
 - **`validate-spec-file`** - Validate a that a spec file is valid, by comparing it to the `specker.spec`
 - **`get-spec-defaults`** - Print the defaults gathered from a spec, following its spec_chain all the way down.
