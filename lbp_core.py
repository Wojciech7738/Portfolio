import numpy as np
import threading

class LBP_core:
    def __local_binary_pattern__(self, image, square_side):
        self.lbp_image = np.zeros(image.shape, dtype=np.int)
        Hist = None
        self.histograms = []
        threads = []
        # 1: divide image into grid
        nrows = int(image.shape[0]/square_side)
        ncols = int(image.shape[1]/square_side)
        for r in range(nrows):
            for c in range(ncols):  # columns
                thread = threading.Thread(target=self.__single_window_descriptor__, args=(image, square_side, r, c))
                threads.append(thread)
                thread.start()
        for t in threads:
            t.join()

        for hist in self.histograms:
            # Concatenate histograms
            if type(Hist) != np.ndarray:
                Hist = hist
            else:
                Hist = np.concatenate((Hist, hist))
        return Hist, self.lbp_image

    def __single_window_descriptor__(self, image, square_side, r, c):
        for i in range(square_side):
            for j in range(square_side):
                binary_values = []
                current = image[square_side * r + i, square_side * c + j]
                nei_position = self.neighbour_positions(i, j)
                for position in nei_position:
                    # 2: compute LBP
                    if square_side * r + position[0] < 0 or \
                            square_side * c + position[1] < 0:
                        binary_values.append(0)
                    else:
                        if position[0] >= square_side or position[1] >= square_side:
                            if square_side * r + position[0] >= image.shape[0] or \
                                    square_side * c + position[1] >= image.shape[1]:
                                # if given point is beyond the image - write 0
                                binary_values.append(0)
                            else:
                                self.__cond_check__(image, square_side * r + position[0],
                                                    square_side * c + position[1], current,
                                                    binary_values)
                        else:
                            self.__cond_check__(image, square_side * r + position[0],
                                                square_side * c + position[1], current, binary_values)
                # convert into decimal
                value = int(bin(int(''.join(map(str, binary_values)), 2)), 2)
                self.lbp_image[square_side * r + i, square_side * c + j] = value
        # create histogram of single window
        hist, _ = np.histogram(self.lbp_image[square_side * r:square_side * (r + 1),
                               square_side * c:square_side * (c + 1)].ravel(), bins=np.arange(0, 256, 1))
        self.histograms.append(hist)

    def neighbour_positions(self, row, col):
        yield (row, col + 1)
        yield (row + 1, col + 1)
        yield (row + 1, col)
        yield (row + 1, col - 1)
        yield (row, col - 1)
        yield (row - 1, col - 1)
        yield (row - 1, col)
        yield (row - 1, col + 1)

    def __cond_check__(self, img, p1, p2, current, binary_values):
        if img[p1][p2] < current:
            binary_values.append(0)
        else:
            binary_values.append(1)
