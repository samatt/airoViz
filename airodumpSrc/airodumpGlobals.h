//
//  airodumpGlobals.h
//  airodumpRealTime
//
//  Created by Surya Mattu on 2/28/14.
//
//
#pragma  once

 enum{
    N_KIND ,
    N_BSSID,
    N_FIRSTTIME,
    N_LASTTIME,
    N_CHANNEL,
    N_SPEED,
    N_PRIVACY,
    N_POWER,
    N_AP,
    N_ESSID
    
};

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

// trim from start
static inline std::string &ltrim(std::string &s) {
    s.erase(s.begin(), std::find_if(s.begin(), s.end(), std::not1(std::ptr_fun<int, int>(std::isspace))));
    return s;
}

// trim from end
static inline std::string &rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), s.rend(), std::not1(std::ptr_fun<int, int>(std::isspace))).base(), s.end());
    return s;
}

// trim from both ends
static inline std::string &trim(std::string &s) {
    return ltrim(rtrim(s));
}
