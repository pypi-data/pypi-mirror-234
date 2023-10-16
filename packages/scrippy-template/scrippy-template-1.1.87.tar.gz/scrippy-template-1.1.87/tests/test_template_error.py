"""Test de fichier modèle à boucle."""

from scrippy_template import template
from scrippy_template import ScrippyTemplateError


EXPECTED = """Bonjour Harry Fink

Vous recevez cet e-mail car vous faites partie des administrateurs fonctionnels de l'application Flying Circus.

L'exécution du script dead_parrot.py s'est terminé avec les erreurs suivantes:

  2: It&#39;s not pinin’! It&#39;s passed on! This parrot is no more!

  3: Ohh! The cat&#39;s eaten it.


--
Cordialement.
Luiggi Vercotti"""


def test_template_error():
  """Test de levée d'erreur."""
  params = {"user": "Harry Fink",
            "app": "Flying Circus",
            "script": "dead_parrot.py",
            'errors': [{'code': 2, 'msg': "It's not pinin’! It's passed on! This parrot is no more!"},
                       {'code': 3, 'msg': "Ohh! The cat's eaten it."}],
            "sender": "Luiggi Vercotti"}
  base_path = "./tests/templates"
  template_file = "inexistant"
  try:
    renderer = template.Renderer(base_path, template_file)
    renderer.render(params)
  except ScrippyTemplateError:
    pass
