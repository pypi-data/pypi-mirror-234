import os
import sys
import yaml

class ProjectConfigManager:
    def __init__(self, project_name, project_env='prod'):
        self.project_name = project_name
        self.project_env = project_env

        yaml_fn = os.path.expanduser(f"~/.config/{self.project_name}/{self.project_name}_{self.project_env}.yaml")
        
        if not os.path.exists(yaml_fn):
            raise Exception(f"\n\n\nThe expected yaml config file has not been detected in the expected location: {yaml_fn}")
        
        self.config_file_path = yaml_fn
        

    def get_config(self):
        """
        Load the project configuration from the YAML file.
        """
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, "r") as file:
                return yaml.safe_load(file)
        else:
            return {}

    def set_config(self, username, access_key, secret_access_key):
        """
        Save the project configuration to the YAML file.
        """
        config = {
            "username": username,
            "access_key": access_key,
            "secret_access_key": secret_access_key,
        }

        with open(self.config_file_path, "w") as file:
            yaml.dump(config, file, default_flow_style=False)

    def clear_config(self):
        """
        Remove the project configuration file.
        """
        if os.path.exists(self.config_file_path):
            os.remove(self.config_file_path)

def main(project_name=None):
    config_manager = ProjectConfigManager(project_name)

    while True:
        print("1. Set project configuration")
        print("2. Get project configuration")
        print("3. Clear project configuration")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            access_key = input("Enter access key: ")
            secret_access_key = input("Enter secret access key: ")
            config_manager.set_config(username, access_key, secret_access_key)
            print("Configuration saved.")
        elif choice == "2":
            config = config_manager.get_config()
            if config:
                print("Project Configuration:")
                print(f"Username: {config['username']}")
                print(f"Access Key: {config['access_key']}")
                print(f"Secret Access Key: {config['secret_access_key']}")
            else:
                print("No configuration found.")
        elif choice == "3":
            config_manager.clear_config()
            print("Configuration cleared.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("The first argument to this script must be a project_name, with a directory named as such under ~/.config, then the second argument must be the project_environment (ie: prod or sandbox-A), which combined with the project_name, specifies the configuration yaml file to be parsed.  In this case: ~/.config/ARG[1]/ARG[1]_ARG[2].yaml ")
    
    project_name = sys.argv[1]
    project_env = sys.argv[2]
    main(project_name, project_env)
