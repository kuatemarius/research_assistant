# app_test.py



from main_router.main_router import MainRouter
from start_server import start_server

main_router = MainRouter()
AGENT_APP = main_router.get_agent_app()

    
    
    
    
if __name__ == "__main__":
    try:
        start_server(AGENT_APP, main_router.auth_config)
    except Exception as error:
        raise error