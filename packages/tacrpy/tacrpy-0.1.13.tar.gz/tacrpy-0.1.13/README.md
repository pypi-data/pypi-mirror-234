## **tacrpy**

Python knihovna, která slouží pro práci s daty a vypracování analýz TA ČR

## Prerekvizity

- Python 3.9+

## Práce s repozitářem

1) Naklonuj si tento repozitář:

   `git clone git@git.tacr.cz:data-team/tacrpy.git`

2) Přejdi do složky _'tacrpy'_

   `cd tacrpy`

3) Vytvoř si virtuální prostředí

   `python -m venv .venv`

4) Aktivuj si virtuální prostředí

   `source .venv/bin/activate`

5) Nainstaluj požadavky

   `pip install -r requirements.txt`

## Generování dokumentace
### Prerekvizity

- Sphinx (`pip install sphinx`)
- Read The Docs Theme (`pip install sphinx_rtd_theme`)

### Generování dokumentace
1) Naklonuj si tento repozitář:

   `git clone git@git.tacr.cz:data-team/tacrpy.git`
2) Přejdi do adresáře _'docs'_:

   `cd docs`
3) Spusť _'sphinx-apidoc'_ pro vygenerování souborů dokumentace

   `sphinx-apidoc -f -o source ../tacrpy`
4) Pro vygenerování html dokumentace:
   
   `make.bat clean`

   `make.bat html`

5) Vygenerovaná dokumentace se nachází v adresáři _'docs/build/html'_

## Release nové verze knihovny

### Prerekvizity

- Twine (`pip install twine`)
- Účet na PyPI (https://pypi.org/)
- role Owner nebo Maintainer v projektu tacrpy (správce rolí: David Šulc)

### Release nové verze knihovny

1) Naklonuj si tento repozitář:

   `git clone git@git.tacr.cz:data-team/tacrpy.git`
2) Přejdi do zdrojového adresáře _'tacrpy'_ (resp. složka, ve které je _'setup.py'_):

      `cd tacrpy`
3) Spusť generování souborů knihovny

   `python setup.py sdist bdist_wheel`
4) Spusť nahrání souborů na PyPI

   `twine upload --skip-existing dist/*`
5) Vyplň username a heslo (případně API klíč)
