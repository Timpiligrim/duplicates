import os
from tqdm import tqdm
from PIL import Image
import imagehash
import pandas as pd

folder_path = 'images'

hash_dict = {}

image_files = []
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):  
            image_files.append(os.path.join(root, filename))

for image_path in tqdm(image_files, desc="Обработка изображений"):
    filename = os.path.basename(image_path)
    try:
        with Image.open(image_path) as image:
            image_hash = imagehash.phash(image)
            if image_hash in hash_dict:
                hash_dict[image_hash].append(image_path)
            else:
                hash_dict[image_hash] = [image_path]
    except Exception as e:
        print(f"Ошибка обработки файла {filename}: {e}")

duplicate_records = []

group_number = 0  # Счетчик для групп

for image_hash, image_paths in hash_dict.items():
    if len(image_paths) > 1:
        group_number += 1  # Увеличиваем номер группы только для дубликатов
        for file_path in image_paths:
            original_filename = os.path.basename(file_path)
            duplicate_records.append({
                'Название файла': original_filename,
                'Группа': group_number
            })

duplicates_df = pd.DataFrame(duplicate_records)

# Сохранение в Excel
try:
    duplicates_df.to_excel('duplicates_dataset.xlsx', index=False)
    print("Дубликаты успешно сохранены в 'duplicates_dataset.xlsx'.")
except Exception as e:
    print(f"Ошибка при сохранении файла Excel: {e}")