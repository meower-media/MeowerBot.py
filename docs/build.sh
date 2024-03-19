# removing prev build, but saving index.rst



# generating documentation
sphinx-apidoc -o ./autogen ../MeowerBot/  ../MeowerBot/data/* -e
sphinx-autogen -o ./autogen ../MeowerBot/**.py -a

# converting it to HTML
MAKEVARS="html"

if [[ "$OSTYPE" == "msys" ]]; then
        ./make.bat $MAKEVARS
else
        make $MAKEVARS
fi
