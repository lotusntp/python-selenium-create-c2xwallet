import requests

class LINE:
    def __init__(self, token):
        self.url = 'https://notify-api.line.me/api/notify'
        self.LINE_HEADERS = {'Authorization': 'Bearer ' + token}
        self.session = requests.Session()
        
    def sendtext(self, msg):
        response = self.session.post(self.url,
                                     headers=self.LINE_HEADERS,
                                     params={"message": msg})
        return response.text

    def send_pictur(self,url_image):
            response = self.session.post(self.url,
                                     headers=self.LINE_HEADERS,
                                     params={"message": " "},files=url_image)
            return response.text