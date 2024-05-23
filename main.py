from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_fetch
import ast
import output
import newRecommendation

app = FastAPI()

@app.post("/")
async def handle_userid(request: Request):
    # Retrieve JSON data from the request
    payload = await request.json()

    # Extract essential information from the payload
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_context = payload['queryResult']['outputContexts']

    
    # uid = ''
    if intent == 'last.recommendation.IDCheck':
        return last_rec(parameters)
    # elif intent == 'new.recommendation - more':
    #     uid = int(parameters['user_id'])
    elif intent == 'new.recommendation - more - next':
        return nrec_prompt(output_context[0]['parameters'],payload['queryResult']['queryText'])
    

def nrec_prompt(parameters: dict, prompt: str):
    prompt = prompt.split(" ", 1)[-1]
    user_id = int(parameters['user_id'])
    ix = newRecommendation.prompt_embedding(prompt, 3)[0]

    if ix:
        result = output.finalString(ix)
        fulfillmentText = f"The recommendations of current query {prompt} for User ID {user_id} are: {result}"
        if db_fetch.save_to_db(user_id, ix, prompt):
            pass
            # print("Result uploaded to DB successfully")
    else:
        fulfillmentText = f"No recommendation for User ID {user_id} found"
    return JSONResponse(content={
            "fulfillmentText": fulfillmentText
            })

    

def last_rec(parameters: dict):
    user_id = int(parameters['user_id'])

    ix = db_fetch.getLastRecommendation(user_id)
    ix = ast.literal_eval(ix)

    if ix:
        result = output.finalString(ix)
        fulfillmentText = f"The recommendations of last query for User ID {user_id} are: {result}"
    else:
        fulfillmentText = f"No records for User ID {user_id} found"
    return JSONResponse(content={
            "fulfillmentText": fulfillmentText
            })