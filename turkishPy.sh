if test "$#" -ne 1; then
    python3 -i -c "from turkish import *"
else
    filename=$1
    filename="${filename%.*}"
    python3 -c "import turkish; turkish.catch_indentation_errors = True; import ${filename}"
fi
 
