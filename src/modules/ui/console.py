from colorama import Fore, Style
import time


def print_user(text):
    print(
        f"{Fore.WHITE}You:{Style.RESET_ALL} {text}"
    )


def print_assistant(text):
    print(
        f"{Fore.RED}assistant:{Style.RESET_ALL} {text}"
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