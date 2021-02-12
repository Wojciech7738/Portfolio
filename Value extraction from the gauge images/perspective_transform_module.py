import numpy as np
from pynput.mouse import Controller
import cv2
import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk


class TKWindow(object):
    def __init__(self, master, image, dims):
        self.dims = dims
        self.master = master
        self.img = image
        self.image = np.copy(np.asarray(self.img))
        self.disp_img = ImageTk.PhotoImage(self.img)
        # Variable for blocking clicking on image while showing a messagebox
        self.locked = False
        self.warped = None

        self.mouse_points = []
        self.imgLabel = tk.Canvas(self.master, width=self.dims[0]+100, height=self.dims[1]+100)
        self.imgLabel.pack()
        self.imgLabel.bind("<Button-1>", lambda k: self.draw(k))
        self.imgLabel.create_image(20, 20, anchor=tk.NW, image=self.disp_img)

    def draw(self, event):
        if not self.locked:
            self.x = self.imgLabel.winfo_rootx() + 19
            self.y = self.imgLabel.winfo_rooty() + 19
            mouse = Controller()

            if len(self.mouse_points) + 1 > 4:
                self.mouse_points.clear()
            self.mouse_points.append(mouse.position)
            image_with_points = np.asarray(self.img.copy())
            cv2.circle(image_with_points, (int(mouse.position[0] - self.x), int(mouse.position[1] - self.y)), 5, (0,255,0), -1)
            self.paste_image(Image.fromarray(image_with_points))

            if len(self.mouse_points) == 4:
                self.rectangle_coordinates = [(self.mouse_points[0][0] - self.x, self.mouse_points[0][1] - self.y),
                                              (self.mouse_points[1][0] - self.x, self.mouse_points[1][1] - self.y),
                                              (self.mouse_points[2][0] - self.x, self.mouse_points[2][1] - self.y),
                                              (self.mouse_points[3][0] - self.x, self.mouse_points[3][1] - self.y)]
                self.warped = self.four_point_transform(self.image, np.asarray(self.rectangle_coordinates, dtype="float32"))
                self.warped = cv2.resize(self.warped, self.dims)

                # Show dialog
                self.paste_image(Image.fromarray(self.warped.copy()))

                # Make the label ignoring mouse click
                self.locked = True
                apply = tk.messagebox.askyesno("Applied transform", "Apply changes?", parent=self.master)
                self.locked = False
                if not apply:
                    self.warped = self.image
                    self.paste_image(Image.fromarray(self.warped.copy()))
                self.master.destroy()
                self.master.quit()


    def paste_image(self, img):
        self.disp_img.paste(img)
        self.imgLabel.create_image(20, 20, anchor=tk.NW, image=self.disp_img)

    def four_point_transform(self, image, pts):
        # obtain a consistent order of the points and unpack them
        # individually
        rect = self.order_points(pts)
        (tl, tr, br, bl) = rect
        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")
        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        # return the warped image
        return warped

    def order_points(self, points):
        # initialize a list of coordinates that will be ordered
        # such that the first entry in the list is the top-left,
        # the second entry is the top-right, the third is the
        # bottom-right, and the fourth is the bottom-left
        rectangle = np.zeros((4, 2), dtype="float32")
        s = points.sum(axis=1)

        # the top-left point will have the smallest sum, whereas
        # the bottom-right point will have the largest sum
        rectangle[0] = points[np.argmin(s)]
        rectangle[2] = points[np.argmax(s)]

        # now, compute the difference between the points, the
        # top-right point will have the smallest difference,
        # whereas the bottom-left will have the largest difference
        diff = np.diff(points, axis=1)
        rectangle[1] = points[np.argmin(diff)]
        rectangle[3] = points[np.argmax(diff)]
        return rectangle

    def return_warped_image(self):
        return self.warped


def showDialog(root, image, dims):
    # filename = "Images/temp/zdj.jpg"

    second_root = tk.Toplevel(root)
    second_root.title("Perspective transform")
    subwindow = TKWindow(second_root, image, dims)
    second_root.mainloop()
    if subwindow.warped.any():
        return subwindow.return_warped_image()
    return None
