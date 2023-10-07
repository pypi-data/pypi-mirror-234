""" Test function of luhn's Formula """

from src.luhnformula import luhnformula as lf


def test_checksum():
    """ Test function luhn's Formula checksum"""
    assert lf.checksum('120027016') == 0
    assert lf.checksum('79927398713') == 0
    assert lf.checksum('00717324800068') == 0
    assert lf.checksum('01724359300070') == 0
    assert lf.checksum('74987198400029') == 0
    assert lf.checksum('123456789012345678906') == 0
    assert lf.checksum('12345678901234567890123459') == 0


def test_validate():
    """ Test function luhn's Formula is valid"""
    assert lf.isvalid('1') is False
    assert lf.isvalid('7992739Z713') is False
    assert lf.isvalid('1234567890') is False
    assert lf.isvalid('120027016') is True
    assert lf.isvalid('79927398713') is True
    assert lf.isvalid('00717324800068') is True
    assert lf.isvalid('01724359300070') is True
    assert lf.isvalid('749871984000299') is True
    assert lf.isvalid('123456789012345678906') is True
    assert lf.isvalid('12345678901234567890123459') is True


def test_getcheckdigit():
    """ Test function luhn's Formula getcheckdigit with exception"""
    try:
        lf.getcheckdigit('34F4')
    except ValueError:
        pass
    assert lf.getcheckdigit('12002701') == '6'
    assert lf.getcheckdigit('7992739871') == '3'
    assert lf.getcheckdigit('0071732480006') == '8'
    assert lf.getcheckdigit('0172435930007') == '0'
    assert lf.getcheckdigit('74987198400029') == '9'
    assert lf.getcheckdigit('12345678901234567890') == '6'
    assert lf.getcheckdigit('1234567890123456789012345') == '9'


def test_addcheckdigit():
    """ Test function luhn's Formula addcheckdigit with exception"""
    try:
        lf.addcheckdigit('34F4')
    except ValueError:
        pass
    assert lf.addcheckdigit('12002701') == '120027016'
    assert lf.addcheckdigit('7992739871') == '79927398713'
    assert lf.addcheckdigit('0071732480006') == '00717324800068'
    assert lf.addcheckdigit('0172435930007') == '01724359300070'
    assert lf.addcheckdigit('74987198400029') == '749871984000299'
    assert lf.addcheckdigit('12345678901234567890') == '123456789012345678906'
    assert lf.addcheckdigit('1234567890123456789012345')\
        == '12345678901234567890123459'
