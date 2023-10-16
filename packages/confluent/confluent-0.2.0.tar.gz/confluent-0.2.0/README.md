# confluent
In times of distributed systems and en vogue micro-architecture it can get quite cumbersome to keep constants that are required by several components up-to-date and in sync. It can get especially hard when these components or services are written in different languages. *confluent* targets this issue by using a language neutral YAML configuration that lets you generate language specific config files in the style of classes and structs.

## Currently supported languages
- [x] Java
- [x] JavaScript
- [x] TypeScript
- [x] Python
- [x] C
- [x] Go

## Installation
```bash
python -m pip install confluent  # On Linux use python3.
```

## Configuration
For details about the configuration file, please check *example/test-config.yaml*. All possible values are described there. Basically the configuration consists of a *languages*- and a *properties*-section. The first one describes language specific properties e.g. for which language to generate, which naming convention to use for the output file or how much indent to use. The *properties*-section defines the actual values whereis the following types are supported: *bool*, *int*, *float*, *double*, *string* and *regex*. Properties can also act as helpers for other properties which don't need to be written to the final config-file. These properties must be marked as *hidden*. Acting as a helper-property means that it defines a value which other properties can use as substitute values referencing them via *${property-name}*. Additionally, other configuration files can be included via the *includes*-section. This way it is possible to use properties from external files in combination with currently defined properties via *${include-alias.property-name}* (see example config).

## Usage
### Commandline
```bash
python3 -m confluent -c test-config.yaml -o generated
```

### Script
```python
from confluent import Orchestrator

# Create Orchestrator instance from file.
orchestrator = Orchestrator.read_config('test-config.yaml')

# Write configs to 'generated' directory.
orchestrator.write('generated')
```

## Example

### Configuration
```yaml
# test-config.yaml file.

# Optional
includes:
  # --- Common properties ---------------------------------------------------
  # path (required): Specifies the path to the external configuration file.
  # as   (required): Specifies how the file will be referenced in value substitutions (e.g., ${ti.myIncludedString}).
  # -------------------------------------------------------------------------
  - path: test-include.yaml
    as: ti

# Optional
languages:
  # --- Common properties (valid for all languages) -------------------------
  # type            (required): Specifies the output language (java | javascript | typescript | python | c | go).
  #
  # file_naming     (optional): Specifies the file naming convention (snake | screaming_snake | camel | pascal | kebap). Defaults to the file-name without the extension.
  # property_naming (optional): Specifies the property naming convention (snake | screaming_snake | camel | pascal | kebap).
  # type_naming     (optional): Specifies the naming convention for the generated type (snake | screaming_snake | camel | pascal | kebap). The default value is language specific.
  # indent          (optional): Specifies the amount of spaces before each constant. Defaults to 4.
  # transform       (optional): Specifies a Python script to transform the currently processed property. To reflect changes to the outside of the script, the value variable
  #                             must be modified. The script has access to the following variables:
  #
  #                             name: Property name.
  #                             value: Property value.
  #                             type: Property type.
  #                             properties: List of all properties (must not be modified).
  # -------------------------------------------------------------------------

  # --- Java specific properties --------------------------------------------
  # package (required): Specifies the Java package name.
  # -------------------------------------------------------------------------
  - type: java
    file_naming: pascal
    type_naming: pascal
    package: my.test.package

  # --- JavaScript/TypeScript specific properties ---------------------------
  # export (optional): Specifies how to export the class (esm | common_js | none). Defaults to esm.
  # -------------------------------------------------------------------------
  - type: javascript
    file_naming: screaming_snake
    indent: 4
    export: common_js

  - type: typescript
    indent: 4
    export: esm

  # -------------------------------------------------------------------------
  - type: python
    file_naming: snake
    property_naming: screaming_snake

  # -------------------------------------------------------------------------
  - type: c
    file_naming: snake
    property_naming: pascal

  # --- Go specific properties ----------------------------------------------
  # package (required): Specifies the Go package name.
  # -------------------------------------------------------------------------
  - type: go
    file_naming: snake
    package: myconfig
    transform: |  # If the property 'myString' is being processed, replace the value by 'Hello Mars'.
      if name == 'myString':
        value = 'Hello Mars'

properties:
  # -------------------------------------------------------------------------
  # type    (required): Specifies the constant data type (bool | int | float | double | string | regex).
  # name    (required): Specifies the constant's name.
  # value   (required): Specifies the constant's value.
  #
  # comment (optional): Adds an extra comment to the constant.
  # hidden  (optional): Constants serves as helper and will not be written to the final result.
  # -------------------------------------------------------------------------

  - type: bool
    name: myBoolean
    value: true

  - type: int
    name: myInteger
    value: 142

  - type: float
    name: myFloat
    value: 322f  # Float with float specifier. However, an additional specifier (f) is not required and will be trimmed.

  - type: float
    name: myCombinedFloat
    value: ${myInteger} * ${myFloat}  # Number and boolean combinations get evaluated during the dump process.

  - type: double
    name: myDouble
    value: 233.9

  - type: string
    name: myString
    value: Hello World
    hidden: true  # If a property should act as a helper but should not be written to the generated file, it must be marked as 'hidden'.

  - type: regex
    name: myRegex
    value: Test Reg(E|e)x
    comment: Just another RegEx.  # Variables can be described using the comment property.

  - type: string
    name: mySubstitutedString
    value: Sometimes I just want to scream ${myString}!  # To use the value of another property, simply use its name with ${}. E.g., ${myString}.

  - type: string
    name: myCombinedString
    value: I am telling you that ${ti.myIncludedString}.  # To use the value of another property from an included file, simply use the file's
                                                          # alias and the corresponding property name. E.g., ${ti.myIncludedString}.
```

```yaml
# test-include.yaml file.

properties:
  - type: string
    name: myIncludedString
    value: this string got included from test-include.yaml
```

### Output
#### Java
```java
package my.test.package;

// Generated with confluent v0.2.0 (https://pypi.org/project/confluent/).
public class TestConfig {
    public final static boolean myBoolean = true;
    public final static int myInteger = 142;
    public final static float myFloat = 322.0f;
    public final static float myCombinedFloat = 45724.0f;
    public final static double myDouble = 233.9d;
    public final static String myRegex = "Test Reg(E|e)x"; // Just another RegEx.
    public final static String mySubstitutedString = "Sometimes I just want to scream Hello World!";
    public final static String myCombinedString = "I am telling you that this string got included from test-include.yaml.";
}
```

#### JavaScript
```javascript
// Generated with confluent v0.2.0 (https://pypi.org/project/confluent/).
class TestConfig {
    static get myBoolean() { return true; }
    static get myInteger() { return 142; }
    static get myFloat() { return 322.0; }
    static get myCombinedFloat() { return 45724.0; }
    static get myDouble() { return 233.9; }
    static get myRegex() { return /Test Reg(E|e)x/; } // Just another RegEx.
    static get mySubstitutedString() { return 'Sometimes I just want to scream Hello World!'; }
    static get myCombinedString() { return 'I am telling you that this string got included from test-include.yaml.'; }
}
module.exports = TestConfig
```

#### TypeScript
```typescript
// Generated with confluent v0.2.0 (https://pypi.org/project/confluent/).
export class TestConfig {
    public static readonly myBoolean = true;
    public static readonly myInteger = 142;
    public static readonly myFloat = 322.0;
    public static readonly myCombinedFloat = 45724.0;
    public static readonly myDouble = 233.9;
    public static readonly myRegex = /Test Reg(E|e)x/; // Just another RegEx.
    public static readonly mySubstitutedString = 'Sometimes I just want to scream Hello World!';
    public static readonly myCombinedString = 'I am telling you that this string got included from test-include.yaml.';
}
```

#### Python
```python
# Generated with confluent v0.2.0 (https://pypi.org/project/confluent/).
class TestConfig:
    MY_BOOLEAN = True
    MY_INTEGER = 142
    MY_FLOAT = 322.0
    MY_COMBINED_FLOAT = 45724.0
    MY_DOUBLE = 233.9
    MY_REGEX = r'Test Reg(E|e)x'  # Just another RegEx.
    MY_SUBSTITUTED_STRING = 'Sometimes I just want to scream Hello World!'
    MY_COMBINED_STRING = 'I am telling you that this string got included from test-include.yaml.'
```

#### C
```c
#ifndef TEST_CONFIG_H
#define TEST_CONFIG_H

/* Generated with confluent v0.2.0 (https://pypi.org/project/confluent/). */
const struct {
    unsigned char MyBoolean;
    int MyInteger;
    float MyFloat;
    float MyCombinedFloat;
    double MyDouble;
    char* MyRegex; /* Just another RegEx. */
    char* MySubstitutedString;
    char* MyCombinedString;
} TestConfig = {
    1,
    142,
    322.0f,
    45724.0f,
    233.9,
    "Test Reg(E|e)x",
    "Sometimes I just want to scream Hello World!",
    "I am telling you that this string got included from test-include.yaml.",
};

#endif /* TEST_CONFIG_H */
```

#### Go
```go
package myconfig

// Generated with confluent v0.2.0 (https://pypi.org/project/confluent/).
var TestConfig = struct {
    myBoolean           bool
    myInteger           int
    myFloat             float64
    myCombinedFloat     float64
    myDouble            float64
    myRegex             string // Just another RegEx.
    mySubstitutedString string
    myCombinedString    string
}{
    myBoolean:           true,
    myInteger:           142,
    myFloat:             322.0,
    myCombinedFloat:     45724.0,
    myDouble:            233.9,
    myRegex:             "Test Reg(E|e)x",
    mySubstitutedString: "Sometimes I just want to scream Hello Mars!",
    myCombinedString:    "I am telling you that this string got included from test-include.yaml.",
}
```

## Possible use case

### Configuration
```yaml
languages:
  - type: java
    file_naming: pascal
    package: com.app.endpoints
    transform: value = value.replace(':id', '{id}')  # For Java replace ':id' by '{id}'

  - type: typescript
    file_naming: kebap

properties:
  # === Helper properties ===============
  - type: string
    name: PATH_PARAM_ID
    value: :id
    hidden: true

  # === Exported properties =============
  - type: string
    name: API_ENDPOINT
    value: /api

  - type: string
    name: USERS_ENDPOINT
    value: ${API_ENDPOINT}/users

  - type: string
    name: USER_PERMISSIONS_ENDPOINT
    value: ${USERS_ENDPOINT}/${PATH_PARAM_ID}/permissions

  - type: string
    name: CUSTOMERS_ENDPOINT
    value: ${API_ENDPOINT}/customers
```

### Output
#### Java
```java
package com.app.endpoints;

// Generated with confluent v0.1.0 (https://pypi.org/project/confluent/).
public class Endpoints {
    public final static String API_ENDPOINT = "/api";
    public final static String USERS_ENDPOINT = "/api/users";
    public final static String USER_PERMISSIONS_ENDPOINT = "/api/users/{id}/permissions";
    public final static String CUSTOMERS_ENDPOINT = "/api/customers";
}
```

#### TypeScript
```typescript
// Generated with confluent v0.1.0 (https://pypi.org/project/confluent/).
export class Endpoints {
    public static readonly API_ENDPOINT = '/api';
    public static readonly USERS_ENDPOINT = '/api/users';
    public static readonly USER_PERMISSIONS_ENDPOINT = '/api/users/:id/permissions';
    public static readonly CUSTOMERS_ENDPOINT = '/api/customers';
}
```

## How to participate
If you feel that there's a need for another language, feel free to add it. For detailed information how to add support for a new language, please refer to [README.md](https://github.com/monstermichl/confluent/tree/main/misc/language_support/README.md).
