from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends, Query

from repositories.tx_repo import TxRepo
from schemas.transactionRead import TransactionRead

router = APIRouter(tags=['activity'])


@router.get('/activity', status_code=status.HTTP_200_OK)
def get_address_activities(account_address: str = Query(le=42), repository: TxRepo = Depends(TxRepo)) -> list[TransactionRead]:
    if (result := repository.get_all_tx(account_address)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account address not exists"
        )
    return result
