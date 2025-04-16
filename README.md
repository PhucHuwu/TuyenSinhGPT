# TuyenSinhGPT

Dự án này xây dựng một hệ thống hỏi đáp thông tin tuyển sinh đại học tại Việt Nam. Hệ thống sử dụng tìm kiếm ngữ nghĩa dựa trên embedding và mô hình ngôn ngữ lớn để tạo ra câu trả lời bằng tiếng Việt.

## Cấu trúc Dự án
```
TUYENSINHGPT/
├── crawl/
│   ├── crawl.py                         # Chương trình cào dữ liệu tuyển sinh đại học
│   └── nganh_dao_tao.csv                # Dữ liệu về các ngành đào tạo
├── data/
│   ├── data_diem_chuan_cleaned.csv      # Dữ liệu điểm chuẩn đã được làm sạch
│   ├── data_diem_chuan_nam_2024.csv     # Điểm chuẩn đại học năm 2024
│   ├── data1.csv                        # Phần đầu của kết quả embedding 
│   ├── data2.csv                        # Phần sau của kết quả embedding
│   ├── train_data.json                  # Từ điển cặp câu hỏi-câu trả lời (hơn 200.000 mục)
│   └── vector_db.faiss                  # Cơ sở dữ liệu vector FAISS cho tìm kiếm ngữ nghĩa
├── .gitignore
├── README.md                            # README.md
├── requirements.txt                     # Các thư viện cần thiết
├── run.py                               # Script chính để chạy chức năng hỏi đáp
└── save_vector_db.py                    # Script để tạo và lưu cơ sở dữ liệu vector FAISS
```

## Tổng quan

Hệ thống cung cấp câu trả lời cho các câu hỏi về tuyển sinh đại học, các ngành học và yêu cầu đầu vào. Hệ thống sử dụng:

1. **Tìm kiếm ngữ nghĩa**: Sử dụng embeddings từ mô hình BAAI/bge-small-en-v1.5 để tìm thông tin liên quan
2. **Cơ sở dữ liệu vector FAISS**: Để tìm kiếm hiệu quả các vector văn bản tương đồng
3. **Tích hợp LLM**: Sử dụng API của Groq với Llama 3 70B để tạo câu trả lời phù hợp bằng tiếng Việt

## Cách hoạt động

1. Hệ thống nhận câu hỏi từ người dùng về tuyển sinh đại học bằng tiếng Việt
2. Chuyển đổi câu hỏi thành vector embedding sử dụng SentenceTransformer
3. Tìm kiếm trong cơ sở dữ liệu vector FAISS các nội dung tương đồng về mặt ngữ nghĩa
4. Trích xuất các ngữ cảnh liên quan nhất từ cơ sở kiến thức
5. Sử dụng Llama 3 thông qua Groq để tạo câu trả lời toàn diện bằng tiếng Việt dựa trên ngữ cảnh đã trích xuất

## Nguồn dữ liệu

Hệ thống được xây dựng trên dữ liệu tuyển sinh đại học Việt Nam:
- Điểm chuẩn đại học năm 2024
- Thông tin về các ngành đào tạo
- Dữ liệu tuyển sinh đã được làm sạch và xử lý

## Thiết lập và Sử dụng

### Yêu cầu
- Python 3.8 trở lên
- Các thư viện Python cần thiết (xem requirements.txt)
- API key của Groq

### Cài đặt
1. Clone repository này
2. Cài đặt các thư viện cần thiết:
   ```
   pip install -r requirements.txt
   ```
3. Thiết lập API key của Groq trong file run.py hoặc như một biến môi trường

### Chạy hệ thống
Để chạy hệ thống hỏi đáp:
```
python run.py
```

Chương trình sẽ xử lý câu hỏi mẫu: "Tôi thích lập trình thì nên học ngành gì của trường nào?"

### Tạo hoặc Cập nhật Cơ sở dữ liệu Vector
Nếu bạn có dữ liệu mới cần thêm:
```
python save_vector_db.py
```

## Phát triển

### Cào dữ liệu mới
Script `crawl.py` trong thư mục `crawl` được sử dụng để thu thập dữ liệu tuyển sinh đại học từ các nguồn liên quan.

### Quy trình Embedding
Quá trình embedding được chia thành hai phần do kích thước tập dữ liệu lớn (hơn 200.000 mục), tạo ra `data1.csv` và `data2.csv` sau đó được kết hợp để tạo chỉ mục FAISS.

## Ghi chú
- Hệ thống được thiết kế đặc biệt cho các truy vấn tiếng Việt về tuyển sinh đại học
- Tất cả các phản hồi được tạo ra bằng tiếng Việt như được quy định trong prompt hệ thống