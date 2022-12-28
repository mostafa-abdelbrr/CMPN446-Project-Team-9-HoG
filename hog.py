import math
import numpy as np


# Takes a grayscale image of size 128*64 and returns its 3780-long descriptor vector
def hog(img):
    # bins = 9, block size (size of cell) = 8x8
    nbins = 9
    block_size = 8
    # Initialize magnitudes and angles matrix
    m_img = img.copy()
    angles = np.zeros(img.shape)
    step = 180 / nbins  # width of bin
    # Initialize histogram matrix.
    hist = np.zeros((img.shape[0] // block_size, img.shape[1] // block_size, nbins))
    for row in range(0, img.shape[0] - 1):
        for col in range(0, img.shape[1] - 1):
            # Compute gradients, for border pixels just ignore the other parameter in the gradient equation.
            if col == 0:
                gx = img[row, col + 1]
            elif col + 1 == img.shape[1]:
                gx = - img[row, col - 1]
            else:
                gx = img[row, col + 1] - img[row, col - 1]
            if row == 0:
                gy = - img[row + 1, col]
            elif row + 1 == img.shape[0]:
                gy = img[row - 1, col]
            else:
                gy = img[row - 1, col] - img[row + 1, col]
            m_img[row, col] = math.sqrt(gx ** 2 + gy ** 2)
            angles[row, col] = (math.atan2(gy, gx) % math.pi) * 180 / math.pi
    hist_row = 0

    # For each 8x8 block, calculate the value of the histogram based
    # on how much each angle deviates from the center of the bin.
    for row_index in range(0, img.shape[0], block_size):
        hist_col = 0
        for col_index in range(0, img.shape[1], block_size):
            for window_row_index in range(block_size):
                for window_col_index in range(block_size):
                    angle = angles[window_row_index, window_col_index]
                    magnitude = m_img[row_index + window_row_index, col_index + window_col_index]
                    hist_vector_index = int(angle / step - 0.5) % nbins
                    cj1 = step * (hist_vector_index + 1 + 0.5)  # Next bin's center.
                    cj = step * (hist_vector_index + 0.5)  # Current bin's center
                    # How much current angle deviates from next bin's center.
                    distance_from_angle_percentage = (cj1 - angle) / step
                    hist[hist_row, hist_col, hist_vector_index] = distance_from_angle_percentage * magnitude
                    # How much current angle deviates from the current bin's center.
                    distance_from_angle_percentage = (angle - cj) / step
                    hist[hist_row, hist_col, (hist_vector_index + 1) % 9] = distance_from_angle_percentage * magnitude
            hist_col += 1
        hist_row += 1

    final_hist = []
    # For each 16x16 block, concatenate the histogram of the underlying 2x2 cell of 8x8 blocks.
    for row_index in range(0, hist.shape[0] - 1):
        for col_index in range(0, hist.shape[1] - 1):
            new_vector = np.array([list(hist[row_index, col_index]) + list(hist[row_index, col_index + 1]) +
                                   list(hist[row_index + 1, col_index]) + list(hist[row_index + 1, col_index + 1])])
            # Normalize the vector using L2 normalization, the vector's values are divided by the vector's magnitude
            new_vector_list = np.round((new_vector / math.sqrt(np.sum(new_vector ** 2) + 10 ** -5)), 10).tolist()[0]
            final_hist += new_vector_list
    return final_hist
