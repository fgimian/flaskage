Feature: Home page loads and shows the correct information

  Scenario: The homepage loads
    Given we have a Flaskage-based application setup
     When I load the home page at "/"
     Then ensure the word "Flaskage" is displayed

  Scenario: The PyJade version of the homepage loads
    Given we have a Flaskage-based application setup
     When I load the home page at "/pyjade"
     Then ensure the word "Flaskage" is displayed
