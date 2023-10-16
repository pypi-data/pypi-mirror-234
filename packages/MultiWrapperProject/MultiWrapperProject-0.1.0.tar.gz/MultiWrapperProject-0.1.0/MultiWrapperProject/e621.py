#import
import requests
import sys
from random import randrange
from typing import NoReturn

# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# File : e621.py
# Author : philou404
# Creation date : 05/10/2023 (DD/MM/AAAA)
# Description : Wrapper for e621.net on python
# -----------------------------------------------------------------------------
#
#     github : https://github.com/philou404
#
#
# -----------------------------------------------------------------------------


import requests


class E621():
    """
    ### MultiWrapperProject
    by : philou404 (github : https://github.com/philou404)

    a wide range of methods for e621 :
    - get 
    - getRandomPost
    - getRandomLink
    - dictOfAPost
    - download
    - downloadRandom
    - safeModeSwitch
    - explicitModeSwitch 


    version : 0.1.0
    """

    def __init__(self, username: str = "", api_key: str = "") -> None:
        """Constructorclass E621Project():


        Args:
            username (str, optional): username on e621. Defaults to "".
            api_key (str, optional): api key of account on e621. Defaults to "".
        """
        self.username = username
        self.API_KEY = api_key
        self.url_site = 'https://e621.net/posts.json'
        self.explicit_mode = False
        self.safe_mode = False

    def paramsGenerator(self, tags: str = "") -> dict[str]:
        """
        Function that generates the params for an HTTP request

        Args:
            tags (str, optional): tags for a search like in the e621 search bar. Defaults to "".

        Returns:
            dict[str]: dictionary for params
        """

        self.modeVerification()

        if self.username != "" and self.API_KEY != "":
            if self.safe_mode:
                return {'tags': f"{tags}" + "rating:s", "login": self.username, "api_key": self.API_KEY}

            elif self.explicit_mode:
                return {'tags': f"{tags}" + "-rating:s", "login": self.username, "api_key": self.API_KEY}
            else:
                return {"tags": f"{tags}"}
        else:
            if self.safe_mode:
                return {'tags': f"{tags}" + "rating:s"}

            elif self.explicit_mode:
                return {'tags': f"{tags}" + "-rating:s"}

            else:
                return {"tags": f"{tags}"}

    def headersGenerator(self):
        """
        Function that generates the headers for an HTTP request

        Args:
            tags (str, optional): tags for a search like in the e621 search bar. Defaults to "".

        Returns:
            dict[str]: dictionary for headers
        """
        if self.username != "":
            return {'User-Agent': f'E621Project/1.0 (by {self.username} on e621)'}
        else:
            return {'User-Agent': f'E621Project/1.0'}

    def get(self, tags: str = "") -> list[dict]:
        """
        Function which returns the last 320 posts from e621.net (if we do not modify the limit in the tags)

        Everything is in the format of a dictionary list

        More information on structure of one dictionary : use method `structureOfPost()`

        Args:   
            tags (str, optional): tags for a search like in the e621 search bar. Defaults to "".

        Returns:
            list[dict]: dictionary list, each dictionary is a post on the site
        """
        
        params = self.paramsGenerator(tags=tags)

        headers = self.headersGenerator()

        response = requests.get(
            url=self.url_site, params=params, headers=headers)

        if response.status_code == 200:
            return response.json()["posts"]

        else:
            dict_error = {
                "204": "No Content	Request was successful, nothing will be returned. Most often encountered when deleting a record",
                "403": "Forbidden	Access denied. May indicate that your request lacks a User-Agent header ",
                "404": "Not Found	Not found",
                "412": " Precondition failed	",
                "420": "Invalid Record	Record could not be saved",
                "421": "User Throttled	User is throttled, try again later",
                "422": "Locked	The resource is locked and cannot be modified",
                "423": "Already Exists	Resource already exists",
                "424": "Invalid Parameters	The given parameters were invalid",
                "500": "Internal Server Error	Some unknown error occurred on the server",
                "502": "Bad Gateway	A gateway server received an invalid response from the e621 servers",
                "503": "Service Unavailable	Server cannot currently handle the request or you have exceeded the request rate limit. Try again later or decrease your rate of requests",
                "520": "Unknown Error	Unexpected server response which violates protocol",
                "522": "Origin Connection Time-out	CloudFlare's attempt to connect to the e621 servers timed out",
                "524": "Origin Connection Time-out	A connection was established between CloudFlare and the e621 servers, but it timed out before an HTTP response was received",
                "525": "SSL Handshake Failed	The SSL handshake between CloudFlare and the e621 servers failed"}

            print(dict_error[f"{response.status_code}"])
            sys.exit(1)

    def structureOfPost(self) -> str:
        """ 
        Return the structure and explication of every key in dictionary

        Returns:
            str : text of structure

        """

        structure = """

id The ID number of the post.
created_at The time the post was created in the format of YYYY-MM-DDTHH:MM:SS.MS+00:00.
updated_at The time the post was last updated in the format of YYYY-MM-DDTHH:MM:SS.MS+00:00.

file (array group)
    width The width of the post.
    height The height of the post.
    ext The file’s extension.
    size The size of the file in bytes.
    md5 The md5 of the file.
    url The URL where the file is hosted on E6


preview (array group)
    width The width of the post preview.
    height The height of the post preview.
    url The URL where the preview file is hosted on E6
    
sample (array group)
    has If the post has a sample/thumbnail or not. (True/False)
    width The width of the post sample.
    height The height of the post sample.
    url The URL where the sample file is hosted on E6.

score (array group)
    up The number of times voted up.
    down A negative number representing the number of times voted down.
    total The total score (up + down).
    
tags (array group)
    general A JSON array of all the general tags on the post.
    species A JSON array of all the species tags on the post.
    character A JSON array of all the character tags on the post.
    artist A JSON array of all the artist tags on the post.
    invalid A JSON array of all the invalid tags on the post.
    lore A JSON array of all the lore tags on the post.
    meta A JSON array of all the meta tags on the post.

locked_tags A JSON array of tags that are locked on the post.
change_seq An ID that increases for every post alteration on E6 (explained below)

flags (array group)
    pending If the post is pending approval. (True/False)
    flagged If the post is flagged for deletion. (True/False)
    note_locked If the post has it’s notes locked. (True/False)
    status_locked If the post’s status has been locked. (True/False)
    rating_locked If the post’s rating has been locked. (True/False)
    deleted If the post has been deleted. (True/False)
    
rating The post’s rating. Either s, q or e.
fav_count How many people have favorited the post.
sources The source field of the post.
pools An array of Pool IDs that the post is a part of.

relationships (array group)
    parent_id The ID of the post’s parent, if it has one.
    has_children If the post has child posts (True/False)
    has_active_children
    children A list of child post IDs that are linked to the post, if it has any.

approver_id The ID of the user that approved the post, if available.
uploader_id The ID of the user that uploaded the post.
description The post’s description.
comment_count The count of comments on the post.
is_favorited If provided auth credentials, will return if the authenticated user has favorited the post or not.
"""
        return structure

    def getRandomPost(self, tags: str = "") -> dict:
        """
        Function that returns a post drawn randomly from the most recent posts based on the tags used

        Args:
            tags (str, optional): tags for a search like in the e621 search bar. Defaults to "".

        Returns:
            dict: a dictionary of a post 
        """
        list_dict = self.get(tags=tags)
        try:
            post_dict = list_dict[randrange(len(list_dict))]
        except Exception as e:

            raise Exception("0 post found")
        else:
            return post_dict

    def getRandomLink(self, tags: str = "") -> str:
        """
        Function that returns a link of a random image based on the tags

        Without tags, this is a random image from the last 320 posts on the site

        Args:
            tags (str, optional): tags for a search like in the e621 search bar. Defaults to "".

        Returns:
            str: link of pics
        """
        post_dict = self.getRandomPost(tags=tags)
        link_pic = post_dict["file"]["url"]
        return link_pic

    def dictOfAPost(self, id: int) -> dict:
        """
        Function that returns the dictionary of a post via its id

        Args:
            id (int): id of a post

        Raises:
            Exception: Post no found, problem with the id either invalid (error in number placed in argument) or the id does not exist on the site

        Returns:
            dict: dictionary of the post 
        """
        url = f"https://e621.net/posts/{id}.json"
        params = self.paramsGenerator()
        headers = self.headersGenerator()
        response = requests.get(url=url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()["posts"]

        elif response.status_code == 404:
            raise Exception("Post no found,  id is invalid or incorrect")

        else:
            dict_error = {
                "204": "No Content	Request was successful, nothing will be returned. Most often encountered when deleting a record",
                "403": "Forbidden	Access denied. May indicate that your request lacks a User-Agent header ",
                "404": "Not Found	Not found",
                "412": " Precondition failed	",
                "420": "Invalid Record	Record could not be saved",
                "421": "User Throttled	User is throttled, try again later",
                "422": "Locked	The resource is locked and cannot be modified",
                "423": "Already Exists	Resource already exists",
                "424": "Invalid Parameters	The given parameters were invalid",
                "500": "Internal Server Error	Some unknown error occurred on the server",
                "502": "Bad Gateway	A gateway server received an invalid response from the e621 servers",
                "503": "Service Unavailable	Server cannot currently handle the request or you have exceeded the request rate limit. Try again later or decrease your rate of requests",
                "520": "Unknown Error	Unexpected server response which violates protocol",
                "522": "Origin Connection Time-out	CloudFlare's attempt to connect to the e621 servers timed out",
                "524": "Origin Connection Time-out	A connection was established between CloudFlare and the e621 servers, but it timed out before an HTTP response was received",
                "525": "SSL Handshake Failed	The SSL handshake between CloudFlare and the e621 servers failed"}

            print(dict_error[f"{response.status_code}"])
            sys.exit(1)

    def download(self, url_file: str, file_name: str = "", save_path: str = "") -> NoReturn:
        """
        Function to download images or videos to e621 via link from e621 only

        Args:
            url_pic (str): Url picture
            file_name (str, optional): file name after download . Defaults to "".
            save_path (str, optional): path on hard disk to download, basic downloads in the file where the library is. Defaults to "".

        Raises:
            ValueError: The URL is not authorized for downloading.
                        Link to download must start with `https://static1.e621.net/data/`

        Returns:
            NoReturn: no return
        """

        link_base = "https://static1.e621.net/data/"

        try:

            if link_base not in url_file:
                raise ValueError("The URL is not authorized for downloading.")

            print("Start of download")
            response = requests.get(url=url_file)

            if response.status_code == 200:

                image_data = response.content

                if file_name != "":
                    save_path = save_path+file_name + \
                        "." + url_file.split(".")[-1]
                else:
                    save_path = save_path+url_file.split("/")[-1]

                with open(save_path, "wb") as file:
                    file.write(image_data)
                print(f"Image or video downloaded and saved to {save_path}")
            else:
                print(
                    f"Failed to download the image or video. Status code: {response.status_code}")

        except Exception as e:
            # You can log the error
            print(f"An error occurred: {str(e)}")

    def downloadRandom(self, tags: str = "", file_name: str = "", save_path: str = "") -> NoReturn:
        """
        Downloads a random image or video in the last 320 posts without modification via tags

        Args:
            tags (str, optional): tags for a search like in the e621 search bar.. Defaults to "".
            file_name (str, optional): file name after download . Defaults to "".
            save_path (str, optional): path on hard disk to download, basic downloads in the file where the library is. Defaults to "".

        Returns:
            NoReturn: no return
        """
        self.download(url_file=self.getRandomLink(
            tags=tags), file_name=file_name, save_path=save_path)

    def safeModeSwitch(self):
        """
        Function which allows you to have only post safe on e621

        If explicit mode and safe mode are activated at the same time, both modes will be deactivated giving access to all explicit, questionable and safe ranting content
        """
        if self.safe_mode:
            self.safe_mode = False
        else:
            self.safe_mode = True

    def explicitModeSwitch(self):
        """
        Function which allows you to have only explicit and questionable posts on e621

        If explicit mode and safe mode are activated at the same time, both modes will be deactivated giving access to all explicit, questionable and safe ranting content
        """
        if self.explicit_mode:
            self.explicit_mode = False
        else:
            self.explicit_mode = True

    def modeVerification(self):
        """If explicit mode and safe mode are activated at the same time, both modes will be deactivated giving access to all explicit, questionable and safe ranting content
        """
        if self.explicit_mode and self.safe_mode:
            self.explicitModeSwitch()
            self.safeModeSwitch()

    def __str__(self) -> str:
        pass
