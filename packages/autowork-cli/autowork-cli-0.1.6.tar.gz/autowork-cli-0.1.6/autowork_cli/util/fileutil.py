class FileUtil:

    @staticmethod
    def genFile(file_path: str, content: str):
        with open(file_path, 'w+', encoding='utf-8') as f:
            f.write(content)
