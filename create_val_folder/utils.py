import os


def get_label_and_image(directory):
    subdirectories = []
    images = []
    labels = []

    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            subdirectories.append(os.path.join(root, dir))
        for file in files:
            if file.lower().endswith(('.jpg')):
                images.append(os.path.join(root, file))
            elif file.lower().endswith(('.txt')):
                labels.append(os.path.join(root, file))

    return subdirectories, images, labels

def get_different_elements(list1, list2):
    different_elements = list(set(list1) - set(list2)) + list(set(list2) - set(list1))
    return different_elements
