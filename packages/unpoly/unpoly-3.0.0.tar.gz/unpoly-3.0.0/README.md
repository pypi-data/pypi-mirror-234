[![version](https://img.shields.io/pypi/v/unpoly.svg)](https://pypi.org/project/unpoly)
[![python versions](https://img.shields.io/pypi/pyversions/unpoly.svg)](https://pypi.org/project/unpoly)
[![docs](https://img.shields.io/readthedocs/unpoly)](https://unpoly.readthedocs.io)
[![pipeline status](https://gitlab.com/rocketduck/python-unpoly/badges/main/pipeline.svg)](https://gitlab.com/rocketduck/python-unpoly/-/commits/main)
[![coverage report](https://gitlab.com/rocketduck/python-unpoly/badges/main/coverage.svg)](https://gitlab.com/rocketduck/python-unpoly/-/commits/main)

# Unpoly

Unpoly is a framework agnostic python library implementing the [Unpoly server protocol](https://unpoly.com/up.protocol).

## Features

* **Full protocol implementation**: The whole Unpoly server protocol is implemented and well tested.
* **Django support**: Out of the box we currently ship a middleware for Django support.
* **Easily extendable**: The library abstracts the actual HTTP stuff via adapters and can easily plugged into frameworks like Flask etc.

## Download & Install

```
pip install unpoly
```

### Usage with Django

Add `unpoly.contrib.django.UnpolyMiddleware` to your middlewares and then you can access `request.up`. Details can be found in the usage section of the [docs](https://unpoly.readthedocs.io/en/latest/usage.html).

Example usage:

```py
def my_view(request):
    if request.up: # Unpoly request
        # Send an event down to unpoly
        request.up.emit("test:event", {"event": "params"})
        # ... and also clear the cache for certain paths
        request.up.expire("/users/*")
    else:
        ...

def form_view(request):
    form = MyForm(request.GET)
    # When unpoly wants to validate a form it sends
    # along X-Up-Validate which contains the field
    # being validated.
    if form.is_valid() and not request.up.validate:
        form.save()
    return render(request, "template.html", {"form": form})
```

### Usage with Flask etc

Subclass `unpoly.adapter.BaseAdapter` and initialize `unpoly.Unpoly` with it for every request (see the [docs](https://unpoly.readthedocs.io/en/latest/adapters.html) for details).
