import traceback

import cv2
import nltk
import string
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from tensorflow.keras.preprocessing import image

from Enum_data import StatusCodes
from data_class.general import CustomException
from utils.common_utils import handle_exception




# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Initialize PorterStemmer
ps = PorterStemmer()



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



def prepare_image_horse_human_classifier(image_path):
    try:
        img = image.load_img(image_path, target_size=(300, 300))
        # Convert the image to an array
        img_array = image.img_to_array(img)
        # Reshape the image to add an extra dimension (since the model expects batches)
        img_array = np.expand_dims(img_array, axis=0)
        # Rescale the pixel values
        img_array /= 255.0

        # print("img_array", img_array)
        # input("check img_array")

        return img_array
    except Exception as e:
        custom_exception = CustomException(
            error_msg="error while predicting horse or human in image",
            data = {"image": image_path},
            exception=str(e),
            trace=traceback.format_exc()
        )
        exception_ans = handle_exception(custom_exception)
        return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value


def preprocess_email(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

