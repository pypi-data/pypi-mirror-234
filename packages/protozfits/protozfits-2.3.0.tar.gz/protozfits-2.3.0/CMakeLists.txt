# =============================================================================
#      Top-level CMake for APIs of the CTA Array Data Handler project
# =============================================================================
cmake_minimum_required (VERSION 3.15...3.19 FATAL_ERROR)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/cmake)
include(ADHVersion)
project(ADH-APIS VERSION "${ADH_VERSION_MAJOR}.${ADH_VERSION_MINOR}.${ADH_VERSION_PATCH}" LANGUAGES C CXX)

option(PYTHON "Build the python bindings" ON)

if(APPLE)
    # SWAT currently does not work on MACOS, so switching off by default
    # Can be turned on to test if its working
    option(SWAT "Build swat interface" OFF)
else()
    option(SWAT "Build swat interface" ON)
endif()

include(GNUInstallDirs) # initialize CMAKE_INSTALL_*DIR
include(CTest)

include(RPATHHandling)
include(DefaultBuildType)
include(Git)
include(ADHAddLibrary)


# find dependencies
find_package(Threads REQUIRED)
find_package(ZEROMQ REQUIRED) # uses cmake/FindZEROMQ.cmake
find_package(Protobuf REQUIRED) # use cmake default FindProtobuf.cmake

# Locate source protobuf files
set(PROTOBUF_PATTERN "${CMAKE_CURRENT_LIST_DIR}/data_model/raw/*.proto")
message(STATUS "Looking for protobuf files with pattern ${PROTOBUF_PATTERN}")
file(GLOB DataModelProto "${PROTOBUF_PATTERN}")
protobuf_generate_cpp(ProtoSources ProtoHeaders ${DataModelProto})

# include third party modules
add_subdirectory(ThirdParty/zstd)

configure_file (
  CMakeDefs.h.in
  ${CMAKE_CURRENT_BINARY_DIR}/CMakeDefs.h
)
adh_add_library(
    NAME ADHCore
    SOURCES
        BasicDefs.cpp
        ThreadedObject.cpp
        AnyArrayHelper.cpp
        zmq_streamer/ZMQStreamer.cpp
        Logger.cpp
        commandline_input/Config.cpp
        commandline_input/ConfigService.cpp
        commandline_input/InsertionOperator.cpp
        ${ProtoSources}
    PUBLIC_HEADERS
        ${CMAKE_CURRENT_LIST_DIR}/AnyArrayHelper.h
        ${CMAKE_CURRENT_LIST_DIR}/ThreadedObject.h
        ${CMAKE_CURRENT_LIST_DIR}/Logger.h
        ${CMAKE_CURRENT_LIST_DIR}/BasicDefs.h
        ${ProtoHeaders}
    LINK_LIBRARIES
    #link core library against protocol buffers, zeroMQ and the configuration service
    ${ZEROMQ_LIBRARIES} Threads::Threads ${Protobuf_LIBRARIES}
)
target_include_directories(ADHCore PUBLIC commandline_input)
target_include_directories(ADHCore PUBLIC zmq_streamer)
target_include_directories(ADHCore PUBLIC ${CMAKE_CURRENT_LIST_DIR})
target_include_directories(ADHCore PUBLIC ${CMAKE_CURRENT_BINARY_DIR})
target_include_directories(ADHCore PUBLIC ${Protobuf_INCLUDE_DIRS})
target_compile_features(ADHCore PUBLIC cxx_std_11)
set_target_properties(
    ADHCore PROPERTIES
    CXX_EXTENSIONS OFF
    CXX_STANDARD_REQUIRED ON
)

add_subdirectory(zfits)

add_executable(events_server ExecExampleEventsServer.cpp)
target_link_libraries(events_server PRIVATE ADHCore)

add_executable(events_server_flashcam ExecExampleEventsServerFlashcamStyle.cpp
                                      R1CherenkovDataImpl.cpp)
target_link_libraries(events_server_flashcam PRIVATE ADHCore)

add_executable(events_reader_flashcam ExecExampleEventsReaderFlashcamStyle.cpp
                                      R1CherenkovDataImpl.cpp)
target_link_libraries(events_reader_flashcam PRIVATE ADHCore)

add_executable(events_consumer ExecExampleEventsConsumer.cpp)
target_link_libraries(events_consumer PRIVATE ADHCore)

install(
    TARGETS events_server events_consumer
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

if(SWAT)
    add_subdirectory(swat)
    add_executable(swat_client ExecExampleSWATClient.cpp)
    target_link_libraries(swat_client PRIVATE swat)
    target_link_libraries(swat_client PRIVATE ADHCore)
    target_compile_options(swat_client PRIVATE -std=c++11 -g -O1 -Wno-write-strings -Wno-sign-compare)

    install(
        TARGETS swat_client
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    )
endif()



