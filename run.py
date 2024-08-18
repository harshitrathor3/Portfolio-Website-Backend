import uvicorn
from fastapi import FastAPI
from APIs.home.view import home_router
from APIs.project.view import project_router

# from utils.common_utils import handle_exception
# from data_class.general import CustomException




app = FastAPI(title="Portfolio Backend")


app.include_router(home_router)
app.include_router(project_router)



if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
    # custom_exception = CustomException(
    #     error_msg = "my error msg",
    #     data = {"key", "value"},
    #     exception=str(ValueError),
    #     trace=traceback.print_exc()
    # )
    # # print(custom_exception)
    # ans = handle_exception(custom_exception)
    # print("output", ans)
    # print("type", type(ans))


