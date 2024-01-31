import numpy as np
import cv2

def get_uw_index(image):
    '''
    Calculates the underwater index
    (paper: 'Towards Real-Time Advancement of Underwater Visual Quality with GAN')
    '''
    # Convert the image from BGR to LAB
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    lab_image = lab_image.astype("float32")
    # Normalize the image
    lab_image = np.divide(lab_image, 255)    # Split the Lab image into its channels
    l_values, a_values, b_values = cv2.split(lab_image)
    # print(np.mean(l_values),np.min(a_values),np.min(b_values))
    d_a = np.abs(np.min(a_values)-np.max(a_values))
    d_b = np.abs(np.min(b_values)-np.max(b_values))
    d_o = np.sqrt(np.mean(a_values)**2 + np.mean(b_values)**2)
    a_l = np.mean(l_values) # average L channel
    UW_idx = np.sqrt(d_o)/(10*a_l*d_a*d_b)
    return UW_idx
