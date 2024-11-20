import azure.functions as func
import logging
from src.main import generate_description

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="generate_description_http_trigger")
def generate_description_http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    category = req.params.get('category')
    if not result:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. But category is missed.",
             status_code=400
        )        
    
    keyWords = req.params.get('key_words')
    keyWordsArray = keyWords.split(',') if keyWords else []

    result = generate_description(category, keyWordsArray)

    if result:
        return func.HttpResponse(f"{result}.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. But something goes wrong in ai part.",
             status_code=200
        )