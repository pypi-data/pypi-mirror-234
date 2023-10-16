import os
import importlib
import support_toolbox.utils.helper as utils


def main():
    print("\nWelcome to the Support Toolbox!")

    while True:
        # Get the absolute path to the 'support_toolbox' package directory
        package_dir = os.path.dirname(os.path.abspath(__file__))

        # List available tools
        tools = [f[:-3] for f in os.listdir(package_dir) if f.endswith('.py') and f != '__init__.py' and f != 'main.py' and f != 'helper.py']

        # Display the available tools
        print("\nAvailable tools:")
        for idx, tool in enumerate(tools, start=1):
            print(f"{idx}. {tool}")

        # Ask the user to select a tool
        selection = input("\nEnter the number corresponding with the tool you want to use, or 'q' to quit: ")

        if selection == 'q':
            break

        try:
            selected_tool = tools[int(selection) - 1]

            # Check if the tokens for the selected tool exist and set them up if needed
            utils.check_tokens(selected_tool)

            module = importlib.import_module(f"support_toolbox.{selected_tool}")
            module.run()
        except (ValueError, IndexError):
            print("Invalid selection. Please enter a valid number.")


if __name__ == "__main__":
    main()
