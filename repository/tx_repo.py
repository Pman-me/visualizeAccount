from datetime import datetime
from typing import Optional

from sqlalchemy import select, exc, insert, delete, func

from models.transaction_model import TransactionModel
from repository.base_psql_repo import BasePSQLRepo


class TxRepo(BasePSQLRepo):
    def get(self, key: str):
        try:
            stmt = select(TransactionModel).where(TransactionModel.hash == key)
            return self.session.execute(stmt).scalar()
        except exc.SQLAlchemyError as err:
            pass

    def set(self, data: dict, /, key: Optional[str]):
        try:
            values = {
                'hash': data['hash'],
                'wallet': data['wallet'],
                'to_contract_name': data['to_contract_name'],
                'send': data['send'],
                'recv': data['recv'],
                'fee': data['fee'],
                'nonce': data['nonce'],
                'date_time': datetime.fromtimestamp(int(data['timeStamp'])).strftime("%b-%d-%Y %I:%M:%S %p %Z"),
                'chain': data['chain'],
                'type': data['type']
            }
            # stmt = update(TransactionModel).where(TransactionModel.hash == key).values(
            #     hash=data['hash'],
            #     from_address=data['from'],
            #     to_contract_name=data['to_contract_name'],
            #     send=data['send'],
            #     recv=data['recv'],
            #     call_data=data['input'],
            #     tx_fee=data['fee'],
            #     nonce=data['nonce'],
            #     timestamp=data['timeStamp'],
            #     chain=data['chain']
            # )
            # if self.session.execute(stmt).rowcount == 0:
            stmt = insert(TransactionModel)
            self.session.execute(stmt, values)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def delete(self, key: str) -> None:
        try:
            stmt = delete(TransactionModel).where(TransactionModel.hash == key)
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def get_max_nonce_per_chain(self):
        try:
            stmt = select(
                TransactionModel.chain,
                func.max(TransactionModel.nonce)
            ).group_by(TransactionModel.chain)
            return self.session.execute(stmt).fetchall()
        except exc.SQLAlchemyError as err:
            pass
