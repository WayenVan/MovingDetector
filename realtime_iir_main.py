camera = webcam2rgb.Webcam2rgb()
#start the thread and stop it when we close the plot windows
camera.start(callback = callBack, cameraNumber=0)
print("camera samplerate: ", camera.cameraFs(), "Hz")