# Gauge Reader (in development)

This application was created in purpose of testing automation process. It's task is to compare two images and read the value displayed by the gauges, with some additional features.

## The appearance of the application

![The main window.](https://user-images.githubusercontent.com/45498344/113289997-48bc3680-92f1-11eb-90a6-ad19e8f6b76b.jpg)

An application is divided into two sections. First of them (on top of the image) is used for reading images. The second one's purpose is the displaying images and changing their size. The third section is used for applaying the image transformations and the fourth one - for the main purpose of the application.
Each one of sections contains buttons, which represents various features:

![The main window with marked buttons.](https://user-images.githubusercontent.com/45498344/113290753-5de59500-92f2-11eb-8ba8-a00c662a473f.jpg)

1. Read the image into the field below (file formats: JPG, PNG, BMP);
2. Read the screenshot into the field below;
3. Change the size of the image into the marked one before;
4. Apply the color balance algorithm on the image;
5. Select the color balance algorithm;
6. Apply the perspective transform of the image;
7. Find the differences between images;
8. Read the value displayed by the gauges;
9. Restore the original images;
10. Set the comparison area (part of images used for comparing them) to default (the whole image);
11. Switch between two modes: selecting the size changing area of the image and marking the comparison area.

Buttons 1 and 3-6 have their counterparts on the right side.

## How to use

After launching the application the following window will be displayed:

![The appearance of application after running it.](https://user-images.githubusercontent.com/45498344/113292489-dfd6bd80-92f4-11eb-91ef-d442e9fdf995.png)

There is not possible to use any feature before reading two images. There is possible to read two images from directory or read the screenshot as a second one, using Buttons 1 and 2. 

Now you should apply the image processing. If any of images is disorted use Button 6 in order to execute the perspective transformation. The following window will be displayed:

![Perspective transform](https://user-images.githubusercontent.com/45498344/113293478-1b25bc00-92f6-11eb-80a0-7ff327497241.png)


