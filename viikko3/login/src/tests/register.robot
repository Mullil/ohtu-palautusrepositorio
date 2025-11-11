*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  aaaa
    Set Password  AaAa1212
    Set Confirmation  AaAa1212
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  aa
    Set Password  AaAa1212
    Set Confirmation  AaAa1212
    Click Button  Register
    Register Should Fail With Message  too short username

Register With Valid Username And Too Short Password
    Set Username  aaaa
    Set Password  AaAa1
    Set Confirmation  AaAa1
    Click Button  Register
    Register Should Fail With Message  too short password

Register With Valid Username And Invalid Password
    Set Username  aaaa
    Set Password  AaAaaaaa
    Set Confirmation  AaAaaaaa
    Click Button  Register
    Register Should Fail With Message  password cannot only consist of letters

Register With Nonmatching Password And Password Confirmation
    Set Username  aaaa
    Set Password  AaAa1212
    Set Confirmation  AaAa1213
    Click Button  Register
    Register Should Fail With Message  passwords do not match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  kalle123
    Set Confirmation  kalle123
    Click Button  Register
    Register Should Fail With Message  username already in use

*** Keywords ***

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Confirmation
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page