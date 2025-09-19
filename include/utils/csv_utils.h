#ifndef CSV_UTILS_H
#define CSV_UTILS_H

#include <string>
#include <vector>

class CSVUtils {
    private:
    std::string input_file_;
    std::string output_file_;

    public:
    CSVUtils(const std::string& input_file, const std::string& output_file);
    int read_file(auto& header, std::vector<std::vector<std::string>>& data);
    int delete_row();
};

#endif //CSV_UTILS_H
