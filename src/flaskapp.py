from flask import Flask
from pythonjsonlogger import jsonlogger
import logging
import moneyforward.money

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.DEBUG)
json_fmt = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s",
    json_ensure_ascii=False,
)
h.setFormatter(json_fmt)
logger.addHandler(h)

app = Flask("flaskapp")
@app.route("/", methods=["GET"])
def index_get():
    return "OK"


def main():
    ## Get Initial Browser setup
    logger.info("api setup start")
    logger.info("get driver")
    driver = driver.get_driver()

main()
