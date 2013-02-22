@echo off

echo Checking if all tests are successfull...

:: Checks if the parameter check works
fc /b .\test\param_actual .\test\param_expected > nul
IF errorlevel 1 (
	echo The parameter check needs some more work
) ELSE (
	echo The parameter check is working properly
)
:syntax_check
:: Checks if the syntax check works
fc /b .\test\syntax_actual .\test\syntax_expected > nul
IF errorlevel 1 (
	echo The syntax check needs some more work
) ELSE (
	echo The parameter check is working properly
)

:logic_check
:: Checks if the logic check works
fc /b .\test\logic_actual .\test\logic_expected > nul
IF errorlevel 1 (
	echo The logic check needs some more work
) ELSE (
	echo The parameter check is working properly
)

