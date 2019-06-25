import face_recognition
import cv2
import numpy as np
from datetime import datetime
import time

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
global cnt 
global aux_
global old
global string_IN
cnt = 0
aux_ = 0
old = 0
string_IN = []

file = open("out.txt","w")
#file = open("FACE_OUT.txt","w")

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("wallis.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("obama.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

india_image = face_recognition.load_image_file("India_Eisley.jpg")
india_face_encoding = face_recognition.face_encodings(india_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    india_face_encoding
]
known_face_names = [
    "Diogenes",
    "Obama",
    "India Eisley"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

frame_IN = np.zeros((480,640,3),np.uint8)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    
    flag_detection = False
    time_detection_face_diogenes = 0
    #reference = 0
    #aux_ = 0

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    #small_frame = small_frame[0:480,0:640]
    #print(small_frame.shape) 120,160
    #small_frame = small_frame[0:120,0:75]
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Não identificado"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
            #cv2.putText(frame, "face_detected", (0,70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):

        flag_detection = True

        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        #cv2.putText(frame, "OOOO", (right, bottom), font, 1.0, (255, 255, 255), 1)
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        #cv2.putText(frame, "1", (10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1)
        if name == "Diogenes":
            try:
                if reference == 0:
                    reference = datetime.now()
                    reference_ct = time.time()
                if reference != 0: 
                    #aux_ = 0
                    time_detection_face_diogenes = time.time() - reference_ct
                    #cv2.putText(frame, "diogenes_detected", (0,70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1)
                    #print((datetime.now() - reference).microseconds)
                
                    #if time.time() - reference_ct > old:
                    #    aux_ = 0
                    #print(time.time() - reference_ct,aux_,old)
                    #print(time.time() - reference_ct)
                    if time.time() - reference_ct > 2:
                        #print(right)
                        if right < 310:
                            #print("a")
                            #if right < 310:
                            #print(bool(aux) ^ bool(aux_))
                            #old = time.time() - reference_ct
                            #aux_ = 1
                            #print((datetime.now() - reference).microseconds)
                            file.write("Diogenes - " + str(reference) + "\n")
                            string_IN.append("Diogenes - " + str(reference) + "\n")
                            cnt = cnt + 1 
            except:
                reference=0

    if flag_detection == False:
        reference = 0
        aux = 0
    
#    time_detection_face_diogenes = time.time() - reference_ct
#    if time_detection_face_diogenes == 2:
#        print("a")
#        file.write("Diogenes - " + str(reference) + "\n") 
     
        #cv2.putText(frame, "diogenes_detected", (0,70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(frame, "0", (0,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1)
    current_time = str(datetime.now())
    #print(frame.shape) 480, 640
    #name2 = "FACE_IN = " + str(datetime.datetime.now())
    
    print(string_IN)

    cv2.putText(frame, current_time, (0,20), font, 0.5, (255, 0, 0), 1)
    cv2.putText(frame, "Entry", (0,40), font, 0.5, (255, 0, 0), 1)
    cv2.putText(frame, "Exit", (340,40), font, 0.5, (255, 0, 0), 1)
    
    #frame_IN.fill(255)
    frame_IN[0:480,0:310] = frame[0:480,0:310]
    frame_IN[0:480,330:640] = frame[0:480,330:640]
    
    # Display the resulting image
    cv2.imshow('Video', frame_IN)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcamfont = cv2.FONT_HERSHEY_SIMPLEX

file.close()

lines_seen = set() # holds lines already seen
outfile = open("FACE_IN.txt", "w")
for line in open("out.txt", "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()

num_lines = 0
with open("FACE_IN.txt", 'r') as f:
    for line in f:
        num_lines += 1

file = open("FACE_NUMB.txt","w")
file.write("Diogenes - " + str(num_lines) + "\n")
file.close()
video_capture.release()
cv2.destroyAllWindows()