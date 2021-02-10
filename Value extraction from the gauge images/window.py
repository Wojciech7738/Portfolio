import cv2, numpy as np, copy
from skimage.metrics import structural_similarity as ssim
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
from pynput.mouse import Controller
import colorcorrect.algorithm as cca
import colorcorrect.util as ccu
import matplotlib.pyplot as plt
import os
import Train.test as te
import perspective_transform_module as pt


class Window:
    def __del__(self):
        self.webcam.release()

    def __init__(self, master, X, Y, image_name=None, image_name2=None, mat_plot_lib=False):
        # There are two variables which represents an images: img(2) and displayed_image(2).
        # Their types are "PIL.Image.Image" and "PIL.ImageTk.PhotoImage", respectively. This is
        # necessary, because any operation can be made on the first type of data and there are
        # some issues with converting the picture from "PhotoImage" to "Image".

        # Mouse positions for each picture
        self.mouse_positions1 = []
        self.mouse_positions2 = []
        # Default dimensions of the image
        self.dims = (558, 335)
        self.__master = master
        # Variable used for detecting whether perspective transform has been applied
        self.applied_pers_trans = False
        # Variable (...) the area of images' comparison has been set
        self.area_setting = False
        self.comp_area_changed = False
        # List for saving colours
        self.__prev_colours__ = []
        # Value used in "show_differences" function
        self.thresh_value = 0
        self.__new_image_dim__ = []
        self.__comp_image_area__ = []
        # Variable for choosing type of plots
        self.mat_plot_lib = mat_plot_lib
        # True, if images are identical (see "__show_subwindow" method for more details)
        self.identical = False
        # Necessary for avoiding issues with choosing the comparison area
        self.first_image = False
        self.image1_exists = False
        self.image2_exists = False
        # Pointer to webcam
        self.webcam = cv2.VideoCapture(0)

        self.image_name1 = image_name
        self.image_name2 = image_name2
        self.img = Image.new('RGB', self.dims)
        self.img2 = Image.new('RGB', self.dims)
        self.orig_img1 = Image.new('RGB', self.dims)
        self.orig_img2 = Image.new('RGB', self.dims)
        self.displayed_image = ImageTk.PhotoImage(self.img)
        self.displayed_image2 = ImageTk.PhotoImage(self.img2)

        # Frames
        top_frame1 = tk.Frame(self.__master)
        top_frame1.grid(row=0, column=0)
        top_frame2 = tk.Frame(self.__master)
        top_frame2.grid(row=0, column=1)
        center_frame1 = tk.Frame(self.__master)
        center_frame1.grid(row=1, column=0)
        center_frame2 = tk.Frame(self.__master)
        center_frame2.grid(row=1, column=1)
        bottom_frame1 = tk.Frame(self.__master)
        bottom_frame1.grid(row=2, column=0)
        bottom_frame2 = tk.Frame(self.__master)
        bottom_frame2.grid(row=2, column=1)
        hell_frame1 = tk.Frame(self.__master)
        hell_frame1.grid(row=3, column=0)
        hell_frame2 = tk.Frame(self.__master)
        hell_frame2.grid(row=3, column=1)
        hell_frame3 = tk.Frame(self.__master)
        hell_frame3.grid(row=4, column=0)
        hell_frame4 = tk.Frame(self.__master)
        hell_frame4.grid(row=4, column=1)

        # Buttons for searching pictures
        button_search_pics1 = tk.Button(top_frame1, text="Open...",
                                        command=lambda: self.open_file(self.__open_file1__, self.displayed_image,
                                                                       self.__imgLabel__))
        button_search_pics1.pack()
        button_search_pics2 = tk.Button(top_frame2, text="Open...",
                                        command=lambda: self.open_file(self.__open_file2__, self.displayed_image2,
                                                                       self.__imgLabel2__))
        button_search_pics2.pack(side=tk.LEFT)
        button_camera = tk.Button(top_frame2, text="Read image from camera", command=self.read_camera)
        button_camera.pack(side=tk.LEFT)

        # Widget with an image (in center frames)
        self.__imgLabel__ = tk.Canvas(center_frame1, width=X, height=Y)
        self.__imgLabel__.pack()
        self.__imgLabel__.bind("<Button-1>",
                           lambda k: self.__draw_rectangle(k, self.__imgLabel__, self.img, self.displayed_image,
                                                         self.mouse_positions1))
        # Make sure that that filename has been given. If yes - open an image
        if self.image_name1 is not None:
            self.img = Image.open(image_name)
            self.img = self.img.resize(self.dims)
            self.orig_img1 = self.img.copy()
            self.displayed_image = ImageTk.PhotoImage(self.img)
            self.image1_exists = True
        # Display an image
        self.__imgLabel__.create_image(20, 20, anchor=tk.NW, image=self.displayed_image)

        self.__imgLabel2__ = tk.Canvas(center_frame2, width=X, height=Y)
        self.__imgLabel2__.pack()
        self.__imgLabel2__.bind("<Button-1>",
                            lambda k: self.__draw_rectangle(k, self.__imgLabel2__, self.img2, self.displayed_image2,
                                                          self.mouse_positions2))
        # Open an image
        if self.image_name2 is not None:
            self.img2 = Image.open(image_name2)
            self.img2 = self.img2.resize(self.dims)
            self.orig_img2 = self.img2.copy()
            self.displayed_image2 = ImageTk.PhotoImage(self.img2)
            self.image2_exists = True
        # Display an image
        self.__imgLabel2__.create_image(20, 20, anchor=tk.NW, image=self.displayed_image2)

        # A buttons for changing the size of the image etc (in bottom frames)
        # Left side
        button = tk.Button(bottom_frame1, text="Change size",
                           command=lambda: self.change_size(self.__change_size1__, self.displayed_image, self.__imgLabel__,
                                                            self.mouse_positions1))
        button.pack(side=tk.LEFT)
        self.__user_choice1__ = 0

        # Color Balance algorithm
        # List of algorithms
        self.alg_names = {'Max White': 0, 'Grey World': 1, 'ACE': 2}
        buttonCB1 = tk.Button(bottom_frame1, text="Color Balance",
                              command=lambda: self.color_balance(self.__imgLabel__, self.__user_choice1__, self.img,
                                                                 self.displayed_image))
        buttonCB1.pack(side=tk.LEFT)
        # Display list of algorithms
        self.__var__ = tk.StringVar()
        self.__var__.set("Max White")
        CB_alg_button1 = tk.OptionMenu(bottom_frame1, self.__var__, *self.alg_names,
                                       command=lambda k: self.__display_algorithm1__(k, self.__var__))
        CB_alg_button1.pack(side=tk.LEFT)

        # Right side
        button2 = tk.Button(bottom_frame2, text="Change size",
                            command=lambda: self.change_size(self.__change_size2__, self.displayed_image2, self.__imgLabel2__,
                                                             self.mouse_positions2))
        button2.pack(side=tk.LEFT)
        self.__user_choice2__ = 0
        buttonCB = tk.Button(bottom_frame2, text="Color Balance",
                             command=lambda: self.color_balance(self.__imgLabel2__, self.__user_choice2__, self.img2,
                                                                self.displayed_image2))
        buttonCB.pack(side=tk.LEFT)

        # List of algorithms
        self.__var2__ = tk.StringVar()
        self.__var2__.set("Max White")
        CB_alg_button = tk.OptionMenu(bottom_frame2, self.__var2__, *self.alg_names,
                                      command=lambda k: self.__display_algorithm2__(k, self.__var2__))
        CB_alg_button.pack(side=tk.LEFT)

        # Perspective transform buttons
        self.__button_perspective1__ = tk.Button(bottom_frame1, text="Perspective transform",
                                             command=lambda: self.perspectiveTransform(self.img, self.displayed_image,
                                                                                       self.__imgLabel__))
        self.__button_perspective1__.pack(side=tk.LEFT)
        self.__button_perspective2__ = tk.Button(bottom_frame2, text="Perspective transform",
                                            command=lambda: self.perspectiveTransform(self.img2, self.displayed_image2,
                                                                                      self.__imgLabel2__))
        self.__button_perspective2__.pack(side=tk.LEFT)

        # Show differences between two images (in hell_frame)
        buttonSD = tk.Button(hell_frame1, text="Show differences", command=self.show_differences)
        buttonSD.pack(side=tk.LEFT)
        # Search for digits
        button_digi = tk.Button(hell_frame1, text="Find digits", command=lambda: self.detect_digits(image_name))
        button_digi.pack(side=tk.LEFT)

        # Buttons for restoring images and the field of comparison
        button_restore_img = tk.Button(hell_frame1, text="Restore images",
                                       command=lambda: self.restore_images(self.orig_img1, self.orig_img2))
        button_restore_img.pack()
        button_restore_area = tk.Button(hell_frame2, text="Reset comparison area", command=self.restore_area)
        button_restore_area.pack(side=tk.LEFT)

        # Button for mode choosing
        self.__text__ = tk.StringVar()
        self.__text__.set("Size changing")
        button_area = tk.Button(hell_frame2, textvariable=self.__text__, command=self.set_comp_area)
        button_area.pack(side=tk.LEFT)

    # Two variables with the same value have the same address. If I use c_types, the compare operation and
    # conversion from 'c_long' into 'int' will not be possible, so I don't know how to avoid the creation
    # of two functions instead of one.
    def __display_algorithm1__(self, value, var):
        # Displays algorithm name on the button
        self.__user_choice1__ = self.alg_names[value]
        var.set(value)

    def __display_algorithm2__(self, value, var):
        # Displays algorithm name on the button
        self.__user_choice2__ = self.alg_names[value]
        var.set(value)

    def __draw_rectangle(self, event, imgLabel, image, displayed_image, mouse_positions):
        # The coordinates of the "imgLabel" widget,
        # "19" has been given by trial and error method
        self.error = 19
        self.x = imgLabel.winfo_rootx() + self.error
        self.y = imgLabel.winfo_rooty() + self.error
        mouse = Controller()

        if self.area_setting and image == self.img:
            self.first_image = True

        # The coordinates of upper-left and down-right edge of the rectangle are needed.
        # So, when there is more than 2 - the list is being cleared
        if len(mouse_positions) + 1 > 2:
            mouse_positions.clear()
        mouse_positions.append(mouse.position)
        # Convert an image into array
        img_with_rectangle = np.asarray(image.copy())

        # Draw selected points
        # If user chose to select the comparison area - set color to blue
        if self.area_setting:
            colour = (0, 0, 255)
        else:
            # set color to red otherwise
            colour = (255, 0, 0)
        self.__prev_colours__.append(colour)

        cv2.circle(img_with_rectangle, (int(mouse.position[0] - self.x), int(mouse.position[1] - self.y)), 5,
                   colour, -1)
        # Show an image with rectangle
        self.__paste_image__(Image.fromarray(img_with_rectangle), displayed_image, imgLabel)

        # If user selected two edges of rectangle and two last colors are the same
        if len(mouse_positions) == 2 and self.__prev_colours__[-1] == self.__prev_colours__[-2]:
            self.__prev_colours__.clear()
            # Draw a rectangle saving original image
            cv2.rectangle(img_with_rectangle,
                          (int(mouse_positions[0][0] - self.x), int(mouse_positions[0][1] - self.y)),
                          (int(mouse_positions[1][0] - self.x), int(mouse_positions[1][1] - self.y)), colour, 2)
            self.__paste_image__(Image.fromarray(img_with_rectangle), displayed_image, imgLabel)

            if not self.area_setting:
                # Calculate dimensions of potentially new image
                self.__new_image_dim__ = (mouse_positions[0][0] - self.x, mouse_positions[0][1] - self.y,
                                      mouse_positions[1][0] - self.x, mouse_positions[1][1] - self.y)
            else:
                # Or set image comparison area
                self.__comp_image_area__ = (mouse_positions[0][0], mouse_positions[0][1],
                                        mouse_positions[1][0], mouse_positions[1][1])
                # If user is choosing comparing area - also draw rectangle on second image
                self.__draw_second_rectangle__(image, mouse_positions, colour)

        elif len(mouse_positions) == 2 and self.__prev_colours__[-1] != self.__prev_colours__[-2]:
            # In this case delete the first element
            mouse_positions.pop(-2)

    def change_size(self, function, displayed_image, imgLabel, mouse_positions):
        if len(mouse_positions) == 2:
            # Crop an image
            img = function()
            # Show an image
            self.__paste_image__(img, displayed_image, imgLabel)
            mouse_positions.clear()
        else:
            tk.messagebox.showwarning("Warning", "The area has not been selected!")

    def __change_size1__(self):
        self.img = self.img.crop(self.__new_image_dim__)
        self.img = self.img.resize(self.dims)
        return self.img

    def __change_size2__(self):
        self.img2 = self.img2.crop(self.__new_image_dim__)
        self.img2 = self.img2.resize(self.dims)
        return self.img2

    def __paste_image__(self, img, disp_img, img_label):
        disp_img.paste(img)
        img_label.create_image(20, 20, anchor=tk.NW, image=disp_img)

    def color_balance(self, imgLabel, n_algorithm, image, displayed_image):
        # Check if images exists
        if not self.__images_exists():
            return
        # Choose algorithm and save original image
        orig_image = copy.deepcopy(image)
        if n_algorithm == 0:
            image.paste(ccu.to_pil(cca.max_white(ccu.from_pil(image))))
        elif n_algorithm == 1:
            image.paste(ccu.to_pil(cca.grey_world(ccu.from_pil(image))))
        elif n_algorithm == 2:
            image.paste(ccu.to_pil(cca.automatic_color_equalization(ccu.from_pil(image))))

        self.__paste_image__(image, displayed_image, imgLabel)
        answer = tk.messagebox.askyesno("Changes prompt", "Apply changes?")
        # If no, restore image
        if not answer:
            image.paste(orig_image.copy())
            self.__paste_image__(image, displayed_image, imgLabel)

    def detect_digits(self, filename):
        if not self.__images_exists():
            return
        if self.comp_area_changed and self.__comp_image_area__ is not None:
            x, y = self.__x_y_calc__(self.__comp_image_area__)
            # Image 2
            dims = (self.__comp_image_area__[0] - x, self.__comp_image_area__[1] - y, self.__comp_image_area__[2] - x,
                    self.__comp_image_area__[3] - y)
            img = np.copy(np.asarray(self.img2.crop(dims).resize(self.dims)))
        else:
            img = np.copy(np.asarray(self.img2))
        img = cv2.bilateralFilter(img, 9, 75, 75)
        img = self.__blurring__(img)
        te.Main(img, os.getcwd(), 1)
        # te.Main(filename)

    def perspectiveTransform(self, image, disp_img, imgLabel):
        if not self.__images_exists(1):
            return
        img = pt.showDialog(self.__master, image, self.dims)
        if img.any():
            self.applied_pers_trans ^= True
            image.paste(Image.fromarray(img))
            self.__paste_image__(image, disp_img, imgLabel)

    def __blurring__(self, img):
        img = cv2.GaussianBlur(img, (5, 5), 0)
        img = cv2.bilateralFilter(img, 9, 75, 75)
        img = cv2.blur(img, (5, 5))
        return img

    def show_differences(self):
        if not self.__images_exists():
            return
        # If user chose the area for comparing images
        if self.comp_area_changed and self.__comp_image_area__ is not None:
            x, y = self.__x_y_calc__(self.__comp_image_area__)
            # Image 1
            dims = (self.__comp_image_area__[0] - x, self.__comp_image_area__[1] - y, self.__comp_image_area__[2] - x,
                    self.__comp_image_area__[3] - y)
            img1 = np.copy(np.asarray(self.img.crop(dims).resize(self.dims)))
            # Image 2
            img2 = np.copy(np.asarray(self.img2.crop(dims).resize(self.dims)))
        else:
            img1 = np.copy(np.asarray(self.img))
            img2 = np.copy(np.asarray(self.img2))

        b_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        a_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # __blurring__
        img1 = self.__blurring__(img1)
        # For better results, when the perspective transform has been applied before
        if self.applied_pers_trans:
            img2 = cv2.bilateralFilter(img2, 9, 75, 75)
        img2 = self.__blurring__(img2)
        b_gray = self.__blurring__(b_gray)
        a_gray = self.__blurring__(a_gray)

        (score, diff) = ssim(b_gray, a_gray, full=True, win_size=121)

        # Call window with slider
        subwin = self.__show_subwindow(score)
        # Wait until this window is closed
        self.__master.wait_window(subwin)

        # Conversion of 'diff' image from [0,1] range to [0, 255]
        # this is necessary before using it by OpenCV
        diff = (diff * 255).astype("uint8")

        thresh = cv2.threshold(diff, self.thresh_value, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        mask = np.zeros(img1.shape, dtype='uint8')
        filled_after = img2.copy()

        # Draw green rectangles
        for c in contours:
            area = cv2.contourArea(c)
            if area > 40:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(img1, (x, y), (x + w, y + h), (36, 255, 12), 2)
                cv2.rectangle(img2, (x, y), (x + w, y + h), (36, 255, 12), 2)
                cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
                cv2.drawContours(filled_after, [c], 0, (0, 255, 0), -1)

        if not self.mat_plot_lib:
            cv2.imshow('Image 1', img1)
            cv2.imshow('Image 2', img2)
            cv2.imshow('diff', diff)
            cv2.imshow('mask', mask)
            cv2.imshow('filled after', filled_after)
            cv2.waitKey()
            cv2.destroyWindow('Image 1')
            cv2.destroyWindow('Image 2')
            cv2.destroyWindow('diff')
            cv2.destroyWindow('mask')
            cv2.destroyWindow('filled after')
        else:
            plt.subplot(2, 3, 1)
            plt.imshow(img1)
            plt.subplot(2, 3, 2)
            plt.imshow(img2)
            plt.subplot(2, 3, 3)
            plt.imshow(diff)
            plt.subplot(2, 3, 4)
            plt.imshow(mask)
            plt.subplot(2, 3, 5)
            plt.imshow(filled_after)
            plt.show()

    def open_file(self, function, displayed_image, imgLabel, repeat=False):
        filetypes = (("JPG", "*.jpg"), ("PNG", "*.png"), ("JPEG", "*.jpeg"), ("BMP", "*.bmp"))
        if repeat:
            filename = ''
            # If function is set to repeat itself
            while repeat:
                filename = filedialog.askopenfilename(
                    filetypes=filetypes)
                if filename != '':
                    break
        else:
            filename = filedialog.askopenfilename(
                filetypes=filetypes)
            if filename == '':
                return
        img = function(filename)
        self.__paste_image__(img, displayed_image, imgLabel)

    def __open_file1__(self, filename):
        self.img = Image.open(filename)
        self.img = self.img.resize(self.dims)
        self.orig_img1 = self.img.copy()
        self.image1_exists = True
        return self.img

    def __open_file2__(self, filename):
        self.img2 = Image.open(filename)
        self.img2 = self.img2.resize(self.dims)
        self.orig_img2 = self.img2.copy()
        self.image2_exists = True
        return self.img2

    def __show_subwindow(self, score):
        subwindow = tk.Toplevel(self.__master)
        subwindow.geometry(
            "+{}+{}".format(int(subwindow.winfo_screenwidth() / 2), int(subwindow.winfo_screenheight() / 2)))
        top_frame = tk.Frame(subwindow)
        top_frame.grid(row=0, column=0)
        bottom_frame = tk.Frame(subwindow)
        bottom_frame.grid(row=1, column=0)

        percent = round(score * 100.0, 2)
        self.identical = False
        # If ssim score is more than 90 - images are identical, if it's between 75 and 90 - are similar
        if np.ceil(percent) < 75:
            message = "not similar"
        elif np.ceil(percent) >= 75 and np.ceil(percent) <= 90:
            message = "similar"
        else:
            message = "identical"
            self.identical = True
        label = tk.Label(top_frame,
                         text=f"Images are {message}.\nSimilarity score: {percent}%\nIf multiple windows - press \"Q\" to close those windows.\n\tThreshold:")
        label.pack()
        slider = tk.Scale(top_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        slider.pack()

        string = tk.StringVar()
        string.set(self.__compare_plot__())
        button1 = tk.Button(bottom_frame, textvariable=string, command=lambda: self.set_plot_type(string))
        button1.pack(side=tk.LEFT)
        button2 = tk.Button(bottom_frame, text="Apply", command=lambda: self.__close_subwindow__(subwindow, slider))
        button2.pack(side=tk.LEFT)
        return subwindow

    def set_plot_type(self, text):
        self.mat_plot_lib ^= True  # xor
        text.set(self.__compare_plot__())

    def __compare_plot__(self):
        if self.mat_plot_lib:
            return "One window"
        else:
            return "Multiple windows"

    def __close_subwindow__(self, subwindow, slider):
        self.thresh_value = slider.get()
        subwindow.destroy()

    def set_comp_area(self):
        self.area_setting ^= True  # xor
        self.comp_area_changed = True
        if self.area_setting:
            self.__text__.set("Comparison area changing")
        else:
            self.__text__.set("Size changing")

    def __x_y_calc__(self, rectangle, reverse=False):
        # If this is list with two tuples - convert it into list
        if len(rectangle) == 2:
            rectangle = list(rectangle[0]) + list(rectangle[1])
        # Convert area into list. This is necessary for proper compare result
        area = [(rectangle[0], rectangle[1]), (rectangle[2], rectangle[3])]
        # If selected area comes from first image
        if (area == self.mouse_positions1 and not reverse) or (area != self.mouse_positions1 and reverse) \
                or (self.first_image and not reverse):
            x = self.__imgLabel__.winfo_rootx() + self.error
            y = self.__imgLabel__.winfo_rooty() + self.error
        else:
            x = self.__imgLabel2__.winfo_rootx() + self.error
            y = self.__imgLabel2__.winfo_rooty() + self.error
        return x, y

    def __draw_second_rectangle__(self, image, mouse_positions, colour):
        if image == self.img:
            # x = self.__imgLabel2__.winfo_rootx() + self.error
            # y = self.__imgLabel2__.winfo_rooty() + self.error

            second_img_with_rectangle = np.asarray(self.img2.copy())
            disp_img = self.displayed_image2
            imglabel = self.__imgLabel2__
        else:
            # x = self.__imgLabel__.winfo_rootx() + self.error
            # y = self.__imgLabel__.winfo_rooty() + self.error
            second_img_with_rectangle = np.asarray(self.img.copy())
            disp_img = self.displayed_image
            imglabel = self.__imgLabel__
        x, y = self.__x_y_calc__(self.__comp_image_area__, reverse=True)
        cv2.rectangle(second_img_with_rectangle,
                      (int(mouse_positions[0][0] - x), int(mouse_positions[0][1] - y)),
                      (int(mouse_positions[0][0] - x), int(mouse_positions[0][1] - y)),
                      colour, 2)
        if image == self.img:
            self.__paste_image__(Image.fromarray(second_img_with_rectangle), self.displayed_image2, self.__imgLabel2__)
        else:
            self.__paste_image__(Image.fromarray(second_img_with_rectangle), self.displayed_image, self.__imgLabel__)

    def restore_images(self, im1, im2):
        if not self.__images_exists(1):
            return
        self.__paste_image__(im1, self.displayed_image, self.__imgLabel__)
        self.__paste_image__(im2, self.displayed_image2, self.__imgLabel2__)

    def restore_area(self):
        self.comp_area_changed = False
        self.__comp_image_area__ = None
        self.restore_images(self.img, self.img2)

    def __images_exists(self, switcher=0):
        if self.image1_exists and self.image2_exists:
            return True
        if switcher != 0:
            tk.messagebox.showwarning("Warning", "You have to load both images.")
        else:
            tk.messagebox.showwarning("Warning", "Images haven't been loaded!")
        return False

    def read_camera(self):
        _, image = self.webcam.read()
        self.img2 = Image.fromarray(image)
        self.img2 = self.img2.resize(self.dims)
        self.orig_img2 = self.img2.copy()
        self.__paste_image__(self.img2, self.displayed_image2, self.__imgLabel2__)
        self.image2_exists = True
