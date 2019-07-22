"""
App entry point
"""
from app18 import create_app
# import matplotlib.pyplot as plt
# import seaborn as sea

app = create_app()

if __name__ == "__main__":
    app.run() #host='0.0.0.0', debug=True)
