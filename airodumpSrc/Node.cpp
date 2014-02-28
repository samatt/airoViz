//
//  Node.cpp
//  airodumpSketch
//
//  Created by Surya Mattu on 2/24/14.
//
//

#include "Node.h"

Node::Node(){
    NodeType type = Router;
    BSSID = " ";
//    firstTimeSeen = " ";
//    lastTimeSeen = " ";
    channel  = -1;
    Speed = -1;
    Privacy = " ";
    
    
    Power = -1;
    IP = " ";
    ESSID = " ";
    probedESSID = " ";
}

Node::Node(string args){
    
}

void Node::setTimeString(string dateTime, bool firsTime){
    if (firsTime) {
        firstTimeSeen = convertDateAndTime(dateTime);
        firstTimeString = dateTime;
    }
    else{
        lastTimeSeen = convertDateAndTime(dateTime);
        lastTimeString = dateTime;
    }
}

DateAndTime Node::convertDateAndTime(string dateTime){
    
    vector<string> strings;
    DateAndTime curTime;
    strings = ofSplitString(dateTime, " ");
    
    //Date
    vector<string> d = ofSplitString(strings[0],"-");
    
    curTime.year = ofToInt(d[0]);
    curTime.month = ofToInt(d[1]);
    curTime.day = ofToInt(d[2]);

    vector<string> t = ofSplitString(strings[1],":");
    
    curTime.hour = ofToInt(t[0]);
    curTime.minute = ofToInt(t[1]);
    curTime.second = ofToInt(t[2]);
    
    return curTime;
}