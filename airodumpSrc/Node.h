//
//  Node.h
//  airodumpSketch
//
//  Created by Surya Mattu on 2/24/14.
//
//
#include "ofMain.h"

typedef enum{
    Client =0,
    Router,
    
}NodeType;

struct DateAndTime{
    
    int second;
    int minute;
    int hour;
    int day;
    int month;
    int year;
    
};


class Node{
public:
    Node();
    
    
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

