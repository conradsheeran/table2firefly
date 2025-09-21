#ifndef CSV_UTILS_H
#define CSV_UTILS_H

#include <string>
#include <vector>

class CSVUtils {
    private:
    std::string input_file_;
    std::string output_file_;
    std::vector<std::string> header;
    std::vector<std::vector<std::string>> data;

    public:
    CSVUtils(const std::string& input_file, const std::string& output_file);
    int read_file();
    int delete_row(const std::string& columns_to_drop);

    ~CSVUtils();
};

#endif //CSV_UTILS_H
