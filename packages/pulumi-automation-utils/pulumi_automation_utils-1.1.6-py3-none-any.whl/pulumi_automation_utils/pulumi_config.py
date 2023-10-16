#!/usr/bin/env python3

from datetime import datetime, timedelta
import json
import os
import subprocess
import sys

from pulumi_automation_utils import common
from pulumi_automation_utils.environment import Environment
from pulumi_automation_utils.login_config import LoginConfig

class PulumiConfig:
    def __init__(self,
                 login_config : LoginConfig,
                 yaml_vars : dict,
                 repo_root : str=""
                 ):
        self.login_config = login_config
        self.repo_root = repo_root
        self.yaml_vars = yaml_vars
        self.environment_vars = os.environ.copy()
        self.__set_project_info()
        self.__set_pulumi_vars()
        self.__set_environment()
        self.__set_storage_account_information()
        self.__set_key_vault_information()
        self.__set_location_information()

    def configure_pulumi(self):
        if not self.login_config.is_logged_in():
            self.login_config.login_to_azure()

        self.__setup_storage_account()
        self.__setup_storage_container()
        self.__setup_encryption_key()
        self.__setup_sas_token()
        self.__setup_virtual_network()

        self.environment_vars["AZURE_STORAGE_ACCOUNT"] = self.storage_account_name
        self.environment_vars["AZURE_STORAGE_SAS_TOKEN"] = self.sas_token
        if self.environment == Environment.SANDBOX:
            self.environment_vars["ARM_ENVIRONMENT"] = "public"
        else:
            self.environment_vars["ARM_ENVIRONMENT"] = "usgovernment"
        self.environment_vars["PULUMI_CONFIG_PASSPHRASE"] = ""

        # storage account URL will change in usgovernment
        self.__run_pulumi_command("/pulumi/bin/pulumi login azblob://" + self.storage_container_name + "?storage_account=" + self.storage_account_name + " --non-interactive")
        # Key Vault URL will change in usgovernment
        command_succeeded = False
        while not command_succeeded:
            try: 
                self.__run_pulumi_command("/pulumi/bin/pulumi stack select --stack " + self.stack_name + " --create --secrets-provider azurekeyvault://" + self.key_vault_name + ".vault.azure.net/keys/" + self.encryption_key_name + " --non-interactive")
                command_succeeded = True
            except subprocess.CalledProcessError:
                pass

        self.__pulumi_set_config(namespace="azure", 
                                 config_variable_name="skipProviderRegistration", 
                                 value="true")
        self.__pulumi_set_config(namespace="azure-native", 
                                 config_variable_name="location", 
                                 value=self.location)
        self.__pulumi_set_config(namespace=self.project_name, 
                                 config_variable_name="location", 
                                 value=self.location)
        self.__pulumi_set_config(namespace=self.project_name, 
                                 config_variable_name="environment", 
                                 value=self.environment.name)
        self.__pulumi_set_config(namespace=self.project_name, 
                                 config_variable_name="subscription", 
                                 value=self.login_config.get_subscription())
        if "key_vault_name" not in self.pulumi_vars.keys():
            self.__pulumi_set_config(namespace=self.project_name, 
                                     config_variable_name="key_vault_name", 
                                     value=self.key_vault_name)
        if "key_vault_id" not in self.pulumi_vars.keys():
            self.__pulumi_set_config(namespace=self.project_name, 
                                     config_variable_name="key_vault_id", 
                                     value=common.get_key_vault_id(login_config=self.login_config, key_vault_name=self.key_vault_name))
        if "resource_group_name" not in self.pulumi_vars.keys():
            self.__pulumi_set_config(namespace=self.project_name, 
                                     config_variable_name="resource_group_name", 
                                     value=common.get_resource_group_from_subscription(login_config=self.login_config))
            if "resource_group_id" not in self.pulumi_vars.keys():
                self.__pulumi_set_config(namespace=self.project_name, 
                                        config_variable_name="resource_group_id", 
                                        value="/subscriptions/" + self.login_config.get_subscription() + "/resourceGroups/" + common.get_resource_group_from_subscription(login_config=self.login_config))
        elif "resource_group_id" not in self.pulumi_vars.keys():
            self.__pulumi_set_config(namespace=self.project_name, 
                                    config_variable_name="resource_group_id", 
                                    value="/subscriptions/" + self.login_config.get_subscription() + "/resourceGroups/" + self.pulumi_vars["resource_group_name"])
        if "storage_account_name" not in self.pulumi_vars.keys():
            self.__pulumi_set_config(namespace=self.project_name, 
                                     config_variable_name="storage_account_name", 
                                     value=self.storage_account_name)
        if "storage_account_id" not in self.pulumi_vars.keys():
            self.__pulumi_set_config(namespace=self.project_name, 
                                     config_variable_name="storage_account_id", 
                                     value=common.get_storage_account_id(login_config=self.login_config, storage_account_name=self.storage_account_name))
        # Iterate through each variable under 'pulumi' YAML config section to apply it
        for var in self.pulumi_vars.keys():
            self.__pulumi_set_config(namespace=self.project_name, 
                                     config_variable_name=var, 
                                     value=self.pulumi_vars[var])
        # Iterate through each variable under 'pulumi-secrets' YAML config section to 
        # retrieve the secret from the Azure Key Vault and apply it as a secret to the 
        # pulumi configuration
        for secret_name in self.pulumi_secret_vars.keys():
            secret_val = common.get_secret_from_key_vault(login_config=self.login_config, 
                                                          key_vault_name=self.key_vault_name, 
                                                          secret_name=self.pulumi_secret_vars[secret_name])
            self.__pulumi_set_config(namespace=self.project_name, 
                                     config_variable_name=secret_name, 
                                     value=secret_val, 
                                     is_secret=True)

    def deploy_pulumi(self):
        command = "/pulumi/bin/pulumi up"
        print(command)
        popen = subprocess.Popen(
                    command, 
                    stdin=sys.stdin,
                    stdout=sys.stdout,
                    stderr=sys.stderr, 
                    env=self.environment_vars, 
                    cwd=self.pulumi_directory, 
                    shell=True, 
                    universal_newlines=True)
        return_code = popen.wait()
        if return_code and return_code != 255:
            raise subprocess.CalledProcessError(return_code, command)
        return return_code
    
    def get_container_host(self):
        try:
            fqdn = self.__run_pulumi_command("pulumi stack output --stack " + self.stack_name + " container_fqdn", is_secret=True)
            if fqdn is not None and fqdn != "":
                return fqdn[0].strip()
        except subprocess.CalledProcessError:
            try: 
                ip_addr = self.__run_pulumi_command("pulumi stack output --stack " + self.stack_name + " container_ip", is_secret=True)
                return ip_addr[0].strip()
            except subprocess.CalledProcessError as e:
                print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.stderr))
                print("Unable to retrieve FQDN or IP from created Azure Container Instance. Exiting...")
                exit()
    def get_encryption_key_name(self):
        return self.encryption_key_name
    
    def get_file_share_name(self):
        return self.file_share_name
    
    def get_key_vault_name(self) -> str:
        return self.key_vault_name
    
    def get_location(self):
        return self.location
    
    def get_pulumi_var(self, var_name : str):
        value = None
        if var_name in self.pulumi_vars:
            value = self.pulumi_vars[var_name]
        return value

    def get_sas_token(self):
        return self.sas_token
    
    def get_sas_token_name(self):
        return self.sas_token_name
    
    def get_storage_account_name(self):
        return self.storage_account_name
    
    def get_storage_account_sku(self):
        return self.storage_account_sku
    
    def get_storage_container_name(self):
        return self.storage_container_name

    def __pulumi_set_config(self, namespace : str, config_variable_name : str, value : str, is_secret : bool=False):
        if namespace is not None and namespace != "":
            pass
        else:
            print("namespace was not provided to 'pulumi config " + namespace + ":" + config_variable_name + "' command. Skipping...")
            return
        if config_variable_name is not None and config_variable_name != "":
            pass
        else:
            print("config_variable_name was not provided to 'pulumi config" + namespace + ":" + config_variable_name + "' command. Skipping...")
            return
        if value is not None and value != "":
            pass
        else:
            print("value was not provided to 'pulumi config " + namespace + ":" + config_variable_name + "' command. Skipping...")
            return

        if is_secret:
            self.__run_pulumi_command(command="/pulumi/bin/pulumi config set --secret " + namespace + ":" + config_variable_name + " " + str(value), 
                                      is_secret=True)
        else:
            self.__run_pulumi_command(command="/pulumi/bin/pulumi config set " + namespace + ":" + config_variable_name + " " + str(value) + " --plaintext")

    def __run_pulumi_command(self, command: str, is_secret : bool=False):
        output = None
        try:
            output = common.send_os_command(command=command, cwd=self.pulumi_directory, env=self.environment_vars, is_secret=is_secret)
        except subprocess.CalledProcessError as e:
            print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.stderr))
            raise subprocess.CalledProcessError(
                returncode=e.returncode, 
                cmd=e.cmd, 
                output=e.output, 
                stderr=e.stderr)
        return output

    def __set_project_info(self):
        self.project_name = None
        if "project_name" in self.yaml_vars:
            self.project_name = self.yaml_vars["project_name"]
        else:
            print("Project name was not found in YAML. Exiting...")
            exit

        self.stack_name = None
        if "stack_name" in self.yaml_vars:
            self.stack_name = self.yaml_vars["stack_name"]
        else:
            print("Stack name was not found in YAML. Exiting...")
            exit

        if "project_location" in self.yaml_vars:
            if self.repo_root is not None and self.repo_root != "":
                project_location = os.path.join(self.repo_root, self.yaml_vars["project_location"])
            else:
                project_location = self.yaml_vars["project_location"]
            self.pulumi_directory = os.path.abspath(project_location)
        else:
            self.pulumi_directory = os.path.abspath(os.path.join(os.curdir, "pulumi"))

        # Set the random value, useful in name randomization when setting up 
        # and tearing down numerous times quickly
        self.random_value = None
        if "random_value" in self.yaml_vars:
            self.random_value = self.yaml_vars["random_value"]

    def __set_environment(self):
        self.environment = Environment.SANDBOX
        if type(self.yaml_vars) is dict:
            if "environment" in self.yaml_vars:
                if self.yaml_vars["environment"].lower() == "zonec":
                    self.environment = Environment.ZONEC
                if self.yaml_vars["environment"].lower() == "zoneb":
                    self.environment = Environment.ZONEB
                if self.yaml_vars["environment"].lower() == "zonea":
                    self.environment = Environment.ZONEA
                if self.yaml_vars["environment"].lower() == "prod":
                    self.environment = Environment.PROD

    def __set_key_vault_information(self):
        self.key_vault_resource_group_name = None
        self.key_vault_name = None
        self.encryption_key_name = None
        if type(self.yaml_vars) is dict:
            if "key_vault" in self.yaml_vars:
                if "name" in self.yaml_vars["key_vault"]:
                    self.key_vault_name = self.yaml_vars["key_vault"]["name"]
                    if self.key_vault_name is not None and self.random_value is not None:
                        self.key_vault_name = self.key_vault_name + self.random_value
                else:
                    print("Name for Azure Key Vault not found in YAML. Exiting...")
                    exit
                if "resource_group" in self.yaml_vars["key_vault"]:
                    self.key_vault_resource_group_name = self.yaml_vars["key_vault"]["resource_group"]
                else:
                    self.key_vault_resource_group_name = common.get_resource_group_from_subscription(login_config=self.login_config)
                if "encryption_key" in self.yaml_vars["key_vault"]:
                    self.encryption_key_name = self.yaml_vars["key_vault"]["encryption_key"]
                else:
                    print("Name for pulumi encryption key not found in YAML. Exiting...")
                    exit
            else:
                print("No key vault was defined in the YAML config. Exiting...")
                exit

    def __set_location_information(self):
        self.location = None
        if type(self.yaml_vars) is dict:
            if "location" in self.yaml_vars.keys():
                self.location = self.yaml_vars["location"]
        if (self.location is None or self.location == ""):
            if "resource_group_name" in self.pulumi_vars:
                self.location = common.get_location_from_resource_group(
                    login_config=self.login_config, 
                    resource_group=self.pulumi_vars["resource_group_name"])
            else:
                self.location = common.get_location_from_resource_group(
                    login_config=self.login_config, 
                    resource_group=common.get_resource_group_from_subscription(
                                        login_config=self.login_config))

    def __set_pulumi_vars(self):
        # Dictionary of key/values for pulumi configuration
        self.pulumi_vars = {}
        # Dictionary of key/values values are names of secrets in AKV
        self.pulumi_secret_vars = {} 
        if type(self.yaml_vars) is dict:
            if "pulumi" in self.yaml_vars:
                for var_name in self.yaml_vars["pulumi"]:
                    self.pulumi_vars[var_name] = self.yaml_vars["pulumi"][var_name]
            if "pulumi_secrets" in self.yaml_vars:
                for var_name in self.yaml_vars["pulumi_secrets"]:
                    self.pulumi_secret_vars[var_name] = self.yaml_vars["pulumi_secrets"][var_name]

    def __set_storage_account_information(self):
        self.storage_account_resource_group_name = None
        self.file_share_name = None
        self.storage_account_name = None
        self.storage_account_sku = "Standard_LRS"
        self.storage_container_name = None
        self.sas_token_name = "pulumisas"
        if self.random_value is not None:
            self.sas_token_name = self.sas_token_name + self.random_value
        if type(self.yaml_vars) is dict:
            if "storage_account" in self.yaml_vars:
                if "name" in self.yaml_vars["storage_account"]:
                    self.storage_account_name = self.yaml_vars["storage_account"]["name"]
                    if self.storage_account_name is not None and self.random_value is not None:
                        self.storage_account_name = self.storage_account_name + self.random_value
                else:
                    print("Storage account name not defined in YAML. Exiting...")
                    exit
                if "resource_group" in self.yaml_vars["storage_account"]:
                    self.storage_account_resource_group_name = self.yaml_vars["storage_account"]["resource_group"]
                else:
                    self.storage_account_resource_group_name = common.get_resource_group_from_subscription(login_config=self.login_config)
                if "sku" in self.yaml_vars["storage_account"]:
                    self.storage_account_sku = self.yaml_vars["storage_account"]["sku"]
                if "storage_container" in self.yaml_vars["storage_account"]:
                    self.storage_container_name = self.yaml_vars["storage_account"]["storage_container"]["name"]
                    if self.storage_container_name is not None and self.random_value is not None:
                        self.storage_container_name = self.storage_container_name + self.random_value
                else:
                    print("Storage account name not defined in YAML. Exiting...")
                    exit
                if "sas_token" in self.yaml_vars["storage_account"]:
                    if "name" in self.yaml_vars["storage_account"]["sas_token"]:
                        self.sas_token_name = self.yaml_vars["storage_account"]["sas_token"]["name"]
                        if self.sas_token_name is not None and self.random_value is not None:
                            self.sas_token_name = self.sas_token_name + self.random_value
                    else:
                        print("SAS token name not defined in YAML. Using \"" + self.sas_token_name + "\" as the name of the secret when storing in the AKV.")
                else:
                    print("SAS token name not defined in YAML. Using \"" + self.sas_token_name + "\" as the name of the secret when storing in the AKV.")
            else:
                print("No storage account defined in the YAML config. Exiting...")
                exit

    def __setup_encryption_key(self):
        if self.key_vault_name and self.encryption_key_name:
            self.__setup_key_vault()
            key_exists = False
            try:
                az_cli_command = "az keyvault key show --name " + self.encryption_key_name + " --vault-name " + self.key_vault_name
                output = json.loads(common.sanitize_stdout_for_json(common.send_os_command(az_cli_command)))
                if "key" in output and "kid" in output["key"]:
                    key_exists = True
                    print("Key " + self.encryption_key_name + " exists in key vault " + self.key_vault_name + ". Nothing to do.")
            except subprocess.CalledProcessError:
                pass
            if not key_exists:
                az_cli_command = "az keyvault key create --name " + self.encryption_key_name + " --vault-name " + self.key_vault_name
                output = json.loads(common.sanitize_stdout_for_json(common.send_os_command(az_cli_command)))
        else:
            print("PulumiConfig: One of the following variables was not defined. Exiting...")
            print("self.key_vault_name: " + str(self.key_vault_name))
            print("self.encryption_key_name: " + str(self.encryption_key_name))
            exit()

    def __setup_key_vault(self):
        if self.key_vault_name and self.key_vault_resource_group_name:
            key_vault_exists = common.does_key_vault_exist(login_config=self.login_config, key_vault_name=self.key_vault_name)
            if not key_vault_exists:
                az_cli_command = "az keyvault check-name --name " + self.key_vault_name
                output = json.loads(common.sanitize_stdout_for_json(common.send_os_command(az_cli_command)))
                if "nameAvailable" in output:
                    if output["nameAvailable"] == True:
                        try:
                            az_cli_command = "az keyvault create --name " + self.key_vault_name + " --resource-group " + self.key_vault_resource_group_name + " --location " + self.location
                            output = common.send_os_command(az_cli_command)
                        except subprocess.CalledProcessError as e:
                            print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
                            print("Could not create Azure Key Vault with name: " + self.key_vault_name)
                            print("Please choose a new name for the Azure Key Vault.")
                            exit
                    else:
                        print("Cannot create a key vault with the name: " + self.key_vault_name)
                        exit()
                else:
                    print("nameAvailable was not found in JSON output returned from az cli command.")
                    exit()
            else:
                print("Key vault " + self.key_vault_name + " exists. Nothing to do.")
        else:
            print("PulumiConfig: One of the following variables was not defined. Exiting...")
            print("self.key_vault_name: " + str(self.key_vault_name))
            print("self.key_vault_resource_group_name: " + str(self.key_vault_resource_group_name))
            exit()

    def __setup_sas_token(self):
        if self.key_vault_name and self.sas_token_name:
            self.sas_token = common.get_secret_from_key_vault(login_config=self.login_config, 
                                                              key_vault_name=self.key_vault_name, 
                                                              secret_name=self.sas_token_name)
            if self.sas_token is not None:
                print("Using the current SAS from Azure Key Vault. Nothing to do.")
            else:
                start_date = datetime.utcnow().date().strftime("%Y-%m-%dT%H:%M:%SZ")
                expiration_date = (datetime.utcnow() + timedelta(days=7)).date().strftime("%Y-%m-%dT%H:%M:%SZ")
                az_cli_command = "az storage container generate-sas --account-name " + self.storage_account_name + " --name " + self.storage_container_name + " --permissions acdlrw --start " + start_date + " --expiry " + expiration_date + " --https-only --auth-mode login --as-user"
                sas_token = common.send_os_command(az_cli_command, is_secret=True)
                self.sas_token = ("".join(sas_token)).strip().replace('"', '')
                az_cli_command = "az keyvault secret set --name " + self.sas_token_name + " --vault-name " + self.key_vault_name + " --value " + self.sas_token + " --expires " + expiration_date
                output = common.send_os_command(az_cli_command)
        else:
            print("PulumiConfig: One of the following variables was not defined. Exiting...")
            print("self.key_vault_name: " + str(self.key_vault_name))
            print("self.sas_token_name: " + str(self.sas_token_name))
            exit()

    def __setup_storage_account(self):
        print("Setting up storage account for file share connected to Azure Container Instance.")
        if self.storage_account_resource_group_name and self.storage_account_name:
            az_cli_command = "az storage account list -g " + self.storage_account_resource_group_name
            output = json.loads(common.sanitize_stdout_for_json(common.send_os_command(az_cli_command)))
            storage_account_exists = False
            for account in output:
                if account["name"] == self.storage_account_name:
                    print("Storage account " + self.storage_account_name + " in resource group " + self.storage_account_resource_group_name + " already exists. Nothing to do.")
                    storage_account_exists = True
                    break
            if not storage_account_exists:
                print("Creating storage account " + self.storage_account_name + " in resource group " + self.storage_account_resource_group_name)
                az_cli_command = "az storage account create --name " + self.storage_account_name + " --resource-group " + self.storage_account_resource_group_name + " --location " + self.location + " --sku " + self.storage_account_sku + " --encryption-services blob"
                output = common.send_os_command(az_cli_command)
        else:
            print("PulumiConfig: One of the following variables was not defined. Exiting...")
            print("self.storage_account_resource_group_name: " + str(self.storage_account_resource_group_name))
            print("self.storage_account_name: " + str(self.storage_account_name))
            exit()

    def __setup_storage_container(self):
        if self.storage_account_resource_group_name and self.storage_account_name and self.storage_container_name:
            az_cli_command = "az storage container exists --account-name " + self.storage_account_name + " --auth-mode login --name " + self.storage_container_name
            output = json.loads(common.sanitize_stdout_for_json(common.send_os_command(az_cli_command)))
            container_exists = False
            if "exists" in output and output["exists"] == True:
                print("Storage container " + self.storage_container_name + " in storage account " + self.storage_account_name + " already exists. Nothing to do.")
                container_exists = True
            if not container_exists:
                print("Creating storage container " + self.storage_container_name + " in storage account " + self.storage_account_name + ".")
                az_cli_command = "az storage container create --account-name " + self.storage_account_name + " --name " + self.storage_container_name + " --auth-mode login"
                output = common.send_os_command(az_cli_command)
        else:
            print("PulumiConfig: One of the following variables was not defined. Exiting...")
            print("self.storage_account_resource_group_name: " + str(self.storage_account_resource_group_name))
            print("self.storage_account_name: " + str(self.storage_account_name))
            print("self.storage_container_name: " + str(self.storage_container_name))
            exit()

    def __setup_virtual_network(self):
        if "container_instance_public_ip" in self.pulumi_vars:
            if self.pulumi_vars["container_instance_public_ip"] == False:
                vnet_exists = False
                vnet_resource_group = None
                vnet_subnet = None
                if "container_instance_vnet_resource_group" in self.pulumi_vars:
                    vnet_resource_group = self.pulumi_vars["container_instance_vnet_resource_group"]
                else:
                    vnet_resource_group = common.get_resource_group_from_subscription(login_config=self.login_config)
                if "container_instance_subnet_name" in self.pulumi_vars:
                    vnet_subnet = self.pulumi_vars["container_instance_subnet_name"]
                else:
                    print("Could not locate container_instance_subnet_name in YAML config even though container_instance_public_ip is False.")
                    print("Need a VNET and SUBNET defined to connect container instance to private network. Exiting...")
                    exit()
                if "container_instance_vnet_name" in self.pulumi_vars:
                    vnet_name = self.pulumi_vars["container_instance_vnet_name"]
                    az_cli_command = "az network vnet list"
                    output = json.loads(common.sanitize_stdout_for_json(common.send_os_command(az_cli_command)))
                    for network in output:
                        if "name" in network and network["name"] == vnet_name:
                            print("VNET already exists. ")
                            vnet_exists = True
                            break
                        else:
                            print(network)
                    if not vnet_exists and vnet_name is not None and vnet_resource_group is not None and vnet_subnet is not None:
                        az_cli_command = "az network vnet create --name " + vnet_name + " --resource-group " + vnet_resource_group + " --address-prefix 10.0.0.0/16 --subnet-name " + vnet_subnet + " --subnet-prefixes 10.0.10.0/24"
                        output = json.loads(common.sanitize_stdout_for_json(common.send_os_command(az_cli_command)))
                        az_cli_command = "az network vnet subnet update --resource-group " + vnet_resource_group + " --name " + vnet_subnet + " --vnet-name " + vnet_name + " --delegations Microsoft.ContainerInstance/containerGroups"
                        output = json.loads(common.sanitize_stdout_for_json(common.send_os_command(az_cli_command)))
                    elif vnet_exists and vnet_resource_group is not None and vnet_subnet is not None:
                        az_cli_command = "az network vnet subnet show -g " + vnet_resource_group + " -n " + vnet_subnet + " --vnet-name " + vnet_name
                        try:
                            output = json.loads(common.sanitize_stdout_for_json(common.send_os_command(az_cli_command)))
                        except subprocess.CalledProcessError:
                            az_cli_command = "az network vnet subnet create -g " + vnet_resource_group + " --vnet-name " + vnet_name + " -n " + vnet_subnet + " --address-prefixes 10.0.10.0/24 --delegations Microsoft.ContainerInstance/containerGroups"
                            output = json.loads(common.sanitize_stdout_for_json(common.send_os_command(az_cli_command)))
                    else:
                        print("Could not setup the VNET and SUBNET for private networking on the container instance, please make sure all of the necessary vars are set in the YAML config.")
                else:
                    print("container_instance_vnet_name was not found in YAML config even though container_instance_public_ip is False.")
                    print("Need a VNET and SUBNET defined to connect container instance to private network. Exiting...")
                    exit()