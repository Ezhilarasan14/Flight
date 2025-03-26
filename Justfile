# Default command: Lists all available 'just' recipes when run without arguments.
[private]
default:
    just --list

# Alias: 'just run python'; Runs the Flight Data Processor using uv.
@run-app:
	uv run python3 flight_data_processor.py

# Alias: 'just run test'; Runs pytest on the specified test file.
@run-test:
	uv run -m unittest test_flight_data_processor.py

# Alias: 'just run shell'; Starts a shell session within the uv virtual environment.
@run-shell:
	uv shell

@run-clean:
	find . -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Helper function to allow running various commands dynamically by passing arguments.
[private]
run $PARAM *OTHERPARAMS:
	#!/bin/zsh
	case $PARAM in 
		app) 
			# Runs the Finacle banking application.
			just run-app
		;;
		ipython) 
			# Launches an IPython shell.
			just run-ipython
		;;
		test) 
			# Executes pytest on the given test file.
			just run-test {{OTHERPARAMS}}
		;;
		shell)
			# Opens a shell within the uv virtual environment.
			just run-shell
		;;
		clean)
			# Opens a shell within the uv virtual environment.
			just run-clean
		;;
		*)
			# Displays an error message for invalid parameters.
			echo "Invalid parameter $PARAM when invoking just run"
	esac
