from robot.libraries.BuiltIn import BuiltIn

class devicelist_table:
    def __init__(self):
        self.selib = BuiltIn().get_library_instance('SeleniumLibrary')

    def extract_device_table(self, table_id='deviceTable'):
        """
        Return all rows of the device table as a list of lists of strings.
        Each inner list corresponds to one table row.
        """
        table = self.selib.get_webelement(f"//table[@id='{table_id}']")
        rows = table.find_elements("xpath", ".//tbody/tr")
        result = []
        for row in rows:
            cells = row.find_elements("xpath", ".//td")
            # Convert all cell values to strings
            row_values = [str(cell.text.strip()) for cell in cells]
            result.append(row_values)
        return result
