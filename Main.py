import cv2 as cv
import sys
import numpy as np
import streamlit as st

def main():

    uploaded_file = st.file_uploader("Choose a file")
    current = False

    if uploaded_file:
        color = st.color_picker("Pick a Color", '#000000').lstrip("#")

        threshold = st.number_input(
            "Enter Threshold Value (0-255)",
            value=None,
            placeholder="106"
        )  

        if st.button("Change Color") and threshold:
            current = st.image(changeColor(transparent(uploaded_file, int(threshold)), [int(color[:2], 16), int(color[2:4], 16), int(color[4:6], 16)]), "Changed Color")
        elif st.button("Transparent") and uploaded_file and threshold:
            current = st.image(transparent(uploaded_file, int(threshold)), caption="Transparent Image")
        elif uploaded_file:
            current = st.image(uploaded_file, caption='Uploaded Image')

def changeColor(img, rgb):

    r, g, b, a = cv.split(img)

    img = cv.merge([r+rgb[0], g+rgb[1], b+rgb[2], a])

    return img

def transparent(file, threshold):

    bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv.imdecode(bytes, 1)

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret,img = cv.threshold(img, threshold, 255, cv.THRESH_BINARY)

    img = cv.cvtColor(img, cv.COLOR_RGB2RGBA)

    r, g, b, a = cv.split(img)
    img = cv.merge([r, g, b, (a-r)])

    cv.imwrite("transparent.png", img)

    return img


if __name__ == "__main__":
    main()