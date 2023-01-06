import requests
from urllib.parse import urljoin


class MeowerAPI:
    base_uri = "https://api.meower.org/"

    def __init__(self, token, username):

        self.session = requests.session()
        self.session.headers.update({"token": token, "usename": username})

    def get_page(self, page=1, chatid="home"):
        if chatid == "home":
            return self.session.get(
                urljoin(self.base_uri, "/home?autoget&page={0}".format(page))
            ).json()
        else:
            return self.session.get(
                urljoin(
                    self.base_uri, "/posts/{0}?autoget&page={1}".format(chatid, page)
                )
            ).json()

    def get_user(self, username):
        return self.session.get(
            urljoin(self.base_uri, "/users/{0}".format(username))
        ).json()

    def get_user_posts(self, username, page=1):
        return self.session.get(
            urljoin(
                self.base_uri,
                "/users/{0}/posts?autoget&page={page}".format(username, page),
            )
        ).json()

    def statistics(self):
        return self.session.get(urljoin(self.base_uri, "statistics")).json()

    def status(self):
        return self.session.get(urljoin(self.base_uri, "/status")).json()
