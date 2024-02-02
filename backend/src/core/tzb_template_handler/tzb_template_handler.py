import io
from datetime import datetime
from typing import Dict

import pandas as pd
from fastapi import Response, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pandas import DataFrame, ExcelFile

from src.core.beautifier.beautifier_tzb import PhoneNumbersBeautifierTZB
from src.core.config_maker.tzb_config_maker import ConfigMaker
from src.core.gender_age_extender.gender_age_extender import GenderAgeExtender
from src.core.quotas_filter.quotas_filter import QuotasFilter
from src.core.quotas_parser.quotas_parser import QuotasParser
from src.core.tzb_checker.tzb_checker import TZBChecker
from src.core.tzb_template_parser.tzb_template_parser import TZBTemplateParser


class TZBTemplateHandler:
    def __init__(self, dates: Dict, files: list[UploadFile]) -> None:
        self.files = files
        self.dates = dates
        self.config_maker = ConfigMaker()

    def run(self):
        try:
            files_dict = self.get_files_matches(self.files)
        except ValueError as error:
            error_description = f"{error}"
            return self.make_error_response(error_description)

        try:
            # Make a config from the Alive file and make a beautifier instance
            config = self.config_maker.make_config_file(files_dict["beautifier"]["excel_file"])
            beautifier = PhoneNumbersBeautifierTZB(config)

        except ValueError as error:
            error_description = f"File name: {files_dict['beautifier']['file_name']}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

        except KeyError as error:
            error_description = f"File name: {files_dict['beautifier']['file_name']}, KeyError: {str(error)}"
            return self.make_error_response(error_description)

        try:
            # Create a source dataframe from the template
            template_parser = TZBTemplateParser()
            source_dataframe = template_parser.make_merged_source_dataframe(
                self.dates, files_dict["template"]["excel_file"]
            )

        except ValueError as error:
            error_description = f"File name: {files_dict['template']['file_name']}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

        try:
            check_list = pd.read_excel(files_dict["check"]["excel_file"])
            checker = TZBChecker(check_list)
            checked_source_dataframe, completed_dataframe = checker.check_source(source_dataframe)

        except ValueError as error:
            error_description = f"File name: {files_dict['check']['file_name']}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

        try:
            # Add gender, age, and adjusted region details to the original dataframe
            extender = GenderAgeExtender()
            macros_dataframe = pd.read_excel(files_dict["template"]["excel_file"], sheet_name="Макрос")
            extended_dataframe = extender.make_extended_dataframe(macros_dataframe, checked_source_dataframe)

        except ValueError as error:
            error_description = f"File name: {files_dict['template']['file_name']}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

        except KeyError as error:
            error_description = f"File name: {files_dict['template']['file_name']}, KeyError: {str(error)}"
            return self.make_error_response(error_description)

        try:
            # Make a dataset structured for TZB
            result_dataframes = beautifier.run(extended_dataframe)
            result_dataframes = list(result_dataframes)

        except ValueError as error:
            error_description = f"File name: {files_dict['source_macros']['file_name']}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

        except KeyError as error:
            error_description = f"File name: {files_dict['source_macros']['file_name']}, KeyError: {str(error)}"
            return self.make_error_response(error_description)

        try:
            # Add isCallable flag to dataframes[0]
            quotas_dataframe = pd.read_excel(files_dict["quotas"]["excel_file"])
            quotas_parser = QuotasParser(beautifier)
            quotas_filter = QuotasFilter()
            quotas_dict = quotas_parser.make_quotas_dictionary(quotas_dataframe)
            quota_application_results = quotas_filter.filter_phone_numbers(result_dataframes[0], quotas_dict)

            result_dataframes[0] = quota_application_results[0]
            result_dataframes.append(quota_application_results[1])
            result_dataframes.append(checked_source_dataframe)
            result_dataframes.append(completed_dataframe)

            result_dataframes[0].drop(inplace=True, columns=["Пол", "Возраст"])

            response = self.export_to_excel_file(result_dataframes)

            return response

        except ValueError as error:
            error_description = f"File name: {files_dict['quotas']['file_name']}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

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

            elif "ПРОВЕРКА" == file.filename[0:8]:
                files_dict["check"] = {
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
