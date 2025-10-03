#ifndef CSV_UTILS_H
#define CSV_UTILS_H

#include <csv2/reader.hpp>
#include <string>
#include <vector>

class CSVUtils {
private:
    std::string input_file_;
    std::string output_file_;
    std::vector<std::string> header;
    std::vector<std::vector<std::string>> data;
    csv2::Reader<csv2::delimiter<','>, csv2::first_row_is_header<true>, csv2::quote_character<'"'>> reader_;

public:
    CSVUtils(const std::string &input_file, const std::string &output_file);
    int read_file();
    int delete_row(const std::string &columns_to_drop);
    int add_column_with_a_same_value(const int &index, const std::string &column_name, const std::string &value);

    ~CSVUtils();
};

#endif // CSV_UTILS_H
