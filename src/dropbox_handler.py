import dropbox
import logging
from pathlib import Path
import json

class DropboxHandler:
    def __init__(self, access_token):
        self.dbx = dropbox.Dropbox(access_token)
        self.logger = logging.getLogger('MacTagsToDropbox')
    
    def find_file(self, file_name):
        try:
            results = self.dbx.files_search_v2(query=file_name)
            matches = results.matches
            print(results.matches[0].metadata)
            exit()
            
            if not matches:
                self.logger.warning(f"在 Dropbox 中找不到檔案: {file_name}")
                return None
            
            # 添加調試日誌
            self.logger.debug(f"搜尋結果類型: {type(matches[0])}")
            self.logger.debug(f"搜尋結果內容: {matches[0]}")
            
            # 獲取檔案元數據
            match = matches[0]
            if hasattr(match, 'metadata'):
                file_metadata = match.metadata
                # 檢查是否為 FileMetadata 對象
                if hasattr(file_metadata, 'is_downloadable'):
                    return file_metadata.path_display
                # 如果是巢狀結構
                elif hasattr(file_metadata, 'metadata'):
                    return file_metadata.metadata.path_display
            
            self.logger.error("無法從搜尋結果中獲取檔案路徑")
            return None
            
        except Exception as e:
            self.logger.error(f"搜尋 Dropbox 檔案時發生錯誤: {str(e)}")
            self.logger.debug(f"錯誤詳情: {type(e).__name__}")
            return None
    
    def update_file_tags(self, file_path, tags):
        try:
            
            # 使用 Dropbox API 更新檔案標籤
            for tag in tags:
                self.dbx.files_tags_add(file_path, json.dumps(tag))
                self.logger.info(f"成功更新檔案標籤: {file_path} - {tag}")
            
        except dropbox.exceptions.ApiError as e:
            self.logger.error(f"更新 Dropbox 標籤時發生 API 錯誤: {str(e)}")
        except Exception as e:
            self.logger.error(f"更新 Dropbox 標籤時發生錯誤: {str(e)}") 