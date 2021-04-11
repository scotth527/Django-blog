# Microblog - Social Media

Personal project to create a social media platform. Allows users to be created, each person can make posts, comment and like each other's content. With friend requests. 

## Installation

Please git clone the project. Create a python environment.

## Run server

python manage.py runserver

## Run tests 

python manage.py test

## Automate testing 

Requires entr 

```
find . -name '*.py' | entr python ./manage.py test
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
