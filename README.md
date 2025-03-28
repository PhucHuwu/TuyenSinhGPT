﻿# TuyenSinhGPT

## Tổng quan
TuyenSinhGPT là một dự án trí tuệ nhân tạo tạo ra một chatbot tư vấn tuyển sinh đại học tại Việt Nam. Hệ thống được xây dựng dựa trên việc fine-tuning mô hình ngôn ngữ lớn GPT-neo-1.3B phiên bản tiếng Việt với dữ liệu về điểm chuẩn và thông tin tuyển sinh năm 2024 từ các trường đại học.

## Tính năng
- Cung cấp thông tin về điểm chuẩn năm 2024 của các ngành học tại các trường đại học Việt Nam.
- Trả lời các câu hỏi về tổ hợp môn thi, mã ngành, tên ngành, và các thông tin tuyển sinh khác.
- Tư vấn lựa chọn ngành học dựa trên sở thích và định hướng của người dùng.
- Giao diện hội thoại tự nhiên bằng tiếng Việt.

## Cấu trúc dự án
```
TuyenSinhGPT/
├── crawl.py                      # Script thu thập dữ liệu từ trang web tuyển sinh
├── train.ipynb                   # Notebook huấn luyện mô hình
├── data_diem_chuan_nam_2024.csv  # Dữ liệu điểm chuẩn gốc
├── data_diem_chuan_cleaned.csv   # Dữ liệu điểm chuẩn đã làm sạch
├── train_data.jsonl              # Dữ liệu huấn luyện dạng prompt-completion
├── fine_tuned_gpt2_model/        # Thư mục chứa model đã huấn luyện (checkpoints)
└── fine_tuned_gpt2_model_final/  # Thư mục chứa model cuối cùng
```

## Cài đặt
### Yêu cầu hệ thống
- Python 3.8+
- PyTorch
- CUDA (để huấn luyện và sinh văn bản nhanh hơn)
- Transformers
- PEFT (Parameter-Efficient Fine-Tuning)
- Pandas
- Selenium, undetected-chromedriver (cho việc crawl dữ liệu)

### Cài đặt các thư viện
```bash
pip install torch transformers datasets peft pandas selenium undetected-chromedriver
```

## Cách sử dụng
### Thu thập dữ liệu
```bash
python crawl.py
```
Sau khi chạy script, trình duyệt Chrome sẽ được mở. Nhập "ok" vào terminal để bắt đầu quá trình thu thập dữ liệu.

### Huấn luyện mô hình
Mở file `train.ipynb` trong Jupyter Notebook hoặc Google Colab và chạy từng cell. File này bao gồm:
- Đọc và làm sạch dữ liệu
- Chuẩn bị dữ liệu huấn luyện
- Fine-tune mô hình GPT-neo-1.3B-vietnamese-news
- Kiểm tra mô hình đã huấn luyện

### Sử dụng mô hình đã huấn luyện
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Tải mô hình và tokenizer
model_name = "VietAI/gpt-neo-1.3B-vietnamese-news"
peft_model_id = "./fine_tuned_gpt2_model_final"

tokenizer = AutoTokenizer.from_pretrained(peft_model_id)
model = AutoModelForCausalLM.from_pretrained(model_name)
model = PeftModel.from_pretrained(model, peft_model_id)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Hàm tạo câu trả lời
def generate_response(prompt, max_length=500):
    input_text = f"Người dùng: {prompt}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)

    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    if "Chatbot:" in response:
        response = response.split("Chatbot:")[1].strip()
    else:
        response = response.strip()
    return response

# Sử dụng mô hình
question = "Ngành Công nghệ thông tin tại Đại học Bách khoa Hà Nội lấy bao nhiêu điểm năm 2024?"
answer = generate_response(question)
print(answer)
```

## Dữ liệu
Dự án sử dụng dữ liệu điểm chuẩn năm 2024 từ các trường đại học Việt Nam, bao gồm:
- Nhóm ngành
- Tên ngành
- Trường đào tạo
- Mã ngành
- Tên ngành chi tiết
- Tổ hợp môn xét tuyển
- Điểm chuẩn năm 2024
- Ghi chú (nếu có)

## Fine-tuning
Mô hình được fine-tune bằng phương pháp LoRA (Low-Rank Adaptation) với các tham số:
- `r=8`
- `lora_alpha=16`
- `lora_dropout=0.05`
- `target modules: "c_attn", "c_proj", "c_fc"`

## Liên hệ
Nếu có bất kỳ câu hỏi hoặc đóng góp, vui lòng tạo issue trong repository này.
