from behave import given, when, then


@given('we have a Flaskage-based application setup')  # noqa
def step_impl(context):
    assert context.client and context.ctx


@when('I load the home page at "{url_path}"')  # noqa
def step_impl(context, url_path):
    context.response = context.client.get(url_path)
    assert context.response


@then('ensure the word "{expected_word}" is displayed')  # noqa
def step_impl(context, expected_word):
    assert expected_word.encode('u8') in context.response.data
