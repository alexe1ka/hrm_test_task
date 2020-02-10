import json

import numpy as np
from aiohttp import web

import decoder

routes = web.RouteTableDef()

text_decoder = decoder.Decoder()


@routes.post('/make_bs')
async def make_beam_search(request):
    data_str = await request.json()
    data_dict = json.loads(data_str)
    probabilities_list = data_dict["probabilities"]
    alphabet = data_dict["alphabet"]
    probs_np = np.array(probabilities_list)
    # print(f"probs: {probabilities_list}")
    # print(f"alphabet: {alphabet}")
    decoded_result = text_decoder.beam_search(probs_np, alphabet)
    print(f"decoded result: {decoded_result}")
    return web.json_response({"result": decoded_result})


app = web.Application()
app.add_routes(routes)
web.run_app(app)
