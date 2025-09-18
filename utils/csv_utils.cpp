#include "csv_utils.h"

class CSVUtils {
    private:
    std::string input_file_;
    std::string output_file_;

    public:
    CSVUtils(const std::string& input_file, const std::string& output_file):
            input_file_(input_file),
            output_file_(output_file)
    {
        if (!std::filesystem::exists(input_file_)) {
            throw std::invalid_argument("File does not exist.");
        }
    }

    int read_file(auto& header, std::vector<std::vector<std::string>>& data) {
        csv2::Reader<csv2::delimiter<','>, csv2::first_row_is_header<true>, csv2::quote_character<'"'>> reader;
        if (reader.mmap(input_file_)) {
            header = reader.header;
        } else {
            throw std::runtime_error("Failed to read CSV file.");
        }

        //todo: 将数据写入内存
    }

    int delete_row() {
        //todo: 删除指定行
    }
};
