//
//  oscReceiver.h
//  airodumpSketch
//
//  Created by Surya Mattu on 2/28/14.
//
//



#include "ofxOsc.h"
#include "ofMain.h"

typedef enum{
    kind =0,
    BSSID,
    firsTimeSeen,
    lastTimeSeen,
    Channel,
    Speed,
    Privacy,
    Power,
    probedESSID
    
}NodeParmas;

class OscReceiver{
public:
    OscReceiver();
    ofxOscReceiver receiver;
    void update();
    
};

