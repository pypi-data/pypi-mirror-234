import json
from typing import Optional, Type

from promptmanager.script.base.callbacks.manager import AsyncCallbackManagerForToolRun
from promptmanager.script.base.pydantic_v1 import BaseModel, Field
from promptmanager.script.base.tools.ainetwork.base import AINBaseTool


class TransferSchema(BaseModel):
    address: str = Field(..., description="Address to transfer AIN to")
    amount: int = Field(..., description="Amount of AIN to transfer")


class AINTransfer(AINBaseTool):
    name: str = "AINtransfer"
    description: str = "Transfers AIN to a specified address"
    args_schema: Type[TransferSchema] = TransferSchema

    async def _arun(
        self,
        address: str,
        amount: int,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        try:
            res = await self.interface.wallet.transfer(address, amount, nonce=-1)
            return json.dumps(res, ensure_ascii=False)
        except Exception as e:
            return f"{type(e).__name__}: {str(e)}"
