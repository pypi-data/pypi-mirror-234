
![Build Status](https://drone-ext.mcos.nc/api/badges/scrippy/scrippy-template/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)


![Scrippy, my scrangourou friend](./scrippy-template.png "Scrippy, my scrangourou friend")

# `scrippy_template`

Simplified management of template files for the [`Scrippy`](https://codeberg.org/scrippy) framework.

## Prerequisites

### Python modules

#### List of required modules

The modules listed below will be automatically installed.

- jinja2

## Installation

### Manual

```bash
git clone https://codeberg.org/scrippy/scrippy-template.git
cd scrippy-template
python -m pip install -r requirements.txt
make install
```

### With `pip`

```bash
pip install scrippy-template
```

### Usage

This module allows document generation from template files using the *[jinja2](http://jinja.pocoo.org/)* rendering engine.

To be usable, template files must be located in the directory defined by the `base_path` parameter passed to the `template.Renderer` object.

To handle variable interpolation, the template file **MUST** accept a dictionary named `params` as a parameter.

This dictionary must contain all the variables necessary for the complete rendering of the template file.

The rendering of the template file is obtained from the `template.Renderer` object, whose instantiation requires the name of a template file and the base path in which to search for the template file.

Environment-specific parameters for _Jinja2_ can be modified through the `env` attribute of the `template.Renderer` object.

By convention, the template files used by the _Scrippy_ framework are stored in the directory defined by the `env::templatedirdir` configuration parameter (see the configuration of the [_Scrippy_](https://codeberg.org/scrippy) framework in the relevant [documentation](https://codeberg.org/scrippy/scrippy-core)).

A template is a simple text file with certain duly marked passages interpolated by the variables passed as parameters.

The `Renderer.render()` method returns the rendering of the template file.

The variables must be supplied to the template file as a dictionary named `params`.

The dictionary will be passed to the template file which will be responsible for interpolating the variables it contains.

Template files can include:
- control structures
- loops

#### Simple template file

With the following template file named *template_test.mod* located in the directory `/var/scrippy/templates`:

```txt
Hello {{params.user}}

You received this email because you are a member of the functional administrators of {{params.app}}.

The {{params.script}} script execution on {{params.date}} ended with the following error code:
- {{params.error.code}}: {{params.error.msg}}

--
Regards.
{{params.sender}}
```

The template file can be used as follows:

```python
import datetime
from scrippy_template import template

params = {"user": "Harry Fink",
          "app": "Flying Circus",
          "script": "dead_parrot.py",
          "date": datetime.datetime.now().strftime("%Y/%m/%d"),
          "error": {"code": 42,
                    "msg": "It’s not pinin’! It’s passed on! This parrot is no more!"},
          "sender": "Luiggi Vercotti", }

base_path = '/var/lib/scrippy/templates'
template_file = 'template.j2'
renderer = template.Renderer(base_path, template_file)

print(renderer.render(params))

```

With the default values, the message displayed at the end of the script will contain:

```txt
Hello Harry Fink

You received this email because you are a member of the functional administrators of Flying Circus.

The  dead_parrot.py script execution on 2019/09/15 ended with the following error code:
- 42: It’s not pinin’! It’s passed on! This parrot is no more!

--
Regards.
Luigi Vercotti
```

#### Template file with control structures

```python
params = {"user": "Harry Fink",
          "app": "Flying Circus",
          "script": "dead_parrot.py",
          "date": datetime.datetime.now().strftime("%Y/%m/%d"),
          "num_error": 42,
          "sender": "Luiggi Vercotti", }
```

```txt
Hello {{params.user}}

You received this email because you are a member of the functional administrators of {{params.app}}.

The {{params.script}} script execution on {{params.date}} ended
{% if params.num_errors == 0 %}
- without error
{% else %}
 with {{params.num_errors}} error(s)
{% endif %}

--
Regards.
{{params.sender}}
```

#### Template file with loop

```python
params = {"user": "Harry Fink",
          "app": "Flying Circus",
          "script": "dead_parrot.py",
          "date": datetime.datetime.now().strftime("%Y/%m/%d"),
          'errors': [{'code': 2, 'msg': "It's not pinin’! It's passed on! This parrot is no more!"},
                     {'code': 3, 'msg': "Ohh! The cat's eaten it."}],
          "sender": "Luiggi Vercotti", }
```


```txt
Hello {{params.user}}

You received this email because you are a member of the functional administrators of {{params.app}}.

The {{params.script}} script execution on {{params.date}} ended with the following errors:
{% for error in params.errors %}
- {{ error.code }}: {{ error.msg}}
{% endfor %}

--
Regards.
{{params.sender}}
```
