set(CMAKE_CXX_FLAGS "-std=c++0x ${CMAKE_CXX_FLAGS}")

include_directories(/usr/local/include/tnet)
link_directories(/usr/local/lib)

set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

set (SRCS
    comet.cpp
    )

add_executable(comet ${SRCS})
target_link_libraries(comet tnet tnet_http)

install(TARGETS comet DESTINATION qpush/comet)
