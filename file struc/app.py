import os
import shutil

def create_folders(base_path, categories):
    for category in categories:
        path = os.path.join(base_path, category)
        if not os.path.exists(path):
            os.makedirs(path)

def categorize_and_move_files(base_path, categories):
    for file_name in os.listdir(base_path):
        file_path = os.path.join(base_path, file_name)
        if os.path.isfile(file_path):
            # Example logic: Categorize by file name keywords
            for category in categories:
                if category.lower() in file_name.lower():
                    shutil.move(file_path, os.path.join(base_path, category, file_name))
                    break

def main():
    base_path = "E:\\DATA SCINE\\DS full video"  # Adjust this to your folder path
    categories = ["Topic1", "Topic2", "Topic3"]  # Replace with your actual categories
    
    create_folders(base_path, categories)
    categorize_and_move_files(base_path, categories)

if __name__ == "__main__":
    main()
