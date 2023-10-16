ARG PYTHON_VERSION

FROM python:$PYTHON_VERSION
ARG PYPI_MIRROR=https://pypi.org/simple

RUN pip install --upgrade --index=$PYPI_MIRROR --no-cache-dir pre-commit pip pdm twine
