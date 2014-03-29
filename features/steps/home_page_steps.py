from behave import given, when, then


@given('we have a Flaskage-based application setup')
def given_we_have_application(context):
    assert context.client and context.ctx


@when('I load the home page at "{url_path}"')
def when_load_home_page(context, url_path):
    context.response = context.client.get(url_path)
    assert context.response


@then('ensure the word "{expected_word}" is displayed')
def then_ensure_word_displayed(context, expected_word):
    assert expected_word.encode('u8') in context.response.data
