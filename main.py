from ultralytics import YOLO
import os
import cv2

new_names = [ 'motor', 'bicycle', 'car', 'taxi', 'coach', 'bus', 'lgv', 'hgv', 'vhgv' ]

def find_center(xyxy):
    x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
    cx = (x2 + x1) / 2
    cy = (y2 + y1) / 2
    w = x2 - x1
    h = y2 - y1
    return int(cx), int(cy), w, h

def create_classes_file(label_dir):
    with open(f"{label_dir}/classes.txt", 'w') as f:
        for obj in new_names[:-1]:
            f.write(f"{obj}")
            f.write('\n')
        f.write(new_names[-1])

def get_video_files(directory):
    video_files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            # Kiểm tra phần mở rộng của tệp tin
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension in ['.mp4', '.avi', '.mkv', '.mov']:
                video_files.append(filename)
    return video_files

# all_sence = os.listdir('/media/thienlv/499e29ef-a7f9-47ef-972e-8ed5f45547e2/code/create_data_9class_SG/Val_dataset/videos/Nga_4')
video_folder_path = ''
save_preproccess_data_folder = ''

for sence in all_sence:
    path_video = f'{video_folder_path}/'
    save_dir = f'{save_preproccess_data_folder}'

    videos = get_video_files(path_video)
    print(videos)

    # limit: so luong anh cua moi thu muc
    limit = 999999
    num_file = 0

    save_path = f'{save_dir}/{str(int(num_file / limit) + 1)}'
    img_path = f'{save_path}/images'
    label_path = f'{save_path}/labels'

    print(save_path)
    print(img_path)
    print(label_path)

    os.mkdir(save_path)
    os.mkdir(img_path)
    os.mkdir(label_path)
    create_classes_file(label_path)

    model = YOLO("yolov8x.pt")
    # accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam

    for video in videos:
        print(path_video + video)
        # vid = cv2.VideoCapture(path_video + video)
        count = 0

        results = model(source=path_video + video,
                            stream=True,
                            device=1)


        for rs in results:
            print('num_file: ', num_file)
            if len(os.listdir(label_path)) == limit + 1:
                print('create dir')
                save_path = f'{save_dir}/{str(int(num_file / limit) + 1)}'
                img_path = f'{save_path}/images'
                label_path = f'{save_path}/labels'

                print(save_path)
                print(img_path)
                print(label_path)

                os.mkdir(save_path)
                os.mkdir(img_path)
                os.mkdir(label_path)
                create_classes_file(label_path)
            # print('ac: ', len(os.listdir(label_path)))

            if count % 15 == 0:
                print('count: ', count)
                ih, iw = rs.orig_shape
                # print('img: ', rs.visualize())
                #boxes = rs.boxes.numpy()
                boxes = rs.boxes.cpu().numpy()
                detection = []
                cls_in_img = []
                if boxes.shape[0]:
                    for box in boxes:
                        cls = int(box.cls[0])
                        #cls = list_vn.index(new_names[cls])
                        # print('class: ', cls)
                        x_b, y_b, w_b, h_b = find_center(box.xyxy[0])
                        x_cen = round(x_b / iw, 6)
                        y_cen = round(y_b / ih, 6)
                        box_w = round(w_b / iw, 6)
                        box_h = round(h_b / ih, 6)
                        # print(f'center: {x_b} {y_b}')
                        # car
                        if cls == 2:
                            continue
                        # motorbike
                        elif cls == 3:
                            cls = 0
                        # truck
                        elif cls == 7:
                            cls = 6
                        # bicycle
                        elif cls == 1:
                            continue
                        elif cls = 5:
                            cls = continue
                            cls_in_img.append(cls)
                        detection.append([cls, x_cen, y_cen, box_w, box_h])

                if len(cls_in_img):
                    name_file = f"{video.split('.')[0]}_{count}"
                    # save image
                    cv2.imwrite(f"{img_path}/{name_file}.jpg", rs.orig_img)
                    # save label
                    with open(f"{label_path}/{name_file}.txt", 'w') as f:
                        for line in detection:
                            f.write(f"{line[0]} {line[1]} {line[2]} {line[3]} {line[4]}")
                            f.write("\n")
                    num_file += 1

            count += 1
