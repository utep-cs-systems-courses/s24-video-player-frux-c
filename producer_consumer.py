#!/usr/bin/env python3

# producer consumer problem using threading
import threading
import cv2
import os
import time

# globals
OUTPUT_DIR    = 'frames'
CLIP_FILE_NAME = 'clip.mp4'
BUFFER_SIZE   = 10
buffer = []
bufferLock = threading.Lock()
bufferFull = threading.Semaphore(0)
bufferEmpty = threading.Semaphore(BUFFER_SIZE)

# producer thread
def extractFrames(clipFileName):
    # initialize frame count
    count = 0

    # open the video clip
    vidcap = cv2.VideoCapture(clipFileName)

    # create the output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        print(f"Output directory {OUTPUT_DIR} didn't exist, creating")
        os.makedirs(OUTPUT_DIR)

    # read one frame
    success, image = vidcap.read()

    print(f'Reading frame {count} {success}')
    while success:
        # add the frame to the buffer
        bufferEmpty.acquire()
        bufferLock.acquire()
        buffer.append(image)
        bufferLock.release()
        bufferFull.release()

        success, image = vidcap.read()
        print(f'Reading frame {count}')
        count += 1

    bufferEmpty.acquire()
    bufferLock.acquire()
    buffer.append(None)
    bufferLock.release()
    bufferFull.release()


# consumer thread
def convertToGrayscale():
    # initialize frame count
    count = 0

    while True:
        bufferFull.acquire()
        bufferLock.acquire()
        if buffer[0] is None:
            bufferLock.release()
            break
        image = buffer.pop(0)
        bufferLock.release()
        bufferEmpty.release()

        print(f'Converting frame {count}')

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # generate output file name
        outFileName = f'{OUTPUT_DIR}/grayscale_{count:04d}.bmp'

        # write output file
        cv2.imwrite(outFileName, grayscaleFrame)

        count += 1

def displayFrames():
    # initialize frame count
    count = 0

    while True:
        bufferFull.acquire()
        bufferLock.acquire()
        if buffer[0] is None:
            bufferLock.release()
            break
        image = buffer.pop(0)
        bufferLock.release()
        bufferEmpty.release()

        print(f'Displaying frame {count}')

        cv2.imshow('Video', image)

        if cv2.waitKey(42) and 0xFF == ord('q'):
            break

        count += 1

        time.sleep(1/24)

    cv2.destroyAllWindows()

# start the producer and consumer threads
extractFramesThread = threading.Thread(target=extractFrames, args=(CLIP_FILE_NAME,))
convertToGrayscaleThread = threading.Thread(target=convertToGrayscale)
displayFramesThread = threading.Thread(target=displayFrames)

extractFramesThread.start()
convertToGrayscaleThread.start()
displayFramesThread.start()

extractFramesThread.join()
convertToGrayscaleThread.join()
displayFramesThread.join()


print('Done.')