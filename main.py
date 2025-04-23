import os
from dotenv import load_dotenv
from interactions import process_plip_file


load_dotenv(override=True)

PATH_TO_REPORTS = os.getenv("PATH_TO_REPORTS")

def list_dir(dir):
    folders = [folder for folder in os.listdir(dir) if os.path.isdir(os.path.join(dir, folder))]
    # return [os.path.join(dir, folder) for folder in folders]
    return {folder:os.path.join(dir, folder) for folder in folders}


for key, value in list_dir(PATH_TO_REPORTS).items():
    print(f"{key}: {value}")
    report = os.path.join(value, "report.txt")
    structure, results = process_plip_file(report)
    print(f"Strutura: {structure}")
    for i in results:
        print(i)
    print("\n")