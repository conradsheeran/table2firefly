#include "table_processing.h"

class TableProcessing {
    private:
    std::string working_directory_;
    std::string input_directory_;
    std::string output_directory_;

    public:
    TableProcessing(const std::string& input_directory, const std::string& output_directory, const std::string& working_directory):
                    input_directory_(input_directory),
                    output_directory_(output_directory),
                    working_directory_(working_directory)
    {
        if (!std::filesystem::exists(working_directory_)) {
            throw std::invalid_argument("Working directory does not exist.");
        } else {
            if (!std::filesystem::exists(input_directory_)) {
                std::filesystem::create_directory(working_directory_);
            }

            if (!std::filesystem::exists(output_directory_)) {
                std::filesystem::create_directory(output_directory_);
            }
        }
    }

    int copy_csv_files() {
        std::vector<std::string> csv_files;

        for (const auto& entry : std::filesystem::directory_iterator(input_directory_)) {
            if (entry.path().extension() == ".csv") {
                csv_files.push_back(entry.path().string());
            }
        }

        for (const auto& csv_file : csv_files) {
            std::filesystem::copy(csv_file, working_directory_);
        }

        return 0;
    }

    int clear_csv_files() {
        std::vector<std::string> csv_files;
        std::vector<std::string> columns_to_drop = {"备注", "对方帐号"};

        for (const auto& entry: std::filesystem::directory_iterator(working_directory_)) {
            if (entry.path().extension() == ".csv") {
                csv_files.push_back(entry.path().string());
            }
        }

        for (const auto& csv_file : csv_files) {
            //todo: 使用 CSVUtils 处理每个文件
        }
    }

};
