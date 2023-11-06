
# removing prev build, but saving index.rst

mv source/index.rst ./index.rst
rm source/*.rst
mv ./index.rst ./source/index.rst

# generating documentation
sphinx-apidoc -o ./source ../MeowerBot/  ../MeowerBot/data/* -e
sphinx-autogen -o ./source ../MeowerBot/**.py -a


# converting it to HTML
MAKEVARS="html"

if [[ "$OSTYPE" == "msys" ]]; then
	./make.bat $MAKEVARS
else
	make $MAKEVARS
fi


# running server
echo "localhost:8000"
python -m http.server -d build/html
