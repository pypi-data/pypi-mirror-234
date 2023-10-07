# LearnTools

### Stucture

 - Network
    - network (class to hold network)
    - layer_dense (dense layer from layer class)
 - Learning

# Getting started
run the command *pip install learntools*\
for network use *from learntools import Network*\
for learning use *from learntools import Learning*

### Note to Self
 - Setup Venv
    - install wheel, twine
 - To upload package
 - build dist:
    - python setup.py sdist bdist_wheel
 - upload dist:
    - twine upload dist/*

 - To Build Documentation: https://realpython.com/python-project-documentation-with-mkdocs/#:~:text=Build%20Your%20Python%20Project%20Documentation%20With%20MkDocs%201,Step%203%3A%20Write%20and%20Format%20Your%20Docstrings%20