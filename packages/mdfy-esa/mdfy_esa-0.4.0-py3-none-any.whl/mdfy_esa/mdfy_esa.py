import os
from typing import List, Optional, Union, Dict, Any
from urllib.parse import urlparse

import piyo
from mdfy import MdElement, Mdfier, MdImage, MdLink


class EsaMdfier(Mdfier):
    """A class to modify Markdown files and upload images to Esa.

    Args:
        post_fullname (Optional[str], optional): The full name of the post to modify.
        post_number (Optional[int], optional): The number of the post to update.
        esa_team (Optional[str], optional): The name of the Esa team. Defaults to None.
            you can set this param or the environment variable ESA_TEAM.

    Raises:
        ValueError: If esa_team param or the environment variable ESA_TEAM is not set.

    Examples:
        >>> from mdfy import MdImage, MdLink, MdText
        >>> from mdfy_esa import EsaMdfier
        >>> contents = [
        ...     MdText("This is a test article."),
        ...     MdImage(src="example/test_image.png"),
        ...     MdLink(url="example/dummy.pdf"),
        ... ]
        >>> mdfier = EsaMdfier(post_fullname="note/me/My Test Article", esa_team="test_team")
        >>> mdfier.write(contents=contents)
    """

    def __init__(
        self,
        post_fullname: Optional[str] = None,
        post_number: Optional[int] = None,
        esa_team: Optional[str] = None,
    ) -> None:
        """Initializes the EsaMdfier class.

        Args:
            post_fullname (Optional[str], optional): The path to the post to modify.
            post_number (Optional[int], optional): The number of the post to update.
            esa_team (Optional[str], optional): The name of the Esa team. Defaults to None.
        """
        self.post_fullname = post_fullname
        self.post_number = post_number
        if self.post_fullname is None and self.post_number is None:
            raise ValueError("Either post_fullname or post_number must be set. Please set one of them.")

        self.team = os.environ['ESA_TEAM'] if "ESA_TEAM" in os.environ else esa_team
        if self.team is None:
            raise ValueError("ESA_TEAM is not set. Please set esa_team param or the environment variable ESA_TEAM.")

        self.client = piyo.Client(current_team=self.team)

    def stringify_element(self, element: Union[MdElement, str]) -> str:
        """Converts the given element to a string.

        Args:
            element (Union[MdElement, str]): The element to convert.

        Returns:
            str: The converted string.
        """
        if isinstance(element, MdImage):
            url = self.client.upload_file(element.src)
            element.src = url
        elif isinstance(element, MdLink):
            parsed_result = urlparse(element.url)
            if parsed_result.scheme == "":
                url = self.client.upload_file(element.url)
            elif parsed_result.scheme == "file":
                url = self.client.upload_file(parsed_result.path)
            element.url = url
        return str(element)

    def write(
        self,
        contents: Union[List[Union[str, MdElement]], MdElement],
        post_params: Dict[str, Any] = {},
        **payloads: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """post the given Markdown content to esa.io.

        Args:
            contents (Union[List[Union[str, MdElement]], MdElement]):
                The Markdown content to write to the file.
            post_params (Dict[str, Any], optional): Additional parameters for the post. see https://docs.esa.io/posts/102#POST%20/v1/teams/:team_name/posts. Defaults to {}.
            **payloads (Optional[Dict[str, Any]]): Additional parameters for piyo see https://github.com/argonism/piyo/blob/master/piyo/client.py#L112.
        """

        if not isinstance(contents, list):
            contents = [contents]

        markdown = ""
        for content in contents:
            content_md = self.stringify_element(content)
            markdown += content_md + "\n"

        if self.post_fullname:
            post_data = {"post": {"name": self.post_fullname, "body_md": markdown, **post_params}}
            return self.client.create_post(post_data, **payloads)
        elif self.post_number:
            update_data = {"post": {"body_md": markdown, **post_params}}
            return self.client.update_post(self.post_number, update_data, **payloads)
        else:
            raise ValueError("Either post_fullname or post_number must be set. Please set one of them.")
