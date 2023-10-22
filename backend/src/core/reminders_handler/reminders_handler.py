import io
import json
from datetime import datetime
from typing import Dict

import pandas as pd
from fastapi import Response, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pandas import DataFrame

from src.core.beautifier.beautifier import PhoneNumbersBeautifier
from src.core.config_maker.tzb_config_maker import ConfigMaker
from src.core.quotas_filter.quotas_filter import QuotasFilter
from src.core.quotas_parser.quotas_parser import QuotasParser


class RemindersHandler:
    def __init__(self, files: list[UploadFile]) -> None:
        self.files = files
        self.config_maker = ConfigMaker()

    def run(self):
        files_dict = self.get_files_matches(self.files)

        try:
            # Try to parse the 'Alive' file
            config = self.config_maker.make_config_file(io.BytesIO(files_dict["beautifier"].file.read()))
            beautifier = PhoneNumbersBeautifier(config, "tzb")

        except ValueError as error:
            error_description = f"File name: {files_dict['beautifier'].filename}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

        except KeyError as error:
            error_description = f"File name: {files_dict['beautifier'].filename}, KeyError: {str(error)}"
            return self.make_error_response(error_description)

        try:
            # Try to parse the file with quotas
            quotas_parser = QuotasParser(beautifier)
            quotas_dataframe = pd.read_excel(io.BytesIO(files_dict["quotas"].file.read()))
            quotas_dict = quotas_parser.make_quotas_dictionary(quotas_dataframe)

        except ValueError as error:
            error_description = f"File name: {files_dict['quotas'].filename}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

        except KeyError as error:
            error_description = f"File name: {files_dict['quotas'].filename}, KeyError: {str(error)}"
            return self.make_error_response(error_description)

        try:
            # Try to parse the file with reminders
            quotas_filter = QuotasFilter()
            reminders_dataframe = pd.read_excel(io.BytesIO(files_dict["reminders"].file.read()))
            quota_application_results = quotas_filter.filter_reminders(reminders_dataframe, quotas_dict)

            quota_application_results[0].drop(inplace=True, columns=["Пол", "Возраст"])

            response = self.export_to_excel_file(quota_application_results)

            return response

        except ValueError as error:
            error_description = f"File name: {files_dict['reminders'].filename}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

        except KeyError as error:
            error_description = f"File name: {files_dict['reminders'].filename}, KeyError: {str(error)}"
            return self.make_error_response(error_description)

    def get_files_matches(self, files: list[UploadFile]) -> Dict:
        files_dict = {}

        for file in files:
            if "Alive" == file.filename[0:5]:
                files_dict["beautifier"] = file
            elif "Reminder" == file.filename[0:8]:
                files_dict["reminders"] = file
            elif "report_common_statistic" == file.filename[0:23]:
                files_dict["quotas"] = file

        return files_dict

    def export_to_excel_file(self, dataframes: [DataFrame]) -> Response:
        stream = io.BytesIO()

        with pd.ExcelWriter(stream) as writer:
            dataframes[0].to_excel(writer, sheet_name="reminders with quotas applied", index=False)
            dataframes[1].to_excel(writer, sheet_name="quota_errors", index=False)

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
        return f"result-{timestamp}.xlsx"

    def make_error_response(self, error_text) -> JSONResponse:
        text = jsonable_encoder(error_text)
        return JSONResponse(content=text, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
