import yaml
from joblib import dump, load
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
# Phương pháp Naive Bayes
from sklearn.naive_bayes import MultinomialNB
# Phương pháp Trees
from sklearn.tree import DecisionTreeClassifier
# Phương pháp Ensemble
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import seaborn as sn
import matplotlib.pyplot as plt


class DiseasePrediction:
    def __init__(self, model_name=None):
        try:
            with open('./config.yaml', 'r') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            print("Lỗi khi đọc tệp cấu hình...")
        self.verbose = self.config['verbose']
        self.train_features, self.train_labels, self.train_df = self._load_train_dataset()
        # Tải dữ liệu kiểm tra
        self.test_features, self.test_labels, self.test_df = self._load_test_dataset()
        # Tương quan tính năng trong Dữ liệu huấn luyện
        self._feature_correlation(data_frame=self.train_df, show_fig=False)
        # Định nghĩa Mô hình
        self.model_name = model_name
        # Đường dẫn Lưu Mô hình
        self.model_save_path = self.config['model_save_path']

    # Hàm Tải Bộ dữ liệu Huấn luyện
    def _load_train_dataset(self):
        df_train = pd.read_csv(self.config['dataset']['training_data_path'])
        cols = df_train.columns
        cols = cols[:-2]
        train_features = df_train[cols]
        train_labels = df_train['prognosis']

        # Kiểm tra tính hợp lệ của dữ liệu
        assert (len(train_features.iloc[0]) == 132)
        assert (len(train_labels) == train_features.shape[0])

        if self.verbose:
            print("Độ dài của Dữ liệu Huấn luyện: ", df_train.shape)
            print("Tính năng Huấn luyện: ", train_features.shape)
            print("Nhãn Huấn luyện: ", train_labels.shape)
        return train_features, train_labels, df_train

    # Hàm Tải Bộ dữ liệu Kiểm tra
    def _load_test_dataset(self):
        df_test = pd.read_csv(self.config['dataset']['test_data_path'])
        cols = df_test.columns
        cols = cols[:-1]
        test_features = df_test[cols]
        test_labels = df_test['prognosis']

        # Kiểm tra tính hợp lệ của dữ liệu
        assert (len(test_features.iloc[0]) == 132)
        assert (len(test_labels) == test_features.shape[0])

        if self.verbose:
            print("Độ dài của Dữ liệu Kiểm tra: ", df_test.shape)
            print("Tính năng Kiểm tra: ", test_features.shape)
            print("Nhãn Kiểm tra: ", test_labels.shape)
        return test_features, test_labels, df_test

    # Tính toán Tương quan Tính năng
    def _feature_correlation(self, data_frame=None, show_fig=False):
        # Lấy Tương quan Tính năng
        corr = data_frame.corr()
        sn.heatmap(corr, square=True, annot=False, cmap="YlGnBu")
        plt.title("Tương quan Tính năng")
        plt.tight_layout()
        if show_fig:
            plt.show()
        plt.savefig('feature_correlation.png')

    # Phân chia Tập dữ liệu Huấn luyện và Xác nhận
    def _train_val_split(self):
        X_train, X_val, y_train, y_val = train_test_split(self.train_features, self.train_labels,
                                                          test_size=self.config['dataset']['validation_size'],
                                                          random_state=self.config['random_state'])

        if self.verbose:
            print(
                "Số lượng Tính năng Huấn luyện: {0}\tSố lượng Nhãn Huấn luyện: {1}".format(len(X_train), len(y_train)))
            print("Số lượng Tính năng Xác nhận: {0}\tSố lượng Nhãn Xác nhận: {1}".format(len(X_val), len(y_val)))
        return X_train, y_train, X_val, y_val

    # Lựa chọn Mô hình
    def select_model(self):
        if self.model_name == 'mnb':
            self.clf = MultinomialNB()
        elif self.model_name == 'decision_tree':
            self.clf = DecisionTreeClassifier(criterion=self.config['model']['decision_tree']['criterion'])
        elif self.model_name == 'random_forest':
            self.clf = RandomForestClassifier(n_estimators=self.config['model']['random_forest']['n_estimators'])
        elif self.model_name == 'gradient_boost':
            self.clf = GradientBoostingClassifier(n_estimators=self.config['model']['gradient_boost']['n_estimators'],
                                                  criterion=self.config['model']['gradient_boost']['criterion'])
        return self.clf

    # Mô hình Học máy
    def train_model(self):
        # Lấy Dữ liệu
        X_train, y_train, X_val, y_val = self._train_val_split()
        classifier = self.select_model()
        # Huấn luyện Mô hình
        classifier = classifier.fit(X_train, y_train)
        # Đánh giá Mô hình đã Huấn luyện trên Bộ Xác nhận
        confidence = classifier.score(X_val, y_val)
        # Dự đoán Dữ liệu Xác nhận
        y_pred = classifier.predict(X_val)
        # Độ chính xác của Mô hình
        accuracy = accuracy_score(y_val, y_pred)
        # Ma trận nhầm lẫn của Mô hình
        conf_mat = confusion_matrix(y_val, y_pred)
        # Báo cáo phân loại của Mô hình
        clf_report = classification_report(y_val, y_pred)
        # Điểm Cross Validation của Mô hình
        score = cross_val_score(classifier, X_val, y_val, cv=3)

        if self.verbose:
            print('\nĐộ chính xác Huấn luyện: ', confidence)
            print('\nDự đoán Xác nhận: ', y_pred)
            print('\nĐộ chính xác Xác nhận: ', classification_report)