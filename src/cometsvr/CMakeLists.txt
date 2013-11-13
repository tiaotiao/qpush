set(CMAKE_CXX_FLAGS "-std=c++0x ${CMAKE_CXX_FLAGS}")

include_directories(/usr/local/include/tnet)
link_directories(/usr/local/lib)

set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

set (SRCS

    )

add_executable(cometsvr ${RCS})
target_link_libraries(cometsvr tnet tnet_http)

install(PROGRAMS cometsvr DESTINATION bin/qpush)
