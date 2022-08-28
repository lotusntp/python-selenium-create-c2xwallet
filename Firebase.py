from pkgutil import get_data
import pyrebase
class FIREBASE:
    def __init__(self,config):
        self.firebase = pyrebase.initialize_app(config)
        self.storage = self.firebase.storage()
        self.auth = self.firebase.auth()
        
        

    def upload(self,path_on_cloud,path_on_local):
        self.storage.child(path_on_cloud).put(path_on_local)
   
    def create_user(self,email,password):
        self.new_user = self.auth.create_user_with_email_and_password(email,password)
        print(self.new_user)
        print(self.new_user['idToken'])
        self.verify_email(self.new_user['idToken'])

    def verify_email(self,idToken):
         result = self.auth.send_email_verification(idToken)
         print(result)

    def auth_sign_get_url(self,email,password,image):
        self.user = self.auth.sign_in_with_email_and_password(email,password)
        self.url = self.storage.child(image).get_url(self.user['idToken'])
        return self.url
