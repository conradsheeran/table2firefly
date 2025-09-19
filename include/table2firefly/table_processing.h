#ifndef TABLE_PROCESSING_H
#define TABLE_PROCESSING_H

#include <string>

class TableProcessing {
    private:
    std::string working_directory_;
    std::string input_directory_;
    std::string output_directory_;

    public:
    TableProcessing(const std::string& input_directory, const std::string& output_directory, const std::string& working_directory);
    int copy_csv_files();
    int clear_csv_files();
};

#endif //TABLE_PROCESSING_H
