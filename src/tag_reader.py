import subprocess
import logging
from pathlib import Path

class MacTagReader:
    def __init__(self):
        self.logger = logging.getLogger('MacTagsToDropbox')
    
    def get_file_tags(self, file_path):
        try:
            cmd = ['mdls', '-name', 'kMDItemUserTags', str(file_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                self.logger.error(f"無法讀取檔案標籤: {file_path}")
                return []
                
            tags_output = result.stdout.strip()
            if "kMDItemUserTags = (null)" in tags_output:
                return []
                
            # 解析輸出格式並提取標籤
            tags = []
            if "kMDItemUserTags = (" in tags_output:
                tags_list = tags_output.split("kMDItemUserTags = (")[1].split(")")[0]
                # 移除多餘的引號和空白
                tags = [tag.strip(' "').strip().strip('"').lower().encode('utf-8').decode('unicode_escape') for tag in tags_list.split(",") if tag.strip()]
            
            return tags
            
        except Exception as e:
            self.logger.error(f"讀取標籤時發生錯誤: {str(e)}")
            return []