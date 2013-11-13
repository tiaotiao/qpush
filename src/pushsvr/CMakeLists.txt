set(CMAKE_CXX_FLAGS "-std=c++0x ${CMAKE_CXX_FLAGS}")

include_directories(/usr/local/include/tnet)
link_directories(/usr/local/lib)

set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

set (SRCS

    )

add_executable(pushsvr ${RCS})
target_link_libraries(pushsvr tnet tnet_http)

install(PROGRAMS pushsvr DESTINATION bin/qpush)
