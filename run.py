import os
from skychain import sky_app

__author__ = "OneTesseractInMultiverse"
__version__ = "1.0.0"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8019))
    sky_app.run(host='0.0.0.0', port=port)