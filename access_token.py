from fyers_api import fyersModel
from fyers_api import accessToken
from selenium import webdriver
from time import sleep
import yaml

from webdriver_manager.chrome import ChromeDriverManager

def get_auth_code(session):

    url = session.generate_authcode()
    #driver = webdriver.Chrome(r"/Users/hardcorecoder/Documents/Python/Projects/ProjectAlpha/chromedriver")
    #driver = webdriver.Chrome()
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(url)

    while True:

        curr_url = driver.current_url

        if "auth_code" in curr_url:

            auth_code = curr_url.split("auth_code=")[1]
            auth_code = auth_code.split("&")[0]

            #print(auth_code)

            break

    return auth_code

def get_access_token(client):

    app_id       = client['client_app_id']
    secret_key   = client['secret_key']
    redirect_uri = client['redirect_uri']

    session=accessToken.SessionModel(client_id=app_id,
                                     secret_key=secret_key, 
                                     redirect_uri=redirect_uri, 
                                     response_type="code", 
                                     grant_type="authorization_code", )

    auth_code = get_auth_code(session=session)

    session.set_token(auth_code)

    response = session.generate_token()

    access_token = response['access_token']

    return access_token


def store_token(data):
    file = open("tokens.yml", "w")
    yaml.dump(data, file)
    file.close()

def connect_to_fyers(client):
    '''
    will call this function from controller class for each client
    '''

    app_id       = client['client_app_id']
    secret_key   = client['secret_key']
    redirect_uri = client['redirect_uri']

    session=accessToken.SessionModel(client_id=app_id,
                                     secret_key=secret_key, 
                                     redirect_uri=redirect_uri, 
                                     response_type="code", 
                                     grant_type="authorization_code", )

    auth_code = get_auth_code(session=session)

    #print(auth_code)
    
    session.set_token(auth_code)

    response = session.generate_token()

    access_token = response['access_token']

    #store_token(client['name'], access_token)

    return get_fyers_object(app_id, access_token)


def get_fyers_object(app_id, access_token):

    fyers = fyersModel.FyersModel(client_id=app_id, token=access_token)

    return fyers

if __name__ == "__main__":

    # client_info = {
    #     'name'          : 'Pranav',
    #     'client_id'     : 'DP00774',
    #     'client_app_id' : "FRBBB40RNP-100",
    #     'secret_key'    : "UJV3CJQKP1",
    #     'redirect_uri'  : "https://127.0.0.1:5000/login",
    #     'pin'           : '0996'
    # }

    # {
    #     'row_id'        : 1,
    #     'name'          : 'Nidhi',
    #     'client_id'     : 'XN01889',
    #     'client_app_id' : "WLY21ISAZS-100",
    #     'secret_key'    : "0E3PHIFXC0",
    #     'redirect_uri'  : "https://127.0.0.1:5000/login"
    # },
    
    client_list = [
        {
            'local_id'        : 3,  # for UI purpose
            'name'          : 'Deepak',
            'client_id'     : 'XD00053',
            'client_app_id' : "UI3GPCQ4NG-100",
            'secret_key'    : "DTD2HERVQL",
            'redirect_uri'  : "https://127.0.0.1:5000/login"
        },

        {
            'local_id'        : 2,
            'name'          : 'Pranav',
            'client_id'     : 'DP00774',
            'client_app_id' : "FRBBB40RNP-100",
            'secret_key'    : "UJV3CJQKP1",
            'redirect_uri'  : "https://127.0.0.1:5000/login"
        },
    ]

    data = {}

    for client in client_list:
        access_token = get_access_token(client)
        
        data[client['local_id']] = {
            "access_token" : access_token
        }

    store_token(data)
    