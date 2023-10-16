import requests
import logging

def write(data:list[dict]):
    """
    data: list[dict], example:
          [{'PLC_TAG1': 2.2}, {'PLC_TAG2': 1.2}]
    """
    try:
      api='http://jp-connector/api/write'
      r = requests.post(api, json=data, timeout=5)
      if r.status_code != 200:
         logging.error(r.text)
         return r.text
      logging.info(f"write opc success: {data}")
      return ""
    except Exception as e:
      logging.error(str(e))
      return str(e)