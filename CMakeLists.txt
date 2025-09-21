cmake_minimum_required(VERSION 3.31)
project(table2firefly)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(table2firefly src/main.cpp
        src/table_processing.cpp
        src/utils/csv_utils.cpp
        src/utils/utils.cpp
)

target_include_directories(table2firefly PRIVATE
        include
        third_party/csv2/include
)

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    target_compile_options(table2firefly PRIVATE
            -O0
    )
elseif(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_options(table2firefly PRIVATE
            -O3 -march=native
    )
endif()

