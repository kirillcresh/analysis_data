from fastapi import APIRouter, Depends

from report.report_service import CallReportService

router = APIRouter(
    prefix="/reports",
    tags=["ReportService"],
)


@router.get("/get-data-to-db")
def data_to_db(
    service: CallReportService = Depends(),
):
    """Метод на заполнение БД данными из экселя"""
    return service.data_to_db()
