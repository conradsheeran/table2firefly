#include "utils/csv_utils.h"
#include "table2firefly/table_processing.h"

#include <iostream>
#include <vector>
#include <string>

int main() {
    std::string input_path = "/home/user/dev/CLionProjects/table2firefly/test/input";
    std::string output_file = "/home/user/dev/CLionProjects/table2firefly/test/output";
    std::string working_directory = "/home/user/dev/CLionProjects/table2firefly/test/tmp";

    TableProcessing table_processing(input_path, output_file, working_directory);
    table_processing.copy_csv_files();
    table_processing.clear_csv_files();
    table_processing.add_currency_column(5, "CNY");
}