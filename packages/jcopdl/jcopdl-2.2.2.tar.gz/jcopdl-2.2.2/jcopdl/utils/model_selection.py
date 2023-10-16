import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split


def folder_stratified_split(source_path, target_path, test_size=0.3, random_state=42):
    source_dir = Path(source_path)
    target_dir = Path(target_path)

    for folder in source_dir.iterdir():
        if folder.is_dir():
            class_name = folder.name
            (target_dir / "train" / class_name).mkdir(parents=True, exist_ok=True)
            (target_dir / "test" / class_name).mkdir(parents=True, exist_ok=True)

            # Dataset Splitting
            files = list(folder.glob("*"))
            train_files, test_files = train_test_split(files, test_size=test_size, random_state=random_state)

            # Copy files
            for file in train_files:
                shutil.copy(file, target_dir / "train" / class_name / file.name)

            for file in test_files:
                shutil.copy(file, target_dir / "test" / class_name / file.name)
