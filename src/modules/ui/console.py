from colorama import Fore, Style
import time


def print_user(text):
    print(
        f"{Fore.BLUE}Вы:{Style.RESET_ALL} {text}"
    )


def print_assistant(text):
    print(
        f"{Fore.GREEN}Ассистент:{Style.RESET_ALL} {text}"
    )


def loading():

    symbols = [
        "⣷",
        "⣯",
        "⣟",
        "⡿"
    ]

    for i in range(10):
        print(
            f"\r{symbols[i%4]} thinking...",
            end=""
        )
        time.sleep(0.1)

    print()