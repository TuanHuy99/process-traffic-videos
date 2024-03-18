import os
import shutil

from utils import get_label_and_image, get_different_elements
from sklearn.model_selection import train_test_split
from pathlib import Path

# Đường dẫn của thư mục bạn muốn kiểm tra
folder_path = "1298-22-POB-H267_1"
save_dir = "val"
val_size = 0.2

# Gọi hàm để lấy danh sách thư mục con và video
subdirectories, images, labels = get_label_and_image(folder_path)

print(f'So anh: {len(images)}')
print(f'So label: {len(labels)}')

image_name = [os.path.basename(path)[:-4] for path in images]
label_name = [os.path.basename(path)[:-4] for path in labels]


different_elements = get_different_elements(image_name, label_name)
print("Cac phan tu khac nhau", different_elements)  # Kết quả: [1, 2, 3, 6, 7, 8]

# Xoa cac anh khong co label
print("Xoa cac anh khong co label:")
for img in images:
    if os.path.basename(img)[:-4] in different_elements:
        print(img)
        image_name.remove(img)

# Xoa cac label khong co anh
print("Xoa cac label khong co anh:")
for lb in labels:
    if os.path.basename(lb)[:-4] in different_elements:
        print(lb)
        labels.remove(lb)

images.sort()
labels.sort()

img_train, img_val , label_train, label_val = train_test_split(images, labels, test_size=val_size, random_state=42)

image_val_dir = f'{save_dir}/images/val'
label_val_dir = f'{save_dir}/labels/val'

if not Path(image_val_dir).exists():
    os.mkdir(f'{save_dir}/images')
    os.mkdir(image_val_dir)
if not Path(label_val_dir).exists():
    os.mkdir(f'{save_dir}/labels')
    os.mkdir(label_val_dir)

# Move val image
print("Move img val")
for img in img_val:
    print(img)
    shutil.move(img, image_val_dir)

# Move val label
print("Move label val")
for lb in label_val:
    print(lb)
    shutil.move(lb, label_val_dir)

print("So luong anh val")
print(len(os.listdir(image_val_dir)))
print("So luong label val")
print(len(os.listdir(label_val_dir)))