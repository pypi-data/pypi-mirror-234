try:
    import colorama  # Replace with the name of the module you want to check
    print(f"{colorama.Fore.CYAN}Thank you for installing WOAHLIB{colorama.Fore.RESET}")
except ImportError:
    print("Thank you for installing WOAHLIB")