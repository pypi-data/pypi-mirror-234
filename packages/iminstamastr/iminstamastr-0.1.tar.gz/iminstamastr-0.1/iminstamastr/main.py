# instapy (module)
def get_image_url(username):
    import requests
    import webbrowser
    data = requests.get("https://www.instagram.com/" + username + "/?__a=1&__d=dis").json()
    webbrowser.open(data["graphql"]["user"]["profile_pic_url_hd"])
def get_bio(username):
    import requests
    import webbrowser
    data = requests.get("https://www.instagram.com/" + username + "/?__a=1&__d=dis").json()
    print(data["graphql"]["user"]["biography"])
def get_full_name(username):
    import requests
    import webbrowser
    data = requests.get("https://www.instagram.com/" + username + "/?__a=1&__d=dis").json()
    print(data["graphql"]["user"]["full_name"])
def get_verifiedbool(username):
    import requests
    import webbrowser
    data = requests.get("https://www.instagram.com/" + username + "/?__a=1&__d=dis").json()
    print(data["graphql"]["user"]["is_verified"])
def get_externalurl(username):
    import requests
    import webbrowser
    data = requests.get("https://www.instagram.com/" + username + "/?__a=1&__d=dis").json()
    print(data["graphql"]["user"]["external_url"])
def get_category(username):
    import requests
    import webbrowser
    data = requests.get("https://www.instagram.com/" + username + "/?__a=1&__d=dis").json()
    print(data["graphql"]["user"]["category_name"])
