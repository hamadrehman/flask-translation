from flask import Flask, abort, send_file, request
import os
from translate import translate_page
from io import BytesIO, StringIO
from waitress import serve
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


app = Flask(__name__)
BASE_DIR = os.path.join(os.getcwd(), "pages")


@app.route("/", defaults={"req_path": "index.html"})
@app.route("/<path:req_path>")
def dir_listing(req_path):
    try:
        lang = request.args.get("lang", "hi")
        tags = request.args.get("tags", None)
        if tags:
            tags = tags.split(',')
        else:
            tags = ["title", "h1", "h2", "a"]

        abs_path = os.path.join(BASE_DIR, req_path)
        file_path = os.path.join(BASE_DIR, req_path)
        translated_page = BytesIO()

        if not os.path.exists(abs_path) and not os.path.exists(file_path):
            logger.error(f"Path does not exist: {abs_path}")
            return abort(404)

        if os.path.isfile(abs_path) or os.path.isfile(file_path):
            if not abs_path.endswith((".htm", ".html")):
                return send_file(file_path)

            try:
                translated_text = translate_page(abs_path, lang, tags)
                translated_page.write(translated_text.encode())
                translated_page.seek(0)
                return send_file(translated_page, mimetype="text/html")
            except Exception as e:
                logger.error(f"Translation failed: {str(e)}")
                # Fallback to serving original file
                return send_file(file_path)
                
    except Exception as e:
        logger.error(f"Request handling failed: {str(e)}")
        return abort(500)


serve(app, host="0.0.0.0", port=80)
