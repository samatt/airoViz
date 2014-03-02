#pragma once

#include "ofMain.h"
#include "Node.h"
#include "OscReceiver.h"
//#include "airodumpEvents.h"
#include "airodumpGlobals.h"

class testApp : public ofBaseApp{
    
public:
    void setup();
    void update();
    void draw();
    void exit();
    void keyPressed(int key);
    void keyReleased(int key);
    void mouseMoved(int x, int y );
    void mouseDragged(int x, int y, int button);
    void mousePressed(int x, int y, int button);
    void mouseReleased(int x, int y, int button);
    void windowResized(int w, int h);
    void dragEvent(ofDragInfo dragInfo);
    void gotMessage(ofMessage msg);
    void nodeAdded(AirodumpEventArgs& args);
    void nodeUpdated(AirodumpEventArgs& args);
    void nodeRemoved(AirodumpEventArgs& args);
    void updateIndices();
    
	
    vector<Node> nodes;
    vector <int> activeNodes;
    vector<int> timeSortedIndices;
    OscReceiver receiver;
    map<string, int> clientMapIndex;
    map<string, int> routerMapIndex;
    vector<pair<int, int> > indexPairs;
    //        AirodumpEvents events;
    int maxPower, minPower;
    ofVec2f currentPos;
    int x,y;
    
    int numAliveRouters, numAliveClients;
    
    map<string, ofPoint>routerPos;
    map<string,vector<int> > routerClientLinks;
    
};
