try:
    from .app import main
except ImportError:
    from smart_notepad.app import main


if __name__ == "__main__":
    main()
