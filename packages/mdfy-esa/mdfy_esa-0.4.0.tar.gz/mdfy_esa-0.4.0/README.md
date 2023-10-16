# mdfy-esa

[![pypi](https://img.shields.io/pypi/v/mdfy-esa.svg)](https://pypi.org/project/mdfy-esa/)
[![python](https://img.shields.io/pypi/pyversions/mdfy-esa.svg)](https://pypi.org/project/mdfy-esa/)
[![release & publish workflow](https://github.com/argonism/mdfy-esa/actions/workflows/release.yml/badge.svg?event=push)](https://github.com/argonism/mdfy-esa/actions/workflows/release.yml)
[![test status](https://github.com/argonism/mdfy-esa/actions/workflows/dev.yml/badge.svg)](https://github.com/argonism/mdfy-esa/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/argonism/mdfy-esa/branch/main/graphs/badge.svg)](https://codecov.io/github/argonism/mdfy-esa)

mdfy plugin for esa

-   Documentation: <https://argonism.github.io/mdfy-esa>
-   GitHub: <https://github.com/argonism/mdfy-esa>
-   PyPI: <https://pypi.org/project/mdfy-esa/>
-   Free software: MIT

## Pre-requirement

You need set esa.io API token and set it to environment veriable ESA_ACCESS_TOKEN.

``` shell
export ESA_ACCESS_TOKEN=YOUR_ACCESS_TOKEN
```

## Usage

The mdfy-esa feature supports uploading of local images and files.
With the EsaMdfier, images or files designated with MdImage or MdLink are uploaded automatically.
Simply pass the MdImage with the local image path, and voila - it’s done!"

```python
from mdfy import MdImage, MdLink, MdText
from mdfy_esa import EsaMdfier

esa_team = "your esa team name"
post_fullname = "post name as you like"
contents = [
    MdText("This is a test article."),
    MdImage(src="examples/test_image.png"),
    MdLink(url="examples/dummy.pdf"),
]

mdfier = EsaMdfier(post_fullname=post_fullname, esa_team=esa_team)
created_post_info = mdfier.write(contents=contents)

# created_post_info = {'number': 4418, 'name': 'My Test Article', 'full_name': 'note/me/My Test Article', 'wip': True, 'body_md': 'This is a test article.\n', 'body_html': '<p data- ...}
# see esa.io api document for detail
# https://docs.esa.io/posts/102#POST%20/v1/teams/:team_name/posts
```

You can also update an existing post using its post number!

```python
from mdfy import MdImage, MdLink, MdText
from mdfy_esa import EsaMdfier

esa_team = "your esa team name"
post_number = 4930
contents = [
    MdText("NEW! This post is updated!"),
    MdText("This is a test article."),
    MdImage(src="examples/test_image.png"),
    MdLink(url="examples/dummy.pdf"),
]

mdfier = EsaMdfier(post_number=post_number, esa_team=esa_team)
updated_post_info = mdfier.write(contents=contents)
```

## Features

-   TODO

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.
