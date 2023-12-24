
import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2 as cv
import matplotlib.pyplot as plt

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 96, kernel_size=(11, 11), stride=(4, 4))
        self.relu1 = nn.ReLU()
        self.norm1 = nn.LocalResponseNorm(5, alpha=9.999999747378752e-05, beta=0.75, k=1.0)
        self.pool1 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.conv2 = nn.Conv2d(96, 256, kernel_size=(5, 5), stride=(1, 1), padding=(2, 2), groups=2)
        self.relu2 = nn.ReLU()
        self.norm2 = nn.LocalResponseNorm(5, alpha=9.999999747378752e-05, beta=0.75, k=1.0)
        self.pool2 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.conv3 = nn.Conv2d(256, 384, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.relu3 = nn.ReLU()
        self.conv4 = nn.Conv2d(384, 384, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), groups=2)
        self.relu4 = nn.ReLU()
        self.conv5 = nn.Conv2d(384, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), groups=2)
        self.relu5 = nn.ReLU()
        self.pool5 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.fc6 = nn.Linear(9216, 4096)
        self.relu6 = nn.ReLU()
        self.drop6 = nn.Dropout(0.5)
        self.fc7 = nn.Linear(4096, 4096)
        self.relu7 = nn.ReLU()
        self.drop7 = nn.Dropout(0.5)
        self.fc8 = nn.Linear(4096, 7)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.norm1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.norm2(x)
        x = self.pool2(x)
        x = self.conv3(x)
        x = self.relu3(x)
        x = self.conv4(x)
        x = self.relu4(x)
        x = self.conv5(x)
        x = self.relu5(x)
        x = self.pool5(x)
        x = x.view(-1, 9216)
        x = self.fc6(x)
        x = self.relu6(x)
        x = self.drop6(x)
        x = self.fc7(x)
        x = self.relu7(x)
        x = self.drop7(x)
        x = self.fc8(x)
        x = self.softmax(x)
        return {"softmax": x}


def prep_image(image):
    # convert to gray scale
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    image = cv.resize(image, (256, 256))

    # convert to PyTorch Variable
    image = torch.Tensor(image).cuda()

    # reshape to (1, 3, 224, 224)
    image = image.view(1, 1, 256, 256)
    
    return image

model = Net()
model.load_state_dict(torch.load("./emotion.pt"))
model.cuda()
model.eval()
torch.set_grad_enabled(False)


# Load the labels
with open("./labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]
    
label_map = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}


#Now lets write a version to run the model on the frame of a webcam stream
#Start capturing the video stream from the default camera
def start_emotion_app(label_map):
    labels = [label_map[i] for i in range(len(label_map.keys()))]
    cap = cv.VideoCapture(0)

    while True:
        # Read a frame from the video stream
        ret, frame = cap.read()

        # Apply the transform to the frame
        input_tensor = prep_image(frame)
        
        # Pass the input tensor through the model
        output_dict = model(input_tensor)

        # Get the prediction
        _, prediction = torch.max(output_dict["softmax"], 1)
        
        # Make a bar chart with all the option predictions
        plt.bar(labels, output_dict["softmax"][0].cpu().detach().numpy())
        plt.pause(0.001)
        

        # Get the actual label
        label = label_map[int(prediction.item())]

        # Display the label on the frame
        cv.putText(frame, label, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv.imshow('frame', frame)

        # Exit if the 'q' key is pressed
        if cv.waitKey(1) & 0xFF == ord('q') or closed==True:
            break
        
        plt.clf()
        

    # Release the video capture object and close all windows
    cap.release()
    cv.destroyAllWindows()


def on_close(event):
    global closed   # to assign value to external variable which I need in `is_sorted
    
    closed = True

    print('Closing window')


closed = False
print("")

plt.xlabel("Emotion")
plt.ylabel("Probability")

plt.ion()

fig = plt.gcf()
fig.canvas.mpl_connect('close_event', on_close)

start_emotion_app(label_map)

input("Press Enter to exit")