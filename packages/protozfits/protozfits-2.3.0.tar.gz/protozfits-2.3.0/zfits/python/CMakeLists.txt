add_subdirectory(${PROJECT_SOURCE_DIR}/ThirdParty/pybind11 ${CMAKE_CURRENT_BINARY_DIR}/pybind11)

protobuf_generate_python(PY_SOURCES ${DataModelProto})
# This fixes import statements in the generated python files
# see https://github.com/protocolbuffers/protobuf/issues/1491
add_custom_target(fixed_pyprotos
    ALL
    sed -E -i\"\" -e 's/^\(import.*_pb2\)/from . \\1/' *.py
    DEPENDS ${PY_SOURCES}
    COMMAND_EXPAND_LISTS
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)

# make sure python protos land in CMAKE_LIBRARY_OUTPUT_DIRECTORY
if ("${CMAKE_LIBRARY_OUTPUT_DIRECTORY}" STREQUAL "")
    set(PY_PATH ".")
else()
    set(PY_PATH ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})
endif()

add_custom_target(
    pyprotos ALL
    COMMAND cp ${PY_SOURCES} ${PY_PATH}
    DEPENDS fixed_pyprotos
    COMMAND_EXPAND_LISTS
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)


# we call it py internally to make clear its a python target
pybind11_add_module(pyrawzfits rawzfits.cpp)
add_dependencies(pyrawzfits pyprotos)
# but the output library will just be called rawzfits
set_target_properties(pyrawzfits PROPERTIES OUTPUT_NAME rawzfits)

target_link_libraries(pyrawzfits PUBLIC ZFitsIO)
install(TARGETS pyrawzfits DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(FILES ${PY_SOURCES} DESTINATION ${CMAKE_INSTALL_LIBDIR})
