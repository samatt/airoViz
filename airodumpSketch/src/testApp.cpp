#include "testApp.h"

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
// 1 BSSID
// 2 First time seen
// 3 Last time seen
// 4 channel
// 5 Speed
// 6 Privacy
// 7 Cipher
// 8 Authentication
// 9 Power
// 10 beacons
// 11 IV
// 12 LAN IP
// 13 ID-length
// 14 ESSID
// 15 Key
//--------------------------------------------------------------
void testApp::setup(){
    
    maxPower = 0;
    minPower = INT_MAX;
    currentPos = ofVec2f(0, 0);

    
    bool isRouter;
    
    dataFile = ofFile("/Users/surya/Desktop/Kali/sharedTest1-01.csv");

    buffer  = dataFile.readToBuffer();

    while (! buffer.isLastLine()) {
        
        Node n;
        string line = buffer.getNextLine();
        cout<<line<<endl;
        vector<string> params = ofSplitString(line, ",");
        
        for (int i =0 ; i<params.size(); i++) {
            params[i] = trim(params[i]);
        }
        if( params.size() < 2 ){
            continue;
        }
        
        if (params[0] == "BSSID") {
            isRouter = true;
            continue;
        }
        else if (params[0] == "Station MAC") {
            isRouter = false;
            continue;
            cout<<"going into client mode"<<endl;
        }
        
        if (isRouter) {
            n.type = Router;
            n.BSSID = params[0];
            //set first time seen
            n.setTimeString(params[1],true);
            //set last time seen
            n.setTimeString(params[2],false);
            
            n.channel = ofToInt(params[3]);
            n.Power = ofToInt(params[8]);
            n.Power = -n.Power;
            n.ESSID = params[13];
            maxPower = MAX(maxPower,n.Power);
            minPower = MIN(minPower,n.Power);
        }
        else{
            //Station MAC
            n.type = Client;
            n.BSSID = params[0];
            
            n.setTimeString(params[1],true);
            n.setTimeString(params[2],false);
            //Power
            n.Power = ofToInt(params[3]);
            n.Power = -n.Power;
            //packets
            
            //BSSID
            //            n
            n.probedESSID = params[6];
            //Probed ESSIDs
            
        }
        nodes.push_back(n);
    }
    
    //TODO: Make sure to include the last string in nodes
    string line = buffer.getNextLine();
    vector<string> params = ofSplitString(line, ",");
    
    for(int i=0; i<nodes.size(); i++){
        cout<<nodes[i].Power<<endl;

    }
    
}



//--------------------------------------------------------------
void testApp::update(){


    
}

//--------------------------------------------------------------
void testApp::draw(){
    ofBackground(0);
    x = 10;
    y = 10;
    for (int i =0; i<nodes.size(); i++) {
        ofColor c = ofColor(0, 0, 0);
//        int sat = ofMap(i, 0, nodes.size(),1 , 255);
        if(nodes[i].type == Router){
            c = ofColor::cyan;
        }
        else{
//        c.setHsb(hue, 100, 100);
            c = ofColor::chartreuse;
            
            if (nodes[i].probedESSID == "") {
                continue;
            }
        }

        float r = ofMap(nodes[i].Power, minPower, maxPower, 5, 10);
        ofSetColor(c);
        ofCircle(x, y, r);

        if (nodes[i].type == Router) {
            ofSetColor(255);
            ofDrawBitmapString(nodes[i].ESSID, ofPoint(x,y));
        }
        else{
//            ofSetColor(c);
//            ofCircle(x, y, r);
            ofSetColor(255);
            ofDrawBitmapString(nodes[i].probedESSID, ofPoint(x,y));
        }

        y +=  30 ;
        
        if(y > ofGetHeight() -20){
            x += 80;
            y = 10;
       
        }

    }

}

//--------------------------------------------------------------
void testApp::keyPressed(int key){
    if(key == 'f'){
        ofToggleFullscreen();
    }
}

//--------------------------------------------------------------
void testApp::keyReleased(int key){
    
}

//--------------------------------------------------------------
void testApp::mouseMoved(int x, int y ){
    
}

//--------------------------------------------------------------
void testApp::mouseDragged(int x, int y, int button){
    
}

//--------------------------------------------------------------
void testApp::mousePressed(int x, int y, int button){
    
}

//--------------------------------------------------------------
void testApp::mouseReleased(int x, int y, int button){
    
}

//--------------------------------------------------------------
void testApp::windowResized(int w, int h){
    
}

//--------------------------------------------------------------
void testApp::gotMessage(ofMessage msg){
    
}

//--------------------------------------------------------------
void testApp::dragEvent(ofDragInfo dragInfo){ 
    
}
