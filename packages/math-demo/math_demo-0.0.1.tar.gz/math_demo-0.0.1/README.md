# Library_Creation
Creating a  pip installable library 

#basic structure
base folder--setup.py and libname folder
inside libname filder should have python files and init files

#cmds

python setup.py sdist bdist_wheel



pip install twine


twine upload dist/*


