import requests
from secrets import API_Key, API_TOKEN

BASE_URL = "https://api.trello.com"


def get_boards():
    """ get list of all boards to determine the ID for further functions """
    url = "https://api.trello.com/1/members/me/boards"

    querystring = {"fields":"name,url","key":API_TOKEN,"token":API_Key}
    payload = ""
    headers = {'cookie': 'dsc=da3e99eaef39e470170776c4e104cb4c0c2c72b2695678276eff16746ac5f6c9'}

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    print(response.text)
    name = response.text['name']
    id = response.text['id']
   


def get_lists_from_board(board_id):
    """
        Access board with ID board_id in the client instance
        and print all non-archived lists with their non-archived  
        cards 
    """

  



