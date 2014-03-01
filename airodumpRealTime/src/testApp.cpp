#include "testApp.h"

//--------------------------------------------------------------
void testApp::setup(){

    receiver.setup();
    ofEnableAlphaBlending();
    ofAddListener(receiver.getEvents().nodeAdded, this, &testApp::nodeAdded);
    ofAddListener(receiver.getEvents().nodeUpdated, this, &testApp::nodeUpdated);
    ofAddListener(receiver.getEvents().nodeRemoved, this, &testApp::nodeRemoved);
    ofEnableBlendMode(OF_BLENDMODE_ADD);

}

//--------------------------------------------------------------
void testApp::update(){
    receiver.update();
    updateIndices();
    
}

//--------------------------------------------------------------
void testApp::draw(){

    if(nodes.size()>0){

        ofBackground(0);
        x = 10;
        y = 10;
        for (int i =0; i<activeNodes.size(); i++) {
            int index = activeNodes[i];
            ofColor c = ofColor(0, 0, 0);
            if(nodes[index].type == Router){
                c = ofColor::cyan;
            }
            else{
                c = ofColor::chartreuse;
                
                if (nodes[i].probedESSID.size() <= 1 ) {
                    continue;
                }
            }
            
            float r = ofMap(nodes[index].Power, 1, 80, 1, 10);
            ofSetColor(c);
            ofCircle(x, y, r,0.5);
            
            if (nodes[index].type == Router) {
                ofSetColor(255);
                ofDrawBitmapString(nodes[index].ESSID, ofPoint(x,y));
            }
            else{
                ofSetColor(255);
                ofDrawBitmapString(nodes[index].probedESSID[0], ofPoint(x,y));
            }
        
            y +=  30 ;
            
            if(y > ofGetHeight() -20){
                x += 180;
                y = 10;
                
            }
            
        }
        
    }
}
//--------------------------------------------------------------
void testApp::nodeAdded(AirodumpEventArgs& args){

    string ID = trim(args.BSSID);
    if(args.type == "Router"){
        routerMapIndex[args.BSSID] = nodes.size();
    }
    else{
        clientMapIndex[args.BSSID] = nodes.size();
    }
 
    nodes.push_back(Node(args.params));
    cout<<"added  "<<args.type<<" : "<<args.BSSID<<endl;//args.params<<endl;
}
//--------------------------------------------------------------
void testApp::nodeUpdated(AirodumpEventArgs& args){

    
    if(args.type == "Router"){
     
        if (routerMapIndex.find(args.BSSID) != routerMapIndex.end()) {
            int index = clientMapIndex[args.BSSID];
            nodes[routerMapIndex[args.BSSID]].updateNode(args.params);

        }
        else{
            ofLogError()<<" Router : "<<args.BSSID<< " not found. It shouldn't be updating"<<endl;
        }

    }
    else{
        if (clientMapIndex.find(args.BSSID) != clientMapIndex.end()) {
            int index = clientMapIndex[args.BSSID];
            nodes[index].updateNode(args.params);

        }
        else{
            ofLogError()<<" Client : "<<args.BSSID<< " not found. It shouldn't be updating"<<endl;
        }
    }
    

    ofLog()<<"[ nodeUpdated ] "<<args.params<<endl;
}

//--------------------------------------------------------------
void testApp::nodeRemoved(AirodumpEventArgs& args){
    string ID = trim(args.BSSID);
    if(args.type == "Router"){

        if (routerMapIndex.find(ID) != routerMapIndex.end()) {
            int index = routerMapIndex[ID];
            nodes[index].alive = false;

        }
        else{
            ofLogError()<<" Router : "<<ID<< " not found. It shouldn't be updating"<<endl;
        }
        
    }
    else{
        if (clientMapIndex.find(ID) != clientMapIndex.end()) {
            int index = clientMapIndex[ID];
            nodes[index].alive = false;
        }
        else{
            ofLogError()<<" Client : "<<ID<< " not found. It shouldn't be updating"<<endl;
        }
    }
    
    ofLog()<<"[ nodeRemoved ] "<<ID<<endl;
    
}

//--------------------------------------------------------------
void testApp::updateIndices(){
    activeNodes.clear();
    for (int i =0 ; i<nodes.size(); i++) {
        if (nodes[i].alive) {
            activeNodes.push_back(i);
        }
    }
}

//--------------------------------------------------------------
void testApp::exit(){
    ofRemoveListener(receiver.getEvents().nodeAdded, this, &testApp::nodeAdded);
    ofRemoveListener(receiver.getEvents().nodeUpdated, this, &testApp::nodeUpdated);
    ofRemoveListener(receiver.getEvents().nodeRemoved, this, &testApp::nodeRemoved);

}
//--------------------------------------------------------------
void testApp::keyPressed(int key){
//    cout<<clientMapIndex.size()<<endl;
    if(key == 'f'){
        ofToggleFullscreen();
    }
    
    if(key == ' '){
        for (int i = 0; i<nodes.size(); i++) {
            cout<<i<<" : "<<nodes[i].firstTimeString<<" : "<<nodes[i].BSSID<< endl;
        }
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
//    AirodumpEventArgs args(" xxxxx ");
//    ofNotifyEvent(events.nodeAdded, args);
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
