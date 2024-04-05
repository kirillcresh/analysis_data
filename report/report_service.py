import datetime

import pandas as pd
from fastapi import Depends

from database import Session, get_session
from report.models import Call, Client, Document, Status, Tariff


class CallReportService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def data_to_db(self):
        flag = True
        file_location = "E:/work_IT/study/analysis_data/report/report_call.xlsx"
        df = pd.read_excel(file_location)
        statuses_call = df["Статус"].tolist()

        # Добавляем уникальные статусы в БД
        # Уникальность можно было проставить на уровне БД, но сделал так
        statuses_set = set(statuses_call)
        for status in statuses_set:
            current_statuses = self.session.query(Status).all()
            for current_status in current_statuses:
                if current_status.type == status:
                    flag = False
                    break
            if flag:
                statuses_bd = Status(type=status, description="Описание статуса")
                self.session.add(statuses_bd)
            flag = True
        self.session.commit()

        # Добавляем документ
        # Так как работа идет над определенным файлом, то добавляю таким способом
        document_bd = (
            self.session.query(Document)
            .filter(Document.date == datetime.date.today())
            .first()
        )
        name_report = "report_call.xlsx"
        try:
            doc_name = document_bd.name
            if name_report == doc_name:
                flag = False
        except:
            flag = True
        if flag:
            document = Document(name=name_report, date=datetime.date.today())
            self.session.add(document)
            self.session.commit()
        tariffs_call = df["Тариф"].tolist()
        flag = True

        # Добавляем уникальные тарифы в БД
        # Уникальность можно проставить на уровне БД
        tariffs_set = set(tariffs_call)
        for tariff in tariffs_set:
            current_tariffs = self.session.query(Tariff).all()
            for current_tariff in current_tariffs:
                if current_tariff.name == tariff:
                    flag = False
                    break
            if flag:
                if tariff == "Грустный тариф":
                    price = 2.5
                elif tariff == "Тариф":
                    price = 1.5
                elif tariff == "Супер-тариф":
                    price = 0.6
                else:
                    price = 4
                tariff_bd = Tariff(
                    name=tariff, description="Наш лучший тариф", price_per_minute=price
                )
                self.session.add(tariff_bd)
            flag = True
        self.session.commit()
        caller_call = df["Вызывающий"].tolist()
        called_call = df["Вызываемый"].tolist()

        # Добавляем клиентов
        tariffs_bd = self.session.query(Tariff).all()
        set_clients = set(caller_call + called_call)
        client_tariff_df = df[["Вызывающий", "Тариф"]]
        client_tariff_df = client_tariff_df.reset_index()
        client_tariff_list = []
        for index, row in client_tariff_df.iterrows():
            client_tariff = {"Вызывающий": row["Вызывающий"], "Тариф": row["Тариф"]}
            client_tariff_list.append(client_tariff)
        for phone in set_clients:
            tariff = "Тариф"
            tariff_id = 2
            current_clients = self.session.query(Client).all()
            for current_client in current_clients:
                if current_client.phone == phone[1:]:
                    flag = False
            if flag:
                for client_tariff in client_tariff_list:
                    # Если бы дата звонка была разной, то здесь была бы проверка на актуальный тариф пользователя
                    if phone == client_tariff["Вызывающий"]:
                        tariff = client_tariff["Тариф"]
                        break
                for tariff_bd in tariffs_bd:
                    if tariff == tariff_bd.name:
                        tariff_id = tariff_bd.id
                        break
                client_bd = Client(
                    full_name="Наш Любимый Клиент",
                    tariff_id=tariff_id,
                    phone=phone[1:],
                    is_active=True,
                    balance=500,
                )
                self.session.add(client_bd)
            self.session.commit()
            flag = True

        # Добавляем звонки
        df = df.fillna(0)
        call_df = df.reset_index()
        call_list = []
        for index, row in call_df.iterrows():
            call = {
                "Вызывающий": row["Вызывающий"],
                "Вызываемый": row["Вызываемый"],
                "Длительность": row["Длительность"],
                "Тариф": row["Тариф"],
                "Статус": row["Статус"],
                "Дата звонка": row["Дата звонка"],
            }
            call_list.append(call)
        for call in call_list:
            # Убрать питоновские ошибки
            document_id = 1
            caller_id = 1
            called_id = 1
            status_id = 1
            clients = self.session.query(Client).all()
            for client in clients:
                if call["Вызывающий"][1:] == client.phone:
                    caller_id = client.id
                if call["Вызываемый"][1:] == client.phone:
                    called_id = client.id
            statuses = self.session.query(Status).all()
            for status in statuses:
                if call["Статус"] == status.type:
                    status_id = status.id
            documents = self.session.query(Document).all()
            for document in documents:
                if (
                    document.name == "report_call.xlsx"
                    and document.date == datetime.date.today()
                ):
                    document_id = document.id
            call_date = call["Дата звонка"]
            # Эксель переделывает 1:14 в 1:14:00
            duration = str(call["Длительность"])
            call_bd = Call(
                caller_id=caller_id,
                called_id=called_id,
                duration=duration,
                status_id=status_id,
                document_id=document_id,
                call_date=call_date,
            )
            self.session.add(call_bd)
        self.session.commit()
        return {"detail": "Success"}
