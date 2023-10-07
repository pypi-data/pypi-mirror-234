import tkinter as tk
from tkinter import filedialog

import cv2
import PySimpleGUI as sg


def get_file_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path


def apply_threshold(image, lower_threshold, upper_threshold):
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(image, lower_threshold, upper_threshold)
    threshold_image = cv2.bitwise_and(image, image, mask=mask)
    return threshold_image


def resize_image(image, height=480):
    aspect_ratio = image.shape[1] / image.shape[0]
    width = int(height * aspect_ratio)
    resized = cv2.resize(image, (width, height))
    return resized


def to_bytes(image):
    is_success, buf = cv2.imencode(".png", image)
    return buf.tobytes()


def select_threshold(image):
    processed_image = None
    original_image = resize_image(image)

    layout = [
        # [sg.Text("Select an image:"), sg.Button("Browse", key="-BROWSE-")],
        [sg.Image(data=to_bytes(original_image), key="-IMAGE-")],
        [
            sg.Text("Lower threshold:"),
            sg.Slider(
                (0, 255),
                key="-LOWER THRESHOLD-",
                orientation="h",
                size=(40, 15),
                default_value=100,
            ),
        ],
        [
            sg.Text("Upper threshold:"),
            sg.Slider(
                (0, 255),
                key="-UPPER THRESHOLD-",
                orientation="h",
                size=(40, 15),
                default_value=200,
            ),
        ],
        [sg.Button("Show Processed"), sg.Button("Show Original")],
        [sg.Button("Exit")],
    ]

    window = sg.Window("Threshold Application", layout, resizable=True)

    # image_path = None
    # original_image = None

    # window["-IMAGE-"].update(data=to_bytes(original_image))

    while True:
        event, values = window.read()

        # original_image = resize_image(image)
        # window["-IMAGE-"].update(data=to_bytes(original_image))

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        # elif event == "-BROWSE-":
        #     image_path = get_file_path()
        #     if image_path:
        #         image = cv2.imread(image_path)
        #         original_image = resize_image(image)
        #         window["-IMAGE-"].update(data=to_bytes(original_image))

        elif event == "Show Processed" and image.any():
            # image = cv2.imread(image_path)
            processed_image = apply_threshold(
                image,
                int(values["-LOWER THRESHOLD-"]),
                int(values["-UPPER THRESHOLD-"]),
            )
            processed_image = resize_image(processed_image)
            window["-IMAGE-"].update(data=to_bytes(processed_image))
        # elif event == "Save" and processed_image is not None:
        #     cv2.imwrite("processed.png", processed_image)
        #     sg.popup("Saved", "Processed image saved as processed.png")
        elif event == "Show Original" and original_image is not None:
            window["-IMAGE-"].update(data=to_bytes(original_image))

    window.close()
    return int(values["-LOWER THRESHOLD-"]), int(values["-UPPER THRESHOLD-"])


if __name__ == "__main__":
    image_path = get_file_path()
    image = cv2.imread(image_path)
    lowth, upth = select_threshold(image)
    print()
