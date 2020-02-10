import asyncio
import aiohttp
import json

import decoder
import utils


async def get_predictions(json_data, url):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data) as r:
            result = await r.json()
            print(result["result"])


if __name__ == '__main__':
    # client-server
    #обработки ошибок нет,сервер надо запустить первым
    #send only lists,without serialization
    decoder = decoder.Decoder()
    prob_list, alphabet_list = utils.parse_arguments()
    send_data_dict = {"probabilities": prob_list, "alphabet": alphabet_list}
    send_json = json.dumps(send_data_dict)
    # print(send_json)
    decoder_server_url = "http://127.0.0.1:8080/make_bs"
    asyncio.run(get_predictions(send_json, decoder_server_url))
