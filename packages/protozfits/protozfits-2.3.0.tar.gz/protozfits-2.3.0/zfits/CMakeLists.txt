
adh_add_library(
    NAME ZFitsIO
    SOURCES
        Checksum.cpp
        IZStream.cpp
        ricecomp.cpp
        MemoryManager.cpp
        ProtobufIFits.cpp
        ZIFits.cpp
        Huffman.cpp
        minilzo.cpp
        ProtobufToFits.cpp
        ProtobufZOFits.cpp
        ProtobufOFits.cpp
        ProtoSerialZOFits.cpp
        ZOFits.cpp
        IFits.cpp
        OFits.cpp
        FlatProtobufZOFits.cpp
    PUBLIC_HEADERS
        ${CMAKE_CURRENT_LIST_DIR}/Checksum.h
        ${CMAKE_CURRENT_LIST_DIR}/FitsDefs.h
        ${CMAKE_CURRENT_LIST_DIR}/Huffman.h
        ${CMAKE_CURRENT_LIST_DIR}/IFits.h
        ${CMAKE_CURRENT_LIST_DIR}/IZStream.h
        ${CMAKE_CURRENT_LIST_DIR}/lzoconf.h
        ${CMAKE_CURRENT_LIST_DIR}/lzodefs.h
        ${CMAKE_CURRENT_LIST_DIR}/MemoryManager.h
        ${CMAKE_CURRENT_LIST_DIR}/minilzo.h
        ${CMAKE_CURRENT_LIST_DIR}/OFits.h
        ${CMAKE_CURRENT_LIST_DIR}/ProtobufIFits.h
        ${CMAKE_CURRENT_LIST_DIR}/ProtobufToFits.h
        ${CMAKE_CURRENT_LIST_DIR}/ProtobufZOFits.h
        ${CMAKE_CURRENT_LIST_DIR}/ProtobufOFits.h
        ${CMAKE_CURRENT_LIST_DIR}/ProtoSerialZOFits.h
        ${CMAKE_CURRENT_LIST_DIR}/ricecomp.h
        ${CMAKE_CURRENT_LIST_DIR}/ZIFits.h
        ${CMAKE_CURRENT_LIST_DIR}/ZOFits.h
        ${CMAKE_CURRENT_LIST_DIR}/Queue.h
        ${CMAKE_CURRENT_LIST_DIR}/FlatProtobufZOFits.h
    LINK_LIBRARIES
        ADHCore
        zstd
        z
)

target_link_libraries(ZFitsIO PUBLIC ADHCore)
target_include_directories(ZFitsIO PUBLIC ${CMAKE_CURRENT_LIST_DIR})
target_compile_features(ZFitsIO PUBLIC cxx_std_11)
set_target_properties(
    ZFitsIO PROPERTIES
    CXX_EXTENSIONS OFF
    CXX_STANDARD_REQUIRED ON
)


add_executable(UnitTestAnyArrayTypesToFits UnitTestAnyArrayTypesToFits.cpp)
add_executable(UnitTestMultipleFitsTables UnitTestMultipleFitsTables.cpp)
add_executable(UnitTestProtobufZFits UnitTestProtobufZFits.cpp)
add_executable(UnitTestSimultaneousReadWrite UnitTestSimultaneousReadWrite.cpp)
add_executable(UnitTestCtaR1ToZFits UnitTestCtaR1ToZfits.cpp)

target_link_libraries(UnitTestAnyArrayTypesToFits ZFitsIO zstd)
target_link_libraries(UnitTestMultipleFitsTables ZFitsIO zstd)
target_link_libraries(UnitTestProtobufZFits ZFitsIO zstd)
target_link_libraries(UnitTestSimultaneousReadWrite ZFitsIO zstd)
target_link_libraries(UnitTestCtaR1ToZFits ZFitsIO zstd)

add_test(AnyArraysToFits UnitTestAnyArrayTypesToFits)
add_test(MultipleFitsTables UnitTestMultipleFitsTables)
add_test(SimultaneousReadWrite UnitTestSimultaneousReadWrite)
add_test(ZFitsCompression UnitTestProtobufZFits)
add_test(R1EventZFITS UnitTestCtaR1ToZFits)

# TODO: need to add option(PYTHON "Build the python bindings to the zfits reader" ON) to top-level CMakeLists.txt
if(PYTHON)
    add_subdirectory(python)
endif()
