#include "testApp.h"

//--------------------------------------------------------------
void testApp::setup(){

    receiver.setup();
    ofEnableAlphaBlending();
    ofAddListener(receiver.getEvents().nodeAdded, this, &testApp::nodeAdded);
    ofAddListener(receiver.getEvents().nodeUpdated, this, &testApp::nodeUpdated);
    ofAddListener(receiver.getEvents().nodeRemoved, this, &testApp::nodeRemoved);
//    ofEnableBlendMode(OF_BLENDMODE_ADD);

}

//--------------------------------------------------------------
void testApp::update(){
    receiver.update();
    updateIndices();
    
}

//--------------------------------------------------------------
void testApp::draw(){

    
    if(activeNodes.size()>0){

        ofBackground(0);
        x = 20;
        y = 10;
        for (int i =0; i<activeNodes.size(); i++) {
            int index = activeNodes[i];
                cout<<nodes[index].type<<endl;
            
            ofColor c = ofColor(0, 0, 0);
            if(nodes[index].type == Router){

                c = ofColor::blueViolet;
            }
            else{
                c = ofColor::chartreuse;
                
                if (nodes[index].probedESSID[0] ==" " ) {
                    continue;
                }
            }
            
//            float r = ofMap(nodes[index].Power, 1, 40, 1, 10);
            ofSetColor(c);
            ofCircle(x, y, 10);
            
            if (nodes[index].type == Router) {
                ofSetColor(c);
                ofDrawBitmapString(nodes[index].ESSID, ofPoint(x,y));
            }
            else{
                ofSetColor(c);
                ofDrawBitmapString(nodes[index].probedESSID[nodes[index].probedESSID.size() - 1], ofPoint(x,y));
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
        routerMapIndex[ID] = nodes.size();
    }
    else{
        clientMapIndex[ID] = nodes.size();
    }
 
    nodes.push_back(Node(args.params));
    cout<<"added  "<<args.type<<" : "<<ID<<endl;//args.params<<endl;
}
//--------------------------------------------------------------
void testApp::nodeUpdated(AirodumpEventArgs& args){

    string ID = trim(args.BSSID);
    if(args.type == "Router"){
     
        if (routerMapIndex.find(ID) != routerMapIndex.end()) {
            int index = routerMapIndex[ID];
            nodes[routerMapIndex[ID]].updateNode(args.params);
        }
        else{
            ofLogError()<<" Router : "<<ID<< " not found. It shouldn't be updating"<<endl;
        }
    }
    else{
        if (clientMapIndex.find(ID) != clientMapIndex.end()) {
            int index = clientMapIndex[ID];
            nodes[index].updateNode(args.params);

        }
        else{
            ofLogError()<<" Client : "<<ID<< " not found. It shouldn't be updating"<<endl;
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
            cout<<"node dead : "<<nodes[index].type<<endl;
        }
        else{
            ofLogError()<<" Router : "<<ID<< " not found. It shouldn't be removing"<<endl;
        }
        
    }
    else{
        if (clientMapIndex.find(ID) != clientMapIndex.end()) {
            int index = clientMapIndex[ID];
            nodes[index].alive = false;
        }
        else{
            ofLogError()<<" Client : "<<ID<< " not found. It shouldn't be removing"<<endl;
        }
    }
    
    ofLog()<<"[ nodeRemoved ] "<<ID<<endl;
    
}

//--------------------------------------------------------------
void testApp::updateIndices(){
    activeNodes.clear();
    int x = 0 ;
    for (int i =0 ; i<nodes.size(); i++) {
        if (nodes[i].alive) {
            activeNodes.push_back(i);
        }
        else{
            x++;
            cout<<"Removing Node : " <<nodes[i].type<<endl;
        }
    }
    
    cout<<"size:    "<<x<<endl;
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
