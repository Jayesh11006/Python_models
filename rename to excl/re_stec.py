# import os
# from openpyxl import Workbook

# def store_filenames_in_excel(directory_path, excel_path):
#     # Excel workbook aur sheet banayein
#     workbook = Workbook()
#     sheet = workbook.active
#     sheet.title = 'File Names'

#     # Sheet ke header mein column ka naam likhein
#     sheet.append(['Original Name', 'New Name'])

#     # Directory ke andar sabhi files ke naam prapt karein
#     for filename in os.listdir(directory_path):
#         # Yaha par aap apne hisaab se new name generate kar sakte hain
#         new_name = filename  # Replace this line with your renaming logic
#         sheet.append([filename, new_name])

#     # Excel file save karein
#     workbook.save(excel_path)
#     print(f"Filenames have been stored in {excel_path}")

# # Is modal ko call karke aap apne directory ke files ke naam Excel file mein store kar sakte hain
# directory_path = 'E:\\DATA SCINE\\DS full video'  # Updated directory path
# excel_path = 'data scine.xlsx'  # Yaha par Excel file ka naam aur path dein
# store_filenames_in_excel(directory_path, excel_path)



import os
from openpyxl import Workbook

def store_filenames_in_excel(directory_path, excel_path):
    # Excel workbook aur sheet banayein p
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'File Names'

    # Sheet ke header mein column ka naam likhein
    sheet.append(['Folder Path', 'File Name', 'New Name'])

    # Directory ke andar sabhi files aur subdirectories ke naamrapt karein
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            folder_path = os.path.relpath(root, directory_path)
            full_path = os.path.join(root, filename)
            # Yaha par aap apne hisaab se new name generate kar sakte hain
            new_name = filename  # Replace this line with your renaming logic
            sheet.append([folder_path, filename, new_name])

    # Excel file save karein
    workbook.save(excel_path)
    print(f"Filenames have been stored in {excel_path}")

# Is modal ko call karke aap apne directory ke files ke naam Excel file mein store kar sakte hain
directory_path = 'F:\\react + video\\video'  # Updated directory path
excel_path = 'react.xlsx'  # Yaha par Excel file ka naam aur path dein
store_filenames_in_excel(directory_path, excel_path)
