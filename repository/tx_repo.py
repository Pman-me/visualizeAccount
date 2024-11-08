from typing import Optional

from sqlalchemy import select, exc, insert, delete, update, values

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
            # _values = values(
            #     hash=data['hash'],
            #     from_address=data['from'],
            #     to_contract_name=data['to'],
            #     send=data['in_amount'],
            #     recv=data['out_amount'],
            #     call_data=data['input_data'],
            #     tx_fee=data['tx_fee'],
            #     nonce=data['nonce'],
            #     timestamp=data['timestamp'],
            #     chain=data['chain']
            # )
            stmt = update(TransactionModel).where(TransactionModel.hash == key).values(
                hash=data['hash'],
                from_address=data['from'],
                to_contract_name=data['to'],
                send=data['in_amount'],
                recv=data['out_amount'],
                call_data=data['input_data'],
                tx_fee=data['tx_fee'],
                nonce=data['nonce'],
                timestamp=data['timestamp'],
                chain=data['chain']
            )
            if self.session.execute(stmt).rowcount == 0:
                stmt = insert(TransactionModel).values(
                    hash=data['hash'],
                    from_address=data['from'],
                    to_contract_name=data['to'],
                    send=data['in_amount'],
                    recv=data['out_amount'],
                    call_data=data['input_data'],
                    tx_fee=data['tx_fee'],
                    nonce=data['nonce'],
                    timestamp=data['timestamp'],
                    chain=data['chain']
                )
                self.session.execute(stmt)
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
