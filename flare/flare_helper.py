import numpy as np

def sort_images(images_array):
    images_array = sorted(images_array, key=np.mean)
    return __to_dict(images_array)


def __to_dict(images_array):
    return {
        'white_1x': images_array[1],
        'white_8x': images_array[2],
        'black_1x': images_array[0]
    }