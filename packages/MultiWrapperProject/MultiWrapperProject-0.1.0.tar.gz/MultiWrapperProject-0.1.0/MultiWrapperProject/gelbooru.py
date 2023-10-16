import requests
from typing import NoReturn
from random import randrange


# -----------------------------------------------------------------------------
# File : gelbooru.py
# Author : philou404
# Creation date : 05/10/2023 (DD/MM/AAAA)
# Description : Wrapper for gelbooru.com on python
# -----------------------------------------------------------------------------
#
#     github : https://github.com/philou404
#
#
# -----------------------------------------------------------------------------



class Gelbooru():
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

    def __init__(self) -> None:
        """constructor of gelbooru class
        """
        self.url = "https://gelbooru.com/index.php"
        self.explicit_mode = False
        self.safe_mode = False

    def paramsGenerator(self, tags: str = "") -> dict[str]:
        """
        Function that generates the params for an HTTP request

        Args:
            tags (str, optional): tags for a search like in the gelbooru search bar. Defaults to "".

        Returns:
            dict[str]: dictionary for params
        """
        self.modeVerification()
        if self.safe_mode:
            return {'tags': f"{tags}" + "rating:general", "json": "1", "s": "post", "page": "dapi","q":"index"}

        elif self.explicit_mode:
            return {'tags': f"{tags}" + "-general:general", "json": "1", "s": "post", "page": "dapi","q":"index"}

        else:
            return  {"tags": f"{tags}", "json": "1", "s": "post", "page": "dapi","q":"index"}


    def headersGenerator(self) -> dict[str]:
        """
        Function that generates the headers for an HTTP request

        Args:
            tags (str, optional): tags for a search like in the gelbooru search bar. Defaults to "".

        Returns:
            dict[str]: dictionary for headers
        """
        return {'User-Agent': 'MultiWarpperProject/1.0'}

    def get(self, tags: str = "") -> list[dict]:

        params = self.paramsGenerator(tags=tags)
        headers = self.headersGenerator()

        response = requests.get(url=self.url, params=params, headers=headers)

        if response.status_code == 200:
            li = response.json()["post"]
            return li

        else:
            raise Exception(f"Error with requests : {response.status_code}")

    def structureOfPost(self) -> str :
        structure = '''
preview_url picture preview

sample_url picture url SD Quality

file_url picture url HD quality

directory

hash   hash of post name 

width  width of picture

height width of picture

id     id of post

image  name of picture or video file

change 

owner name account of publisher on site

parent_id parent id of the post

rating rating : safe , questionable or explicit

sample sample of post on site without show the original

sample_height height of the sample

sample_width  width of the sample

score score of upvote on the post

tags tags post

source link of where the picture comes from 

status post status

has_notes boolean 

comment_count number comment under a post

'''
        return structure
    
    def getRandomPost(self,tags : str = ""):
        """
        Function that returns a post drawn randomly from the most recent posts based on the tags used

        Args:
            tags (str, optional): tags for a search like in the gelbooru search bar. Defaults to "".

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


    def getRandomLink(self, tags : str = ""):
        """
        Function that returns a link of a random image based on the tags

        Without tags, this is a random image from the last 100 posts on the site

        Args:
            tags (str, optional): tags for a search like in the gelbooru search bar. Defaults to "".

        Returns:
            str: link of pics
        """
        post_dict = self.getRandomPost(tags=tags)
        link_pic = post_dict["file_url"]
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
        url = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&id={id}"
        params = self.paramsGenerator()
        headers = self.headersGenerator()
        response = requests.get(url=url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()["posts"]

        elif response.status_code == 404:
            raise Exception("Post no found,  id is invalid or incorrect")
        
        else :
            raise Exception(f"Error : {response.status_code}")
        
    def download(self, url_file: str, file_name: str = "", save_path: str = "") -> NoReturn:
        """
        Function to download images or videos to gelbooru via link from gelbooru only

        Args:
            url_pic (str): Url picture
            file_name (str, optional): file name after download . Defaults to "".
            save_path (str, optional): path on hard disk to download, basic downloads in the file where the library is. Defaults to "".

        Raises:
            ValueError: The URL is not authorized for downloading.
                        Link to download must start with `https://img3.gelbooru.com/`

        Returns:
            NoReturn: no return
        """

        link_base = "https://img3.gelbooru.com/"
        link_base2 = "https://video-cdn3.gelbooru.com/"

        try:

            if link_base not in url_file or link_base2 not in url_file:
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
        Downloads a random image or video in the last 100 posts without modification via tags

        Args:
            tags (str, optional): tags for a search like in the gelbooru search bar.. Defaults to "".
            file_name (str, optional): file name after download . Defaults to "".
            save_path (str, optional): path on hard disk to download, basic downloads in the file where the library is. Defaults to "".

        Returns:
            NoReturn: no return
        """
        self.download(url_file=self.getRandomLink(
            tags=tags), file_name=file_name, save_path=save_path)
        
    def safeModeSwitch(self):
        """
        Function which allows you to have only post safe on gelbooru

        If explicit mode and safe mode are activated at the same time, both modes will be deactivated giving access to all explicit, questionable and safe ranting content
        """
        if self.safe_mode:
            self.safe_mode = False
        else:
            self.safe_mode = True

    def explicitModeSwitch(self):
        """
        Function which allows you to have only explicit and questionable posts on gelbooru

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




