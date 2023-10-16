from unittest.mock import patch

import pytest
from mdfy import MdImage, MdLink

from mdfy_esa import EsaMdfier


@patch('piyo.Client.upload_file', return_value="http://uploaded.file")
@patch('piyo.Client.create_post')
def test_write_with_MdImage(mock_create_post, mock_upload_file):
    post_fullname = "Test Article"
    mdfier = EsaMdfier(post_fullname=post_fullname, esa_team="test_team")
    img_element = MdImage(src="./test_image.png")

    mdfier.write(contents=img_element)

    mock_upload_file.assert_called_once_with("./test_image.png")
    mock_create_post.assert_called_once()
    assert mock_create_post.call_args[0][0] == {
        "post": {
            "name": post_fullname,
            "body_md": "![](http://uploaded.file)\n",
        }
    }


@patch('piyo.Client.upload_file', return_value="http://uploaded.file")
@patch('piyo.Client.create_post')
def test_write_with_post_params(mock_create_post, mock_upload_file):
    post_fullname = "Test Article"
    mdfier = EsaMdfier(post_fullname=post_fullname, esa_team="test_team")
    img_element = MdImage(src="./test_image.png")
    post_data = {"wip": True, "tags": ["test", "mdfy"]}

    mdfier.write(contents=img_element, post_params=post_data)

    mock_upload_file.assert_called_once_with("./test_image.png")
    mock_create_post.assert_called_once()
    assert mock_create_post.call_args[0][0] == {
        "post": {"name": post_fullname, "body_md": "![](http://uploaded.file)\n", "wip": True, "tags": ["test", "mdfy"]}
    }


@patch('piyo.Client.upload_file', return_value="http://uploaded.file")
@patch('piyo.Client.create_post')
def test_write_with_None_for_fullname_and_number(mock_create_post, mock_upload_file):
    post_fullname = None
    with pytest.raises(ValueError, match="Either post_fullname or post_number must be set"):
        EsaMdfier(post_fullname=post_fullname, esa_team="test_team")


@patch('piyo.Client.upload_file', return_value="http://uploaded.file")
@patch('piyo.Client.create_post')
def test_write_with_file_scheme_url(mock_create_post, mock_upload_file):
    post_fullname = "Test Article"
    file_path = "/path-to-mdfy/tests/example_file.txt"
    mdfier = EsaMdfier(post_fullname=post_fullname, esa_team="test_team")
    link_element = MdLink(url=f"file://{file_path}")

    mdfier.write(contents=link_element)

    mock_upload_file.assert_called_once_with(file_path)
    mock_create_post.assert_called_once()
    assert mock_create_post.call_args[0][0] == {
        "post": {
            "name": post_fullname,
            "body_md": "[http://uploaded.file](http://uploaded.file)\n",
        }
    }


@patch('piyo.Client.upload_file', return_value="http://uploaded.file")
@patch('piyo.Client.create_post')
def test_write_with_MdLink(mock_create_post, mock_upload_file):
    post_fullname = "Test Article"
    mdfier = EsaMdfier(post_fullname=post_fullname, esa_team="test_team")
    link_element = MdLink(url="test_link.png")

    mdfier.write(contents=link_element)

    mock_upload_file.assert_called_once_with("test_link.png")
    mock_create_post.assert_called_once()
    assert mock_create_post.call_args[0][0] == {
        "post": {
            "name": post_fullname,
            "body_md": "[http://uploaded.file](http://uploaded.file)\n",
        }
    }


@patch('piyo.Client.upload_file', return_value="http://uploaded.file")
@patch('piyo.Client.update_post')
def test_update_with_MdImage(mock_update_post, mock_upload_file):
    post_number = 123456789
    mdfier = EsaMdfier(post_number=post_number, esa_team="test_team")
    img_element = MdImage(src="./test_image.png")

    mdfier.write(contents=img_element)

    mock_upload_file.assert_called_once_with("./test_image.png")
    mock_update_post.assert_called_once()
    assert mock_update_post.call_args[0][0] == post_number
    assert mock_update_post.call_args[0][1] == {
        "post": {
            "body_md": "![](http://uploaded.file)\n",
        },
    }


@patch('piyo.Client.upload_file', return_value="http://uploaded.file")
@patch('piyo.Client.update_post')
def test_update_with_post_params(mock_update_post, mock_upload_file):
    post_number = 123456789
    mdfier = EsaMdfier(post_number=post_number, esa_team="test_team")
    img_element = MdImage(src="./test_image.png")
    post_data = {"wip": True, "tags": ["test", "mdfy"]}

    mdfier.write(contents=img_element, post_params=post_data)

    mock_upload_file.assert_called_once_with("./test_image.png")
    mock_update_post.assert_called_once()
    assert mock_update_post.call_args[0][0] == post_number
    assert mock_update_post.call_args[0][1] == {
        "post": {
            "body_md": "![](http://uploaded.file)\n",
            "wip": True,
            "tags": ["test", "mdfy"],
        },
    }


@patch('piyo.Client.upload_file', return_value="http://uploaded.file")
@patch('piyo.Client.create_post')
def test_write_raise_error_when_post_fullname_and_post_number_None(mock_create_post, mock_upload_file):
    post_fullname = "Test Article"
    mdfier = EsaMdfier(post_fullname=post_fullname, esa_team="test_team")
    mdfier.post_fullname = None
    with pytest.raises(ValueError, match="Either post_fullname or post_number must be set"):
        mdfier.write(contents=MdImage(src="./test_image.png"))


# 環境変数のテスト
def test_missing_ESA_TEAM_env_var():
    with pytest.raises(ValueError):
        EsaMdfier(post_fullname="Test Article")
