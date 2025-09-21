#include "utils/csv_utils.h"

#include <iostream>
#include <vector>
#include <string>

int main() {
    std::vector<std::string> data2drop = {"交易单号", "商户单号", "备注", "当前状态"};
    CSVUtils csv_utils("/home/user/dev/CLionProjects/table2firefly/test/input/test.csv", "/home/user/dev/CLionProjects/table2firefly/test/output/test.csv");
    for (const auto& row_data : data2drop) {
        csv_utils.delete_row(row_data);
    }
}