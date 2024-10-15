import traceback

import cv2
import joblib
import numpy as np
import pandas as pd
# from matplotlib import pyplot as plt

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





def prepare_titanic_data(data):
    try:
        ordinal_encoder = joblib.load("APIs/project/ml_models/titanic_ordinal_encoder_embarked_col.joblib")
        sex = 1 if data['sex'].lower() == "male" else 0

        embarked_df = pd.DataFrame(
            [[data['embarked']]], columns=['Embarked']
        )
        print("embarked_df", embarked_df)

        embarked_encoded = ordinal_encoder.transform(embarked_df)[0][0]
        print("embarked_encoded", embarked_encoded)

        input_data = np.array(
            [[data['pclass'], sex, data['age'], data['sibsp'], data['parch'], embarked_encoded]]
        )
        print("input_data", input_data)
        return input_data
    except Exception as e:
        custom_exception = CustomException(
            error_msg="error while preparing titanic data",
            data = {"data": data},
            exception=str(e),
            trace=traceback.format_exc()
        )
        exception_ans = handle_exception(custom_exception)
        return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value
