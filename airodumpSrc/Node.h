//
//  Node.h
//  airodumpSketch
//
//  Created by Surya Mattu on 2/24/14.
//
//
#include "ofMain.h"
#include "airodumpGlobals.h"


class Node{
public:
    Node();
    Node(string args);
    
    
    NodeType type;
    string BSSID;
    DateAndTime firstTimeSeen;
    DateAndTime lastTimeSeen;
    int channel;
    int Speed;
    string Privacy;

    int Power;
    string IP;
    string ESSID;
    
    string firstTimeString;
    string lastTimeString;
    //    string Cipher;
    //    string Authentication;
    //    int numBeacons;
    //    int numIV;
    
    //Client only
    string probedESSID;
//    Station MAC,
//   int  numPackets;


    DateAndTime convertDateAndTime(string dateTime);
    void setFirstTimeSeen(string dateTime);
    void setLastTimeSeen(string dateTime);
    void setTimeString(string dateTime,bool firsTime);
    string getDateString( bool firstTime);
};

