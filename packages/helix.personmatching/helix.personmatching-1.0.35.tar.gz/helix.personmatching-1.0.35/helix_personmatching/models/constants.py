from helix_personmatching.models.attribute_entry import AttributeEntry


class Attribute:
    # Rule
    RULE_ID: AttributeEntry = AttributeEntry(name="rule_id")
    RULE_NAME: AttributeEntry = AttributeEntry(name="rule_name")
    RULE_DESC: AttributeEntry = AttributeEntry(name="rule_desc")
    RULE_SCORE: AttributeEntry = AttributeEntry(name="rule_score")

    # FHIR Person or Patient attributes
    ID: AttributeEntry = AttributeEntry(name="id_")
    META_SECURITY_CLIENT_SLUG: AttributeEntry = AttributeEntry(
        name="meta_security_client_slug", exact_only=True
    )
    NAME_USE: AttributeEntry = AttributeEntry(
        name="name_use"
    )  # required, "usual | official | temp | nickname | anonymous | old | maiden"
    NAME_TEXT: AttributeEntry = AttributeEntry(name="name_text")
    NAME_GIVEN: AttributeEntry = AttributeEntry(name="name_given", nick_name_match=True)
    NAME_MIDDLE: AttributeEntry = AttributeEntry(name="name_middle")
    NAME_MIDDLE_INITIAL: AttributeEntry = AttributeEntry(name="name_middle_initial")
    NAME_FAMILY: AttributeEntry = AttributeEntry(name="name_family")
    TELECOM_SYSTEM: AttributeEntry = AttributeEntry(
        name="telecom_system", exact_only=True
    )  # required, "phone | fax | email | pager | url | sms | other"
    TELECOM_USE: AttributeEntry = AttributeEntry(
        name="telecom_use", exact_only=True
    )  # required, "home | work | temp | old | mobile"
    TELECOM_VALUE: AttributeEntry = AttributeEntry(
        name="telecom_value", exact_only=True
    )
    GENDER: AttributeEntry = AttributeEntry(name="gender")
    BIRTH_DATE: AttributeEntry = AttributeEntry(name="birth_date", exact_only=True)
    ADDRESS_USE: AttributeEntry = AttributeEntry(
        name="address_use", exact_only=True
    )  # required, "home | work | temp | old | billing"
    ADDRESS_TYPE: AttributeEntry = AttributeEntry(
        name="address_type", exact_only=True
    )  # required, "postal | physical | both"
    ADDRESS_LINE_1: AttributeEntry = AttributeEntry(name="address_line_1")
    ADDRESS_LINE_2: AttributeEntry = AttributeEntry(name="address_line_2")
    ADDRESS_CITY: AttributeEntry = AttributeEntry(name="address_city")
    ADDRESS_STATE: AttributeEntry = AttributeEntry(
        name="address_state", exact_only=True
    )
    ADDRESS_POSTAL_CODE: AttributeEntry = AttributeEntry(
        name="address_postal_code", exact_only=True
    )
    ADDRESS_POSTAL_CODE_FIRST_FIVE: AttributeEntry = AttributeEntry(
        name="address_postal_code_first_five", exact_only=True
    )
    ADDRESS_COUNTRY: AttributeEntry = AttributeEntry(name="address_country")
    ACTIVE: AttributeEntry = AttributeEntry(name="active", exact_only=True)
    LINK_TARGET: AttributeEntry = AttributeEntry(name="link_target", exact_only=True)
    LINK_ASSURANCE: AttributeEntry = AttributeEntry(
        name="link_assurance", exact_only=True
    )  # required, "level1 | level2 | level3 | level4"

    # other attributes specifics, needs to be parsed
    EMAIL: AttributeEntry = AttributeEntry(
        name="email", exact_only=True
    )  # WHEN telecom.system = "email"
    EMAIL_USERNAME: AttributeEntry = AttributeEntry(
        name="email_username", exact_only=True
    )  # email username, AttributeEntrying before the "@"

    PHONE: AttributeEntry = AttributeEntry(
        name="phone", exact_only=True
    )  # WHEN telecom.system = "phone"
    PHONE_AREA: AttributeEntry = AttributeEntry(
        name="phone_area", exact_only=True
    )  # phone area number (first 3 digit)
    PHONE_LOCAL: AttributeEntry = AttributeEntry(
        name="phone_local", exact_only=True
    )  # phone local number (middle 3 digit)
    PHONE_LINE: AttributeEntry = AttributeEntry(
        name="phone_line", exact_only=True
    )  # phone line number (last 4 digit)

    BIRTH_DATE_YEAR: AttributeEntry = AttributeEntry(
        name="birth_date_year", exact_only=True
    )  # YYYY from birthDate
    BIRTH_DATE_MONTH: AttributeEntry = AttributeEntry(
        name="birth_date_month", exact_only=True
    )  # MM from birthDate
    BIRTH_DATE_DAY: AttributeEntry = AttributeEntry(
        name="birth_date_day", exact_only=True
    )  # DD from birthDate

    ADDRESS_LINE_1_ST_NUM: AttributeEntry = AttributeEntry(name="address_line_1_st_num")

    # this is a "calculate-on-the-fly" attribute,
    #   IS_ADULT_TODAY = (today's Date - birthDate) >= 18 years old
    IS_ADULT_TODAY: AttributeEntry = AttributeEntry(
        name="is_adult_today", exact_only=True
    )

    # ssn can be under the identifier array, identifier.value
    #   WHEN identifier.system = "http://hl7.org/fhir/sid/us-ssn"
    SSN: AttributeEntry = AttributeEntry(name="ssn", exact_only=True)
    SSN_LAST4: AttributeEntry = AttributeEntry(name="ssn_last4", exact_only=True)

    # Scores
    SCORE: AttributeEntry = AttributeEntry(name="score")
    TOTAL_SCORE: AttributeEntry = AttributeEntry(name="total_score")
    MAX_POSSIBLE_SCORE: AttributeEntry = AttributeEntry(name="max_possible_score")
