import os
from pypdf import PdfReader

def load_and_split_pdf(file_path: str, chunk_size: int = 500, overlap: int = 50):
    """
    读取指定的 PDF 文件，提取文本并按照指定字符数进行切片（Chunking）。
    这是构建 RAG 知识库的第一步。
    """
    if not os.path.exists(file_path):
        print(f"[-] 错误：找不到文件 '{file_path}'，请确保同目录下有名为该名字的 PDF。")
        return []

    print(f"[+] 正在读取 PDF 文件: {file_path} ...")
    reader = PdfReader(file_path)
    
    # 1. 提取所有页面的文本
    full_text = ""
    for index, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_text += text + "\n"
            
    print(f"[+] 读取完成！总共提取了 {len(reader.pages)} 页，文本总字符数: {len(full_text)}")

    # 2. 对文本进行滑动窗口切片
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + chunk_size
        chunk = full_text[start:end]
        chunks.append(chunk)
        # 下一个切片保留一定的重叠部分（overlap），防止上下文断开
        start += (chunk_size - overlap)

    print(f"[+] 文本切片完成！总共切分出 {len(chunks)} 个文本块（Chunks）。")
    return chunks

if __name__ == "__main__":
    # 测试代码：在同目录下放一个名为 test.pdf 的文件，或者修改成你的 PDF 文件名
    pdf_filename = "test.pdf"
    
    # 运行切片函数
    text_chunks = load_and_split_pdf(pdf_filename, chunk_size=500, overlap=50)
    
    # 打印前 3 个切片的内容预览，验证效果
    for i, chunk in enumerate(text_chunks[:3]):
        print(f"\n--- [Chunk {i+1} 预览] ---")
        print(chunk[:200] + "..." if len(chunk) > 200 else chunk)