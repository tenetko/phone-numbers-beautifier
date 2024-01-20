import io
from datetime import datetime
from typing import Dict

import pandas as pd
from fastapi import Response, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pandas import DataFrame, ExcelFile

from src.core.beautifier.beautifier_os import PhoneNumbersBeautifierOS
from src.core.config_maker.os_config_maker import ConfigMaker


class OSHandler:
    def __init__(self, files: list[UploadFile], project_name: str) -> None:
        self.files = files
        self.project_name = project_name
        self.config_maker = ConfigMaker()

    def run(self):
        try:
            files_dict = self.get_files_matches(self.files)
        except ValueError as error:
            error_description = f"{error}"
            return self.make_error_response(error_description)

        try:
            # Passing bytes to 'read_excel' is deprecated and will be removed in a future version.
            # To read from a byte string, wrap it in a `BytesIO` object.
            config = self.config_maker.make_config_file(files_dict["beautifier"]["excel_file"])
            beautifier = PhoneNumbersBeautifierOS(config, self.project_name)

        except ValueError as error:
            error_description = f"File name: {files_dict['beautifier']['file_name']}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

        except KeyError as error:
            error_description = f"File name: {files_dict['beautifier']['file_name']}, KeyError: {str(error)}"
            return self.make_error_response(error_description)

        try:
            # Make the initial file structured for TZB
            dataframe = pd.read_excel(files_dict["os"]["excel_file"])
            result_dataframes = beautifier.run(dataframe)
            result_dataframes = list(result_dataframes)

            response = self.export_to_excel_file(result_dataframes)

            return response

        except ValueError as error:
            error_description = f"File name: {files_dict['os']['file_name']}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

        except KeyError as error:
            error_description = f"File name: {files_dict['os']['file_name']}, KeyError: {str(error)}"
            return self.make_error_response(error_description)

    def get_files_matches(self, files: list[UploadFile]) -> Dict[str, Dict[str, ExcelFile]]:
        files_dict = {}

        for file in files:
            if "Alive" == file.filename[0:5]:
                files_dict["beautifier"] = {
                    "file_name": file.filename,
                    "excel_file": pd.ExcelFile(io.BytesIO(file.file.read())),
                }
                continue

            else:
                files_dict["os"] = {
                    "file_name": file.filename,
                    "excel_file": pd.ExcelFile(io.BytesIO(file.file.read())),
                }

        return files_dict

    def export_to_excel_file(self, dataframes: [DataFrame]) -> Response:
        stream = io.BytesIO()

        with pd.ExcelWriter(stream) as writer:
            dataframes[0].to_excel(writer, sheet_name="base with quotas applied", index=False)
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
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M")
        return f"os-result-{timestamp}.xlsx"

    def make_error_response(self, error_text) -> JSONResponse:
        text = jsonable_encoder(error_text)
        return JSONResponse(content=text, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
