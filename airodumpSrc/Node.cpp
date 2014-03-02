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
    Channel  = -1;
    Speed = -1;
    Privacy = " ";
    
    
    Power = -1;
    IP = " ";
    ESSID = " ";
    alive = false;
//    probedESSID = " ";
}

Node::Node(string args){
    vector<string> params = ofSplitString(args, ",");
    params[N_KIND] = trim(params[N_KIND]);
    if( params[N_KIND] == "Router"){
        type = Router;
        ESSID = trim(params[N_ESSID]);
        AP = " ";
    }
    else{
        type = Client;
        AP = trim(params[N_AP]);
        if(ofSplitString(params[N_ESSID], ":").size() >0){
            probedESSID  =ofSplitString(params[N_ESSID], ":");
        }
        else{
            probedESSID.push_back(" ");
        }
    }
    BSSID = trim(params[N_BSSID]);
    
    setTimeString(params[N_FIRSTTIME],true);
    setTimeString(params[N_LASTTIME],false);
    duration = 0;
    Channel =  ofToInt(params[N_CHANNEL]);
    Speed = ofToInt(params[N_SPEED]);
    Power = ofToInt(params[N_POWER]);
    alive = true;

}

void Node::updateNode(string args){
    vector<string> params = ofSplitString(args, ",");

    params[N_KIND] =trim(params[N_KIND]);
    if( params[N_KIND] == "Router"){
        type = Router;
        ESSID = trim(params[N_ESSID]);
        AP = " ";
    }
    else{
        type = Client;
        AP = trim(params[N_AP]);
        if(ofSplitString(params[N_ESSID], ":").size() >0){
            probedESSID  =ofSplitString(params[N_ESSID], ":");
        }

    }
    
    alive = true;
    BSSID = trim(params[N_BSSID]);
    
    setTimeString(params[N_FIRSTTIME],true);
    setTimeString(params[N_LASTTIME],false);
    
    Channel =  ofToInt(params[N_CHANNEL]);
    Speed = ofToInt(params[N_SPEED]);
    Power = ofToInt(params[N_POWER]);
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
    
    dateTime = trim(dateTime);
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

void Node::updateDuration(){
    
    int h =0;
    int m = 0;
    int s = 0;;
    if (ofGetHours() > lastTimeSeen.hour) {
        h = ofGetHours() - lastTimeSeen.hour;
    }
    if (ofGetMinutes() > lastTimeSeen.minute) {
        m = ofGetMinutes() - lastTimeSeen.minute;
    }
    if (ofGetSeconds() > lastTimeSeen.second) {
        s = ofGetSeconds() - lastTimeSeen.second;
    }
    
    h *= 3600;
    m *= 60;
    duration = h + m + s;
    
}

int Node::getDuration(){
    return duration;
}