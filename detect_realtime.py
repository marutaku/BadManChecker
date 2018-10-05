from Extract_face import predict
import cv2
import os
from keras.preprocessing.image import img_to_array

CASCADE_FILE_PATH = os.environ['CV2_CASCADE_FILE_PATH']

image_size = 32

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cascade = cv2.CascadeClassifier(CASCADE_FILE_PATH)
    bad_man_color = (255, 0, 0)
    good_man_color = (0, 0, 255)
    try:
        while True:
            # 内蔵カメラから読み込んだキャプチャデータを取得
            ret, frame = cap.read()

            # モノクロで表示する
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 顔認識の実行
            facerect = cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))

            # 顔が見つかったらcv2.rectangleで顔に白枠を表示する
            if len(facerect) > 0:
                for rect in facerect:
                    x = rect[0]
                    y = rect[1]
                    width = rect[2]
                    height = rect[3]
                    dst = frame[y:y + height, x:x + width]
                    dst = cv2.resize(dst, (image_size, image_size))
                    in_data = img_to_array(dst)
                    pre = predict(in_data)
                    print(pre)
                    if pre[0][0] > pre[0][1]:
                        cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), good_man_color,
                                      thickness=2)
                    else:
                        cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), bad_man_color,
                                      thickness=2)
            # 表示
            cv2.imshow("frame", frame)

            # qキーを押すとループ終了
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        cap.release()
        cv2.destroyAllWindows()
        print('Finish Task')
        quit(0)
        # 内蔵カメラを終了
    cap.release()
    cv2.destroyAllWindows()
