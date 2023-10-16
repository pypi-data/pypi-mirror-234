#!/usr/bin/env python3
"""
This module allows the generation of documents from template files.

To be usable, template files must be located in the directory 'self.base_path'.

To manage variable interpolation, the template file MUST accept a dictionary named 'params' as a parameter.

This dictionary should contain all the variables required for the complete rendering of the template file.

Example:

With the following simple template file:

"Hello {{params.user}}, this email is sent to you by {{params.sender}}."

The 'params' dictionary should be:

params = {'user': 'harry.fink', 'sender': 'Luigi Vercotti'}
"""
import jinja2
from scrippy_template import ScrippyTemplateError, logger


class Renderer:
  """
  The Renderer object is responsible for loading and rendering template files.
  """

  def __init__(self, base_path, template_filename):
    """
    Instantiating a Renderer object requires the name of the template file to load.
    The template file will be automatically retrieved from the 'self.base_path' directory and should not be an absolute path but the name of the file itself.
    """
    self.base_path = base_path
    self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.base_path), autoescape=True)
    self.load(base_path, template_filename)

  def load(self, base_path, template_filename):
    """
    Allows the same Renderer object to load another template file.
    The previously loaded template file is lost when loading the new file.
    """
    logger.debug("[+] Loading template")
    logger.debug(f" '-> Template: {base_path}/{template_filename}")
    self.template_filename = template_filename

  def render(self, params=None):
    """
    Returns the rendering of the template file.

    If variables need to be provided to the template file, they must be in the form of a dictionary.

    The dictionary will then be passed to the template file, which will be responsible for interpolating these variables.
    """
    logger.debug("[+] Rendering template")
    try:

      template = self.env.get_template(self.template_filename)
      return template.render(params=params)
    except jinja2.exceptions.TemplateNotFound as err:
      err_msg = f"Template not found: {self.template_filename}"
      raise ScrippyTemplateError(err_msg) from err
    except jinja2.exceptions.UndefinedError as err:
      err_msg = f"Unknown error: [{err.__class__.__name__}] {err}"
      raise ScrippyTemplateError(err_msg) from err
    except Exception as err:
      err_msg = f"Unexpected error: [{err.__class__.__name__}] {err}"
      raise ScrippyTemplateError(err_msg) from err
