# -*- coding: utf-8 -*-
"""
    flaskage.features.steps.home_page_steps
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    BDD tests for home page of the Flaskage template application.

    :copyright: (c) 2014 Fotis Gimian.
    :license: MIT, see LICENSE for more details.
"""
from behave import given, when, then


@given('we have a Flaskage-based application setup')
def given_we_have_application(context):
    assert context.client and context.ctx


@when('I load the home page at "{url_path}"')
def when_load_home_page(context, url_path):
    context.response = context.client.get(url_path)
    assert context.response


@then('ensure the word "{expected_phrase}" is displayed')
def then_ensure_word_displayed(context, expected_phrase):
    assert expected_phrase.encode('u8') in context.response.data
