# Build documentation
(cd doc && make latexpdf)
cp doc/_build/latex/spix.pdf .

# Built CTAN package
ctanify --notds --pkgname=spix \
  CHANGELOG.md \
  LICENSE.txt \
  README.md \
  spix.1 \
  spix.pdf \
  spix.py
