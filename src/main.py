import argparse
import yaml
from pathlib import Path
from logger import setup_logger
from tag_reader import MacTagReader
from dropbox_handler import DropboxHandler

def main():
    # 設定命令列參數
    parser = argparse.ArgumentParser(description='同步 Mac 檔案標籤到 Dropbox')
    parser.add_argument('--folder', required=True, help='要處理的資料夾路徑')
    args = parser.parse_args()
    
    # 設定日誌
    logger = setup_logger()
    
    # 讀取配置
    try:
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"無法讀取配置文件: {str(e)}")
        return
    
    # 初始化元件
    tag_reader = MacTagReader()
    dropbox_handler = DropboxHandler(config['dropbox_token'])
    
    # 處理資料夾中的檔案
    folder_path = Path('/Users/robbie/Dropbox'+args.folder)
    if not folder_path.exists():
        logger.error(f"資料夾不存在: {folder_path}")
        return
        
    for file_path in folder_path.rglob('*'):
        if file_path.is_file():
            logger.info(f"處理檔案: {file_path}")
            
            # 讀取 Mac 標籤
            raw_tags = tag_reader.get_file_tags(file_path)
            
            # 清理和解碼標籤
            cleaned_tags = []
            for tag in raw_tags:
                try:
                    cleaned_tags.append(tag)
                except Exception as e:
                    # 在錯誤訊息中也使用解碼後的標籤
                    decoded_tag = tag.encode('ascii').decode('unicode-escape')
                    logger.warning(f"無法解碼標籤 '{decoded_tag}': {str(e)}")
                    continue
            
            # 使用解碼後的中文標籤寫入日誌
            logger.info(f"檔案標籤: {cleaned_tags}")
            
            if not cleaned_tags:
                continue
            
            # 在 Dropbox 中尋找對應檔案
            # dropbox_path = dropbox_handler.find_file(args.folder)
            # if not dropbox_path:
            #     continue
                
            # 更新 Dropbox 檔案標籤
            dropbox_handler.update_file_tags(args.folder+'/'+file_path.name, cleaned_tags)

if __name__ == '__main__':
    main() 