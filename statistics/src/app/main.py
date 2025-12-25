from src.settings.settings import Settings


def main() -> None:
    settings = Settings.load_from_yaml()

    print(settings)


if __name__ == '__main__':
    main()
