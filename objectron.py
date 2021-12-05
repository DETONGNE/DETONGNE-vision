import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_objectron = mp.solutions.objectron

# For static images:
IMAGE_FILES = []
with mp_objectron.Objectron(static_image_mode=True,
                            max_num_objects=5,
                            min_detection_confidence=0.1,
                            model_name='Cup') as objectron:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    # Convert the BGR image to RGB and process it with MediaPipe Objectron.
    results = objectron.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Draw box landmarks.
    if not results.detected_objects:
      print(f'No box landmarks detected on {file}')
      continue
    print(f'Box landmarks of {file}:')
    annotated_image = image.copy()
    for detected_object in results.detected_objects:
      mp_drawing.draw_landmarks(
          annotated_image, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
      mp_drawing.draw_axis(annotated_image, detected_object.rotation,
                           detected_object.translation)
      cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_objectron.Objectron(static_image_mode=False,
                            max_num_objects=5,
                            min_detection_confidence=0.1,
                            min_tracking_confidence=0.99,
                            model_name='Cup') as objectron:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)
    # ī�޶� �ػ�(�̹��� ũ��)
    h,w = image.shape[0], image.shape[1]
    results = objectron.process(image)

    depth=[0.9,0.8]

    # Draw the box landmarks on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.detected_objects:
        for detected_object in results.detected_objects:
            mp_drawing.draw_landmarks(
              image, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
            mp_drawing.draw_axis(image, detected_object.rotation,
                                 detected_object.translation)
            # x:w, y:h
            print("x:",(1-detected_object.landmarks_2d.landmark[0].x)*w)
            print("y:",detected_object.landmarks_2d.landmark[0].y*h)
            #############str�� ���̴� ������ �����########################
            str = "HERE~!!!!!!!"
            ############################################################

            cv2.putText(image, str, (int(detected_object.landmarks_2d.landmark[0].x*w),int(detected_object.landmarks_2d.landmark[0].y*h)), cv2.FONT_HERSHEY_SIMPLEX, depth[0], (0, 0, 255), 2)


    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('test', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
