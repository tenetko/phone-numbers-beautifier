import io
from datetime import datetime
from typing import Dict

import pandas as pd
from fastapi import Response, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger
from pandas import DataFrame, ExcelFile

from src.core.beautifier.beautifier_tzb import PhoneNumbersBeautifierTZB
from src.core.quotas_filter.quotas_filter import QuotasFilter
from src.core.quotas_parser.quotas_parser import QuotasParser
from src.core.tzb_filter.tzb_filter import TZBFilter
from src.core.tzb_template_parser.tzb_template_parser import TZBTemplateParser
from src.utils.config_storage.config_storage import ConfigStorage
from src.utils.logging.logging import Sink


class TZBTemplateHandler:
    def __init__(self, files: list[UploadFile]) -> None:
        self.files = files
        self.logs = Sink()
        logger.add(sink=self.logs, serialize=True)

    def run(self):
        # Try to figure what uploaded files are for based on their names
        try:
            files_dict = self.get_files_matches(self.files)
        except ValueError:
            return self.make_error_response(self.logs.records[0])

        # Make a config from the config storage which corresponds to the latest Alive file
        # and make a beautifier instance
        config = ConfigStorage.get_config()
        beautifier = PhoneNumbersBeautifierTZB(config)

        # Create a merged source dataframe from the template file filtered by dates
        template_parser = TZBTemplateParser()
        source_dataframe = template_parser.make_merged_source_dataframe(files_dict["template"]["excel_file"])

        # Perform a 'check' operation that filters phone numbers that are already present in the 'check' file
        # Also, filter 'source' phone numbers with the 'macros' sheet. If a number is not present in the 'macros',
        # we remove it from the 'source'.
        check_list_dataframe = pd.read_excel(files_dict["check"]["excel_file"])
        macros_dataframe = pd.read_excel(files_dict["template"]["excel_file"], sheet_name="Макрос")
        checker = TZBFilter(check_list_dataframe, macros_dataframe)
        try:
            checked_source_dataframe, completed_dataframe = checker.filter_with_checklist(source_dataframe)
            filtered_by_macros_dataframe = checker.filter_with_macros(checked_source_dataframe)

        except KeyError:
            error_description = "; ".join(checker.logs.records)
            return self.make_error_response(error_description)

        try:
            # Make a dataset structured for TZB
            result_dataframes = beautifier.run(filtered_by_macros_dataframe)
            result_dataframes = list(result_dataframes)

        except KeyError:
            error_description = "; ".join(beautifier.logs.records)
            return self.make_error_response(error_description)

        try:
            # Add isCallable flag to dataframes[0] according to quotas
            quotas_dataframe = pd.read_excel(files_dict["quotas"]["excel_file"])
            quotas_parser = QuotasParser(beautifier)
            quotas_filter = QuotasFilter(config)
            quotas_dict = quotas_parser.make_quotas_dictionary(quotas_dataframe)
            quota_application_results = quotas_filter.filter_phone_numbers(result_dataframes[0], quotas_dict)

            result_dataframes[0] = quota_application_results[0]
            result_dataframes.append(quota_application_results[1])
            result_dataframes.append(checked_source_dataframe)
            result_dataframes.append(completed_dataframe)

            # Drop 'Пол' and 'Возраст' columns according to the client requirement
            if set(["Пол", "Возраст"]).issubset(result_dataframes[0].columns):
                result_dataframes[0].drop(inplace=True, columns=["Пол", "Возраст"])

            result_dataframes[0].drop_duplicates(inplace=True, subset="Number", keep="first")

            response = self.export_to_excel_file(result_dataframes)

            return response

        except KeyError as error:
            error_description = f"File name: {files_dict['quotas']['file_name']}, KeyError: {str(error)}"
            return self.make_error_response(error_description)

    def get_files_matches(self, files: list[UploadFile]) -> Dict[str, Dict[str, ExcelFile]]:
        # Passing bytes to 'read_excel' is deprecated and will be removed in a future version.
        # To read from a byte string, wrap it in a `BytesIO` object.

        files_dict = {}

        for file in files:
            if "Alive" == file.filename[0:5]:
                files_dict["beautifier"] = {
                    "file_name": file.filename,
                    "excel_file": pd.ExcelFile(io.BytesIO(file.file.read())),
                }
                continue

            elif "report_common_statistic" == file.filename[0:23]:
                files_dict["quotas"] = {
                    "file_name": file.filename,
                    "excel_file": pd.ExcelFile(io.BytesIO(file.file.read())),
                }
                continue

            elif "iSay" == file.filename[0:4]:
                files_dict["template"] = {
                    "file_name": file.filename,
                    "excel_file": pd.ExcelFile(io.BytesIO(file.file.read())),
                }

            elif "ПРОВЕРКА" in file.filename:
                files_dict["check"] = {
                    "file_name": file.filename,
                    "excel_file": pd.ExcelFile(io.BytesIO(file.file.read())),
                }
            else:
                logger.exception(f"File {file.filename} didn't match any pattern")
                raise ValueError

        return files_dict

    def export_to_excel_file(self, dataframes: [DataFrame]) -> Response:
        stream = io.BytesIO()

        with pd.ExcelWriter(stream) as writer:
            dataframes[0].to_excel(writer, sheet_name="base with quotas applied", index=False)
            dataframes[1].to_excel(writer, sheet_name="empty", index=False)
            dataframes[2].to_excel(writer, sheet_name="ignored", index=False)
            dataframes[3].to_excel(writer, sheet_name="quota errors", index=False)
            dataframes[4].to_excel(writer, sheet_name="source", index=False)
            dataframes[5].to_excel(writer, sheet_name="completed", index=False)

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
        return f"tzb-template-result-{timestamp}.xlsx"

    def make_error_response(self, error_text) -> JSONResponse:
        text = jsonable_encoder(error_text)
        return JSONResponse(content=text, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
