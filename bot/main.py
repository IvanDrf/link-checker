from app.config.config import Config


def main():
    cfg: Config = Config.new(Config.get_config_path_from_flag())


if __name__ == '__main__':
    main()
