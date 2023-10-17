import os
import argparse
import shutil

def create_project(project_name):
    # Create the project directory
    os.makedirs(project_name)

    # Create the runner.py file at the top level
    with open(os.path.join(project_name, "runner.py"), "w") as file:
        file.write("# Your runner code here")

    # Create the configurations folder at the top level
    os.makedirs(os.path.join(project_name, "configurations"))

    # Create the application-local.yml file
    with open(os.path.join(project_name, "configurations", "application-local.yml"), "w") as file:
        file.write("# Your local configuration here")

    # Create the application-dev.yml file
    with open(os.path.join(project_name, "configurations", "application-dev.yml"), "w") as file:
        file.write("# Your dev configuration here")

    # Create the application-stage.yml file
    with open(os.path.join(project_name, "configurations", "application-stage.yml"), "w") as file:
        file.write("# Your stage configuration here")

    print(f"Project '{project_name}' created successfully.")

def create_app(project_name, app_name):
    app_dir = os.path.join(project_name, app_name)

    # Create the app directory
    os.makedirs(app_dir)

    # Create subdirectories for models, flows, tests, service-clients, and assertions
    for subdir in ["models", "flows", "tests", "service-clients", "assertions"]:
        os.makedirs(os.path.join(app_dir, subdir))

    print(f"App '{app_name}' created in project '{project_name}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a project or app.")
    parser.add_argument("command", choices=["createproject", "createapp"], help="Command to run")
    parser.add_argument("name", help="Name of the project or app")

    args = parser.parse_args()

    if args.command == "createproject":
        create_project(args.name)
    elif args.command == "createapp":
        project_name = input("Enter the project name: ")
        create_app(project_name, args.name)
