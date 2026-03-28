"""
title: Example Filter
author: open-webui
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1
"""

# 這是一個 Open WebUI 的 Filter（過濾器）範例
# Filter 的作用是在使用者送出訊息「前」和 AI 回應「後」，攔截並處理資料
# 常見用途：限制對話輪數、過濾敏感詞、記錄日誌等

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    """
    Filter 主類別。
    Open WebUI 會自動載入這個類別，並在對話流程中呼叫 inlet / outlet 方法。
    """

    class Valves(BaseModel):
        """
        管理員層級的設定（後台可調整）。
        Valves 是給「系統管理員」設定的參數，優先權較高。
        """
        priority: int = Field(
            default=0, description="Filter 的執行優先順序，數字越小越先執行。"
        )
        max_turns: int = Field(
            default=8, description="整個系統允許的最大對話輪數上限。"
        )
        pass

    class UserValves(BaseModel):
        """
        使用者層級的設定（使用者自己可調整）。
        UserValves 是給「一般使用者」設定的參數，受 Valves 限制。
        """
        max_turns: int = Field(
            default=4, description="單一使用者允許的最大對話輪數，不可超過管理員設定值。"
        )
        pass

    def __init__(self):
        """
        初始化 Filter，建立 Valves 實例以載入預設設定。
        """
        # self.file_handler = True
        # 若啟用此旗標，WebUI 會將檔案處理交由此 Filter 自行管理，
        # 而不使用預設的檔案處理流程。目前已註解停用。

        # 建立 Valves 實例，載入管理員層級的預設設定
        self.valves = self.Valves()
        pass

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        前處理器（Pre-processor）：在使用者訊息送往 AI 之前執行。
        可用來驗證、修改請求內容，或在不符合條件時拋出例外中斷對話。

        參數：
            body: 包含對話訊息的請求字典（messages、model 等）
            __user__: 目前使用者的資訊（role、valves 等）

        回傳：
            處理後的 body 字典
        """
        print(f"inlet:{__name__}")
        print(f"inlet:body:{body}")
        print(f"inlet:user:{__user__}")

        # 只對 role 為 "user" 或 "admin" 的使用者進行輪數檢查
        if __user__.get("role", "admin") in ["user", "admin"]:
            messages = body.get("messages", [])

            # 取使用者設定與管理員設定的較小值，確保使用者無法超過系統上限
            max_turns = min(__user__["valves"].max_turns, self.valves.max_turns)

            # 若對話訊息數量超過上限，拋出例外，中斷本次請求
            if len(messages) > max_turns:
                raise Exception(
                    f"Conversation turn limit exceeded. Max turns: {max_turns}"
                )

        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        後處理器（Post-processor）：在 AI 回應產生之後執行。
        可用來修改回應內容、記錄日誌或進行額外分析。

        參數：
            body: 包含 AI 回應的字典
            __user__: 目前使用者的資訊

        回傳：
            處理後的 body 字典
        """
        print(f"outlet:{__name__}")
        print(f"outlet:body:{body}")
        print(f"outlet:user:{__user__}")

        # 目前不做任何修改，直接回傳原始回應
        return body
