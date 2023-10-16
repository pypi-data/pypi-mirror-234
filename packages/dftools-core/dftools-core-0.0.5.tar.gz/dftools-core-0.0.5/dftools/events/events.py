
import os
from dftools.events.base import ExtendedInfoLevel, ErrorLevel, WarnLevel


####################################################################
##                       Generic events                           ##
####################################################################

class MissingMandatoryArgument(ErrorLevel):
    def code(self):
        return "X-001"

    def message(self):
        return f"Missing mandatory argument {self.argument_name} on call of method '{self.method_name}' on {self.object_type.__name__}"

####################################################################
##                         CSV events                             ##
####################################################################
class CSVFileReadSuccessful(ExtendedInfoLevel):
    def code(self):
        return "CSV-001"

    def message(self):
        return f"{self.object_type_name} was loaded successfully from file {self.file_path}"

class CSVFileWriteSuccessful(ExtendedInfoLevel):
    def code(self):
        return "CSV-002"

    def message(self):
        return f"{self.object_type_name} export to CSV successful. File was exported at {os.path.abspath(self.file_path)}"

####################################################################
##                 JSON configuration file read                   ##
####################################################################
class ConfigurationFileLoadCompleted(ExtendedInfoLevel):
    def code(self):
        return "PRV-001"

    def message(self):
        return f"{self.object_type_name} was loaded successfully from files in folder {self.folder_path}"

class ConfigurationMissingFolder(WarnLevel):
    def code(self):
        return "PRV-002"

    def message(self):
        return f"No folder is available at location {self.folder_path} for objects {self.object_type_name}"


####################################################################
##                      Structure events                          ##
##                            [A]                                 ##
####################################################################

class MissingField(ErrorLevel):
    def code(self):
        return "A-001"

    def message(self):
        return f"Field {self.field_name} does not exist in structure {self.structure_name}"

class FieldAdditionInvalidPosition(ErrorLevel):
    def code(self):
        return "A-002"

    def message(self):
        return f"Field {self.field_name} is requested to be added in last position {self.position} but expected last position is {self.expected_last_position} in structure {self.structure_name}"
    

class CreatedStructureFromTemplate(ExtendedInfoLevel):
    def code(self):
        return "A-101"

    def message(self):
        return f"Structure {self.structure_name} was created based on the template {self.template_name} from original structure {self.original_structure_name}"