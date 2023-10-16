


# Not Yet Implemented Requirements
```sh
[tool.poetry.dependencies]
python = "^3.8"
python-jose = "^3.3.0"
requests = ">=2.11"
feedparser = "^6.0.8"
strawberry-graphql = {extras = ["debug-server", "fastapi"], version = "^0.139.0"}
deep-translator = "1.8.3"
pillow = "9.1.0"
pytesseract = "0.3.9"
chardet = "4.0.0"
opencv-python = "4.5.5.64"
python-multipart = "^0.0.5"
boto3 = "^1.26.117"
markupsafe = "2.0.1"
pydantic = "1.10.13"
motor = "^3.3.1"
```






# Install requirements for local development:

`pip install -r requirements.txt`

# Compiled Package Commands

build poetry package:

`python cli.py build`

install poetry package:

`python cli.py install`


# poetry

## poetry add

__update package to latest version__

- Use @latest, you dont need to use the latest version number.
```sh
poetry add langchain@latest
```


__add package to dev__

- The --dev option is deprecated, use the `--group dev` notation instead.
```sh
# not dev
poetry add types-aiofiles
# dev
poetry add --group dev install types-aiofiles
```

## poetry remove

- Remove library from dev dependancies
```sh
poetry remove --group dev httpx
```

## poetry update
- updates poetry.lock with changes from `pyproject.toml`

## poetry shell
- activates virtual env associated with poetry

## poetry install
- __Installs poetry.lock into virtual env__
- Checks poetry.lock file for exact versions of all dependencies to install.
    - Install's those versions into the virtual environment that Poetry is managing for your project.

## poetry install --all-extras --dry-run
- Install all dependencies.
- Install dev dependancies listed in pyproject.toml file. 



# Notes:

## Dependancies

### langchain
```sh
# https://colab.research.google.com/drive/1rU4UGE_WK1ED59E5zHeq_aXk8ksf7njW?authuser=1#scrollTo=2VXlucKiW7bX
!pip install langchain
!pip install openai
!pip install PyPDF2
!pip install faiss-cpu
!pip install tiktoken

pip install pypdf
    - required by PyPDFLoader

pip install pymilvus
    - required by Zilliz
```

```sh
opencv-python
langchain = "^0.0.189"
faiss-cpu = "^1.7.4"
tiktoken = "^0.4.0"
pypdf2 = "^3.0.1"
pytesseract = "^0.3.10"
markupsafe = "2.0.1"
promptify = "^0.1.4"

- pip install markupsafe==2.0.1 --force-reinstall

poetry add opencv-python langchain faiss-cpu tiktoken pypdf2 pytesseract markupsafe promptify
```
### transformers
```
transformers = {extras = ["torch"], version = "^4.31.0"}
tensorflow = "^2.13.0"
```

### opencv-python

- Select the correct package for your environment:
    - There are four different packages (see options 1, 2, 3 and 4 below) and you should SELECT ONLY ONE OF THEM. 
- Do not install multiple different packages in the same environment. There is no plugin architecture: all the packages use the same namespace (cv2). 
- If you installed multiple different packages in the same environment, uninstall them all with pip uninstall and reinstall only one package.
    - a. Packages for standard desktop environments (Windows, macOS, almost any GNU/Linux distribution)
        - Option 1 - __Main modules package__: `pip install opencv-python`
        - Option 2 - __Full package (contains both main modules and contrib/extra modules):__ `pip install opencv-contrib-python` (check contrib/extra modules listing from OpenCV documentation)
    - b. Packages for server __(headless) environments (such as Docker, cloud environments etc.),__ no GUI library dependencies
        - These packages are smaller than the two other packages above because they do not contain any GUI functionality (not compiled with Qt / other GUI components). 
        - This means that the packages avoid a heavy dependency chain to X11 libraries and you will have for example smaller Docker images as a result. 
        - __You should always use these packages if you do not use cv2.imshow et al.__ or you are using some other package (such as PyQt) than OpenCV to create your GUI.
            - Option 3 - Headless main modules package: `pip install opencv-python-headless`
            - Option 4 - Headless full package (contains both main modules and contrib/extra modules): `pip install opencv-contrib-python-headless` (check contrib/extra modules listing from OpenCV documentation)



# Issues

__Deployment__

__Summary__

- This codebase is a python library.
    - Uses `poetry` as build tool.
- Needs to be installable via internal pip.

