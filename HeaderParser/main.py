from conflicts import save_conflicts_from_ue_source
from Parser import Parser
from Config import Config


if __name__ == '__main__':
    # save_conflicts_from_ue_source("C:\\Program Files\\Epic Games\\UE_4.25\\Engine\\Source")
    config = Config()

    P = Parser(config)
    print("=== Header parsing finished ===")
    P.generate_files()
    print("=== File generation finished ===\n")

    if config.FETCH_AFTER_RUN:
        import fetch_class
        fetch_class.main()

