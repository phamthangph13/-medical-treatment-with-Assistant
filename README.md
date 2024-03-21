Dự đoán Bệnh từ các Triệu chứng
Dự án này khám phá việc sử dụng các thuật toán máy học để dự đoán bệnh từ các triệu chứng.

Các Thuật toán Khám phá
Các thuật toán sau đã được khám phá trong mã nguồn:

Naive Bayes
Decision Tree
Random Forest
Gradient Boosting
Bộ dữ liệu
Nguồn-1
Bộ dữ liệu được sử dụng với kịch bản main.py được tải xuống từ đây:

bash
Copy code
https://www.kaggle.com/kaushil268/disease-prediction-using-machine-learning
Bộ dữ liệu này có tổng cộng 133 cột, trong đó có 132 cột là các triệu chứng mà bệnh nhân gặp phải và cột cuối cùng là dự đoán cho cùng một bệnh.

Nguồn-2
Bộ dữ liệu được sử dụng với Jupyter notebook được tải xuống từ đây:

bash
Copy code
https://impact.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html
Bộ dữ liệu này có 3 cột:

css
Copy code
Bệnh  | Số lần Xuất hiện của Bệnh | Triệu chứng
Bạn có thể sao chép toàn bộ bảng từ đây vào một bảng tính Excel hoặc lấy nó bằng cách sử dụng Beautifulsoup.

Cấu trúc Thư mục
css
Copy code
|_ dataset/
         |_ training_data.csv
         |_ test_data.csv

|_ saved_model/
         |_ [các mô hình được huấn luyện trước]

|_ main.py [ mã nguồn cho việc tải bộ dữ liệu từ Kaggle, huấn luyện và lưu mô hình ]

|_ notebook/
         |_ dataset/
                  |_ raw_data.xlsx [ Bộ dữ liệu Columbia cho notebook ]
         |_ Disease-Prediction-from-Symptoms-checkpoint.ipynb [ Notebook IPython cho việc tải bộ dữ liệu Columbia, huấn luyện mô hình và Suy luận ]
Sử dụng
Vui lòng đảm bảo cài đặt tất cả các phụ thuộc trước khi chạy bản demo, bằng cách sử dụng lệnh sau:

Copy code
pip install -r requirements.txt
Bản Demo Tương tác
Để chạy một bản demo tương tác hoặc chia sẻ nó với người khác, vui lòng chạy demo.py bằng Jupyter Notebook hoặc Jupyter Lab.

Copy code
jupyter notebook demo.ipynb
Bản Demo Độc lập
Để chạy suy luận trên tập dữ liệu kiểm tra hoặc trên đầu vào tùy chỉnh, bạn cũng có thể sử dụng tệp infr.py như sau:

Copy code
python infer.py
LƯU Ý: Dự án này chỉ dành cho mục đích demo. Đối với bất kỳ triệu chứng/bệnh nào, vui lòng tham khảo ý kiến của Bác sĩ.





