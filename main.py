from source import create_app

def main():
    """
    This is the main function that runs the web application.

    It imports the create_app function from the source module and calls it to create the Flask app.
    Then it checks if the script is being run directly and not imported as a module.
    If it is being run directly, it runs the app in debug mode.

    :return: None
    """
    app = create_app()

    if __name__ == '__main__':
        app.run(debug=True)

main()