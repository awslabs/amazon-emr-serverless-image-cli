from amazon_emr_serverless_image_cli.validation_tool.validation_tests import base_check


class CheckFiles(base_check.BaseCheck):

    def __init__(self, file_structure_list, file_structure, docker_cmd, docker_image_uri, env_vars, image_env_vars, log):
        self.file_structure_list = file_structure_list
        self.file_structure = file_structure
        self.docker_cmd = docker_cmd
        self.docker_image_uri = docker_image_uri
        self.env_vars = env_vars
        self.image_env_vars = {}
        self.log = log

        for env in image_env_vars:
            var, val = env.split("=")
            self.image_env_vars[var] = val

    def check(self):
        file_system_test = True
        for file_structure_name in self.file_structure_list:
            file_structure = [structure for structure in self.file_structure
                              if structure.name == file_structure_name][0]
            name = file_structure.name

            if file_structure.env_var is None:
                path = file_structure.relative_location
            else:
                env_var = [env for env in self.env_vars if env.key == file_structure.env_var][0]
                path = self.image_env_vars[env_var.env_name] + file_structure.relative_location

            file_prefixes = file_structure.file_prefixes
            if not self.match(name, path, file_prefixes):
                file_system_test = False
        return file_system_test

    def match(self, name, path, file_prefixes):
        local_test_pass = True
        docker_log = self.docker_cmd.docker_list_files(self.docker_image_uri, path)
        files = docker_log.decode().split('\n')[1:]
        for prefix in file_prefixes:
            is_match = False
            for file in files:
                if file.startswith(prefix):
                    is_match = True
                    break
            if not is_match:
                self.log.error("%s MUST be in %s : FAIL" % (prefix, path))
                local_test_pass = False

        if local_test_pass:
            self.log.info("File Structure Test for %s in %s: PASS" % (name, path))
        return local_test_pass

    def set_file_structure_list(self, file_structure_list):
        self.file_structure_list = file_structure_list

    def set_file_structure(self, file_structure):
        self.file_structure = file_structure

    def set_image_uri(self, image_uri):
        self.docker_image_uri = image_uri
