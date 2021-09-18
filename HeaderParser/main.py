from conflicts import save_conflicts_from_ue_source
from Parser import Parser
from Config import Config


if __name__ == '__main__':
    # save_conflicts_from_ue_source("C:\\Program Files\\Epic Games\\UE_4.25\\Engine\\Source")

    P = Parser(Config())
    print("="*50)
    P.generate_files()

