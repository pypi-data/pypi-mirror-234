import os
import ultralytics
import yaml
from ultralytics import YOLO
from IPython import display
from importlib import resources
import io
HOME = os.getcwd()
print(HOME)

display.clear_output()

ultralytics.checks()
from IPython.display import display, Image
from dotenv import load_dotenv
load_dotenv()
from roboflow import Roboflow
#with open('../creds.yaml', 'r') as file:
 #   prime_service = yaml.safe_load(file)
# create a .env file to run from
api_key = os.getenv("ROBOFLOW_API_KEY")
# finds the roboflow dataset online and downloads the selected version of the set


rf = Roboflow(api_key=api_key)
#rf = Roboflow(api_key=prime_service['creds'])
project = rf.workspace("enviromental-robotics").project("gold-mine-detection")
dataset = project.version(8).download("yolov8")

# finds the information pertneatn to the dataset

loc = dataset.location + '\data.yaml'

# with resources.open_binary('src',dataset.location + '\data.yaml') as fp:
#     loc=fp.read()

print(dataset.location)
# creates a model based on the selected weights
model = YOLO('currentModel.pt')  # takes current model

# uncomment to train another version, you must update the current model if you do
# model.train(data=loc, epochs=13, imgsz=640, plots=True)

print("trained!")
# creates states of the model
#metrics = model.val(data=loc, save=False)

# metrics.box.map    # map50-95
# metrics.box.map50  # map50
# metrics.box.map75  # map75
# metrics.box.maps   # a list contains map50-95 of each category

print("printed metrics:")
#print(metrics)
#pics = ['testPic2.jpg', 'testPicture.jpg']

# model.predict(source='..\drone Photos jpg', save=True, conf=.45)
print("predicted")


# project.version(6).deploy(model_type="yolov8", model_path="runs/detect/train/")
# project.version(DATASET_VERSION).deploy(model_type=”yolov8”, model_path=f”{HOME}/runs/detect/train/”)
def one_image(imagePath):
    print(imagePath)
    return model.predict(source=imagePath, save=True, conf=.45)

#print(one_image('..\..\drone Photos jpg\DJI_0216.jpg'))