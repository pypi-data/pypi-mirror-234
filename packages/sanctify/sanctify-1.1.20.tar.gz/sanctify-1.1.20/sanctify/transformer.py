# External Imports
import re
from datetime import datetime

import phonenumbers
from dateutil import parser
from loguru import logger

# Internal Imports
from sanctify.constants import DIGIT_TRANSLATION_TABLE, STRING_TRANSLATION_TABLE, CalendarDateComponents
from sanctify.exception import ValidationError


class Transformer:
    @staticmethod
    def parse_boolean(value: str):
        """
        Parses a boolean value from a string.

        Args:
            value (str): The input string.

        Returns:
            bool: The parsed boolean value.

        Raises:
            ValidationError: If the input string is not a valid boolean.
        """
        bool_string = str(value).lower()
        if bool_string in {"true", "false"}:
            return str(value).lower() == "true"
        else:
            raise ValidationError(f"Invalid boolean input: {bool_string = }")

    @staticmethod
    def remove_dot_from_string(value: str) -> str:
        """
        Removes all dots from a string except for "jr." and "sr.".

        Args:
            value (str): The input string.

        Returns:
            str: The string with dots removed.
        """
        return str(value).replace(".", "")

    @staticmethod
    def remove_punctuations(value: str) -> str:
        """
        Removes all punctuations from a string.

        Args:
            value (str): The input string.

        Returns:
            str: The string with punctuations removed.
        """
        # Remove punctuation using the translation table
        return str(value).translate(STRING_TRANSLATION_TABLE)

    @staticmethod
    def remove_all_digits(value: str) -> str:
        """
        Removes all digits from a string.

        Args:
            value (str): The input string.

        Returns:
            str: The string with digits removed.
        """
        # Remove digits using the translation table
        return str(value).translate(DIGIT_TRANSLATION_TABLE)

    @staticmethod
    def remove_punctuations_except_plus(value: str) -> str:
        """
        Removes all punctuations from a string except plus.

        Args:
            value (str): The input string. (Possible Phonenumber)

        Returns:
            str: The string with punctuations and spaces except + removed.
        """
        return re.sub(r"[^+\d]", "", str(value).replace(" ", ""))

    @staticmethod
    def remove_all_spaces(value: str) -> str:
        """
        Removes all spaces from a string.

        Args:
            value (str): The input string.

        Returns:
            str: The string with spaces removed.
        """
        return re.sub(r"\s", "", str(value))

    @staticmethod
    def convert_to_lowercase(value: str) -> str:
        """
        Converts a string to lowercase.

        Args:
            value (str): The input string.

        Returns:
            str: The lowercase string.
        """
        return str(value).lower()

    @staticmethod
    def convert_to_uppercase(value: str) -> str:
        """
        Converts a string to uppercase.

        Args:
            value (str): The input string.

        Returns:
            str: The uppercase string.
        """
        return str(value).upper()

    @staticmethod
    def convert_to_titlecase(value: str) -> str:
        """
        Converts a string to titlecase.

        Args:
            value (str): The input string.

        Returns:
            str: The titlecase string.
        """
        return str(value).title()

    @staticmethod
    def replace_ii_with_II(value: str) -> str:
        """
        Replaces "ii" with "II" in a string.

        Args:
            value (str): The input string.

        Returns:
            str: The string with "ii" replaced by "II".
        """
        return re.sub(r"\bii\b", "II", str(value))

    @staticmethod
    def convert_jr_to_Junior(value: str) -> str:
        """
        Replaces "jr." with "Junior." in a string.

        Args:
            value (str): The input string.

        Returns:
            str: The string with "jr." replaced by "Junior.".
        """
        return str(value).replace("jr.", "junior ")

    @staticmethod
    def convert_sr_to_Senior(value: str) -> str:
        """
        Replaces "sr." with "Senior." in a string.

        Args:
            value (str): The input string.

        Returns:
            str: The string with "sr." replaced by "Senior.".
        """
        return str(value).replace("sr.", "senior ")

    @staticmethod
    def parse_date_from_string(
        value: str, date_order_tuple: tuple, return_datetime: bool = False
    ) -> str | datetime | NotImplementedError | parser.ParserError:
        """
        Parses a date from a string using a specified date order.

        Args:
            value (str): The input string representing the date.
            date_order_tuple (tuple): The tuple specifying the order of date components (day, month, year).
            return_datetime (bool, optional): Whether to return a datetime object instead of a string date.
                Defaults to False.

        Returns:
            str | datetime: The parsed date as a string or datetime object.

        Raises:
            NotImplementedError: If the date order tuple is invalid.
            parser.ParserError: If the input string cannot be parsed as a date.
        """
        logger.debug(f"In parse_date_from_string received: {value = } | {date_order_tuple = }")
        error_message = f"({type(value)}, {value}) | {date_order_tuple = } | {return_datetime = }"

        try:
            value = str(value)
            day_first = date_order_tuple.index(CalendarDateComponents.DAY.value) < date_order_tuple.index(
                CalendarDateComponents.MONTH.value
            )
            year_first = date_order_tuple.index(CalendarDateComponents.YEAR.value) < date_order_tuple.index(
                CalendarDateComponents.MONTH.value
            )
        except ValueError as value_err:
            err = NotImplementedError(f"Invalid `date_order` tuple | {date_order_tuple = } | {value_err = }")
            logger.exception(f"{str(err) = }")
            raise err

        try:
            parsed_datetime = parser.parse(value, dayfirst=day_first, yearfirst=year_first)
        except parser.ParserError as err:
            logger.exception(f"{str(err) = } | DEBUG: {error_message}")
            raise ValidationError(f"Invalid date passed: {str(err)}")
        else:
            if return_datetime is True:
                return parsed_datetime
            else:
                return str(parsed_datetime.date())

    @staticmethod
    def extract_digits_from_string(value: str):
        """
        Extracts only the digits from a string.

        Args:
            value (str): The input string.

        Returns:
            str: The string containing only the digits.
        """
        return re.sub(r"\D", "", str(value))

    @staticmethod
    def extract_currency_from_amount(value: str) -> str:
        """
        Extracts the currency symbol from an amount string.

        Args:
            value (str): The input amount string.

        Returns:
            str: The extracted currency symbol.
        """
        match = re.search(r"[^\d.,\s]+", str(value))
        if match:
            return match.group()
        else:
            return ""

    @staticmethod
    def remove_currency_from_amount(value: str) -> str | ValidationError:
        """
        Removes currency symbols and separators from an amount string.

        Args:
            value (str): The input amount string.

        Returns:
            str: The amount string with currency symbols and separators removed.
            ValidationError: if amount is invalid or negative
        """
        _amount = re.sub(r"[^\d.-]", "", str(value))
        match = re.search(r"(-)?0*([1-9])", _amount)

        if match:
            hyphen = match.group(1) if match.group(1) else ""
            non_zero_digit = match.group(2)
            _amount = f"{hyphen}{non_zero_digit}{_amount[match.end():]}"

        try:
            amount = float(_amount)
            if amount > 0:
                return str(amount)
            else:
                raise ValidationError(f"Amount {str(amount)} should not be negative")

        except ValueError:
            raise ValidationError(f"Failed to parse amount {str(_amount)}")

    @staticmethod
    def extract_phone_number(value: str) -> str | ValidationError:
        """
        Validates and Extracts the 10 digit phone number from a phone number string.

        Args:
            value (str): The input phone number string.

        Returns:
            str: The extracted phone number
        """
        try:
            cleaned_number = Transformer.remove_punctuations_except_plus(value=value)
            if len(cleaned_number) == 10:  # Edge Case "9876543210"
                if cleaned_number.startswith("0"):  # Edge Case "0987654321"
                    raise ValidationError("Invalid phone number")
                else:
                    return cleaned_number
            elif len(cleaned_number) == 11 and cleaned_number.startswith("0"):  # Edge Case "09876543210"
                return cleaned_number.removeprefix("0")

            else:
                phone_number = phonenumbers.parse(number=cleaned_number)

        except phonenumbers.NumberParseException as err:
            # Raise an error if the phone number is invalid
            raise ValidationError(f"{cleaned_number}: Invalid phone number | {str(err)}")

        else:
            return str(phone_number.national_number)

    @staticmethod
    def extract_country_code(value: str) -> str | ValidationError:
        """
        Extracts the country code from a phone number string.

        Args:
            value (str): The input phone number string.

        Returns:
            str: The extracted country code.
        """
        try:
            cleaned_number = Transformer.remove_punctuations_except_plus(value=value)
            phone_number = phonenumbers.parse(number=cleaned_number)

        except phonenumbers.NumberParseException:
            # Raise an error if the phone number is invalid
            raise ValidationError(f"Invalid country code in phone_number = {value}")

        else:
            return str(phone_number.country_code)
