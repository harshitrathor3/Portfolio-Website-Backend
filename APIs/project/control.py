import traceback

import joblib
from fastapi import UploadFile

from Enum_data import StatusCodes
from utils.image_utils import ImageUtils
from data_class.general import CustomException
from utils.common_utils import handle_exception
from APIs.project.preprocess_ml_inputs import prepare_image_digit_classifier



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

