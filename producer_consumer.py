import cv2
import threading
import queue

# Create the queues
queue1 = queue.Queue()
queue2 = queue.Queue()

def extractFrames(fileName):
    # initialize frame count
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success,image = vidcap.read()

    while success:
        # add the frame to queue1
        queue1.put(image)

        success,image = vidcap.read()

        print(f'Reading frame {count} {success}')
        count += 1

    # indicate that we're done adding frames to the queue
    queue1.put(None)

def convertToGrayscale():
    # initialize frame count
    count = 0

    while True:
        # get the next frame from queue1
        frame = queue1.get()

        # if we got a None for a frame, then we're done
        if frame is None:
            break

        print(f'Converting frame {count}')

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # add the grayscale frame to queue2
        queue2.put(grayscaleFrame)

        count += 1

    # indicate that we're done adding grayscale frames to the queue
    queue2.put(None)

def displayFrames():
    # initialize frame count
    count = 0

    while True:
        # get the next grayscale frame from queue2
        grayscaleFrame = queue2.get()

        # if we got a None for a frame, then we're done
        if grayscaleFrame is None:
            break

        print(f'Displaying frame {count}')

        cv2.imshow('Video', grayscaleFrame)

        if cv2.waitKey(42) and 0xFF == ord('q'):
            break

        count += 1

    cv2.destroyAllWindows()

# start the producer and consumer threads
extractFramesThread = threading.Thread(target=extractFrames, args=('clip.mp4',))
convertToGrayscaleThread = threading.Thread(target=convertToGrayscale)
displayFramesThread = threading.Thread(target=displayFrames)

extractFramesThread.start()
convertToGrayscaleThread.start()
displayFramesThread.start()

extractFramesThread.join()
convertToGrayscaleThread.join()
displayFramesThread.join()