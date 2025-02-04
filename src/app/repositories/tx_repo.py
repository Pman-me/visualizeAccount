from datetime import datetime
from typing import Optional

from sqlalchemy import select, exc, insert, delete, func, Integer
from sqlalchemy.testing.plugin.plugin_base import logging

from src.app.models.transaction_model import TransactionModel
from src.app.repositories.base_psql_repo import BasePSQLRepo
from src.app.schemas.transactionRead import TransactionRead


class TxRepo(BasePSQLRepo):
    def get(self, key: str):
        try:
            stmt = select(TransactionModel).where(TransactionModel.hash == key)
            if (result := self.session.execute(stmt).scalar()) is not None:
                return TransactionRead.model_validate(result)
            return None
        except exc.SQLAlchemyError as err:
            logging.exception("An error occurred: %s", err)

    def get_all_tx(self, account_addres: str):
        try:
            stmt = select(TransactionModel).where(TransactionModel.wallet == account_addres)
            if (result := self.session.execute(stmt).scalars().all()) is not None:
                return [TransactionRead.model_validate(tx) for tx in
                        self.session.execute(stmt).scalars().all()]
            return None
        except exc.SQLAlchemyError as err:
            logging.exception("An error occurred: %s", err)

    def get_txs_per_chain(self, chain: str):
        try:
            stmt = select(TransactionModel).where(TransactionModel.chain == chain)
            return self.session.execute(stmt).fetchall()
        except exc.SQLAlchemyError as err:
            logging.exception("An error occurred: %s", err)

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
                'chain_id': data['chain_id'],
                'type': data['type']
            }
            stmt = insert(TransactionModel)
            self.session.execute(stmt, values)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            logging.exception("An error occurred: %s", err)

    def delete(self, key: str) -> None:
        try:
            stmt = delete(TransactionModel).where(TransactionModel.hash == key)
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            logging.exception("An error occurred: %s", err)

    def get_max_nonce_per_chain(self):
        try:
            stmt = select(
                TransactionModel.chain_id,
                func.max(func.nullif(TransactionModel.nonce, '').cast(Integer))
            ).group_by(TransactionModel.chain_id)
            return self.session.execute(stmt).fetchall()
        except exc.SQLAlchemyError as err:
            logging.exception("An error occurred: %s", err)
