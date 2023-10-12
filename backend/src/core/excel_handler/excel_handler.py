import io
from datetime import datetime, timedelta

import pandas as pd
from fastapi import Response, UploadFile
from pandas import DataFrame

from src.core.beautifier.beautifier import PhoneNumbersBeautifier
from src.core.config_maker.tzb_config_maker import ConfigMaker


class ExcelHandler:
    def __init__(self, files: list[UploadFile], project_name: str):
        self.files = files
        self.project_name = project_name
        self.config_maker = ConfigMaker()

    def export_to_excel_file(self, dataframes: [DataFrame]) -> Response:
        stream = io.BytesIO()

        with pd.ExcelWriter(stream) as writer:
            dataframes[0].to_excel(writer, sheet_name="base", index=False)
            dataframes[1].to_excel(writer, sheet_name="empty", index=False)
            dataframes[2].to_excel(writer, sheet_name="ignored", index=False)

        return Response(
            content=stream.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Access-Control-Expose-Headers": "Content-Disposition",
                f"Content-Disposition": f"attachment; filename={self.get_result_file_name()}",
            },
        )

    def get_result_file_name(self):
        now = datetime.now() + timedelta(hours=3)
        timestamp = now.strftime("%Y-%m-%d_%H-%M")
        return f"result-{timestamp}.xlsx"

    def run(self):
        config = self.config_maker.make_config_file(io.BytesIO(self.files[1].file.read()))
        beautifier = PhoneNumbersBeautifier(config, self.project_name)
        dataframes = beautifier.run(io.BytesIO(self.files[0].file.read()))
        response = self.export_to_excel_file(dataframes)

        return response
