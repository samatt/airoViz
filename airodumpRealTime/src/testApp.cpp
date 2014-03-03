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
    //    updateIndices();
    
    int routerX = 20;
    int routerY = 10;
    for(int i =0; i<nodes.size(); i++){
        Node& n = nodes[i];
        
        n.updateDuration();
        //TODO: Add check for duration
        if (n.type == Router) {
            routerPos[n.BSSID] = ofPoint(routerX,routerY);
            routerX +=  200 ;
            
            if(routerX > ofGetWidth() -90){
                routerX  = 20;
                routerY += 100;
                
            }
            
        }
        else{
            
            //check if there is a link bertween the current client and its associated AP
            if( ! ofContains(routerClientLinks[n.AP],i)){
                
                routerClientLinks[n.AP].push_back(i);
                
            }
        }
    }
    
    
    //    for(int i =0; i<activeNodes.size(); i++){
    //
    //        Node& n = nodes[activeNodes[i]];
    //
    //        if (n.type == Router) {
    //            routerPos[n.BSSID] = ofPoint(routerX,routerY);
    //        }
    //
    //        routerX +=  200 ;
    //
    //        if(routerX > ofGetWidth() -90){
    //            routerX  = 20;
    //            routerY += 100;
    //
    //        }
    //    }
    //
}

//--------------------------------------------------------------
void testApp::draw(){
    
    
    
    ofBackground(0);
    x = 20;
    y = 10;
    
    for (int i =0; i<nodes.size(); i++) {
        
        if (nodes[i].type == Client) {
            continue;
        }
        
        Node& router = nodes[i];
        
        stringstream ss;
        
        ofSetColor(ofColor::lightSkyBlue);
        ofDrawBitmapString(router.ESSID +"\n", routerPos[router.BSSID]);
        
        vector<int> clientIndex = routerClientLinks[router.BSSID];
        
        if (clientIndex.size() == 0) {
            ofSetColor(ofColor::grey);
            ss<<"\nNo Clients"<<endl;
            ofDrawBitmapString(ss.str(), routerPos[router.BSSID]);
            continue;
            
        }
        
        string ID = "\n" + nodes[clientIndex[0]].BSSID;
        ID += " : "+ofToString(nodes[clientIndex[0]].getDuration());
        
        float hue = ofMap(nodes[clientIndex[0]] .getDuration(), 0, 500, ofColor::red.getHue(), ofColor::blue.getHue());
        ofColor c1;
        c1.setHsb(hue, 128, 128);
        ofSetColor(c1);
        
        ofDrawBitmapString(ID, routerPos[router.BSSID]);
        
        for (int j = 1 ; j<clientIndex.size(); j++) {
            string ID;
            ID= "\n\n";
            for (int k = 1 ; k<j; k++) {
                ID += "\n";
            }
            
            ID += nodes[clientIndex[j]].BSSID;
            ID += " : "+ofToString(nodes[clientIndex[j]].getDuration());
            
            
            
            float hue = ofMap(nodes[clientIndex[j]].getDuration(), 0, 500, ofColor::red.getHue(), ofColor::blue.getHue());
            ofColor c1;
            c1.setHsb(hue, 128, 128);
            ofSetColor(c1);
            
            ofDrawBitmapString(ID, routerPos[router.BSSID]);
        }
        
        
    }
//    for (int i =0; i<activeNodes.size(); i++) {
//        Node& n  = nodes[activeNodes[i]];
//        
//        if (n.type == Router) {
//            stringstream ss;
//            
//            ofSetColor(ofColor::lightSkyBlue);
//            //                ss<<n.ESSID<<endl;
//            ofDrawBitmapString(n.ESSID +"\n", routerPos[n.BSSID]);
//            vector<int> cIdx = routerClientLinks[n.BSSID];
//            if (cIdx.size() == 0) {
//                ofSetColor(ofColor::grey);
//                ss<<"\nNo Clients"<<endl;
//                ofDrawBitmapString(ss.str(), routerPos[n.BSSID]);
//                
//            }
//            else{
//                
//                string ID = "\n" + nodes[activeNodes[cIdx[0]]].BSSID;
//                ID += " : "+ofToString(nodes[activeNodes[cIdx[i]]].duration);
//                
//                float hue = ofMap(nodes[activeNodes[cIdx[i]]].getDuration(), 0, 500, ofColor::red.getHue(), ofColor::blue.getHue());
//                ofColor c1;
//                c1.setHsb(hue, 128, 128);
//                ofSetColor(c1);
//                
//                ofDrawBitmapString(ID, routerPos[n.BSSID]);
//                
//                for (int i = 1 ; i<cIdx.size(); i++) {
//                    
//                    string ID;
//                    ID= "\n\n";
//                    for (int j = 1 ; j<i; j++) {
//                        ID += "\n";
//                    }
//                    
//                    ID += nodes[activeNodes[cIdx[i]]].BSSID;
//                    ID += " : "+ofToString(nodes[activeNodes[cIdx[i]]].duration);
//                    float hue = ofMap(nodes[activeNodes[cIdx[i]]].getDuration(), 0, 500, ofColor::red.getHue(), ofColor::blue.getHue());
//                    ofColor c1;
//                    //                        cout<<hue<<","<<n.getDuration()<<endl;
//                    c1.setHsb(hue, 128, 128);
//                    ofSetColor(c1);
//                    
//                    ofDrawBitmapString(ID, routerPos[n.BSSID]);
//                }
//            }
//        }
//    }
    //        for (int i =0; i<activeNodes.size(); i++) {
    //            int index = activeNodes[i];
    //            cout<<nodes[index].type<<endl;
    
    //            ofColor c = ofColor(0, 0, 0);
    //            if(nodes[index].type == Router){
    //
    //                c = ofColor::blueSteel;
    //            }
    //            else{
    //                c = ofColor::chartreuse;
    //
    //                if (nodes[index].probedESSID[0] ==" " ) {
    //                    continue;
    //                }
    //            }
    //
    //            ofSetColor(c);
    //            ofCircle(x, y, 1);
    //
    //            if (nodes[index].type == Router) {
    //                ofSetColor(c);
    //                ofDrawBitmapString(nodes[index].ESSID, ofPoint(x,y));
    //            }
    //            else{
    //                ofSetColor(c);
    //                if (nodes[index].AP == " ") {
    //                    ofDrawBitmapString(nodes[index].probedESSID[nodes[index].probedESSID.size() - 1], ofPoint(x,y));
    //                }
    //                else{
    //                    string routerID = nodes[index].AP;
    //                    int routerIndex = routerMapIndex[routerID];
    //                    string networkName = nodes[routerIndex].ESSID;
    //                    ofDrawBitmapString(nodes[index].BSSID + "\n" + networkName, ofPoint(x,y));
    //                    ofSetColor(ofColor::white);
    //                    ofDrawBitmapString("\n" + networkName, ofPoint(x,y));
    //                }
    //
    //            }
    //
    //            y +=  30 ;
    //
    //            if(y > ofGetHeight() -20){
    //                x += 180;
    //                y = 10;
    //
    //            }
    //
    //        }
    //
    //    }
}
//--------------------------------------------------------------
void testApp::nodeAdded(AirodumpEventArgs& args){
    
    string ID = trim(args.BSSID);
    if(args.type == "Router"){
        if(routerMapIndex.find(ID) == routerMapIndex.end()){
            routerMapIndex[ID] = nodes.size();
            
        }
        else{
            ofLogError()<<"Duplicate router ignoring"<<endl;
        }
    }
    else{
        
        if (clientMapIndex.find(ID) ==  clientMapIndex.end()) {
            
            clientMapIndex[ID] = nodes.size();
        }
        else{
            ofLogError()<<"Duplicate router ignoring"<<endl;
        }
        
    }
    
    Node cur = Node(args.params);
    
    //TODO: Make less clunky. Figure out how to incoroporate this properly
    if(routerMapIndex.find(cur.AP) != routerMapIndex .end()){
        cur.indexAP = routerMapIndex[nodes[nodes.size() -1].AP];
    }
    else{
        ofLogError()<<" [Node Added] "<<" router index not found for "<<cur.BSSID<<endl;
    }
    
    
    nodes.push_back(cur);
    
    
    
    cout<<"added  "<<args.type<<" : "<<ID<<endl;//args.params<<endl;
}
//--------------------------------------------------------------
void testApp::nodeUpdated(AirodumpEventArgs& args){
    
    string ID = trim(args.BSSID);
    if(args.type == "Router"){
        
        if (routerMapIndex.find(ID) != routerMapIndex.end()) {
            int index = routerMapIndex[ID];
            nodes[index].updateNode(args.params);
        }
        else{
            ofLogError()<<" Router : "<<ID<< " not found. It shouldn't be updating"<<endl;
        }
    }
    else{
        if (clientMapIndex.find(ID) != clientMapIndex.end()) {
            int index = clientMapIndex[ID];
            nodes[index].updateNode(args.params);
            
            //Updating linked router for current client
            
            if(routerMapIndex.find(nodes[index].AP) != routerMapIndex .end()){
                nodes[index].indexAP = routerMapIndex[nodes[index].AP];
            }
            else{
                ofLogError()<<" [Node Updated] "<<" router index not found for "<<nodes[index].BSSID<<endl;
            }
            
            
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
    numAliveClients = 0;
    numAliveRouters = 0;
    routerClientLinks.clear();
    int x = 0 ;
    for (int i =0 ; i<nodes.size(); i++) {
        
        nodes[i].updateDuration();
        if (nodes[i].type == Router) {
            
            numAliveRouters++;
        }
        else{
            
            routerClientLinks[nodes[i].AP].push_back(activeNodes.size());
            numAliveClients++;
        }
        
        if (nodes[i].alive) {
            activeNodes.push_back(i);
        }
        else{
            x++;
        }
    }
    
    
    //    cout<<"num nodes removed:"<<x<<endl;
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
        cout<<activeNodes.size()<<endl;
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
