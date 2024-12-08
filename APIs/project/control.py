import traceback

import joblib
import numpy as np
from fastapi import UploadFile
import tensorflow as tf

from Enum_data import StatusCodes
from utils.image_utils import ImageUtils
from data_class.general import CustomException
from utils.common_utils import handle_exception
from APIs.project.preprocess_ml_inputs import prepare_image_digit_classifier, prepare_titanic_data, prepare_image_horse_human_classifier, preprocess_email



async def predict_digit_in_image(image: UploadFile):
    try:
        image_operations = ImageUtils(image)
        ans, status_code = image_operations.save_image_locally()

        if status_code != StatusCodes.CREATED.value:
            print("image saving failed")
            print("ans", ans)

        print("the image path is", image_operations.image_path)
        # input("check image path")

        # Prediction
        digit_classifier_model = joblib.load("APIs/project/ml_models/digit_clf_knn.joblib")
        image_features = prepare_image_digit_classifier(image_operations.image_path)
        image_features = image_features.reshape(1, -1)
        prediction = digit_classifier_model.predict(image_features)
        # print("new output", digit_classifier_model.predict_proba(image_features))
        print("prediction", prediction)
        # print("dtype", type(prediction))
        # input("check prediction")

        return int(prediction[0]), StatusCodes.SUCCESS.value
    except Exception as e:
        custom_exception = CustomException(
            error_msg="error while predicting digit in image",
            data = {"image": image.filename},
            exception=str(e),
            trace=traceback.format_exc()
        )
        exception_ans = handle_exception(custom_exception)
        return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value
    finally:
        image_operations.delete_local_saved_image()


async def predict_titanic_survival(data):
    try:
        prepared_data = prepare_titanic_data(data)
        titanic_survival_model = joblib.load("APIs/project/ml_models/titanic_forest_reg.joblib")
        prediction = titanic_survival_model.predict(prepared_data)
        print("prediction", prediction)

        return int(np.round(prediction[0], 0)), StatusCodes.SUCCESS.value
    except Exception as e:
        custom_exception = CustomException(
            error_msg="error while predicting titanic survival",
            data = data,
            exception=str(e),
            trace=traceback.format_exc()
        )
        exception_ans = handle_exception(custom_exception)
        return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value


async def predict_horse_human_classifier(image: UploadFile):
    try:
        image_operations = ImageUtils(image)
        ans, status_code = image_operations.save_image_locally()

        if status_code != StatusCodes.CREATED.value:
            print("image saving failed")
            print("ans", ans)

        print("the image path is", image_operations.image_path)
        # input("check image path")

        horse_human_classifier_model = tf.keras.models.load_model('APIs/project/ml_models/horse_human_classifier.keras')
        preprocessed_image = prepare_image_horse_human_classifier(image_operations.image_path)

        # Use the loaded model to predict the class (0 for horse, 1 for human)
        prediction = horse_human_classifier_model.predict(preprocessed_image)
        print("prediction", prediction)
        output = "Horse" if prediction[0][0] < 0.5 else "Human"
        # input("check prediction")

        return output, StatusCodes.SUCCESS.value
    except Exception as e:
        custom_exception = CustomException(
            error_msg="error while predicting horse human classifier",
            data = {"image": image.filename},
            exception=str(e),
            trace=traceback.format_exc()
        )
        exception_ans = handle_exception(custom_exception)
        return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value
    finally:
        image_operations.delete_local_saved_image()



def predict_spam(email_body):
    try:
        # Load the saved TF-IDF vectorizer and voting classifier model
        tfidf = joblib.load('APIs/project/ml_models/vectorizer.joblib')
        voting_classifier = joblib.load('APIs/project/ml_models/spam_email_voting.joblib')
        # input("models loaded")

        # Preprocess the input email
        preprocessed_email = preprocess_email(email_body)
        print("preprocessed_email", preprocessed_email)
        # input("check preprocessed_email")

        # Transform the preprocessed email using the TF-IDF vectorizer
        email_vector = tfidf.transform([preprocessed_email]).toarray()
        print("email_vector", email_vector)
        # input("check email_vector")

        # Predict using the voting classifier model
        prediction = voting_classifier.predict(email_vector)
        print("prediction", prediction)
        # input("check prediction")

        # Return the prediction result
        return "Spam" if prediction[0] == 1 else "Not Spam", StatusCodes.SUCCESS.value
    except Exception as e:
        custom_exception = CustomException(
            error_msg="error while predicting spam in email",
            data={"email_body": email_body},
            exception=str(e),
            trace=traceback.format_exc()
        )
        exception_ans = handle_exception(custom_exception)
        return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value


