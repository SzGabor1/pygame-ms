import pygame
import game_api_client


class UserAuth:

    @staticmethod
    def register():
        username = input("Enter username: ")
        password = input("Enter password: ")
        response_info = game_api_client.register_user(username, password)
        print(response_info)

        if response_info['status_code'] == 200:
            print("User registered successfully")
            return True
        else:
            print("User registration failed")
            return False

    @staticmethod
    def login():
        username = "0"
        password = "0"

        try:
            response = game_api_client.login_user(username, password)
            print(response)
            return response
        except ValueError as e:
            print("Login error:", e)
            return False
