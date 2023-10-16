include(GNUInstallDirs)
function(adh_add_library)
    set(options)
    set(oneValueArgs NAME PYTHON_EXTENSION)
    set(multiValueArgs SOURCES PUBLIC_HEADERS LINK_LIBRARIES ADD_DEFINITIONS)
    cmake_parse_arguments(MODULE "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )

    add_library(${MODULE_NAME} SHARED ${MODULE_SOURCES} ${MODULE_PUBLIC_HEADERS} )
    target_link_libraries(${MODULE_NAME} PUBLIC ${MODULE_LINK_LIBRARIES} )

    set_target_properties(${MODULE_NAME} PROPERTIES PUBLIC_HEADER "${MODULE_PUBLIC_HEADERS}")
    install(
        TARGETS ${MODULE_NAME}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${modulename}
    )
endfunction()

