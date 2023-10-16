/** @file UnitTestProtobufZFits.cpp
 *  @brief Unit test of protobufofits and protobufifits classes
 *
 *  Creates a temporary file where some dummy data is written and read-back to verify its validity.
 *
 *  Created on: Jan 6, 2015
 *      Author: lyard
 *
 *
 */

#include "CommonZFitsUnitTests.h"
#include "FlatProtobufZOFits.h"

//do the full write / read test for a given compression scheme
bool writeAndVerifyAGivenCompression(const string& filename,
                                     const string& comp_string)
{
    //reset global counter
    g_event_number = 0;
    //get a compressed FITS writer
    ProtobufZOFits output(1000,  //write 1000*10 events max.
                           10,  //group events 10 by 10
                      1000000,  //use a max. of 1GB for compression
         ProtobufZOFits::AUTO); //let the writer erase events that are given for writing

    FlatProtobufZOFits flat_output(1000,
                                100,
                            1000000,
                        comp_string,
                                 10,
                             100000);

    output.setDefaultCompression(comp_string);
    //write e.g. 951 events
    uint32 target_num_events = 353;
    output.open(filename.c_str());
    flat_output.open(string(filename+".flat").c_str());

    flat_output.moveToNewTable("DATA");

    //for all events, create dummy event and write it to disk
    for (uint32 i=0;i<target_num_events;i++)
    {
        cout << "\rDoing event " << i;
        cout.flush();
        ProtoDataModel::CameraEvent* event = newDummyCameraEvent();
        ProtoDataModel::CameraEvent* other_event = new ProtoDataModel::CameraEvent;
        other_event->CopyFrom(*event);
        output.writeMessage(event);
        flat_output.writeMessage(other_event);
    }
    //flush and close output file
    output.close(false);
    flat_output.close(true);
    flat_output.flush();

    //now let us try to read-back the data as it was written to disk
    ProtobufIFits input(filename.c_str());
    ProtobufIFits other_input(string(filename+".flat").c_str());

    //make sure that the expected number of events has been written
    if (input.getNumMessagesInTable() != target_num_events)
    {
        cout << "Wrong number of messages: " << input.getNumMessagesInTable() << " vs " << target_num_events << endl;
        return false;
    }
    g_event_number = 0;
    //for all expected events, read them back and verify their content
    for (uint32 i=1;i<=input.getNumMessagesInTable();i++)
    {
        ProtoDataModel::CameraEvent* event = input.readTypedMessage<ProtoDataModel::CameraEvent>(i);

        if (!event)
        {
            cout << "Could not load event #" << i << ": got null instead" << endl;
            return false;
        }
        verifyEventData(event);

        input.recycleMessage(event);
    }
    g_event_number = 0;
    //for all expected events, read them back and verify their content
    for (uint32 i=1;i<=input.getNumMessagesInTable();i++)
    {
        cout << "\rVerifying event " << i;
        cout.flush();
        ProtoDataModel::CameraEvent* other_event = other_input.readTypedMessage<ProtoDataModel::CameraEvent>(i);

        if (!other_event)
        {
            cout << "Could not load other event #" << i << ": got null instead" << endl;
            return false;
        }
        verifyEventData(other_event);

        other_input.recycleMessage(other_event);
    }
    //remove the newly created file
    if (remove(filename.c_str()))
    {
        cout << "Impossible to remove file " << filename << " abort." << endl;
        return false;
    }

    if (remove(string(filename+".flat").c_str()))
    {
        cout << "Impossible to remove file " << string(filename+".flat") << " abort." << endl;
        return false;
    }

    return true;
}

int main(int , char**)
{
    //get a temporary filename to output and verify data
    string filename = getTemporaryFilename();

    //we will be using 10 compression threads, just to make things messy
    ProtobufZOFits::DefaultNumThreads(10);

    if (!writeAndVerifyAGivenCompression(filename, "raw"))             throw runtime_error("raw compression failed");
    cout << "raw" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "fact"))            throw runtime_error("fact compression failed");
    cout << "fact" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "diffman16"))       throw runtime_error("diffman16 compression failed");
    cout << "diffman16" << endl;
//    if (!writeAndVerifyAGivenCompression(filename, "huffman16"))       throw runtime_error("huffman16 compression failed");
//    cout << "huffman16" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "doublediffman16")) throw runtime_error("doublediffman16 compression failed");
    cout << "doublediffman16" << endl;
//    if (!writeAndVerifyAGivenCompression(filename, "riceman16"))       throw runtime_error("riceman16 compression failed");
//    cout << "riceman16" << endl;
//    if (!writeAndVerifyAGivenCompression(filename, "factrice"))        throw runtime_error("factrice compression failed");
//    cout << "factrice" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "ricefact"))        throw runtime_error("ricefact compression failed");
    cout << "ricefact" << endl;
//    if (!writeAndVerifyAGivenCompression(filename, "rrice"))           throw runtime_error("rrice compression failed");
//    cout << "rrice" << endl;
//    if (!writeAndVerifyAGivenCompression(filename, "rice"))            throw runtime_error("rice compression failed");
//    cout << "rice" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "lzo"))             throw runtime_error("lzo compression failed");
    cout << "lzo" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "zrice"))           throw runtime_error("zrice compression failed");
    cout << "zrice" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "zrice32"))         throw runtime_error("zrice32 compression failed");
    cout << "zrice32" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "zstd2"))         throw runtime_error("zstd compression failed");
    cout << "zstd" << endl;

 //   if (!writeAndVerifyAGivenCompression(filename, "lzorice"))         throw runtime_error("lzorice compression failed");
 //   cout << "lzorice" << endl;
//    if (!writeAndVerifyAGivenCompression(filename, "sparselossyfloats")) throw runtime_error("sparselossyfloats compression failed");
//    cout << "sparselossyfloats" << endl;

    return 0;
}
