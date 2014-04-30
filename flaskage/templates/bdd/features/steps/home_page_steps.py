# -*- coding: utf-8 -*-
from behave import given, when, then


@given('we have a Flaskage-based application setup')
def given_we_have_app(context):
    assert context.client and context.ctx


@when('I load the home page at "{url_path}"')
def when_load_home_page(context, url_path):
    context.response = context.client.get(url_path)
    assert context.response


@then('ensure the word "{expected_phrase}" is displayed')
def then_ensure_word_displayed(context, expected_phrase):
    assert expected_phrase.encode('u8') in context.response.data
