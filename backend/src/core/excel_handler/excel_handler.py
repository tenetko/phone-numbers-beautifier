import io
from datetime import datetime

import pandas as pd
from fastapi import Response, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pandas import DataFrame

from src.core.beautifier.beautifier import PhoneNumbersBeautifier
from src.core.config_maker.tzb_config_maker import ConfigMaker
from src.core.gender_age_extender.gender_age_extender import GenderAgeExtender
from src.core.quotas_filter.quotas_filter import QuotasFilter
from src.core.quotas_parser.quotas_parser import QuotasParser


class ExcelHandler:
    def __init__(self, files: list[UploadFile], project_name: str) -> None:
        self.files = files
        self.project_name = project_name
        self.config_maker = ConfigMaker()

    def run(self):
        error = ""
        try:
            config = self.config_maker.make_config_file(io.BytesIO(self.files[0].file.read()))
            beautifier = PhoneNumbersBeautifier(config, self.project_name)
            extender = GenderAgeExtender()

        except ValueError as error:
            error_description = f"File name: {self.files[0].filename}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

        except KeyError as error:
            error_description = f"File name: {self.files[0].filename}, KeyError: {str(error)}"
            return self.make_error_response(error_description)

        try:
            # Make the initial file structured for TZB
            dataframes = beautifier.run(io.BytesIO(self.files[1].file.read()))
            dataframes = list(dataframes)

        except ValueError as error:
            error_description = f"File name: {self.files[1].filename}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

        except KeyError as error:
            error_description = f"File name: {self.files[1].filename}, KeyError: {str(error)}"
            return self.make_error_response(error_description)

        try:
            # Add gender and age details to dataframes[0]
            details_dataframe = pd.read_excel(io.BytesIO(self.files[2].file.read()))
            dataframes[0] = extender.make_extended_dataframe(dataframes[0], details_dataframe)

        except ValueError as error:
            error_description = f"File name: {self.files[2].filename}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

        except KeyError as error:
            error_description = f"File name: {self.files[2].filename}, KeyError: {str(error)}"
            return self.make_error_response(error_description)

        # response = self.export_to_excel_file(dataframes)
        # return response

        try:
            # Add isCallable flag to dataframes[0]
            quotas_dataframe = pd.read_excel(io.BytesIO(self.files[3].file.read()))
            quotas_parser = QuotasParser(beautifier)
            quotas_filter = QuotasFilter()
            quotas_dict = quotas_parser.make_quotas_dictionary(quotas_dataframe)
            quota_application_results = quotas_filter.filter_phone_numbers(dataframes[0], quotas_dict)

            dataframes[0] = quota_application_results[0]
            dataframes.append(quota_application_results[1])

            response = self.export_to_excel_file(dataframes)

            return response

        except ValueError as error:
            error_description = f"File name: {self.files[3].filename}, ValueError: {str(error)}"
            return self.make_error_response(error_description)

        except KeyError as error:
            error_description = f"File name: {self.files[3].filename}, KeyError: {str(error)}"
            return self.make_error_response(error_description)

    def export_to_excel_file(self, dataframes: [DataFrame]) -> Response:
        stream = io.BytesIO()

        with pd.ExcelWriter(stream) as writer:
            dataframes[0].to_excel(writer, sheet_name="base with quotas applied", index=False)
            dataframes[1].to_excel(writer, sheet_name="empty", index=False)
            dataframes[2].to_excel(writer, sheet_name="ignored", index=False)
            dataframes[3].to_excel(writer, sheet_name="quota errors", index=False)

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
