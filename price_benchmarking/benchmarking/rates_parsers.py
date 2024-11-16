import copy
import datetime
import decimal

import dateutil.parser

'''
    This parser is not really need for simple parsing. 
    However, there is a lot of cases where we need to do manipulation and calculations to the data in the sheet.
    This where it comes handy with handle different logic and error handling in a simple way.
'''

MARKET_RATES_FIELDS = {
    'origin': {
        'extract_method': 'extract_origin',
    },
    'destination': {
        'extract_method': 'extract_destination',
    },
    'effective_on': {
        'extract_method': 'extract_effective_on',
    },
    'price': {
        'extract_method': 'extract_price',
    }
}

USER_RATES_FIELDS = copy.deepcopy(MARKET_RATES_FIELDS)
USER_RATES_FIELDS.update({
    'expired_on': {
        'extract_method': 'extract_expire_on',
    },
    'annual_volume': {
        'extract_method': 'extract_annual_volume',
    },
})


class MissingColumn(Exception):
    def __init__(self, row_index, column_name, *args):
        self.error_message = f'Row {row_index} column {column_name} is Missing'
        super().__init__(*args)


class ValueRequired(Exception):
    def __init__(self, column_name, row_index, *args):
        self.error_message = f'Row {row_index} column {column_name} cannot be empty'
        super().__init__(*args)


class InvalidDate(Exception):
    def __init__(self, column_name, row_index, value, *args):
        self.error_message = f'Row {row_index} column {column_name} is an invalid date "{value}"'
        super().__init__(*args)


class InvalidDecimal(Exception):
    def __init__(self, column_name, row_index, value, *args):
        self.error_message = f'Row {row_index} column {column_name} is an invalid decimal number "{value}"'
        super().__init__(*args)


class BaseRatesParser:
    fields = {}

    def __init__(self, data):
        self.data = data
        self.errors = ''
        self.result_data = []

    def get_value(self, row_index, row, column_name):
        try:
            column_name = column_name
            value = row[column_name]
            if not value:
                raise ValueRequired(column_name=column_name, row_index=row_index)
            if isinstance(value, str):
                value = value.strip()
            return value
        except KeyError:
            raise MissingColumn(row_index=row_index, column_name=column_name)

    def get_date_value(self, row_index, row, column_name):
        value = self.get_value(row_index, row, column_name)
        if isinstance(value, datetime.datetime):
            return value.date()
        try:
            return dateutil.parser.parse(value.replace(' utc', '')).date()
        except ValueError:
            raise InvalidDate(column_name=column_name, row_index=row_index, value=value)

    def get_decimal_value(self, row_index, row, column_name):
        value = self.get_value(row_index, row, column_name)
        try:
            return decimal.Decimal(value)
        except ValueError:
            raise InvalidDecimal(column_name=column_name, row_index=row_index, value=value)

    def extract_origin(self, row_index, row):
        return self.get_value(row_index, row, 'origin')

    def extract_destination(self, row_index, row):
        return self.get_value(row_index, row, 'destination')

    def extract_effective_on(self, row_index, row):
        return self.get_date_value(row_index, row, 'date')

    def extract_price(self, row_index, row):
        return self.get_decimal_value(row_index, row, 'price')

    def get_values(self, row_index, row):
        values = {}
        for field, data in self.fields.items():
            try:
                values[field] = getattr(self, data['extract_method'])(row_index, row)
            except (MissingColumn, ValueRequired, InvalidDate, InvalidDecimal) as e:
                self.errors += f'{e.error_message}\n'
        return values

    def extract_row(self, row_index, row):
        self.result_data.append(self.get_values(row_index, row))

    def parse(self):
        for row_index, row in enumerate(self.data):
            # the counter starts from 0 and the header row is not counted, so we need to add 2 to the row_index
            self.extract_row(row_index + 2, row)
        return self.result_data if not self.errors else None


class MarketRatesParser(BaseRatesParser):
    fields = MARKET_RATES_FIELDS


class UserRatesParser(BaseRatesParser):
    fields = USER_RATES_FIELDS

    def extract_effective_on(self, row_index, row):
        return self.get_date_value(row_index, row, 'effective_date')

    def extract_expire_on(self, row_index, row):
        return self.get_date_value(row_index, row, 'expiry_date')

    def extract_annual_volume(self, row_index, row):
        return self.get_decimal_value(row_index, row, 'annual_volume')