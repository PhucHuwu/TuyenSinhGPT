# TuyenSinhGPT
<p align="center">
  <a href="#tiếng-việt">🇻🇳 Tiếng Việt</a> •
  <a href="#english">🇺🇸 English</a>
</p>

---

<h2 id="tiếng-việt"></h2>

Dự án này xây dựng một hệ thống hỏi đáp thông tin tuyển sinh đại học tại Việt Nam. Hệ thống sử dụng tìm kiếm ngữ nghĩa dựa trên embedding và mô hình ngôn ngữ lớn để tạo ra câu trả lời bằng tiếng Việt.

## Cấu trúc Dự án
```
TUYENSINHGPT/
├── crawl/
│   ├── crawl.py                         # Chương trình cào dữ liệu tuyển sinh đại học
│   └── nganh_dao_tao.csv                # Dữ liệu về các ngành đào tạo
│
├── data/
│   ├── data_diem_chuan_cleaned.csv      # Dữ liệu điểm chuẩn đã được làm sạch
│   ├── data_diem_chuan_nam_2024.csv     # Điểm chuẩn đại học năm 2024
│   ├── data1.csv                        # Phần đầu của kết quả embedding 
│   ├── data2.csv                        # Phần sau của kết quả embedding
│   ├── dataset.json                     # Từ điển cặp câu hỏi-câu trả lời
│   └── vector_db.faiss                  # Cơ sở dữ liệu vector FAISS cho tìm kiếm ngữ nghĩa
│
├── README.md                            # README.md
├── build_vector_database.py             # Script để tạo cơ sở dữ liệu vector
├── requirements.txt                     # Các thư viện cần thiết
├── run.py                               # Script chính để chạy chức năng hỏi đáp
└── save_vector_database.py              # Script để lưu cơ sở dữ liệu vector FAISS
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
Chỉnh sửa hoặc thêm dữ liệu trong file `dataset.json` sau đó embedding bằng `build_vector_database.py` và lưu vector database bằng `save_vector_database.py`
```
python build_vector_database.py
```
```
python save_vector_database.py
```

## Ghi chú
- Hệ thống được thiết kế đặc biệt cho các truy vấn tiếng Việt về tuyển sinh đại học
- Hiện tại, dữ liệu chỉ bao gồm điểm chuẩn của các trường đại học năm 2024. Thông tin về điểm chuẩn các năm trước sẽ được cập nhật và bổ sung vào mô hình trong các phiên bản tiếp theo.
- Tất cả các phản hồi được tạo ra bằng tiếng Việt được quy định trong prompt hệ thống

---

<h2 id="english"></h2>

This project builds a question-answering system for university admissions information in Vietnam. The system uses semantic search based on embeddings and a large language model to generate answers in Vietnamese.

## Project Structure
```
TUYENSINHGPT/
├── crawl/
│   ├── crawl.py                         # Program to crawl university admissions data
│   └── nganh_dao_tao.csv                # Data about training majors
│
├── data/
│   ├── data_diem_chuan_cleaned.csv      # Cleaned benchmark score data
│   ├── data_diem_chuan_nam_2024.csv     # University benchmark scores for 2024
│   ├── data1.csv                        # First part of embedding results
│   ├── data2.csv                        # Second part of embedding results
│   ├── dataset.json                     # Dictionary of question-answer pairs
│   └── vector_db.faiss                  # FAISS vector database for semantic search
│
├── README.md                            # README.md
├── build_vector_database.py             # Script to create vector database
├── requirements.txt                     # Required libraries
├── run.py                               # Main script to run the QA function
└── save_vector_database.py              # Script to save FAISS vector database
```

## Overview
The system provides answers to questions about university admissions, study majors, and entry requirements. The system uses:
1. **Semantic Search**: Using embeddings from the BAAI/bge-small-en-v1.5 model to find relevant information
2. **FAISS Vector Database**: For efficient searching of similar text vectors
3. **LLM Integration**: Using Groq's API with Llama 3 70B to generate appropriate answers in Vietnamese

## How It Works
1. The system receives questions from users about university admissions in Vietnamese
2. Converts the question into vector embeddings using SentenceTransformer
3. Searches the FAISS vector database for semantically similar content
4. Extracts the most relevant contexts from the knowledge base
5. Uses Llama 3 through Groq to generate comprehensive answers in Vietnamese based on the extracted context

## Data Sources
The system is built on Vietnamese university admissions data:
- University benchmark scores for 2024
- Information about training majors
- Cleaned and processed admissions data

## Setup and Usage
### Requirements
- Python 3.8 or higher
- Required Python libraries (see requirements.txt)
- Groq API key

### Installation
1. Clone this repository
2. Install the necessary libraries:
   ```
   pip install -r requirements.txt
   ```
3. Set up the Groq API key in the run.py file or as an environment variable

### Running the System
To run the QA system:
```
python run.py
```
The program will process the sample question: "What major and which university should I choose if I like programming?"

### Creating or Updating the Vector Database
If you have new data to add:
Edit or add data in the `dataset.json` file, then embed using `build_vector_database.py` and save the vector database using `save_vector_database.py`
```
python build_vector_database.py
```
```
python save_vector_database.py
```

## Notes
- The system is specifically designed for Vietnamese queries about university admissions
- Currently, the data only includes benchmark scores for universities in 2024. Information about benchmark scores from previous years will be updated and added to the model in future versions
- All responses are generated in Vietnamese as specified in the system prompt
