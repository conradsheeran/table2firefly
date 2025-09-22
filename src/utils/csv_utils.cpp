#include "utils/csv_utils.h"

#include <csv2/writer.hpp>
#include <filesystem>
#include <stdexcept>
#include <fstream>
#include <algorithm>

CSVUtils::CSVUtils(const std::string& input_file, const std::string& output_file):
        input_file_(input_file),
        output_file_(output_file)
{
    if (!std::filesystem::exists(input_file_)) {
        throw std::invalid_argument("File does not exist.");
    }
    if (reader_.mmap(input_file_)) {
        read_file();
    } else {
        throw std::runtime_error("Failed to mmap CSV file.");
    }
}

int CSVUtils::read_file() {
    header.clear();
    data.clear();
    const auto& csv_header = reader_.header();
    for (const auto& col : csv_header) {
        std::string col_name;
        col.read_value(col_name);
        header.push_back(col_name);
    }

    for (const auto& row : reader_) {
        std::vector<std::string> row_data;
        for (const auto& cell : row) {
            std::string cell_data;
            cell.read_value(cell_data);
            row_data.push_back(cell_data);
        }
        data.push_back(row_data);
    }
    return 0;
}

int CSVUtils::delete_row(const std::string& columns_to_drop) {
    auto it = std::find(header.begin(), header.end(), columns_to_drop);
    if (it != header.end()) {
        size_t index = std::distance(header.begin(), it);
        header.erase(it);
        for (auto& row : data) {
            if (index < row.size()) {
                row.erase(row.begin() + index);
            }
        }
    }
    return 0;
}

int CSVUtils::add_column_with_a_same_value(const int& index, const std::string& column_name, const std::string& value) {
    if (index < 0 || index > static_cast<int>(header.size())) {
        throw std::out_of_range("Index is out of range.");
    }
    header.insert(header.begin() + index, column_name);
    for (auto& row : data) {
        if (row.size() <= static_cast<size_t>(index)) {
            row.resize(header.size(), "");
        }
        row.insert(row.begin() + index, value);
    }
    return 0;
}

CSVUtils::~CSVUtils() {
    std::ofstream stream(output_file_);
    csv2::Writer writer(stream);
    if (!header.empty()) {
        writer.write_row(header);
        for (const auto& row : data) {
            if (row.size() == header.size()) {
                writer.write_row(row);
            }
        }
    }
    stream.close();
}