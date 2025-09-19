cmake_minimum_required(VERSION 3.31)
project(table2firefly_cpp)

set(CMAKE_CXX_STANDARD 20)

include_directories(include)
include_directories(third_party/csv2/include)

add_executable(table2firefly_cpp src/main.cpp
        src/table_processing.cpp
        src/utils/csv_utils.cpp
)
