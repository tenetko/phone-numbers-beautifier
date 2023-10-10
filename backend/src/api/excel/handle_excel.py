import io
from datetime import datetime

import pandas as pd
from fastapi import APIRouter, Response, UploadFile
from pandas import DataFrame

from src.core.beautifier.beautifier import PhoneNumbersBeautifier
from src.core.config_maker.tzb_config_maker import ConfigMaker

router = APIRouter()


@router.post("/")
async def handle_xlsx_files(files: list[UploadFile]) -> Response:
    config_maker = ConfigMaker()
    beautifier = PhoneNumbersBeautifier()

    config = config_maker.make_config_file(io.BytesIO(files[1].file.read()))
    beautified_df, empty_numbers, ignored_records = beautifier.run(io.BytesIO(files[0].file.read()), config, "tzb")

    return export_to_file(beautified_df)


def export_to_file(dataframe: DataFrame) -> Response:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    file_name = f"base-{timestamp}.xlsx"
    stream = io.BytesIO()
    with pd.ExcelWriter(stream) as writer:
        dataframe.to_excel(writer, index=False)

    return Response(
        content=stream.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Access-Control-Expose-Headers": "Content-Disposition",
            f"Content-Disposition": f"attachment; filename={file_name}",
        },
    )
