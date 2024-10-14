import cv2
# from matplotlib import pyplot as plt

import traceback
from Enum_data import StatusCodes
from data_class.general import CustomException
from utils.common_utils import handle_exception



def prepare_image_digit_classifier(image_path):
    try:
        image = cv2.imread(image_path)

        # Resize the image to the required size (e.g., 64x64) - adjust as needed
        image_resized = cv2.resize(image, (28, 28))

        # Convert to grayscale if needed
        image_resized = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
        image_resized = cv2.bitwise_not(image_resized)


        # Flatten the image into a 1D array if required
        image_flattened = image_resized.flatten()

        # def plot_digit(data):
        #     image = data.reshape(28, 28)
        #     plt.imshow(image, cmap=plt.cm.binary, interpolation="nearest")
        #     plt.axis('off')
        #     plt.show()

        # print("image_flattened", image_flattened)
        # plot_digit(image_flattened)

        return image_flattened
    except Exception as e:
        custom_exception = CustomException(
            error_msg="error while predicting digit in image",
            data = {"image": image_path},
            exception=str(e),
            trace=traceback.format_exc()
        )
        exception_ans = handle_exception(custom_exception)
        return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value


