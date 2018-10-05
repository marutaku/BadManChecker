## セットアップ
1. opencvのインストール
    * https://qiita.com/irs/items/4748d4bd04649d046861
2. 環境変数設定
    ```commandline
    echo "CV2_CASCADE_FILE_PATH=/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml" >> ~/.bash_profile
    ```
3. 依存パッケージインストール
    ```commandline
       pip install -r requirement.txt
    ```    
4. RUN
    ```commandline
    python detect_readltime.py
    ```
5. 終了
    * ctrl+Cか`q`で終了
